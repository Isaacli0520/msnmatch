from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import Course, Relation
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity
from django.db.models import Q, F
from django.db.models.functions import Lower, Substr, Length
from django.http import JsonResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
import re
import json

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

def list(request):
	list_of_courses = Course.objects.all()
	return render(request, 'courses.html', {
	"list_of_courses":list_of_courses,
	})

def course_taking_add_delete(request):
	user = User.objects.get(username = request.GET.get("username"))
	course = Course.objects.get(course_number = request.GET.get("course_number"))

	if Relation.objects.filter(user=user, course=course, take="taking").exists():
		Relation.objects.get(user=user,course=course, take="taking").delete()
	else:
		Relation.objects.create(user=user,course=course, take="taking")

	return JsonResponse({
		"exist":Relation.objects.filter(user=user, course=course, take="taking").exists(),
	})


def course_taken_add_delete(request):
	user = User.objects.get(username = request.GET.get("username"))
	course = Course.objects.get(course_number = request.GET.get("course_number"))

	if Relation.objects.filter(user=user, course=course, take="taken").exists():
		Relation.objects.get(user=user,course=course, take="taken").delete()
	else:
		Relation.objects.create(user=user,course=course, take="taken")

	return JsonResponse({
		"exist":Relation.objects.filter(user=user, course=course, take="taken").exists(),
	})

def course(request, course_number):
	user = User.objects.get(username = request.user.username)
	tmp_course = Course.objects.get(course_number = course_number)
	return render(request, 'course.html', {
		"user":user,
		"tmp_course":tmp_course,
		"users_taking":tmp_course.course_users.filter(relation__take="taking"),
		"users_taken":tmp_course.course_users.filter(relation__take="taken"),
		})

@login_required
def course_search_auto(request):
	return render(request, 'course_search_auto.html',{
		"user": User.objects.get(username = request.user.username),
		})

def course_search_result(request):
	course_list = []
	query_string = request.GET.get("input").strip()
	retrieved_courses = course_retrieve(query_string)

	for cs in retrieved_courses:
		new_cs = {
			"course_number": cs.course_number.strip(),
			"course_name": cs.course_name.strip(),
			"course_match": lcs(query_string.lower(), cs.course_number.strip().lower() + " " + cs.course_name.strip().lower()),
			"course_exist": cs.course_users.filter(username__iexact = request.user.username).exists(),
			"course_taking": Relation.objects.filter(user=request.user, course=cs, take="taking").exists(),
			"course_taken": Relation.objects.filter(user=request.user, course=cs, take="taken").exists(),
		}
		course_list.append(new_cs)
	return JsonResponse({
		"retrieved_courses":course_list,
		})

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
