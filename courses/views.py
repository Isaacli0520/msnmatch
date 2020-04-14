import re
import time
import json

from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity
from django.db.models import Q, F
from django.db.models.functions import Lower, Substr, Length
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse

from fuzzywuzzy import fuzz, process
from msnmatch import settings

from msnmatch.utils import custom_md5, cmp_semester
from functools import cmp_to_key

from users.models import MAJOR_CHOICES, PlanProfile
from .models import Course, CourseUser, CourseInstructor, Instructor, Department

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
def reviews(request):
	return render(request, 'reviews.html')

@login_required
def instructor(request, instructor_number):
	get_object_or_404(Instructor, pk=instructor_number)
	return render(request, 'instructor.html')

@login_required
def department(request, department_number):
	get_object_or_404(Department, pk=department_number)
	return render(request, 'department.html')

@login_required
def courses_admin(request):
	return render(request, 'courses_admin.html')

@login_required
def get_current_semester(request):
	return JsonResponse({
		"year":settings.CURRENT_SEMESTER[:4],
		"semester":settings.CURRENT_SEMESTER[4:],
	})

# @login_required
def get_basic_info(request):
	if request.user.is_authenticated:
		info = {
			"home_url":reverse('home'),
			"courses_url": reverse('courses'),
			"comment_url": reverse('comments:comments_send'),
			"brand_pic": settings.STATIC_URL + "css/images/brand_compressed.png",
			"profile": reverse('profile', args=[request.user.username]),
			"update_profile":reverse('update_profile', args=[request.user.username]),
			"my_courses":reverse('my_courses', args=[request.user.username]),
			"logout":reverse('logout'),
			"market_url":reverse('market:market'),
			"match_url":reverse('match'),
		}
	else:
		info = {
			"home_url":reverse('home'),
			"courses_url": reverse('courses'),
			"market_url":reverse('market:market'),
			"comment_url": reverse('comments:comments_send'),
			"brand_pic": settings.STATIC_URL + "css/images/brand_compressed.png",
			"match_url":reverse('match'),
		}
	return JsonResponse({
		"all_info":info,
	})

"""
	Get the users with top reviews(sorted by review counts from maximum to minimum).

	HttpRequest Method: GET

	API Parameters:
		None

	Returns:
		JsonResponse:
			review_users: list
				pk: user pk
				username: user username
				name: user name
				reviews: user review count

"""
@login_required
def get_top_review_users(request):
	users = []
	for user in User.objects.all():
		user_review_num = user.courseuser_set.annotate(length=Length("text")).filter(length__gt=0).count()
		if user_review_num > 0:
			users.append({
				"pk":user.pk,
				"username":user.username,
				"name":user.first_name + " " + user.last_name,
				"reviews":user_review_num,
			})
	users = sorted(users, key=lambda x:x["reviews"], reverse=True)[:30]
	return JsonResponse({
		"review_users":users,
	})

@login_required
def get_course_instructors(request):
	course_pk, instructor_pk = request.GET.get("course_pk"), request.GET.get("instructor_pk")
	course = get_object_or_404(Course, pk=course_pk)
	instructor = get_object_or_404(Instructor, pk=instructor_pk)

	course_instructor_relations = []
	course_instructor_query = CourseInstructor.objects.filter(course=course, instructor=instructor)
	for course_instructor in course_instructor_query:
		course_instructor_relations.append({
			"course_instructor_pk":course_instructor.pk,
			"semester":course_instructor.semester,
			"topic":course_instructor.topic,
			})

	return JsonResponse({
		"course_instructors":course_instructor_relations,
	})

@login_required
def get_reviews(request):
	cs_users = CourseUser.objects.filter(user=request.user, take="taken")
	reviews_arr = [cs_user for cs_user in cs_users if cs_user.text]
	return JsonResponse({
		"reviews":[get_json_of_review(review) for review in reviews_arr]
	})

def get_json_of_review(review):
	return {
		"course":{
			"mnemonic":review.course.mnemonic,
			"number":review.course.number,
			"title":review.course.title,
			"course_pk":review.course.pk,
		},
		"semester":review.course_instructor.semester,
		"text":review.text,
		"rating_instructor":review.rating_instructor,
		"rating_course":review.rating_course,
		"instructor_pk":review.instructor.pk,
		"course_instructor_pk":review.course_instructor.pk,
	}

@login_required
def get_list_of_plannable_profiles(request):
	username, credential = request.GET.get("username"), request.GET.get("credential")
	user = get_object_or_404(User, username=username)
	ret_profiles = []
	if credential == custom_md5(settings.SECRET_KEY + user.username, settings.SECRET_KEY):
		profiles_query =PlanProfile.objects.filter(user=user)
		for profile in profiles_query:
			ret_profiles.append({
				"profile_pk":profile.pk,
				"name":profile.name,
			})
	return JsonResponse({
		"profiles":ret_profiles,
	})

@login_required
def get_instructor(request):
	instructor_pk = request.GET.get("instructor_pk")
	instructor = get_object_or_404(Instructor, pk=instructor_pk)
	cs_instr_query = CourseInstructor.objects.filter(instructor=instructor)
	all_courses = {}
	for cs_instr in cs_instr_query:
		tmp_course_number = cs_instr.course.mnemonic + cs_instr.course.number
		if tmp_course_number not in all_courses:
			all_courses[tmp_course_number] = {
				"course_pk":cs_instr.course.pk,
				"mnemonic":cs_instr.course.mnemonic,
				"number":cs_instr.course.number,
				"title":cs_instr.course.title,
				"rating":get_rating_of_instructor_with_course(instructor, cs_instr.course)[0],
				"semesters":[]
			}
		all_courses[tmp_course_number]["semesters"].append(cs_instr.semester)
	tmp_rating, tmp_counter = get_rating_of_instructor(instructor)
	return JsonResponse({
		"name":instructor.__str__(),
		"rating":tmp_rating,
		"rating_counter":tmp_counter,
		"rating_users_count":sum(tmp_counter),
		"courses":all_courses,
	})

@login_required
def get_my_courses(request):
	return JsonResponse({
		"taking_courses":get_take_courses(request.user, "taking"),
		"taken_courses":get_take_courses(request.user, "taken"),
	})

@login_required
def get_taking_courses(request):
	return JsonResponse({
		"taking_courses":get_take_courses(request.user, "taking")
	})

def get_take_courses(user, take):
	final_courses = []
	cs_users = CourseUser.objects.filter(user=user, take=take)
	for cs_user in cs_users:
		final_courses.append({
			"course_pk":cs_user.course.pk,
			"mnemonic":cs_user.course.mnemonic,
			"number":cs_user.course.number,
			"title":cs_user.course.title,
			"take":take,
			"type":cs_user.course.type,
			"semester":cs_user.course_instructor.semester,
		})
	return final_courses

@login_required
def get_credential(request):
	return JsonResponse({
		"credential":request.user.profile.credential,
		"username":request.user.username,
	})

@csrf_exempt
def edit_plannable_profile(request):
	success = False
	if request.method == "POST":
		print("post")
		post = json.loads(request.body)
		username, credential= post["username"][1:-1], post["credential"][1:-1]
		action = post["action"]
		user = get_object_or_404(User, username=username)
		if credential == custom_md5(settings.SECRET_KEY + user.username, settings.SECRET_KEY):
			if action == "rename":
				oldName, newName = post["oldName"], post["newName"]
				tmp_profile = get_object_or_404(PlanProfile, user=user ,name=oldName)
				tmp_profile.name = newName
				tmp_profile.save()
				success = True
			elif action == "delete":
				print("delete")
				tmp_name = post["name"]
				tmp_profile = get_object_or_404(PlanProfile, user=user ,name=tmp_name)
				tmp_profile.delete()
				success = True
	return JsonResponse({
		"success":success,
	})

@csrf_exempt
def get_plannable_profile(request):
	ret_profile = []
	if request.method == "POST":
		post = json.loads(request.body)
		username, credential= post["username"][1:-1], post["credential"][1:-1]
		user = get_object_or_404(User, username=username)
		if credential == custom_md5(settings.SECRET_KEY + user.username, settings.SECRET_KEY):
			if "name" in post:
				profile = PlanProfile.objects.filter(name=post["name"], user=user).first()
				if profile != None:
					ret_profile.append(profile.content)
			else:
				profiles = PlanProfile.objects.filter(user=user)
				for profile in profiles:
					ret_profile.append(profile.content)
	return JsonResponse(
		ret_profile, safe=False
	)

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

@login_required
def get_recommendations(request):
	year, semester, major = request.GET.get('year'), request.GET.get('semester'), request.GET.get('major')
	users_pk = [sth.pk for sth in User.objects.filter(profile__major=major).exclude(username="admin")]
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

@login_required
def get_major_options(request):
	major = ""
	semester = settings.CURRENT_SEMESTER[4:]
	year = 0
	majors = [{"text":item[0], "value":item[0]} for item in MAJOR_CHOICES]

	if request.user.profile.major:
		major = request.user.profile.major
	if request.user.profile.graduate_year:
		year = int(settings.CURRENT_YEAR) + 4 - int(request.user.profile.graduate_year)

	return JsonResponse({
		"major_options":majors,
		"major":major,
		"year":year,
		"semester":semester,
	})

"""
Seperate the year and semester of the input string, and the year is incremented if semester is Fall

Parameters:
	ys(String): String with format like "2019Fall"

Returns:
	int: The year part of ys
	string: The semester part of ys
"""
def year_and_semester(ys):
	year, semester = ys[:4], ys[4:]
	if semester == "Fall":
		return int(year) + 1, semester
	else:
		return int(year), semester

@login_required
def get_trending_courses(request):
	trending_courses = {}
	for cs_user in CourseUser.objects.all():
		tmp_course = cs_user.course
		if tmp_course.pk not in trending_courses and tmp_course.last_taught == settings.CURRENT_SEMESTER:
			trending_courses[tmp_course.pk] = {"taking":0, "taken":0,}
		if tmp_course.pk in trending_courses:
			trending_courses[tmp_course.pk][cs_user.take] += 1
	tmp_courses = []
	for cs_pk, take in trending_courses.items():
		tmp_course = get_object_or_404(Course, pk = cs_pk)
		tmp_courses.append({
			"course_pk":cs_pk,
			"title":tmp_course.title,
			"mnemonic":tmp_course.mnemonic,
			"number":tmp_course.number,
			"description":tmp_course.description,
			"taking":take["taking"],
			"taken":take["taken"],
		})
	taking_courses = sorted(tmp_courses, key=lambda x:(x["taking"]), reverse=True)
	taken_courses = sorted(tmp_courses, key=lambda x:(x["taken"]), reverse=True)

	final_taking_courses = [cs for cs in taking_courses if cs["taking"] > 0]
	final_taken_courses = [cs for cs in taken_courses if cs["taken"] > 0]

	return JsonResponse({
		"taking_courses":final_taking_courses[:10],
		"taken_courses":final_taken_courses[:10],
	})

@login_required
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

@login_required
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

@login_required
def submit_review(request):
	if request.method == "POST":
		post = json.loads(request.body)
		text, rating_course, rating_instructor = post["text"], post["rating_course"], post["rating_instructor"]
		course_pk, instructor_pk, course_instructor_pk =  post["course_pk"], post["instructor_pk"], post["course_instructor_pk"]
		if len(text.strip()) == 0 or rating_course == 0 or rating_instructor == 0:
			return JsonResponse({
				"success":False,
			})
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
	
		cs_instr = get_object_or_404(CourseInstructor, pk=post["course_instructor_pk"])

		if past_query.first() != None:
			past_query.first().delete()
		if not delete:
			cs_user = CourseUser.objects.create(user=request.user, course = course, instructor = instructor, course_instructor = cs_instr)
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
	pk = request.GET.get("pk")
	course = get_object_or_404(Course, pk=pk)
	return JsonResponse({
		"course":get_detailed_json_of_course(course, request.user,with_take=True, with_instructors=True),
	})

@login_required
def get_course_instructor(request):
	course_pk, instructor_pk = request.GET.get("course_pk"), request.GET.get("instructor_pk")
	course = get_object_or_404(Course, pk=course_pk)
	instructor = get_object_or_404(Instructor, pk=instructor_pk)
	return JsonResponse(get_detailed_json_of_course_instructor(course, instructor, request.user))

@login_required
def course_search_result(request):
	# time_start = time.time()
	# score_cutoff = 85
	query = request.GET.get("query").strip()
	query_time = request.GET.get("time")
	field_queryset = course_and_instructor_retrieve(query)
	# if query.upper() in mnemonics:
	# 	field_queryset = Course.objects.filter(mnemonic = query.upper()).exclude(units="0")
	# else:
	# 	pk_queryset = {fq.pk:(str(getattr(fq, "mnemonic")) + str(getattr(fq,"number")) + " " + str(getattr(fq, "title")) ) for fq in Course.objects.exclude(units="0")}
	# 	if len(pk_queryset) > 0:
	# 		all_pks = process.extractBests(query, pk_queryset,scorer=fuzz.partial_ratio, score_cutoff=score_cutoff, limit=20)
	# 		all_pks = [item[2] for item in all_pks]
	# 		field_queryset = Course.objects.filter(pk__in=all_pks)
	# 	else:
	# 		field_queryset = None
	course_reslt = get_json_of_search_result(field_queryset)
	# time_end = time.time()
	# print("Time spent:", time_end - time_start)
	return JsonResponse({
		"course_result": course_reslt,
		"time":query_time,
	})

def course_and_instructor_retrieve(query):
	query = query.strip().lower()

	nums = re.findall(r'\d+', query)
	strs = []
	for s in re.findall(r'[^\d.]+', query):
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

	# print(query, "----", query_string_mn, "----", query_string_num, "----",query_string_str, "----")

	exact_course_query = Course.objects.filter(mnemonic__iexact=query_string_mn, number__iexact=query_string_num)
	
	if len(query.split()) == 2:
		tmp_a, tmp_b = query.split()[0], query.split()[1]
		exact_instructor_query = Instructor.objects.filter(first_name__iexact = tmp_a, last_name__iexact = tmp_b) | Instructor.objects.filter(first_name__iexact = tmp_b, last_name__iexact = tmp_a)

	if query.upper() in mnemonics:
		return [(course, "course") for course in sorted(Course.objects.filter(mnemonic=query.upper()).exclude(units="0"), key=lambda c:(c.mnemonic, c.number))]
	elif exact_course_query.first() != None:
		return [(course, "course") for course in exact_course_query.exclude(units="0")]
	elif len(query.split()) == 2 and exact_instructor_query.first() != None:
		return [(tmp_instructor, "instructor") for tmp_instructor in exact_instructor_query]
	else:
		tmp_course_queryset = Course.objects.exclude(units="0").annotate(
			similarity_prefix=TrigramSimilarity('mnemonic',query_string_mn),
			similarity_number=TrigramSimilarity('number',query_string_num),
			similarity_name=TrigramSimilarity('title', query_string_str)).filter((Q(similarity_prefix__gt=0.5) & (Q(number__startswith=query_string_num)|Q(similarity_number__gt=0.3)|Q(similarity_name__gt=0.2))) | Q(similarity_name__gt=0.25))
		retrieved_courses = sorted(tmp_course_queryset, key=lambda c: (-c.similarity_prefix,-c.similarity_number, -c.similarity_name,c.mnemonic,c.number))
		retrieved_courses = [(tmp_r_c, "course") for tmp_r_c in retrieved_courses[:20]]

		tmp_instructor_queryset = Instructor.objects.annotate(
			similarity_first_name=TrigramSimilarity('first_name', query_string_str),
			similarity_last_name=TrigramSimilarity('last_name', query_string_str),
		).filter(Q(similarity_first_name__gt=0.35)|Q(similarity_last_name__gt=0.35))
		retrieved_instructors = sorted(tmp_instructor_queryset, key=lambda c: (-c.similarity_first_name,-c.similarity_last_name))
		retrieved_instructors = [(tmp_r_i, "instructor") for tmp_r_i in retrieved_instructors[:20]]
		
		return retrieved_courses + retrieved_instructors

def get_json_of_search_result(queryset):
	ret_arr = []
	for query in queryset:
		if query[1] == "instructor":
			ret_arr.append(get_json_of_instructor(query[0]))
		if query[1] == "course":
			ret_arr.append(get_json_of_course(query[0]))
	return ret_arr

def get_json_of_courses(queryset):
	if len(queryset) > 0:
		return [get_json_of_course(cs) for cs in queryset]
	return []

def cmp_semester_key(a,b):
	return cmp_semester(a["semester"], b["semester"])

def get_json_of_instructor(instructor):
	last_taught = get_last_taught_of_course_instructors(CourseInstructor.objects.filter(instructor=instructor))
	return {
		"pk":instructor.pk,
		"name": instructor.__str__(),
		"type":"instructor",
		"last_taught":last_taught,
	}

def get_json_of_course(course):
	last_taught = get_last_taught_of_course_instructors(CourseInstructor.objects.filter(course=course))
	return {
		"pk":course.pk,
		"mnemonic":course.mnemonic,
		"number":course.number,
		"title":course.title,
		"last_taught":last_taught,
		"type":"course",
	}

def get_last_taught_of_course_instructors(queryset):
	cs_instr_arr = [cs_instr.semester for cs_instr in queryset]
	cs_instr_arr = sorted(cs_instr_arr, key=cmp_to_key(cmp_semester))
	if settings.CURRENT_SEMESTER not in cs_instr_arr and len(cs_instr_arr) > 0:
		last_taught = cs_instr_arr[-1]
	elif settings.CURRENT_SEMESTER in cs_instr_arr:
		last_taught = settings.CURRENT_SEMESTER
	else:
		last_taught = ""
	return last_taught

def get_detailed_json_of_course_instructor(course, instructor, user):
	course_instructor_relations = []
	course_instructor_query = CourseInstructor.objects.filter(course=course, instructor=instructor)
	for course_instructor in course_instructor_query:
		if course_instructor.semester != settings.CURRENT_SEMESTER:
			course_instructor_relations.append({
				"course_instructor_pk":course_instructor.pk,
				"topic":course_instructor.topic,
				"semester":course_instructor.semester,
				})

	# duplicated_keys = []
	# course_users = []
	# for course_user in CourseUser.objects.filter(course=course, instructor=instructor):
	# 	if course_user.user.pk not in duplicated_keys:
	# 		duplicated_keys.append(course_user.user.pk)
	# 		course_users.append(get_detailed_json_of_course_user(course_user))
	course_users = [get_detailed_json_of_course_user(course_user) for course_user in CourseUser.objects.filter(course=course, instructor=instructor) ]
	tmp_query, tmp_counter = get_rating_of_instructor_with_course(instructor, course)
	return {
		"course":get_detailed_json_of_course(course, user),
		"instructor":{
			"instructor_pk":instructor.pk,
			"name":instructor.__str__(),
			"rating_instructor":tmp_query,
			"rating_instructor_counter":tmp_counter,
			"rating_instructor_users_count":sum(tmp_counter),
			"counter":tmp_counter,
		},
		"course_instructors":course_instructor_relations,
		"course_users":course_users,
	}

def get_detailed_json_of_course_user(course_user):
	return {
		"course_user_pk":course_user.pk,
		"user_pk":course_user.user.pk,
		"username":course_user.user.username,
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

	rating_course, rating_course_counter = get_rating_of_course(course)
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
		"last_taught":course.last_taught,
		"department":{
			"name":course.department.name,
			"department_pk":course.department.pk,
		},
		"rating_course":rating_course,
		"rating_course_counter":rating_course_counter,
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
			rating_instructor, rating_instructor_counter = get_rating_of_instructor_with_course(cs_instructor.instructor, course)
			if tmp_name not in instructors:
				tmp_cs_user_query = CourseUser.objects.filter(course=course, instructor=cs_instructor.instructor)
				instructors[tmp_name] = {
					"semesters":[],
					"pk":cs_instructor.instructor.pk,
					"rating_instructor":rating_instructor,
					# "rating_instructor_counter":rating_instructor_counter,
					"taking":tmp_cs_user_query.filter(take="taking").count(),
					"taken":tmp_cs_user_query.filter(take="taken").count(),
				}
			instructors[tmp_name]["semesters"].append({
				"semester":cs_instructor.semester,
				"course_instructor_pk":cs_instructor.pk,
				"topic":cs_instructor.topic,
			})
		for instructor_name,v in instructors.items():
			topic = ""
			if len(v["semesters"]) > 0:
				v["semesters"] = sorted(v["semesters"], key=cmp_to_key(cmp_semester_key), reverse=True)
				topic = v["semesters"][0]["topic"]
			
			final_instructors.append({
				"name":instructor_name,
				"semesters":v["semesters"],
				"topic":topic,
				"pk":v["pk"],
				"rating_instructor":v["rating_instructor"],
				# "rating_instructor_counter":v["rating_instructor_counter"],
				"taking":v["taking"],
				"taken":v["taken"],
			})
	return final_instructors

def get_rating_of_course(course):
	return get_rating(CourseUser.objects.filter(course=course), "rating_course")

def get_rating_of_instructor_with_course(instructor, course):
	return get_rating(CourseUser.objects.filter(course=course, instructor = instructor), "rating_instructor")

def get_rating_of_instructor(instructor):
	return get_rating(CourseUser.objects.filter(instructor = instructor), "rating_instructor")

def get_rating(course_user_queryset, attr_name):
	rating_arr = []
	counter = [0,0,0,0,0,0]
	for cs_user in course_user_queryset:
		tmp_user_rating = getattr(cs_user, attr_name)
		if tmp_user_rating != None and tmp_user_rating > 0 and tmp_user_rating <= 5:
			rating_arr.append(tmp_user_rating)
			counter[int(tmp_user_rating)] += 1
	if len(rating_arr) > 0:
		rating_instructor = sum(rating_arr)/len(rating_arr)
	else:
		rating_instructor = 0
	return round(rating_instructor,2), counter