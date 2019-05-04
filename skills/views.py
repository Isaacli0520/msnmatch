from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User
from users.models import Profile
from .models import Skill, SkillRelation
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity
from django.db.models import Q, F
from django.db.models.functions import Lower, Substr, Length
from django.http import JsonResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from friendship.models import Follow
import re
import json
import random
import numpy as np
from scipy.spatial import distance
from fuzzywuzzy import fuzz, process

MAXIMUM_COURSES = 12
DEBUGGG = False


def add_del_skill(request):
	user = request.user
	add_del = request.GET.get("add_del")
	if not Skill.objects.filter(pk = request.GET.get("skill_pk")).exists() and add_del == "add":
		exist = False
		if not Skill.objects.filter(skill_name = request.GET.get("skill_name")).exists():
			skill = Skill.objects.create(skill_name=request.GET.get("skill_name"), skill_intro="", skill_type="Custom")
			SkillRelation.objects.create(user=user,skill=skill)
			exist = True
			origin_exist = False
		else:
			origin_exist = True
	else:
		skill = Skill.objects.get(skill_name = request.GET.get("skill_name"))
		origin_exist = SkillRelation.objects.filter(user=user, skill=skill).exists()
		if SkillRelation.objects.filter(user=user, skill=skill).exists() and add_del == "del":
			SkillRelation.objects.get(user=user,skill=skill).delete()
			print("Skill",skill.skill_name, " Count", skill.skill_users.count())
			if skill.skill_users.count() == 0 and skill.skill_type == "Custom":
				skill.delete()
		elif not SkillRelation.objects.filter(user=user, skill=skill).exists() and add_del == "add":
			SkillRelation.objects.create(user=user,skill=skill)
		exist = SkillRelation.objects.filter(user=user, skill=skill).exists()

	return JsonResponse({
		"exist": exist,
		"origin_exist":origin_exist,
	})

@login_required
def skill(request, skill_pk):
	user = User.objects.get(username = request.user.username)
	tmp_skill = Skill.objects.get(pk = skill_pk)
	return render(request, 'skill.html', {
		"user":user,
		"tmp_skill":tmp_skill,
		"users_with_skill":tmp_skill.skill_users.all(),
		})

def get_users_by_sim(request):

	all_tags = request.GET.get("all_tags")
	all_users = User.objects.all().exclude(username="admin")
	if(all_tags != ""):
		all_users = user_retrieve(all_tags.split('`'), all_users.exclude(pk=request.user.pk))

	user_skills = get_format_skills(User.objects.get(pk=request.user.pk).skill_set.all())
	all_user_skills = get_skills_of_users(queryset = all_users)
	# print("debug:::",all_user_skills)
	sims = {u2_pk:similarity_between(user_skills, u2_skills) for u2_pk, u2_skills in all_user_skills.items()}
	sorted_sims = sorted(sims.items(), key = lambda c:c[1], reverse=True)
	print("all_similarities:", sorted_sims)
	print("all_users_sorted:",[User.objects.get(pk = user_pk).username for user_pk, score in sorted_sims])
	return get_user_json_sim([(User.objects.get(pk = user_pk),'{0:.3g}'.format(score*100)) for user_pk, score in sorted_sims])


def similarity_between(u1, u2):
	u1_length = sum([scaler(len(v)) for k,v in u1.items()])
	u1_vec = []
	u2_vec = []
	sims = []
	sims_weight = []
	for sk_type, skills in u1.items():
		if sk_type in u2:
			tmp_skill_ls = list(set(u1[sk_type]+u2[sk_type]))
			# print("skill ls",[Skill.objects.get(pk=tmp_pk).skill_name for tmp_pk in tmp_skill_ls])
			u1_vec.append([int(sk in u1[sk_type]) for sk in tmp_skill_ls])
			u2_vec.append([int(sk in u2[sk_type]) for sk in tmp_skill_ls])
			# print("u1",u1_vec,"u2",u2_vec)
			sims.append(1 - distance.cosine(u1_vec[-1], u2_vec[-1]))
			print("similarity:",sims[-1])
			sims_weight.append(sims[-1]*scaler(len(u1[sk_type]))/u1_length)
	return sum(sims_weight)
	

def scaler(x):
	return (x+1)**(2/3.0)-(x+1)**(-1/8.0)

def get_skills_of_users(queryset):
	all_user_skills = {}
	for user in queryset:
		all_user_skills[user.pk] = get_format_skills(User.objects.get(pk=user.pk).skill_set.all())
	return all_user_skills
		

def get_format_skills(queryset):
	user_skills = {}
	for sk in queryset:
		if sk.skill_type not in user_skills:
			user_skills[sk.skill_type] = []
		user_skills[sk.skill_type].append(sk.pk)
	return user_skills

def add_to_list(request):
	to_user = User.objects.get(pk=request.GET.get("user_pk"))
	if not Follow.objects.filter(follower=request.user, followee=to_user).exists():
		Follow.objects.add_follower(request.user, to_user)

	return JsonResponse({
	})

def get_follow_list(request):
	following = Follow.objects.following(request.user)
	print("following", following)
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
	to_user = User.objects.get(pk = request.GET.get("user_pk"))
	print("from_user", request.user.username, "to_user", to_user.username, Follow.objects.filter(follower=request.user, followee=to_user).exists())
	print("before delete", Follow.objects.following(request.user), Follow.objects.all()),
	if Follow.objects.filter(follower=request.user, followee=to_user).exists():
		Follow.objects.remove_follower(follower=request.user, followee=to_user)
		print("after delete", Follow.objects.following(request.user), Follow.objects.all())
	return JsonResponse({
		
	})


def get_all_skills(request):
	all_skills = Skill.objects.all()
	# skill_list = []
	skill_set = {}
	for skill in all_skills.exclude(skill_type="Custom"):
		if skill.skill_type not in skill_set and skill.skill_type != "Custom":
			skill_set[skill.skill_type] = []
		if not SkillRelation.objects.filter(user=request.user, skill=skill).exists():
			new_skill = {
				"skill_pk": skill.pk,
				"skill_name": skill.skill_name,
				"skill_intro": skill.skill_intro,
				"skill_type": skill.skill_type,
				"skill_exist": False,
			}
			skill_set[skill.skill_type].append(new_skill)

	return JsonResponse({
		"all_skills":skill_set,
		})

def get_all_user_skills(request):
	all_skills = request.user.skill_set.all()

	skill_set = {}
	for skill in Skill.objects.all():
		if skill.skill_type not in skill_set:
			skill_set[skill.skill_type] = []
	for skill in all_skills:
		new_skill = {
			"skill_pk": skill.pk,
			"skill_name": skill.skill_name,
			"skill_intro": skill.skill_intro,
			"skill_type": skill.skill_type,
			"skill_exist": SkillRelation.objects.filter(user=request.user, skill=skill).exists(),
		}
		skill_set[skill.skill_type].append(new_skill)
	return JsonResponse({
		"all_skills":skill_set,
		})

def retrieve_users(request):
	all_tags = request.GET.get("all_tags")
	print("all_tags", all_tags.split('`'))
	all_users = User.objects.all().exclude(username="admin")
	if(all_tags == ""):
		return get_user_json(all_users)
	re_users = user_retrieve(all_tags.split('`'), all_users)
	return get_user_json(re_users)
	
def get_all_users(request):
	# all_users = User.objects.all().exclude(pk=request.user.pk)
	all_users_list = sorted(User.objects.all().exclude(username="admin"), key=lambda x: random.random())
	# all_users = User.objects.all().exclude(username="admin")
	return get_user_json(all_users_list)

def get_user_json_sim(all_users):
	all_users_list = []

	for user, score in all_users:
		skill_set = {}
		for skill in user.skill_set.all():
			if skill.skill_type not in skill_set:
				skill_set[skill.skill_type] = []
			new_skill = {
				"skill_name": skill.skill_name,
				"skill_type": skill.skill_type,
				"skill_url":"/skills/"+str(skill.pk)+"/",
			}
			skill_set[skill.skill_type].append(new_skill)
		if user.profile.picture:
			picture_url = user.profile.picture.url
		else:
			picture_url = "/static/images/brand.jpg"
		if user.profile.video:
			video_url = user.profile.video.url
		else:
			video_url = ""
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
			"sex":user.profile.sex,
			"skills": skill_set,
			"video": video_url,
			"role":user.profile.role,
			"major_two":user.profile.major_two,
			"minor":user.profile.minor,
			"score":score,
			"wechat":user.profile.wechat,
		}
		all_users_list.append(new_user)
	return JsonResponse({
		"all_users":all_users_list,
	})

def get_user_json(all_users):
	all_users_list = []

	for user in all_users:
		skill_set = {}
		for skill in user.skill_set.all():
			if skill.skill_type not in skill_set:
				skill_set[skill.skill_type] = []
			new_skill = {
				"skill_name": skill.skill_name,
				"skill_type": skill.skill_type,
				"skill_url":"/skills/"+str(skill.pk)+"/",
			}
			skill_set[skill.skill_type].append(new_skill)
		if user.profile.picture:
			picture_url = user.profile.picture.url
		else:
			picture_url = "/static/images/brand.jpg"
		if user.profile.video:
			video_url = user.profile.video.url
		else:
			video_url = ""
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
			"sex":user.profile.sex,
			"skills": skill_set,
			"video": video_url,
			"role":user.profile.role,
			"major_two":user.profile.major_two,
			"minor":user.profile.minor,
			"wechat":user.profile.wechat,
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
				"skill_exist": SkillRelation.objects.filter(user=user, skill=skill).exists(),
				"skill_cus": False,
			}
			skill_list.append(new_skill)
	print("skill_search_result", skill_list)
	return JsonResponse({
		"skill_list":skill_list,
		})

def user_retrieve(tags, all_users):
	tmp_queryset = []
	field_queryset = all_users
	field_tags = [(tag[:tag.find(":")].lower(), tag[(tag.find(":") + 1):]) for tag in tags if tag.find(":") != -1]
	user_fields = [sth.name for sth in User._meta.get_fields()]
	profile_fields = [sth.name for sth in Profile._meta.get_fields()]
	for field_tag, field_query in field_tags:
		if field_tag == "name":
			field_queryset = field_queryset.annotate(
				sim_firstname=TrigramSimilarity('first_name', field_query),
				sim_lastname=TrigramSimilarity('last_name', field_query)).filter(Q(sim_firstname__gt=.3) | Q(sim_lastname__gt=.3) )
			field_queryset = sorted(field_queryset, key=lambda c: (-c.sim_firstname, -c.sim_lastname))
		elif field_tag == "major":
			field_queryset = field_queryset.annotate(
				sim_mj1=TrigramSimilarity('profile__major', field_query),
				sim_mj3=TrigramSimilarity('profile__minor', field_query),
				sim_mj2=TrigramSimilarity('profile__major_two', field_query)).filter(Q(sim_mj1__gt=.3) | Q(sim_mj2__gt=.3) | Q(sim_mj3__gt=.3) )
			field_queryset = sorted(field_queryset, key=lambda c: (-c.sim_mj1, -c.sim_mj2, -c.sim_mj3))
		elif field_tag in user_fields:
			field_queryset = filter_by_field(field_queryset, "", field_tag, field_query)
		elif field_tag in profile_fields:
			field_queryset = filter_by_field(field_queryset, "profile__", field_tag, field_query)
	for user in field_queryset:
		similar_tags = set()
		for tag in tags:
			if tag.find(":") == -1:
				tmp_tag = skill_retrieve_new(user.pk, tag)
				if tmp_tag != None:
					similar_tags.add(tmp_tag)

		tmp_queryset.append((user.pk, len(similar_tags)))
	
	if len(field_tags) != len(tags):
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
	if len(retrieved_skills) > 6:
		retrieved_skills = retrieved_skills[:6]
	return retrieved_skills

def skill_retrieve_new(pk, query_string):
	user = User.objects.get(pk=pk)
	all_user_skills = user.skill_set.all()
	if user.skill_set.all().count() == 0:
		return None
	tmp_queryset = {sk.pk:sk.skill_name for sk in all_user_skills}

	best_match = process.extractOne(query_string,tmp_queryset,scorer=fuzz.partial_ratio, score_cutoff=80)

	print("extract one",best_match)
	# retrieved_skills = [Skill.objects.get(pk=sk_pk) for sk_name, sk_pk in sims]
	# tmp_queryset = user.skill_set.all().annotate(
	# 	similarity_name=TrigramSimilarity('skill_name',query_string)).filter(Q(similarity_name__gt=0.45))
	# if tmp_queryset.first() == None:
	# 	return None
	# retrieved_skills = sorted(tmp_queryset, key=lambda c: (-c.similarity_name))
	if best_match != None:
		return Skill.objects.get(pk=best_match[2])
	else:
		return None

def filter_by_field(field_queryset, prefix, field_tag, field_query):
	field_queryset = field_queryset.annotate(
				sth = TrigramSimilarity(prefix+field_tag, field_query)).filter(sth__gt=0.1)
	tmp_list = [item.sth for item in field_queryset]
	if len(tmp_list) > 0 and max(tmp_list) >= 0.9:
		field_queryset = field_queryset.filter(sth__gt=0.9)
	
	return field_queryset

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
