from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import Course, CourseUser, CourseInstructor, Instructor, Department
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity
from django.db.models import Q, F
from django.db.models.functions import Lower, Substr, Length
from django.http import JsonResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from fuzzywuzzy import fuzz, process
import re
from django.shortcuts import get_object_or_404
import json
from django.urls import reverse
from msnmatch import settings
from users.models import MAJOR_CHOICES
from users.views import custom_md5
from users.models import PlanProfile
from functools import cmp_to_key

mnemonics = ['AAS', 'MATH', 'ANTH', 'SWAH', 'MDST', 'ARAD', 'ARAH', 'ARTH', 'ARTS',
'ARAB', 'ARTR', 'HEBR', 'HIND', 'MESA', 'MEST', 'PERS', 'SANS', 'SAST', 'SATR', 'URDU', 'ASTR',
'MUBD', 'MUEN', 'MUPF', 'MUSI', 'BIOL', 'HBIO', 'PHIL', 'CHEM', 'PHYS', 'CLAS', 'GREE', 'LATI',
'PLAD', 'PLAP', 'PLCP', 'PLIR', 'PLPT', 'DANC', 'DRAM', 'PHS', 'PHSE', 'CHIN', 'CHTR', 'EAST',
'JAPN', 'JPTR', 'KOR', 'TBTN', 'PSYC', 'ECON', 'RELA', 'RELB', 'RELC', 'RELG', 'RELH', 'RELI',
'RELJ', 'RELS', 'CPLT', 'ENAM', 'ENCR', 'ENCW', 'ENEC', 'ENGL', 'ENGN', 'ENLP', 'ENLT', 'ENMC',
 'ENMD', 'ENNC', 'ENPG', 'ENPW', 'ENRN', 'ENSP', 'ENWR', 'POL', 'RUSS', 'RUTR', 'SLAV', 'SLTR',
 'EVAT', 'EVEC', 'EVGE', 'EVHY', 'EVSC', 'SOC', 'CREO', 'FRTR', 'FREN', 'ITAL', 'ITTR', 'KICH',
 'PORT', 'POTR', 'SPAN', 'GERM', 'GETR', 'STAT', 'HIAF', 'HIEA', 'HIEU', 'HILA', 'HIME', 'HISA',
 'HIST', 'HIUS', 'EDHS', 'USEM', 'WGS', 'ASL', 'INST', 'AMST', 'JWST', 'ARCY', 'LAST', 'COGS',
 'COLA', 'LASE', 'CS', 'LING', 'LNGS', 'ARH', 'ELA', 'NESC', 'ARCH', 'PLAN', 'EURS', 'PST',
 'GDS', 'GSGS', 'GSMS', 'GSSJ', 'GSVS', 'PAVS', 'FORU', 'EGMT', 'ES', 'NUCO', 'APMA', 'CPE',
 'ECE', 'BME', 'EP', 'MSE', 'CHE', 'MAE', 'CE', 'STS', 'SYS', 'ENGR', 'EDIS', 'EDLF', 'KINE',
 'ALAR', 'LAR', 'PLAC', 'SARC', 'AM', 'LAW', 'GBUS', 'BIMS', 'BIOC', 'BIOP', 'CELL', 'MED',
 'GCOM', 'MICR', 'PATH', 'PHAR', 'PHY', 'COMM', 'GCNL', 'GNUR', 'NUIP', 'NURS', 'ENTP', 'LPPA',
 'LPPL', 'LPPP', 'LPPS', 'DS', 'AIR', 'AIRS', 'CASS', 'EDNC', 'HSCI', 'IMP', 'MISC', 'NAS',
 'NASC', 'PPL', 'UNST', "ESL",]

MAXIMUM_COURSES = 12
DEBUGGG = False

@login_required
def courses(request):
	return render(request, 'courses.html')

@login_required
def course(request, course_number):
	get_object_or_404(Course, pk=course_number)
	return render(request, 'course.html')

@login_required
def course_instructor(request, course_number, instructor_number):
	get_object_or_404(Course, pk=course_number)
	get_object_or_404(Instructor, pk=instructor_number)
	return render(request, 'course_instructor.html')

@login_required
def departments(request):
	return render(request, 'departments.html')

@login_required
def department(request, department_number):
	get_object_or_404(Department, pk=department_number)
	return render(request, 'department.html')

def get_my_courses(request):
	return JsonResponse({
		"taking_courses":get_take_courses(request.user, "taking"),
		"taken_courses":get_take_courses(request.user, "taken"),
	})

def get_taking_courses(request):
	return JsonResponse({
		"taking_courses":get_take_courses(request.user, "taking")
	})

def get_take_courses(user, take):
	cs_users = CourseUser.objects.filter(user=user, take=take)
	courses = []
	for cs_user in cs_users:
		if cs_user.course.pk not in courses:
			courses.append(cs_user.course.pk)
	final_courses = []
	for course_pk in courses:
		tmp_course = get_object_or_404(Course, pk=course_pk)
		final_courses.append({
			"course_pk":course_pk,
			"mnemonic":tmp_course.mnemonic,
			"number":tmp_course.number,
			"title":tmp_course.title,
			"take":take,
			"type":tmp_course.type,
		})
	return final_courses

def get_credential(request):
	return JsonResponse({
		"credential":request.user.profile.credential,
		"username":request.user.username,
	})

@csrf_exempt
def save_plannable_profile(request):
	if request.method == "POST":
		post = json.loads(request.body)
		username, credential, name, profile = post["username"][1:-1], post["credential"][1:-1], post["name"], post["profile"]
		user = get_object_or_404(User, username=username)
		if credential == custom_md5(settings.SECRET_KEY + user.username, settings.SECRET_KEY):
			planProfileQueryset = PlanProfile.objects.filter(user=user, name=name)
			if planProfileQueryset.first() != None:
				plan_profile = planProfileQueryset.first()
				plan_profile.content = profile
				plan_profile.save()
			else:
				plan_profile = PlanProfile.objects.create(user=user, name=name, content=profile)
			success = True
		else:
			success = False
	else:
		success = False
	return JsonResponse({
		"success":success,
	})

def get_recommendations(request):
	year, semester, major = request.GET.get('year'), request.GET.get('semester'), request.GET.get('major')
	users_pk = [sth.pk for sth in User.objects.filter(profile__major=major)]
	if len(users_pk) == 0:
		return JsonResponse({
			"rcm_courses":[],
		})
		
	cs_users = CourseUser.objects.filter(user__pk__in=users_pk, take="taken")
	final_cs_users = []
	courses_dict = {}
	for cs_user in cs_users:
		if cs_user.user.profile.graduate_year:
			tmp_year, tmp_semester = year_and_semester(cs_user.course_instructor.semester)
			if tmp_year + 4 - int(cs_user.user.profile.graduate_year) == int(year) and tmp_semester == semester:
				final_cs_users.append(cs_user)

	for cs_user in final_cs_users:
		if cs_user.course.pk not in courses_dict:
			courses_dict[cs_user.course.pk] = 1
		else:
			courses_dict[cs_user.course.pk] += 1

	courses = []
	for pk, num in courses_dict.items():
		tmp_course = get_object_or_404(Course, pk=pk)
		courses.append({
			"course_pk":pk,
			"mnemonic":tmp_course.mnemonic,
			"number":tmp_course.number,
			"title":tmp_course.title,
			"taken":num,
			})
	return JsonResponse({
		"rcm_courses":courses,
	})

def get_major_options(request):
	if request.user.profile.major:
		major = request.user.profile.major
	majors = []
	for item in MAJOR_CHOICES:
		majors.append({
			"text":item[0],
			"value":item[0],
		})
	return JsonResponse({
		"major_options":majors,
		"major":major,
	})

def year_and_semester(ys):
	year, semester = ys[:4], ys[4:]
	if semester == "Spring":
		return int(year) + 1, semester
	else:
		return int(year), semester

def get_trending_courses(request):
	trending_courses = {}
	for cs_user in CourseUser.objects.all():
		tmp_course = cs_user.course
		if tmp_course.pk not in trending_courses:
			trending_courses[tmp_course.pk] = {"taking":0, "taken":0,}
		if cs_user.take == "taking":
			trending_courses[tmp_course.pk]["taking"] += 1
		elif cs_user.take == "taken":
			trending_courses[tmp_course.pk]["taken"] += 1
	tmp_courses = []
	for cs_pk, take in trending_courses.items():
		tmp_course = get_object_or_404(Course, pk = cs_pk)
		tmp_courses.append({
			"course_pk":cs_pk,
			"title":tmp_course.title,
			"mnemonic":tmp_course.mnemonic,
			"number":tmp_course.number,
			"taking":take["taking"],
			"taken":take["taken"],
		})
	taking_courses = sorted(tmp_courses, key=lambda x:(x["taking"]), reverse=True)[:10]
	taken_courses = sorted(tmp_courses, key=lambda x:(x["taken"]), reverse=True)[:10]
	taking_courses = [cs for cs in taking_courses if cs["taking"] > 0]
	taken_courses = [cs for cs in taken_courses if cs["taken"] > 0]
	return JsonResponse({
		"taking_courses":taking_courses,
		"taken_courses":taken_courses,
	})

def get_departments(request):
	all_departments = Department.objects.all().exclude(name="")
	departments = []
	for department in all_departments:
		departments.append({
			"department_pk":department.pk,
			"name":department.name,
			"school":department.school,
		})
	return JsonResponse({
		"departments":departments,
	})

def get_department(request):
	department_pk = request.GET.get("department_pk")
	department = get_object_or_404(Department, pk=department_pk)
	ret_courses = [get_detailed_json_of_course(cs, request.user, with_take=True) for cs in department.course_set.all().exclude(units="0")]
	
	return JsonResponse({
		"department":{
			"name":department.name,
			"school":department.school,
		},
		"courses":ret_courses,
	})

def submit_review(request):
	if request.method == "POST":
		post = json.loads(request.body)
		text, rating_course, rating_instructor = post["text"], post["rating_course"], post["rating_instructor"]
		course_pk, instructor_pk, course_instructor_pk =  post["course_pk"], post["instructor_pk"], post["course_instructor_pk"]
		
		course = get_object_or_404(Course, pk=course_pk)
		instructor = get_object_or_404(Instructor, pk=instructor_pk)
		course_instructor = get_object_or_404(CourseInstructor, pk=course_instructor_pk)
		cs_user_query = CourseUser.objects.filter(course=course, user=request.user)
		if cs_user_query.first() != None:
			cs_user = cs_user_query.first()
			cs_user.text = text
			cs_user.instructor = instructor
			cs_user.take = "taken"
			cs_user.rating_course = rating_course
			cs_user.rating_instructor = rating_instructor
			cs_user.course_instructor = course_instructor
			cs_user.save()
		else:
			CourseUser.objects.create(course=course,
				user=request.user, 
				instructor=instructor,
				course_instructor=course_instructor,
				text=text,
				take="taken",
				rating_course=rating_course,
				rating_instructor=rating_instructor)
		success = True
	else:
		success = False
	return JsonResponse({
		"success":success,
	})

def save_take(request):
	now_instructor_pk, now_semester, now_take = "", "", ""
	if request.method == "POST":
		post = json.loads(request.body)
		take, semester, delete = post['take'], post['semester'], post['delete']
		course = get_object_or_404(Course, pk=post['course_pk'])
		past_query = CourseUser.objects.filter(user=request.user, course = course)
		if delete:
			if past_query.first() != None:
				past_query.first().delete()
			return JsonResponse({
				"success":True,
			})
		instructor = get_object_or_404(Instructor, pk=post['instructor_pk'])
	
		cs_instr = get_object_or_404(CourseInstructor, pk=post["course_instructor_pk"])

		if past_query.first() != None:
			past_query.first().delete()
		if not delete:
			cs_user = CourseUser.objects.create(user=request.user, course = course, instructor = instructor, take = take, course_instructor = cs_instr)
			now_instructor_pk, now_semester, now_take = cs_user.course_instructor.instructor.pk, cs_user.course_instructor.semester, cs_user.take
		success = True
	else:
		success = False
	return JsonResponse({
		"success":success,
		"now":{
			"instructor_pk":now_instructor_pk,
			"semester":now_semester,
			"take":now_take,
		},
	})

def get_course(request):
	pk = request.GET.get("pk")
	course = get_object_or_404(Course, pk=pk)
	return JsonResponse({
		"course":get_detailed_json_of_course(course, request.user, with_instructors=True),
	})

def get_course_instructor(request):
	course_pk, instructor_pk = request.GET.get("course_pk"), request.GET.get("instructor_pk")
	course = get_object_or_404(Course, pk=course_pk)
	instructor = get_object_or_404(Instructor, pk=instructor_pk)
	return JsonResponse(get_detailed_json_of_course_instructor(course, instructor, request.user))

def course_search_result(request):
	score_cutoff = 85
	query = request.GET.get("query").strip()
	time = request.GET.get("time")
	if query.upper() in mnemonics:
		field_queryset = Course.objects.filter(mnemonic = query.upper()).exclude(units="0")
	else:
		pk_queryset = {fq.pk:(str(getattr(fq, "mnemonic")) + str(getattr(fq,"number")) + " " + str(getattr(fq, "title")) ) for fq in Course.objects.exclude(units="0")}
		if len(pk_queryset) > 0:
			all_pks = process.extractBests(query, pk_queryset,scorer=fuzz.partial_ratio, score_cutoff=score_cutoff, limit=20)
			all_pks = [item[2] for item in all_pks]
			field_queryset = Course.objects.filter(pk__in=all_pks)
		else:
			field_queryset = None
	return JsonResponse({
		"course_result":get_json_of_courses(field_queryset),
		"time":time,
	})

def get_json_of_courses(queryset):
	if queryset != None and queryset.first() != None:
		return [get_json_of_course(cs) for cs in queryset]
	else:
		return []

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
	return cmp_semester(a["semester"], b["semester"])

def get_json_of_course(course):
	cs_instr_arr = [cs_instr.semester for cs_instr in CourseInstructor.objects.filter(course=course)]
	cs_instr_arr = sorted(cs_instr_arr, key=cmp_to_key(cmp_semester))
	last_taught = settings.CURRENT_SEMESTER
	if settings.CURRENT_SEMESTER not in cs_instr_arr:
		last_taught = cs_instr_arr[-1]
	return {
		"pk":course.pk,
		"mnemonic":course.mnemonic,
		"number":course.number,
		"title":course.title,
		"last_taught":last_taught,
	}

def get_basic_info(request):
	tmp = {
		"home_url":reverse('home'),
		"brand_pic": settings.STATIC_URL + "css/images/brand.png",
		"profile": reverse('profile', args=[request.user.username]),
		"update_profile":reverse('update_profile', args=[request.user.username]),
		"my_courses":reverse('my_courses', args=[request.user.username]),
		"logout":reverse('logout'),
	}
	return JsonResponse({
		"all_info":tmp,
	})


def get_detailed_json_of_course_instructor(course, instructor, user):
	course_instructor_relations = []
	course_instructor_query = CourseInstructor.objects.filter(course=course, instructor=instructor)
	for course_instructor in course_instructor_query:
		course_instructor_relations.append({
			"course_instructor_pk":course_instructor.pk,
			"topic":course_instructor.topic,
			"semester":course_instructor.semester,
			})
	course_users = [get_detailed_json_of_course_user(course_user, user) for course_user in CourseUser.objects.filter(course=course, instructor=instructor)]

	return {
		"course":get_detailed_json_of_course(course, user),
		"instructor":{
			"name":instructor.__str__(),
			"rating_instructor":get_rating_of_instructor(instructor),
		},
		"course_instructors":course_instructor_relations,
		"course_users":course_users,
	}

def get_detailed_json_of_course_user(course_user, user):
	return {
		"user_pk":course_user.user.pk,
		"name":course_user.user.first_name + " " + course_user.user.last_name,
		"take":course_user.take,
		"text":course_user.text,
		"semester":course_user.course_instructor.semester,
		"rating_course":course_user.rating_course,
		"rating_instructor":course_user.rating_instructor,
	}

def get_detailed_json_of_course(course, user, with_instructors=False, with_take=False):
	courseUser_query = CourseUser.objects.filter(user=user, course=course).first()
	take = {"instructor_pk":"", "course_pk":"", "semester":"", "take":""}

	rating_course = get_rating_of_course(course)
	if courseUser_query != None:
		take = {
			"instructor_pk":courseUser_query.course_instructor.instructor.pk,
			"course_pk":courseUser_query.course.pk,
			"semester":courseUser_query.course_instructor.semester,
			"take":courseUser_query.take,
			"course_instructor_pk":courseUser_query.course_instructor.pk,
		}
	course_dict = {
		"course_pk":course.pk,
		"mnemonic":course.mnemonic,
		"number":course.number,
		"title":course.title,
		"description":course.description,
		"prerequisite":course.prerequisite,
		"type":course.type,
		"take":take,
		"department":{
			"name":course.department.name,
			"department_pk":course.department.pk,
		},
		"rating_course":rating_course,
	}
	if with_instructors:
		course_dict["instructors"] = get_instructors_of_course(course)
	if with_take:
		course_dict["taking"] = CourseUser.objects.filter(course=course, take="taking").count()
		course_dict["taken"] = CourseUser.objects.filter(course=course, take="taken").count()
	return course_dict

def get_instructors_of_course(course):
	courseInstructor_query = CourseInstructor.objects.filter(course=course)
	final_instructors = []
	if courseInstructor_query.first() != None:
		instructors = {}
		for cs_instructor in courseInstructor_query:
			tmp_name = cs_instructor.instructor.__str__()
			rating_instructor = get_rating_of_instructor_with_course(cs_instructor.instructor, course)
			if tmp_name not in instructors:
				instructors[tmp_name] = {"semesters":[{
					"semester":cs_instructor.semester,
					"course_instructor_pk":cs_instructor.pk,
					"topic":cs_instructor.topic,
				}]}
				instructors[tmp_name]["pk"] = cs_instructor.instructor.pk
				instructors[tmp_name]["rating_instructor"] = rating_instructor
			else:
				instructors[tmp_name]["semesters"].append({
					"semester":cs_instructor.semester,
					"course_instructor_pk":cs_instructor.pk,
					"topic":cs_instructor.topic,
				})
		for k,v in instructors.items():
			topic = ""
			if len(v["semesters"]) > 0:
				v["semesters"] = sorted(v["semesters"], key=cmp_to_key(cmp_semester_key), reverse=True)
				topic = v["semesters"][0]["topic"]
			final_instructors.append({
				"name":k,
				"semesters":v["semesters"],
				"topic":topic,
				"pk":v["pk"],
				"rating_instructor":v["rating_instructor"],
			})
	return final_instructors

def get_rating_of_course(course):
	allCourseUser_course_query = CourseUser.objects.filter(course=course)
	rating_course_arr = []
	for cs_user in allCourseUser_course_query:
		if cs_user.rating_course != None and cs_user.rating_course > 0:
			rating_course_arr.append(cs_user.rating_course)
	if len(rating_course_arr) > 0:
		rating_course = sum(rating_course_arr)/len(rating_course_arr)
	else:
		rating_course = 0
	return rating_course

def get_rating_of_instructor_with_course(instructor, course):
	allCourseUser_instructor_query = CourseUser.objects.filter(course=course, instructor = instructor)
	return get_rating(allCourseUser_instructor_query)

def get_rating_of_instructor(instructor):
	allCourseUser_instructor_query = CourseUser.objects.filter(instructor = instructor)
	return get_rating(allCourseUser_instructor_query)

def get_rating(course_user_queryset):
	rating_instructor_arr = []
	for cs_user in course_user_queryset:
		if cs_user.rating_instructor != None and cs_user.rating_instructor > 0:
			rating_instructor_arr.append(cs_user.rating_instructor)
	if len(rating_instructor_arr) > 0:
		rating_instructor = sum(rating_instructor_arr)/len(rating_instructor_arr)
	else:
		rating_instructor = 0
	return rating_instructor