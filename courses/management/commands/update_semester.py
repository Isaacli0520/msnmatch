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
semester_ids = {
	"2016Fall":"1168",
	"2017Spring":"1172",
	"2017Fall":"1178",
	"2018Spring":"1182",
	"2018Fall":"1188",
	"2019Spring":"1192",
	"2019Fall":"1198",
	"2020Spring":"1202",
	"2020Fall":"1208",
	"2021Spring":"1212",
	"2021Fall":"1218",
}


class Command(BaseCommand):
	def add_arguments(self, parser):
		parser.add_argument('semester_id')

	def handle(self, *args, **kwargs):
		semester = kwargs["semester_id"]
		if semester not in semester_ids:
			print("Wrong semester")
			return
		semester_id = semester_ids[semester]
		new_data = {
			"Semester": semester_id,
            "Group": 'CS',
            "Description": 'Yes',
            "submit": 'Submit Data Request',
            "Extended": 'Yes'
		}
		headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
		data, lines = [], []
		with requests.post('https://louslist.org/deliverData.php', headers = headers, data=new_data, stream=True) as r:
			csv_reader = csv.reader(codecs.iterdecode(r.iter_lines(), 'utf-8'))
			# with open("tmp_csv.csv", 'w') as wf:
			# 	writer = csv.writer(wf)
			# 	for row in csv_reader:
			# 		writer.writerow(row)
			headers = next(csv_reader) 
			print("Semester:", semester, "Semester ID:", semester_id)
			print("headers",headers)
			print("Comments Before:", CourseUser.objects.all().count())
			for row in csv_reader:
				lines.append(row)
			print("length of lines", len(lines))
			for i in range(len(lines)): 
				if re.match(r'\d+',lines[i][0]) == None:
					lines[i - 1][-1] += lines[i][0]
					lines[i] = []
			lines = [line for line in lines if len(line) > 0]
			for line in lines:
				tmp_data = {}
				for i in range(len(line)):
					tmp_data[headers[i]] = line[i]

				# split_description = tmp_data['Description'].split(' ')
				split_description = re.split(r'\W+', tmp_data['Description'])
				tmp_data["Prerequisite"] = ""
				for prereq_key in ["Prerequisite:", "Prerequisites:", "Prerequisite", "Prerequisites"]:
					if prereq_key in split_description:
						tmp_data["Prerequisite"] =tmp_data['Description'][(tmp_data['Description'].index(prereq_key) + len(prereq_key)):].strip(':').strip()
				tmp_data["Semester"] = semester
				data.append(tmp_data)
			print("data:",len(data))

		old_cs_instrs = CourseInstructor.objects.filter(semester = semester)
		old_cs_instrs_dict = {}
		for old_cs_instr in old_cs_instrs:
			old_cs_instrs_dict[old_cs_instr] = 1
		 
		for cs in data:
			if cs["Type"] in type_dict:
				cs['Type'] = type_dict[cs['Type']]

			try:
				course = Course.objects.get(number=cs['Number'], mnemonic=cs['Mnemonic'], title=cs['Title'], type=cs['Type'])
				course.units = cs["Units"]
				course.description = cs["Description"]
				course.prerequisite = cs["Prerequisite"]
				course.save()
			except Course.DoesNotExist:
				course = Course.objects.create(number=cs['Number'], mnemonic=cs['Mnemonic'], units=cs['Units'], title=cs['Title'],description=cs["Description"], type=cs['Type'], prerequisite=cs['Prerequisite'])
			
			tbd_instructors = []
			final_instructors = []
			for i in range(1, 5):
				tmp_instructor = cs["Instructor"+str(i)]
				if tmp_instructor != "":
					if len(tmp_instructor.split(',')) > 1:
						for instructor in tmp_instructor.split(','):
							final_instructors.append(instructor.strip().split())
					else:
						final_instructors.append(tmp_instructor.strip().split())

			# ['ClassNumber', 'Mnemonic', 'Number', 'Section', 'Type', 
			# 'Units', 'Instructor1', 'Days1', 'Room1', 'MeetingDates1', 
			# 'Instructor2', 'Days2', 'Room2', 'MeetingDates2', 'Instructor3', 
			# 'Days3', 'Room3', 'MeetingDates3', 'Instructor4', 'Days4', 'Room4'
			# , 'MeetingDates4', 'Title', 'Topic', 'Status', 'Enrollment', 'EnrollmentLimit',
			#  'Waitlist', 'Description']

			for instructor in final_instructors:
				if len(instructor) == 0:
					print("Empty Instructor Name")
					return
				tmp_first_name = instructor[0]
				tmp_last_name = "" if len(instructor) == 1 else instructor[-1]

				try:
					instr = Instructor.objects.get(first_name=tmp_first_name, last_name=tmp_last_name)
				except Instructor.DoesNotExist:
					instr = Instructor.objects.create(first_name=tmp_first_name, last_name=tmp_last_name)
				
				try:
					cs_instr = CourseInstructor.objects.get(instructor=instr, course=course, topic=cs["Topic"], semester=cs["Semester"])
					old_cs_instrs_dict[cs_instr] = 0
				except CourseInstructor.DoesNotExist:
					print("NEW Course Instructor Relation found -", "Instructor:",instr.first_name,instr.last_name, "Course:", course.mnemonic, course.number,)
					cs_instr = CourseInstructor.objects.create(instructor=instr, course=course, topic=cs["Topic"], semester=cs["Semester"])
				
		for old_cs_instr, v in old_cs_instrs_dict.items():
			try:
				if v == 1 and not CourseUser.objects.filter(course_instructor=old_cs_instr).first():
					print("Old Course Instructor Relation Deleted -", "Instructor:",old_cs_instr.instructor.first_name, old_cs_instr.instructor.last_name, "Course:", old_cs_instr.course.mnemonic, old_cs_instr.course.number, old_cs_instr.course.title)
					old_cs_instr.delete()
			except Instructor.DoesNotExist:
				print("OLD instructor error")
		print("Comments After:", CourseUser.objects.all().count())