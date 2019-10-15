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
		for cs in Course.objects.all():
			cs_instr_arr = [cs_instr.semester for cs_instr in CourseInstructor.objects.filter(course=cs)]
			cs_instr_arr = sorted(cs_instr_arr, key=cmp_to_key(cmp_semester))
			cs.last_taught = cs_instr_arr[-1]
			cs.save()