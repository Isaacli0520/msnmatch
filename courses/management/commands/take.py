from django.core.management.base import BaseCommand, CommandError
from courses.models import Course, Instructor, CourseUser, CourseInstructor
import re
import os
import csv
from msnmatch import settings
from functools import cmp_to_key
from msnmatch.utils import cmp_semester


class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		for cs_user in CourseUser.objects.all():
			if cmp_semester(cs_user.course_instructor.semester, settings.CURRENT_SEMESTER) >= 0:
				cs_user.take = "taking"
			else:
				cs_user.take = "taken"
			cs_user.save()