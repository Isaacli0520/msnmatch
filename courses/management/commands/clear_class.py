from django.core.management.base import BaseCommand, CommandError
from courses.models import Course, Instructor, CourseUser, CourseInstructor
import re
import os
import csv
from msnmatch import settings
from functools import cmp_to_key
from msnmatch.utils import cmp_semester

# Seminar 1262
# Independent Study 839
# Lecture 4646
# Laboratory 231
# IND 440
# Studio 152
# Discussion 441
# Workshop 74
# Practicum 131
# Drill 2
# SEM 443
#  32
# Clinical 66
# STO 61
# PRA 75
# CLN 26
# WKS 27
# DRL 1

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
		for cs in Course.objects.all():
			if cs.type in type_dict:
				cs_instrs = CourseInstructor.objects.filter(course=cs)
				real_cs = Course.objects.filter(mnemonic=cs.mnemonic,number=cs.number,title=cs.title, type=type_dict[cs.type])
				if real_cs.first() == None:
					cs.type = type_dict[cs.type]
					cs.save()
					print(cs.mnemonic, cs.number,cs.title,"NUM:", real_cs.count())
				elif real_cs.count() > 1:
					print("Sth is fked up")
					break
				else:
					print(cs.mnemonic, cs.number,cs.title,":::Extra")
					tmp_cs = real_cs.first()
					for cs_instr in cs_instrs:
						cs_instr.course = tmp_cs
						cs_instr.save()
					cs.delete()