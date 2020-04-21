from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from users.models import Profile
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity
from django.db.models import Q, F, Count
from django.db.models.functions import Lower, Substr, Length
from django.http import JsonResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

from courses.models import CourseUser
from django.contrib.auth.models import User
from .models import Skill, SkillRelation
from friendship.models import Follow

import re
import json
import random
import time
import operator
from fuzzywuzzy import fuzz, process
from msnmatch import settings

MAXIMUM_SKILLS = 4
SKILL_TYPES = [
	"Academic",
	"Books",
	"Custom",
	"Film and TV",
	"Game",
	"General",
	"Language",
	"Music",
	"Sport"
]

@login_required
def skills(request):
	return render(request, 'skills.html')

@login_required
def skill(request, skill_pk):
	return render(request, 'skill.html')

# @login_required
# def skill_rank(request):
# 	if Skill.objects.count() >= 75:
# 		all_skills = Skill.objects.all().annotate(num_users=Count('skill_users')).order_by('-num_users')[:75]
# 	else:
# 		all_skills = Skill.objects.all().annotate(num_users=Count('skill_users')).order_by('-num_users')
# 	return render(request, 'skill_rank.html',{
# 		"all_skills":all_skills,
# 		})

@login_required
def get_skill(request):
	skill_id = request.GET.get("id")
	try:
		skill = Skill.objects.get(pk = skill_id)
		users = skill.users.all()
		return JsonResponse({
			"success":True,
			"skill":skill_json(skill),
			"users":[user_json(user) for user in users]
		})
	except:
		return JsonResponse({
			"success":False,
			"message":"Skill doesn't exist."
		})

@login_required
def get_all_and_user_skills(request):
	return JsonResponse({
		"all_skills":skills_as_dict(Skill.objects.all().exclude(type="Custom").exclude(users=request.user)),
		"user_skills":skills_as_dict(request.user.skill_set.all()),
		})

@login_required
def get_all_users(request):
	users = sorted(User.objects.all().exclude(username="admin").exclude(profile__role=""), key=lambda x: random.random())
	return JsonResponse({
		"users":[user_json(user) for user in users],
		"request_user":user_json(request.user),
	})

@login_required
def get_search_result(request):
	skills = []
	query_string = request.GET.get("query").strip()
	query_time = request.GET.get("time")
	skill_queryset = Skill.objects.annotate(
		similarity_name=TrigramSimilarity('name',query_string),
		similarity_type=TrigramSimilarity('type',query_string),
		similarity_intro=TrigramSimilarity('intro', query_string)).filter(Q(similarity_name__gt=0.25)|Q(similarity_type__gt=0.23)|Q(similarity_intro__gt=0.2))
	if skill_queryset.exists():
		sorted_skills = sorted(skill_queryset, key=lambda c: (-c.similarity_name,-c.similarity_type, -c.similarity_intro))
		if len(sorted_skills) > MAXIMUM_SKILLS:
			sorted_skills = sorted_skills[:MAXIMUM_SKILLS]
		for skill in sorted_skills:
			skills.append(skill_json(skill))
	return JsonResponse({
		"skills":skills,
		"time":query_time
		})

@login_required
def user_add_skill(request):
	if request.method == "POST":
		post = json.loads(request.body.decode('utf-8'))
		skill_id = post.get("id")
		skill_name = post.get("name")
		skill = Skill.objects.filter(pk = skill_id).first()
		if not skill:
			skill = Skill.objects.filter(name = skill_name).first()
			if not skill:
				skill = Skill.objects.create(name=skill_name, intro="", type="Custom")
		if SkillRelation.objects.filter(user=request.user, skill=skill).first():
			return JsonResponse({
				"success":False,
				"message":"Tag already added"
			})
		SkillRelation.objects.create(user=request.user, skill=skill)
		return JsonResponse({
			"success":True
		})
	return JsonResponse({
		"success":False,
		"message":"Get request not allowed"
	})

@login_required
def user_del_skill(request):
	if request.method == "POST":
		post = json.loads(request.body.decode('utf-8'))
		skill_id = post.get("id")
		skill = Skill.objects.filter(pk = skill_id).first()
		if not skill:
			return JsonResponse({
				"success":False,
				"message":"Skill doesn't exist"
			})
		skill_relation = SkillRelation.objects.filter(user=request.user, skill=skill).first()
		if skill_relation:
			skill_relation.delete()
			if skill.users.count() == 0 and skill.type == "Custom":
				skill.delete()
			return JsonResponse({
				"success":True
			})
		else:
			return JsonResponse({
				"success":False,
				"message":"You don't have this skill"
			})
	return JsonResponse({
		"success":False,
		"message":"Get request not allowed"
	})

@login_required
def choose_role(request):
	post = json.loads(request.body.decode('utf-8'))
	tmp_role = post.get("role")
	if tmp_role == "Mentor" and request.user.profile.role == "":
		user_review_num = request.user.courseuser_set.annotate(length=Length("text")).filter(length__gt=15).count()
		if user_review_num < 3:
			return JsonResponse({
				"success":False,
				"message":"You don't have enough course comments."
			})
		request.user.profile.role = "Mentor"
		request.user.save()
	elif tmp_role == "Mentee" and request.user.profile.role == "":
		return JsonResponse({
			"success":False,
			"message":"Mentee registration not yet started."
		})
		request.user.profile.role = "Mentee"
		request.user.save()
	return JsonResponse({
		"success":True,
		"role":request.user.profile.role,
	})

def add_to_list(request):
	to_user = User.objects.get(pk=request.GET.get("user_pk"))
	success = 0
	if not Follow.objects.filter(follower=request.user, followee=to_user).exists() and Follow.objects.filter(follower=request.user).count() < 3:
		Follow.objects.add_follower(request.user, to_user)
		success = 1

	return JsonResponse({
		"success": success,
	})

def get_follow_list(request):
	following = Follow.objects.following(request.user)
	# print("following", following)
	flw_ret = []
	for flw in following:
		new_flw = {
			"pk": flw.pk,
			"user_url": "/users/"+flw.username+"/",
			"first_name": flw.first_name,
			"last_name": flw.last_name,
			
		}
		flw_ret.append(new_flw)
	return JsonResponse({
		"following":flw_ret,
	})

def del_fav(request):
	to_user = get_object_or_404(User, pk=request.GET.get("user_pk"))
	# to_user = User.objects.get(pk = request.GET.get("user_pk"))
	# print("from_user", request.user.username, "to_user", to_user.username, Follow.objects.filter(follower=request.user, followee=to_user).exists())
	# print("before delete", Follow.objects.following(request.user), Follow.objects.all()),
	if Follow.objects.filter(follower=request.user, followee=to_user).exists():
		Follow.objects.remove_follower(follower=request.user, followee=to_user)
		# print("after delete", Follow.objects.following(request.user), Follow.objects.all())
	return JsonResponse({
		
	})

def user_json(user):
	if user.profile.picture:
		picture_url = user.profile.picture.url
	else:
		picture_url = settings.STATIC_URL + "css/images/brand.jpg"

	if user.profile.avatar:
		avatar_url = user.profile.avatar.url
	else:
		avatar_url = settings.STATIC_URL + "css/images/brand_blur.jpg"

	if user.profile.video:
		video_url = user.profile.video.url
	else:
		video_url = ""
	if user.profile.graduate_year:
		tmp_year = 4 + settings.CURRENT_YEAR - int(user.profile.graduate_year)
	else:
		tmp_year = ""
	return {
		"pk": user.pk,
		"username":user.username,
		"first_name": user.first_name,
		"last_name": user.last_name,
		"email": user.email,
		"bio": user.profile.bio,
		# "birth_date": user.profile.birth_date,
		"location": user.profile.location,
		"year": tmp_year,
		"sex":user.profile.sex,
		"skills": skills_as_dict(user.skill_set.all()),
		"role":user.profile.role,
		"major": user.profile.major,
		"major_two":user.profile.major_two,
		"minor":user.profile.minor,
		"wechat":user.profile.wechat,
		# "follow": Follow.objects.filter(follower=request.user, followee=user).exists(),
		"video": video_url,
		"picture": picture_url,
		"avatar":avatar_url,
	}
		
def skills_as_dict(queryset):
	skills = {}
	# for skill in Skill.objects.all():
	# 	if skill.type not in skills:
	# 		skills[skill.type] = []
	for s_type in SKILL_TYPES:
		skills[s_type] = []
	for skill in queryset:
		skills[skill.type].append(skill_json(skill))
	return skills

def skill_json(skill):
	return {
		"id":skill.pk,
		"name":skill.name,
		"intro":skill.intro,
		"type":skill.type,
		"name":skill.name,
	}
