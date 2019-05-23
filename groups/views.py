from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User
from users.models import Profile
from skills.models import Skill, SkillRelation
from .models import Group, GroupRelation
from django.db.models import Q, F, Count
from django.http import JsonResponse
from friendship.models import Follow
import re
import json
import random
from msnmatch import settings
from django.shortcuts import get_object_or_404
from .models import Group, GroupRelation, GroupFollowRelation
import time
from .forms import GroupForm


@login_required
def groups_manage(request):
	return render(request, "groups_manage.html")

@login_required
def group(request, group_pk):
	tmp_group = Group.objects.get(pk = group_pk)
	return render(request, 'group.html', {
		"tmp_group":tmp_group,
		"users_in_group":tmp_group.group_users.all(),
		})

@login_required
def family(request):
	return render(request, 'family.html')

def get_all_groups(request):
	groups = Group.objects.all()
	return get_groups_json(groups)

def get_manager_groups(request):
	groups = [groupR.group for groupR in GroupRelation.objects.filter(user=request.user, group_role="Manager")]
	return get_groups_json(groups)

def get_member_groups(request):
	groups = [groupR.group for groupR in GroupRelation.objects.filter(user=request.user, group_role="Member")]
	return get_groups_json(groups)

def get_group(request):
	print("group", int(request.GET.get('group_pk')))
	groups = Group.objects.filter(pk=int(request.GET.get('group_pk')))
	return get_groups_json(groups)

def get_group_edit(request):
	return JsonResponse({
		"edit":GroupRelation.objects.filter(user=request.user, group=get_object_or_404(Group, pk=int(request.GET.get('group_pk'))), group_role="Manager").exists(),
		}) 

def get_all_families(request):
	families = Group.objects.filter(group_type = "Family")
	return get_family_json(request, families)

@login_required
def update_group_tags(request, group_pk):
	return render(request, 'group_tag.html')

@login_required
def update_group(request, group_pk):
	tmp_group = get_object_or_404(Group, pk=group_pk)
	if not GroupRelation.objects.filter(user=request.user, group=tmp_group, group_role="Manager").exists():
		return redirect(reverse('groups_manage'))
	if request.method == 'POST':
		group_form = GroupForm(request.POST, request.FILES, instance=tmp_group)
		if group_form.is_valid():
			group_form.save()
			return redirect(reverse('group', kwargs={"group_pk": group_pk, }))
	else:
		group_form = GroupForm(instance=tmp_group)
	return render(request, 'update_group.html', {
		'group_form': group_form,
	})

def get_family_page_basic_info(request):
	tmp = {
		"request_user_username":request.user.username,
		"request_user_pk":request.user.pk,
		"request_user_role":request.user.profile.role,
	}
	return JsonResponse({
		"all_info":tmp,
	})


def get_family_json(request, group_queryset):
	ret_group_arr = []
	for group in group_queryset:
		skill_set = {}
		for skill in group.group_tags.all():
			if skill.skill_type not in skill_set:
				skill_set[skill.skill_type] = []
			new_skill = {
				"skill_pk": skill.pk,
				"skill_name": skill.skill_name,
				"skill_type": skill.skill_type,
				"skill_url":"/skills/"+str(skill.pk)+"/",
			}
			skill_set[skill.skill_type].append(new_skill)
		
		if group.picture:
			picture_url = group.picture.url
		else:
			picture_url = settings.STATIC_URL + "css/images/brand.jpg"

		if group.avatar:
			avatar_url = group.avatar.url
		else:
			avatar_url = settings.STATIC_URL + "css/images/brand_blur.jpg"

		ret_group_arr.append({
			'pk':group.pk,
			'group_name':group.group_name,
			'group_type':group.group_type,
			'group_intro':group.group_intro,
			'group_tags':skill_set,
			'picture':picture_url,
			'avatar':avatar_url,
			'managers': get_user_arr(group.group_users.filter(grouprelation__group_role="Manager")),
			'members':get_user_arr(group.group_users.filter(grouprelation__group_role="Member")),
			'follow':GroupFollowRelation.objects.filter(user=request.user, group=group).exists(),
		})
	return JsonResponse({
		"groups":ret_group_arr,
	})

def get_groups_json(group_queryset):
	ret_group_arr = []
	for group in group_queryset:
		skill_set = {}
		for skill in group.group_tags.all():
			if skill.skill_type not in skill_set:
				skill_set[skill.skill_type] = []
			new_skill = {
				"skill_pk": skill.pk,
				"skill_name": skill.skill_name,
				"skill_type": skill.skill_type,
				"skill_url":"/skills/"+str(skill.pk)+"/",
			}
			skill_set[skill.skill_type].append(new_skill)
		
		if group.picture:
			picture_url = group.picture.url
		else:
			picture_url = settings.STATIC_URL + "css/images/brand.jpg"

		if group.avatar:
			avatar_url = group.avatar.url
		else:
			avatar_url = settings.STATIC_URL + "css/images/brand_blur.jpg"

		ret_group_arr.append({
			'pk':group.pk,
			'group_name':group.group_name,
			'group_type':group.group_type,
			'group_intro':group.group_intro,
			'group_tags':skill_set,
			'picture':picture_url,
			'avatar':avatar_url,
			'managers': get_user_arr(group.group_users.filter(grouprelation__group_role="Manager")),
			'members':get_user_arr(group.group_users.filter(grouprelation__group_role="Member")),
		})
	return JsonResponse({
		"groups":ret_group_arr,
	})

def get_user_arr(queryset):
	return [{"pk":tmp_user.pk, 
			"year":tmp_user.profile.year, 
			"user_url":("/users/"+tmp_user.username+"/"),
			"first_name":tmp_user.first_name, 
			"last_name":tmp_user.last_name} 
			for tmp_user in queryset]