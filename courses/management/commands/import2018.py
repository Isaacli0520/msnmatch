from django.core.management.base import BaseCommand, CommandError
from courses.models import Course, Instructor, CourseUser, CourseInstructor
import re
import os
import csv
from msnmatch import settings
from functools import cmp_to_key
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

def cmp_int(a,b):
	if a > b:
		return 1
	elif a < b:
		return -1
	else:
		return 0

def cmp_semester(a,b):
	if a == b:
		return 0
	elif a == "":
		return -1
	elif b == "":
		return 1
	elif a[:4] != b[:4]:
		return cmp_int( int(a[:4]), int(b[:4]) )
	elif a[:4] == b[:4]:
		if a[4:] == "Fall":
			return 1
		elif b[4:] == "Fall":
			return -1
	return 0

def cmp_semester_key(a,b):
	return cmp_semester(a["last_taught"], b["last_taught"])

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		user = get_object_or_404(User, username="admin")
		with open("data/new_hoos2018rating_03.csv", 'r') as rf:
			csv_reader = csv.reader(rf)
			headers = next(csv_reader)
			lines = [row for row in csv_reader]
			for line in lines:
				flag = False
				course_num, instructor_name, review, whatever, whatever2, rating_instructor = line[0], line[1], line[2], line[3], line[4], line[5]
				course_query = Course.objects.filter(mnemonic=course_num[:-4], number=course_num[-4:]).exclude(units="0")
				instructor_query = Instructor.objects.filter(first_name = instructor_name.split(' ')[0], last_name = instructor_name.split(' ')[-1])
				instructor = instructor_query.first()
				if course_query.first() == None or instructor_query.first() == None:
					print("course_num", course_num, "instructor:", instructor_name)
					print("course_query:",course_query, "instructor_query:", instructor_query)
					print("Error")
					break
				tmp_courses = []
				for course in course_query:
					cs_instr_arr = [cs_instr.semester for cs_instr in CourseInstructor.objects.filter(course=course)]
					cs_instr_arr = sorted(cs_instr_arr, key=cmp_to_key(cmp_semester))
					last_taught = settings.CURRENT_SEMESTER
					if settings.CURRENT_SEMESTER not in cs_instr_arr:
						last_taught = cs_instr_arr[-1]
					tmp_courses.append({
						"course":course,
						"last_taught":last_taught,
					})
				tmp_courses = sorted(tmp_courses, key=cmp_to_key(cmp_semester_key), reverse=True)
				# print("TMP COURSES:", tmp_courses)
				for course in tmp_courses:
					courses_2 = CourseInstructor.objects.filter(course = course["course"], instructor = instructor)
					if courses_2.first() != None:
						semesters = sorted([cs_instr.semester for cs_instr in courses_2], key=cmp_to_key(cmp_semester))
						if settings.CURRENT_SEMESTER in semesters and len(semesters) > 1:
							tmp_semester = semesters[-2]
						elif settings.CURRENT_SEMESTER in semesters and len(semesters) == 1:
							continue
						else:
							tmp_semester = semesters[-1]
						print("COURSE INSTRUCTOR", CourseInstructor.objects.filter(course=course["course"], instructor=instructor, semester=tmp_semester), tmp_semester)
						cs_instr = CourseInstructor.objects.filter(course=course["course"], instructor=instructor, semester=tmp_semester)
						if len(rating_instructor) == 0:
							for tmptmp_cs_user in CourseUser.objects.filter(course=course["course"], take="taken", instructor=instructor, course_instructor=cs_instr.first(), text=review):
								tmptmp_cs_user.delete()
							CourseUser.objects.create(user=user, course=course["course"], take="taken", instructor=instructor, course_instructor=cs_instr.first(), text=review)
						else:
							for tmptmp_cs_user in CourseUser.objects.filter(course=course["course"], take="taken", instructor=instructor, course_instructor=cs_instr.first(), text=review, rating_instructor=rating_instructor):
								tmptmp_cs_user.delete()
							CourseUser.objects.create(user=user, course=course["course"], take="taken", instructor=instructor, course_instructor=cs_instr.first(), text=review, rating_instructor=rating_instructor)
						break


