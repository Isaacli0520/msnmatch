from django.core.management.base import BaseCommand, CommandError
from courses.models import Course, Instructor, CourseUser, CourseInstructor
import re
import os
import csv
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
class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		# post_data = {
		# 	"Semester": settings.SEMESTER_ID,
		# 	"Group": 'CS',
		# 	"Description": 'Yes',
		# 	"submit": 'Submit Data Request',
		# 	"Extended": 'No'
		# }
		post_data = {
			"iGroup":"", 
			"iMnemonic":"", 
			"iNumber":"", 
			"iStatus":"", 
			"iType":"", 
			"iInstructor":"", 
			"iBuilding":"", 
			"iRoom":"", 
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
			"Request CSV Data": "Request CSV data",
		}
		data, lines = [], []
		with requests.post('https://rabi.phys.virginia.edu/mySIS/CS2/deliverSearchData.php' + '?Semester=' + settings.SEMESTER_ID, data=post_data, stream=True) as r:
		# with requests.post('https://rabi.phys.virginia.edu/mySIS/CS2/deliverData.php', data=post_data, stream=True) as r:
			csv_reader = csv.reader(codecs.iterdecode(r.iter_lines(), 'utf-8'))
			headers = next(csv_reader) 
			print("headers",headers)
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
				if(len(line) == 17):
					for i in range(17):
						if i == 15 and line[i] != '':
							tmp_data[headers[i]] = []
							tmp_data[headers[i]].append(line[i])
						elif i == 15 and line[i] == '':
							tmp_data[headers[i]] = []
						else:
							tmp_data[headers[i]] = line[i]
				else:
					for i in range(15):
						tmp_data[headers[i]] = line[i]
					tmp_data[headers[15]] = []
					for i in range(15, len(line)):
						if re.match(pattern, line[i]):
							tmp_data[headers[15]].append(line[i])
					tmp_data[headers[-1]] = line[-1]
				if "Prerequisite:" in tmp_data['Description'].split(' '):
					tmp_data["Prerequisite"] =tmp_data['Description'][tmp_data['Description'].index("Prerequisite:"):]
				else:
					tmp_data["Prerequisite"] = ""
				tmp_data["Semester"] = settings.CURRENT_SEMESTER
				data.append(tmp_data)
			print("data:",len(data))

		old_cs_instrs = CourseInstructor.objects.filter(semester = settings.CURRENT_SEMESTER)
		old_cs_instrs_dict = {}
		for old_cs_instr in old_cs_instrs:
			old_cs_instrs_dict[old_cs_instr] = 1
		 
		for cs in data:
			if cs["Type"] in type_dict:
				cs['Type'] = type_dict[cs['Type']]
			course_query = Course.objects.filter(number=cs['Number'], mnemonic=cs['Mnemonic'],
			title=cs['Title'], type=cs['Type'])

			if course_query.first() == None:
				tmp_course = Course.objects.create(number=cs['Number'], mnemonic=cs['Mnemonic'], units=cs['Units'],
				title=cs['Title'],description=cs["Description"], type=cs['Type'],
				prerequisite=cs['Prerequisite'])
			else:
				tmp_course = course_query.first()
				tmp_course.units = cs["Units"]
				tmp_course.description = cs["Description"]
				tmp_course.prerequisite = cs["Prerequisite"]
				tmp_course.save()
			tmp_instructors = [ins.strip().split() for ins in cs["Instructor(s)"].split(',')]
			final_instructors = []
			for instructor in tmp_instructors:
				if len(instructor) >= 1 and len(instructor) <= 3:
					final_instructors.append(instructor)
				elif " ".join(instructor).lower()[:12] == "co-taught by":
					for inner_instructor in re.split(r"co-taught by", " ".join(instructor), flags=re.I)[1].split(" and "):
						final_instructors.append(inner_instructor.strip().split())
				elif len(instructor) > 2 and "and" in instructor:
					for inner_instructor in " ".join(instructor).split('and'):
						final_instructors.append(inner_instructor.strip().split())
				elif len(instructor) > 2:
					final_instructors.append(instructor)
			for instructor in final_instructors:
				if len(instructor) == 1:
					tmp_first_name = instructor[0]
					tmp_last_name = ""
				else:
					tmp_first_name = instructor[0]
					tmp_last_name = instructor[-1]
				instr_query = Instructor.objects.filter(first_name=tmp_first_name, last_name=tmp_last_name)
				if instr_query.first() == None:
					tmp_instr = Instructor.objects.create(first_name=tmp_first_name, last_name=tmp_last_name)
				else:
					tmp_instr = instr_query.first()
				cs_instr_query = CourseInstructor.objects.filter(instructor=tmp_instr, course=tmp_course, topic=cs["Topic"],  semester=cs["Semester"])
				if cs_instr_query.first() == None:
					print("NEW cs instructor found")
					print("instructor",tmp_instr.first_name,tmp_instr.last_name, "course", tmp_course.mnemonic, tmp_course.number,)
					CourseInstructor.objects.create(instructor=tmp_instr, course=tmp_course, topic=cs["Topic"], semester=cs["Semester"])
				else:
					# print("OLDDDD", old_cs_instrs_dict[cs_instr_query.first()])
					old_cs_instrs_dict[cs_instr_query.first()] = 0
		for old_cs_instr, v in old_cs_instrs_dict.items():
			if v == 1:
				print("old cs instr", old_cs_instr.course.mnemonic, old_cs_instr.course.number, old_cs_instr.course.title)
				old_cs_instr.delete()
		print('total length:', len(old_cs_instrs_dict))