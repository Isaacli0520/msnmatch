from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import Course, CourseUser, CourseInstructor, Instructor
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
	return render(request, 'course.html')

@login_required
def course_instructor(request, course_instructor_number):
	return render(request, 'course_instructor.html')

@login_required
def submit_review(request):
	if request.method == "POST":
		post = json.loads(request.body)
		text, rating_course, rating_instructor = post["text"], post["rating_course"], post["rating_instructor"]
		course_pk, course_instructor_pk =  post["course_pk"], post["course_instructor_pk"]
		
		course = get_object_or_404(Course, pk=course_pk)
		course_instructor = get_object_or_404(CourseInstructor, pk=course_instructor_pk)
		cs_user_query = CourseUser.objects.filter(course=course, user=request.user)
		if cs_user_query.first() != None:
			cs_user = cs_user_query.first()
			cs_user.text = text
			cs_user.rating_course = rating_course
			cs_user.rating_instructor = rating_instructor
			cs_user.save()
		else:
			CourseUser.objects.create(course=course,
				user=request.user, 
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

@login_required
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
	
		cs_instr = get_object_or_404(CourseInstructor, course=course,instructor=instructor, semester=semester)

		if past_query.first() != None:
			past_query.first().delete()
		if not delete:
			cs_user = CourseUser.objects.create(user=request.user, course = course, take = take, course_instructor = cs_instr)
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

@login_required
def get_course(request):
	print("get course")
	pk = request.GET.get("pk")
	course = get_object_or_404(Course, pk=pk)
	return JsonResponse({
		"course":get_detailed_json_of_course(course, request.user),
	})
@login_required
def get_course_instructor(request):
	print("get course instructor")
	pk = request.GET.get("pk")
	course_instructor = get_object_or_404(CourseInstructor, pk=pk)
	print("ALALALALALAL", course_instructor)
	print(get_detailed_json_of_course_instructor(course_instructor, request.user))
	return JsonResponse(get_detailed_json_of_course_instructor(course_instructor, request.user))

@login_required
def get_course_user(request):
	course_instructor_pk = request.GET.get("course_instructor_pk")
	course_instructor = get_object_or_404(CourseInstructor, pk=course_instructor_pk)
	course_users = [get_detailed_json_of_course_user(course_user, request.user) for course_user in CourseUser.objects.filter(course_instructor=course_instructor)]
	return JsonResponse({
		"course_users":course_users,
	})

@login_required
def course_search_result(request):
	score_cutoff = 85
	query = request.GET.get("query").strip()
	time = request.GET.get("time")
	print("QUERY", query)
	if query.upper() in mnemonics:
		field_queryset = Course.objects.filter(mnemonic = query.upper())
	else:
		pk_queryset = {fq.pk:(str(getattr(fq, "mnemonic")) + str(getattr(fq,"number")) + " " + str(getattr(fq, "title")) ) for fq in Course.objects.exclude(units="0")}
		if len(pk_queryset) > 0:
			all_pks = process.extractBests(query, pk_queryset,scorer=fuzz.partial_ratio, score_cutoff=score_cutoff, limit=None)
			all_pks = [item[2] for item in all_pks]
			field_queryset = Course.objects.filter(pk__in=all_pks)
		else:
			field_queryset = None
	
	return JsonResponse({
		"course_result":get_json_of_courses(field_queryset, request.user),
		"time":time,
	})

def get_json_of_courses(queryset, user):
	return [get_json_of_course(cs, user) for cs in queryset]

def get_json_of_course(course, user):
	tmp_courseUser_query = CourseUser.objects.filter(user=user, course=course).first()
	if tmp_courseUser_query == None:
		take = "Null"
	else:
		take = tmp_courseUser_query.take
	return {
		"pk":course.pk,
		"mnemonic":course.mnemonic,
		"number":course.number,
		"title":course.title,
		"take":take,
	}

def get_basic_info(request):
	tmp = {
		"home_url":reverse('home'),
		"brand_pic": settings.STATIC_URL + "css/images/brand.png",
		"profile": reverse('profile', args=[request.user.username]),
		"update_profile":reverse('update_profile', args=[request.user.username]),
		"logout":reverse('logout'),
	}
	return JsonResponse({
		"all_info":tmp,
	})


def get_detailed_json_of_course_instructor(course_instructor, user):
	course, instructor, topic, semester = course_instructor.course, course_instructor.instructor, course_instructor.topic, course_instructor.semester
	course_users = [get_detailed_json_of_course_user(course_user, user) for course_user in CourseUser.objects.filter(course_instructor=course_instructor)]
	rating_course = []
	rating_instructor = []
	print("course Users", course_users)
	for cs_user in course_users:
		if cs_user['rating_course'] != None:
			rating_course.append(cs_user['rating_course'])
		if cs_user['rating_instructor'] != None:
			rating_instructor.append(cs_user['rating_instructor'])
	r_instr = 0
	r_cs = 0
	if len(rating_instructor) > 0:
		r_instr = sum(rating_instructor)/len(rating_instructor)
	if len(rating_course) > 0:
		r_cs = sum(rating_course)/len(rating_course)

	return {
		"course":{
				"course_pk":course.pk,
				"mnemonic":course.mnemonic,
				"number":course.number,
				"title":course.title,
				"description":course.description,
				"prerequisite":course.prerequisite,
				"type":course.type,
				"rating_instructor":r_instr,
				"rating_course":r_cs,
			},
		"instructor":instructor.__str__(),
		"topic":topic,
		"semester":semester,
		"course_users":course_users,
	}

def get_detailed_json_of_course_user(course_user, user):
	return {
		"user_pk":course_user.user.pk,
		"name":course_user.user.first_name + " " + course_user.user.last_name,
		"take":course_user.take,
		"text":course_user.text,
		"rating_course":course_user.rating_course,
		"rating_instructor":course_user.rating_instructor,
	}

def get_detailed_json_of_course(course, user):
	courseUser_query = CourseUser.objects.filter(user=user, course=course).first()
	courseInstructor_query = CourseInstructor.objects.filter(course=course)
	if courseInstructor_query.first() == None:
		final_instructors = []
	else:
		instructors = {}
		for cs_instructor in courseInstructor_query:
			tmp_name = cs_instructor.instructor.first_name + " " + cs_instructor.instructor.last_name
			if tmp_name not in instructors:
				instructors[tmp_name] = {"semesters":[ cs_instructor.semester ]}
				instructors[tmp_name]["topic"] = cs_instructor.topic
				instructors[tmp_name]["pk"] = cs_instructor.instructor.pk
				instructors[tmp_name]["cs_instr_pk"] = cs_instructor.pk
			else:
				instructors[tmp_name]["semesters"].append(cs_instructor.semester)
		final_instructors = []
		for k,v in instructors.items():
			final_instructors.append({
				"name":k,
				"semesters":v["semesters"],
				"topic":v["topic"],
				"pk":v["pk"],
				"cs_instr_pk":v["cs_instr_pk"],
			})
	if courseUser_query == None:
		take = {
			"instructor_pk":"",
			"course_pk":"",
			"semester":"",
			"take":"",
		}
	else:
		take = {
			"instructor_pk":courseUser_query.course_instructor.instructor.pk,
			"course_pk":courseUser_query.course.pk,
			"semester":courseUser_query.course_instructor.semester,
			"take":courseUser_query.take,
		}
	return {
		"pk":course.pk,
		"mnemonic":course.mnemonic,
		"number":course.number,
		"title":course.title,
		"take":take,
		"instructors":final_instructors,
	}

# def course_search_result(request):
# 	course_list = []
# 	query_string = request.GET.get("input").strip()
# 	retrieved_courses = course_retrieve(query_string)

# 	for cs in retrieved_courses:
# 		new_cs = {
# 			"course_number": cs.course_number.strip(),
# 			"course_name": cs.course_name.strip(),
# 			"course_match": lcs(query_string.lower(), cs.course_number.strip().lower() + " " + cs.course_name.strip().lower()),
# 			"course_exist": cs.course_users.filter(username__iexact = request.user.username).exists(),
# 			"course_taking": CourseUser.objects.filter(user=request.user, course=cs, take="taking").exists(),
# 			"course_taken": CourseUser.objects.filter(user=request.user, course=cs, take="taken").exists(),
# 		}
# 		course_list.append(new_cs)
# 	return JsonResponse({
# 		"retrieved_courses":course_list,
# 		})

@login_required
def course_search(request):
	query_string = ''
	if 'q' in request.GET:
		query_string = request.GET['q'].strip()
		retrieved_courses = course_retrieve(query_string)

		return render(request, 'course_search.html', { "retrieved_courses":retrieved_courses, "query_string":query_string })
	else:
		return render(request, 'course_search.html', { "retrieved_courses":None, "query_string":query_string })

def course_retrieve(query_string):

	# Get the num and non-num strings of the query_string
	nums = re.findall(r'\d+', query_string)
	strs = []
	for s in re.findall(r'[^\d.]+', query_string):
		strs += s.split()
	strs = [s.strip() for s in strs]

	# Extract the mnemonics from the non-num strings
	tmp_mn = [strs[i] for i in range(len(strs)) if strs[i].upper() in mnemonics]
	tmp_ix = [i for i in range(len(strs)) if strs[i].upper() in mnemonics]
	new_strs = [strs[i] for i in range(len(strs)) if i not in tmp_ix]

	# Get the extracted queries of mnemonics, nums, and other non-num strings
	query_string_mn = " ".join(tmp_mn)
	query_string_str = " ".join([s.strip() for s in new_strs])
	query_string_num = nums[0] if len(nums) > 0 else ""

	# Get the exact match class (if there is no such class, exact_match_first_course == None)
	exact_match_courses = Course.objects.filter(course_number = "".join(query_string_mn + query_string_num).upper())
	exact_match_first_course = exact_match_courses.first()

	if DEBUGGG == True:
		print(query_string, "----", query_string_mn, "----", query_string_num, "----",query_string_str, "----")

	if query_string_str == "" and query_string_mn.upper() in mnemonics and exact_match_first_course != None :
		retrieved_courses = exact_match_courses
	elif query_string.upper() in mnemonics:
		retrieved_courses = Course.objects.filter(course_number__startswith = query_string.upper())
	else:
		tmp_queryset = Course.objects.annotate(
			similarity_prefix=TrigramSimilarity(Substr('course_number',1, Length('course_number')-4),query_string_mn),
			similarity_number=TrigramSimilarity(Substr('course_number', Length('course_number')-3, 4),query_string_num),
			similarity_name=TrigramSimilarity('course_name', query_string_str)).filter(Q(similarity_prefix__gt=0.25)|Q(similarity_number__gt=0.23)|Q(similarity_name__gt=0.15))
		retrieved_courses = sorted(tmp_queryset, key=lambda c: (-c.similarity_prefix,-c.similarity_number, -c.similarity_name,re.findall(r'\d+', c.course_number)[0],re.findall(r'[^\d.]+', c.course_number)[0]))
		retrieved_courses = retrieved_courses[:MAXIMUM_COURSES]

		if DEBUGGG == True:
			for course in retrieved_courses:
				print(course.similarity_prefix,"  ",course.similarity_number,"  ",course.similarity_name,"  ", re.findall(r'[^\d.]+', course.course_number)[0],"  ", re.findall(r'\d+', course.course_number)[0])

	return retrieved_courses

def lcs(s1, s2):
	l1, l2 = len(s1), len(s2)
	if l1 == 0 or l2 == 0: return []
	index = 0
	ret = []
	for i in range(len(s2)):
		while index < l1 and s1[index] == " ":
			index += 1
		if index < l1 and s2[i] == s1[index]:
			ret.append(1)
			index += 1
		else:
			ret.append(0)
	return ret
