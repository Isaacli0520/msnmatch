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
from django.http import HttpResponse

class Command(BaseCommand):

	def handle(self, *args, **kwargs):
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="hsmp_comments.csv"'

		writer = csv.writer(response)
		for cs in CourseUser.objects.all():
			tmp_row = []
			for field in CourseUser._meta.fields:
				tmp_row.append(getattr(cs, field.name))
			writer.writerow(tmp_row)
		return response