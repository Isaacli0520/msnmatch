from django.core.management.base import BaseCommand, CommandError
from courses.models import Course, Instructor, CourseUser, CourseInstructor
import re
import os
import csv

departments = {
	"Commerce":{"COMM", "ECON", "ENTP"},
	"Science":{"ASTR", "BIOL", "CHEM", "EVSC", "PHYS", "PSYC"},
	"Humanity":{"AMST", "ANTH", "ARH", "ARTH", "CLAS", "EDIS", "HIEU", "HILA"
	,"HIUS", "PHIL", "PLAD", "PLAP", "PLIR", "PLPT", "PPOL", "RELB", "RELG",
	"RELI", "RELJ", "SOC"},
	"Mathematics":{"APMA", "MATH", "STAT"},
	"Engineering":{"CHE", "CS", "ECE", "ENGR", "MAE", "MSE", "STS"},
	"Architecture":{"ARCH", "ARH", "MDST", "PLAN"},
	"Language":{"CHTR", "CPLT", "ENGL", "ENWR", "FREN", "GERM", "GETR", "JAPN", "KOR",
	"RUTR", "SATR", "SLAV", "SPAN"},
	"ART":{"ARTS", "DANC", "DRAM", "MUEN", "MUSI"},
	"Others":{"COLA", "EDIS", "EGMT", "FORU", "KINE", "USEM", "WGS"}
}

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		pattern = r"co-taught by ((([a-z]+.*)+) and)+ ([a-z]+.*)+"
		ppp=re.compile(pattern,flags=re.IGNORECASE)
		for cs in Course.objects.all():
			cs.delete()
		data = []
		for path, subdirs, files in os.walk("data"):
			for file in files:
				if file[:5] == "Class":
					data.extend(read_course_data(os.path.join(path, file), file))
		for cs in data:
			course_query = Course.objects.filter(number=cs['Number'], mnemonic=cs['Mnemonic'],
			title=cs['Title'], type=cs['Type'])

			if course_query.first() == None:
				tmp_course = Course.objects.create(number=cs['Number'], mnemonic=cs['Mnemonic'], units=cs['Units'],
				title=cs['Title'],description=cs["Description"], type=cs['Type'],
				prerequisite=cs['Prerequisite'])
			else:
				tmp_course = course_query.first()
				if tmp_course.units != cs['Units']:
					tmp_course.units = cs["Units"]
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
			# if sum([len(item) for item in final_instructors]) > 3:
			# 	print("instructors", final_instructors)
			# print("instructors", final_instructors)
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
					CourseInstructor.objects.create(instructor=tmp_instr, course=tmp_course, topic=cs["Topic"], semester=cs["Semester"])
			


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