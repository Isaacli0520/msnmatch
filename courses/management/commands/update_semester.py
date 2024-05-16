from django.core.management.base import BaseCommand, CommandError
from courses.models import Course, Instructor, CourseUser, CourseInstructor
import re
import os
import csv
import sys
import codecs
from contextlib import closing
import requests
from msnmatch import settings
from functools import cmp_to_key
from msnmatch.utils import cmp_semester

pattern = r'[A-Z]+ \d+-\d+  [A-Z]+ \(\d+\)'
type_dict = {
  "IND":"Independent Study",
  "STO":"Studio",
  "PRA":"Practicum",
  "CLN":"Clinical",
  "SEM":"Seminar",
  "DRL":"Drill",
  "WKS":"Workshop",
}
form_data = {
  "iGroup":"", 
  "iMnemonic":"",
  "iNumber":"", 
  "iStatus":"", 
  "iType":"", 
  "iInstructor":"", 
  "iBuilding":"", 
  "iRoom":"", 
  "iMode":"", 
  "iDays":"", 
  "iTime":"", 
  "iDates":"", 
  "iUnits":"", 
  "iTitle":"", 
  "iTopic":"", 
  "iDescription":"", 
  "iDiscipline":"", 
  "iMinPosEnroll":"", 
  "iMaxPosEnroll":"", 
  "iMinCurEnroll":"", 
  "iMaxCurEnroll":"", 
  "iMinCurWaitlist":"", 
  "iMaxCurWaitlist":"", 
  "Request CSV Data": "Request CSV Data"
}
files = {k: (None, v) for k, v in form_data.items()}
req_headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}

start_year = 2016
start_id = 1162
def calc_semester_id(semester):
  if re.match(r'2[0-9]{3}(Spring|Fall)$', semester) is None:
    return None
  year, season = int(semester[:4]), semester[4:]
  return start_id + (year - start_year) * 10 + 6 * int(season=="Fall")


class Command(BaseCommand):
  def add_arguments(self, parser):
    parser.add_argument('semester_id')

  def handle(self, *args, **kwargs):
    semester = kwargs["semester_id"]
    semester_id = calc_semester_id(semester)
    if semester_id is None:
      print("Wrong Semester")
      return
    
    # get all courses of a certain semester from louslist
    lines = []
    params = {"Semester": semester_id }
    with requests.post('https://louslist.org//deliverSearchData.php', headers=req_headers, params=params, files=files, stream=True) as r:
      csv_reader = csv.reader(codecs.iterdecode(r.iter_lines(), 'utf-8'))
      headers = next(csv_reader) 
      print("Semester:", semester, "Semester ID:", semester_id)
      print("headers",headers)
      print("Comments Before:", CourseUser.objects.all().count())
      for row in csv_reader:
        if len(row) > 0 and row[0].isdigit():
          lines.append(row)
      print("length of lines", len(lines))

    # store courses' info as a vector of dict
    data: list[dict] = []
    for line in lines:
      tmp_data = {
        "Semester": semester,
        "Prerequisite": ""
      }
      for i in range(len(line)):
        tmp_data[headers[i]] = line[i]

      # extract prereq if possible
      split_description = re.split(r'\W+', tmp_data['Description'])
      for prereq_key in ["Prerequisite:", "Prerequisites:", "Prerequisite", "Prerequisites"]:
        if prereq_key in split_description:
          tmp_data["Prerequisite"] =tmp_data['Description'][(tmp_data['Description'].index(prereq_key) + len(prereq_key)):].strip(':').strip()
      data.append(tmp_data)
    print("courses size:", len(data))

    old_cs_instrs = CourseInstructor.objects.filter(semester = semester)
    old_cs_instrs_dict = {old_cs_instr : 1 for old_cs_instr in old_cs_instrs}
     
    for cs in data:
      # transform acronym e.g. SEM to Seminar
      if cs["Type"] in type_dict:
        cs['Type'] = type_dict[cs['Type']]

      # update or create course
      try:
        course = Course.objects.get(number=cs['Number'], mnemonic=cs['Mnemonic'], title=cs['Title'], type=cs['Type'])
        course.units = cs["Units"]
        course.description = cs["Description"]
        course.prerequisite = cs["Prerequisite"]
        course.save()
      except Course.DoesNotExist:
        course = Course.objects.create(number=cs['Number'], mnemonic=cs['Mnemonic'], units=cs['Units'], title=cs['Title'],description=cs["Description"], type=cs['Type'], prerequisite=cs['Prerequisite'])
      
      # instructors can be multiple
      final_instructors = []
      split_instructors = cs["Instructor(s)"].split(',')
      for instructor in split_instructors:
        # first name + last name should be at least 3 chars
        if len(instructor.strip()) > 2:
          final_instructors.append(instructor.strip().split())

      # ['ClassNumber', 'Mnemonic', 'Number', 'Section', 'Type', 
      # 'Units', 'Instructor1', 'Days1', 'Room1', 'MeetingDates1', 
      # 'Instructor2', 'Days2', 'Room2', 'MeetingDates2', 'Instructor3', 
      # 'Days3', 'Room3', 'MeetingDates3', 'Instructor4', 'Days4', 'Room4'
      # , 'MeetingDates4', 'Title', 'Topic', 'Status', 'Enrollment', 'EnrollmentLimit',
      #  'Waitlist', 'Description']

      for instructor in final_instructors:
        if len(instructor) == 0:
          print("Empty Instructor Name")
          continue
        tmp_first_name = instructor[0]
        tmp_last_name = "" if len(instructor) == 1 else instructor[-1]

        try:
          instr = Instructor.objects.get(first_name=tmp_first_name, last_name=tmp_last_name)
        except Instructor.DoesNotExist:
          instr = Instructor.objects.create(first_name=tmp_first_name, last_name=tmp_last_name)
        except Instructor.MultipleObjectsReturned:
          instrs = Instructor.objects.filter(first_name=tmp_first_name, last_name=tmp_last_name)
          for instr_dup in instrs:
            instr_dup.delete()
          instr = Instructor.objects.create(first_name=tmp_first_name, last_name=tmp_last_name)
        
        try:
          cs_instr = CourseInstructor.objects.get(instructor=instr, course=course, topic=cs["Topic"], semester=cs["Semester"])
          old_cs_instrs_dict[cs_instr] = 0
        except CourseInstructor.DoesNotExist:
          print("NEW Course Instructor Relation found -", "Instructor:",instr.first_name,instr.last_name, "Course:", course.mnemonic, course.number,)
          cs_instr = CourseInstructor.objects.create(instructor=instr, course=course, topic=cs["Topic"], semester=cs["Semester"])

    # remove course-instructor relation that is not seen in this semester
    for old_cs_instr, v in old_cs_instrs_dict.items():
      try:
        if v == 1 and not CourseUser.objects.filter(course_instructor=old_cs_instr).first():
          print("Old Course Instructor Relation Deleted -", "Instructor:",old_cs_instr.instructor.first_name, old_cs_instr.instructor.last_name, "Course:", old_cs_instr.course.mnemonic, old_cs_instr.course.number, old_cs_instr.course.title)
          old_cs_instr.delete()
      except Instructor.DoesNotExist:
        print("OLD instructor error")
    print("Comments After:", CourseUser.objects.all().count())
