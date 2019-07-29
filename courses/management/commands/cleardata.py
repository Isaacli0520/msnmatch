from django.core.management.base import BaseCommand, CommandError
from courses.models import Course, Instructor, CourseUser, CourseInstructor
import re
import os
import csv


class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		tmp_courses = []
		for cs in Course.objects.all():
			tmp_courses.append({
				"course_pk":cs.pk,
				"mnemonic":cs.mnemonic,
				"number":cs.number,
				"title":cs.title,
				"units":cs.units,
				"description":cs.description,
				"prerequisite":cs.prerequisite,
				"type":cs.type,
			})
		for cs in tmp_courses:
			tmp_query = Course.objects.filter(mnemonic = cs["mnemonic"], number = cs["number"], type=cs["type"])
			if tmp_query.count() > 1:
				tmp_units = 0
				for i in range(len(tmp_query)):
					if i == 0:
						tmp_units = tmp_query[0].units
					elif tmp_units != tmp_query[i].units:
						print(cs)
						print("-----------------")
				# print(cs)
				# print("-----------------")


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