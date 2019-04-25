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


def add_del_skill(request):
	user = User.objects.get(username=request.user.username)
	skill = Skill.objects.get(pk = request.GET.get("skill_pk"))
	add_del = request.GET.get("add_del")
	print("add_del", add_del)

	if SkillRelation.objects.filter(user=user, skill=skill).exists() and add_del == "del":
		SkillRelation.objects.get(user=user,skill=skill).delete()
	elif not SkillRelation.objects.filter(user=user, skill=skill).exists() and add_del == "add":
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

def get_all_skills(request):
	all_skills = request.user.skill_set.all()
	skill_list = []
	for skill in all_skills:
		new_skill = {
			"skill_pk": skill.pk,
			"skill_name": skill.skill_name,
			"skill_intro": skill.skill_intro,
			"skill_type": skill.skill_type,
			"skill_exist": SkillRelation.objects.filter(user=request.user, skill=skill).exists()
		}
		skill_list.append(new_skill)
	return JsonResponse({
		"all_skills":skill_list,
		})

def retrieve_users(request):
	all_tags = request.GET.get("all_tags")
	print("all_tags", all_tags.split('`'))
	all_users = User.objects.all().exclude(username=request.user.username)
	if(all_tags == ""):
		return get_user_json(all_users)
	re_users = user_retrieve(all_tags.split('`'), all_users)
	return get_user_json(re_users)
	
def get_all_users(request):
	all_users = User.objects.all().exclude(pk=request.user.pk)
	return get_user_json(all_users)

def get_user_json(all_users):
	all_users_list = []
	
	for user in all_users:
		if user.profile.picture:
			picture_url = user.profile.picture.url
		else:
			picture_url = "/static/images/brand.jpg"
		new_user = {
			"pk": user.pk,
			"user_url": "/users/"+user.username+"/",
			"picture": picture_url,
			"first_name": user.first_name,
			"last_name": user.last_name,
			"email": user.email,
			"bio": user.profile.bio,
			"birth_date": user.profile.birth_date,
			"location": user.profile.location,
			"year": user.profile.year,
			"major": user.profile.major,
			"skills":[{"skill_name":tmp_skill.skill_name, "skill_type":tmp_skill.skill_type,} for tmp_skill in user.skill_set.all()],
		}
		all_users_list.append(new_user)
	return JsonResponse({
		"all_users":all_users_list,
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
	if retrieved_skills != None:
		for skill in retrieved_skills:
			new_skill = {
				"skill_pk": skill.pk,
				"skill_name": skill.skill_name,
				"skill_intro": skill.skill_intro,
				"skill_type": skill.skill_type,
				"skill_exist": SkillRelation.objects.filter(user=user, skill=skill).exists()
			}
			skill_list.append(new_skill)
	return JsonResponse({
		"skill_list":skill_list,
		})

def user_retrieve(tags, all_users):
	tmp_queryset = []
	for user in all_users:
		similar_tags = []
		for tag in tags:
			tmp_tag = skill_retrieve_new(user.pk, tag)
			if tmp_tag != None:
				similar_tags.append(tmp_tag)
		tmp_queryset.append((user.pk, len(similar_tags)))
	
	tmp_queryset = [some_user for some_user in tmp_queryset if some_user[1] >= 1]
	print("user_retrieve",tmp_queryset)
	return [User.objects.get(pk=k) for k, v in sorted(tmp_queryset, key=lambda tp: tp[1], reverse = True)]

def skill_retrieve(query_string):
	tmp_queryset = Skill.objects.annotate(
		similarity_name=TrigramSimilarity('skill_name',query_string),
		similarity_type=TrigramSimilarity('skill_type',query_string),
		similarity_intro=TrigramSimilarity('skill_intro', query_string)).filter(Q(similarity_name__gt=0.25)|Q(similarity_type__gt=0.23)|Q(similarity_intro__gt=0.2))
	if tmp_queryset.first() == None:
		return None
	retrieved_skills = sorted(tmp_queryset, key=lambda c: (-c.similarity_name,-c.similarity_type, -c.similarity_intro))

	return retrieved_skills

def skill_retrieve_new(pk, query_string):
	user = User.objects.get(pk=pk)
	tmp_queryset = user.skill_set.all().annotate(
		similarity_name=TrigramSimilarity('skill_name',query_string),
		similarity_type=TrigramSimilarity('skill_type',query_string),
		similarity_intro=TrigramSimilarity('skill_intro', query_string)).filter(Q(similarity_name__gt=0.3)|Q(similarity_type__gt=0.3)|Q(similarity_intro__gt=0.22))
	if tmp_queryset.first() == None:
		return None
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
