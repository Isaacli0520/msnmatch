from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import TrigramSimilarity
from django.shortcuts import render
from django.db.models import Q, F, Count

from .models import Skill, SkillRelation
from msnmatch.utils import _get_not_allowed, _post_not_allowed, _success_response, _error_response

import collections
import json
import time

MAXIMUM_SKILLS = 4
SKILL_TYPES = [
	"Academic", "Books", "Custom",
	"Film and TV", "Game", "General",
	"Language", "Music", "Sport"
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
		return _success_response({
			"skill":skill_json(skill),
			"users":[user_json(user, request) for user in users]
		})
	except:
		return _error_response("Skill doesn't exist.")

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
	return _success_response({
		"skills":skills,
		"time":query_time
	})

@login_required
def user_add_skill(request):
	if request.method == "POST":
		post = json.loads(request.body)
		skill_id, skill_name = post.get("id"), post.get("name")
		skill = Skill.objects.filter(Q(pk=skill_id) | Q(name=skill_name)).first()
		if not skill:
			skill = Skill.objects.create(name=skill_name, intro="", type="Custom")
		# skill = Skill.objects.filter(pk = skill_id).first()
		# if not skill:
		# 	skill = Skill.objects.filter(name = skill_name).first()
		# 	if not skill:
		# 		skill = Skill.objects.create(name=skill_name, intro="", type="Custom")
		if SkillRelation.objects.filter(user=request.user, skill=skill).first():
			return _error_response("User-skill relation exists")
		SkillRelation.objects.create(user=request.user, skill=skill)
		return _success_response({
			"id":skill.id,
		})
	if request.method == "GET":
		return _get_not_allowed()

@login_required
def user_del_skill(request):
	if request.method == "POST":
		post = json.loads(request.body)
		skill_id = post.get("id")
		skill = Skill.objects.filter(pk = skill_id).first()
		if not skill:
			return _error_response("Skill doesn't exist")
		skill_relation = SkillRelation.objects.filter(user=request.user, skill=skill).first()
		if skill_relation:
			skill_relation.delete()
			if skill.users.count() == 0 and skill.type == "Custom":
				skill.delete()
			return _success_response()
		else:
			return _error_response("You don't have this skill")
	if request.method == "GET":
		return _get_not_allowed()
		
def skills_as_dict(queryset, empty_list = False):
	skills = collections.defaultdict(list)
	if empty_list:
		for s_type in SKILL_TYPES:
			skills[s_type] = []
	for skill in queryset:
		skills[skill.type].append(skill_json(skill))
	return skills

def skill_json(skill):
	return {
		"id":skill.pk,
		"name":skill.name,
		"type":skill.type,
	}