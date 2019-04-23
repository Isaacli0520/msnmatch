from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import Skill, SkillRelation
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity
from django.db.models import Q, F
from django.db.models.functions import Lower, Substr, Length
from django.http import JsonResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
import re
import json

MAXIMUM_COURSES = 12
DEBUGGG = False


# def course_taking_add_delete(request):
# 	user = User.objects.get(username = request.GET.get("username"))
# 	course = Course.objects.get(course_number = request.GET.get("course_number"))

# 	if Relation.objects.filter(user=user, course=course, take="taking").exists():
# 		Relation.objects.get(user=user,course=course, take="taking").delete()
# 	else:
# 		Relation.objects.create(user=user,course=course, take="taking")

# 	return JsonResponse({
# 		"exist":Relation.objects.filter(user=user, course=course, take="taking").exists(),
# 	})


# def course_taken_add_delete(request):
# 	user = User.objects.get(username = request.GET.get("username"))
# 	course = Course.objects.get(course_number = request.GET.get("course_number"))

# 	if Relation.objects.filter(user=user, course=course, take="taken").exists():
# 		Relation.objects.get(user=user,course=course, take="taken").delete()
# 	else:
# 		Relation.objects.create(user=user,course=course, take="taken")

# 	return JsonResponse({
# 		"exist":Relation.objects.filter(user=user, course=course, take="taken").exists(),
# 	})

def add_del_skill(request):
	user = User.objects.get(username=request.user.username)
	skill = Skill.objects.get(pk = request.GET.get("skill_pk"))

	if SkillRelation.objects.filter(user=user, skill=skill).exists():
		SkillRelation.objects.get(user=user,skill=skill).delete()
	else:
		SkillRelation.objects.create(user=user,skill=skill)

	return JsonResponse({
		"exist":SkillRelation.objects.filter(user=user, skill=skill).exists(),
	})

def skill(request, skill_pk):
	user = User.objects.get(username = request.user.username)
	tmp_skill = Skill.objects.get(pk = skill_pk)
	return render(request, 'skill.html', {
		"user":user,
		"tmp_skill":tmp_skill,
		"users_with_skill":tmp_skill.skill_users.all(),
		})

@login_required
def skill_search(request):
	return render(request, 'skill_search.html',{
		"user": User.objects.get(username = request.user.username),
		})

def skill_search_result(request):
	user = User.objects.get(username=request.user.username)
	skill_list = []
	query_string = request.GET.get("searchquery").strip()
	retrieved_skills = skill_retrieve(query_string)
	print("debuggggg:",query_string)
	for skill in retrieved_skills:
		new_skill = {
			"skill_pk": skill.pk,
			"skill_name": skill.skill_name,
			"skill_intro": skill.skill_intro,
			"skill_type": skill.skill_type,
			"skill_exist": SkillRelation.objects.filter(user=user, skill=skill).exists()
		}
		skill_list.append(new_skill)
	print(skill_list)
	return JsonResponse({
		"skill_list":skill_list,
		})

def skill_retrieve(query_string):
	tmp_queryset = Skill.objects.annotate(
		similarity_name=TrigramSimilarity('skill_name',query_string),
		similarity_type=TrigramSimilarity('skill_type',query_string),
		similarity_intro=TrigramSimilarity('skill_intro', query_string)).filter(Q(similarity_name__gt=0.25)|Q(similarity_type__gt=0.23)|Q(similarity_intro__gt=0.15))
	retrieved_skills = sorted(tmp_queryset, key=lambda c: (-c.similarity_name,-c.similarity_type, -c.similarity_intro))

	return retrieved_skills

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
