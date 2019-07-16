from django.core.management.base import BaseCommand, CommandError
from courses.models import Course, Instructor, CourseUser, CourseInstructor, Review
import re
import os
import csv

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		for cs in Course.objects.all():
			cs.delete()
		data = []
		for path, subdirs, files in os.walk("data"):
			for file in files:
				if file[:5] == "Class":
					data.extend(read_course_data(os.path.join(path, file), file))
		for cs in data:
			course_query = Course.objects.filter(number=cs['Number'], mnemonic=cs['Mnemonic'], units=cs['Units'],
			title=cs['Title'],topic=cs['Topic'], type=cs['Type'])

			if course_query.first() == None:
				tmp_course = Course.objects.create(number=cs['Number'], mnemonic=cs['Mnemonic'], units=cs['Units'],
				title=cs['Title'],topic=cs['Topic'],description=cs["Description"], type=cs['Type'],
				prerequisite=cs['Prerequisite'])
			else:
				tmp_course = course_query.first()

			instr_query = Instructor.objects.filter(name=cs["Instructor(s)"])
			if instr_query.first() == None:
				tmp_instr = Instructor.objects.create(name=cs["Instructor(s)"])
			else:
				tmp_instr = instr_query.first()
			
			cs_instr_query = CourseInstructor.objects.filter(instructor=tmp_instr, course=tmp_course, semester=cs["Semester"])
			if cs_instr_query.first() == None:
				CourseInstructor.objects.create(instructor=tmp_instr, course=tmp_course, semester=cs["Semester"])
			


def read_course_data(path, filename):
	data = []
	pattern = r'[A-Z]+ \d+-\d+  [A-Z]+ \(\d+\)'
	semester = filename[5:-4]
	with open(path, 'r') as rf:
		lines = []
		csv_reader = csv.reader(rf)  
		headers = next(csv_reader) 
		for row in csv_reader:
			lines.append(row)
		# lines = [[l.strip().strip("\"").strip("\'") for l in line.strip().split(',')] for line in rf.readlines()]
		# headers = lines[0]
		# lines = lines[1:]
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
				tmp_data[headers[16]] = line[-1]
			if "Prerequisite:" in tmp_data['Description'].split(' '):
				tmp_data["Prerequisite"] =tmp_data['Description'][tmp_data['Description'].index("Prerequisite:"):]
			else:
				tmp_data["Prerequisite"] = ""
			tmp_data["Semester"] = semester
			data.append(tmp_data)
	return data