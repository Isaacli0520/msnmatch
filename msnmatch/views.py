from django.shortcuts import render, get_object_or_404, get_list_or_404
from users.models import User, Profile
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from courses.models import Relation, Course
from friendship.exceptions import AlreadyExistsError
from django.contrib import messages
from friendship.models import Friend, Follow, FriendshipRequest, Block
from users.models import MatchingHistory
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity
from django.db.models import Q, F, Count
from users.models import ROLE_CHOICES
from skills.models import Skill, SkillRelation
import time
from msnmatch import settings
from django.http import JsonResponse
import collections
from django.urls import reverse
from msnmatch import settings

def handler404(request, exception):
    response = render(request, "404.html")
    response.status_code = 404
    return response

def handler403(request, exception):
    response = render(request, "403.html")
    response.status_code = 403
    return response

def get_home_page_basic_info(request):
	tmp = {
		"home_url":reverse('home'),
		"tags_url":reverse('tags'),
		"family_url":reverse('family'),
		"group_manage_url":reverse('groups_manage'),
		"trending_tags_url":reverse('skill_rank'),
		"brand_pic": settings.STATIC_URL + "css/images/brand.png",
		"profile": reverse('profile', args=[request.user.username]),
		"update_profile":reverse('update_profile', args=[request.user.username]),
		"logout":reverse('logout'),
		"request_user_username":request.user.username,
		"request_user_pk":request.user.pk,
		"request_user_role":request.user.profile.role,
	}
	return JsonResponse({
		"all_info":tmp,
	})

def get_all_ranked_users(request):
	all_users = User.objects.all().exclude(username="admin")
	all_users_dict = {}
	start_time = time.time()
	for user in all_users:
		if user.profile.picture:
			picture_url = user.profile.picture.url
		else:
			picture_url = settings.STATIC_URL + "css/images/brand.jpg"

		if user.profile.avatar:
			avatar_url = user.profile.avatar.url
		else:
			avatar_url = settings.STATIC_URL + "css/images/brand_blur.jpg"

		all_users_dict[user.pk] = {
			"pk":user.pk,
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
			"role":user.profile.role,
			"major_two":user.profile.major_two,
			"minor":user.profile.minor,
			"wechat":user.profile.wechat,
			"follow": [flw.follower.pk for flw in Follow.objects.filter(followee=user)],
			"followee": [flw.followee.pk for flw in Follow.objects.filter(follower=user)],
			"avatar":avatar_url,
		}
	print("Get all ranked users --- %s seconds ---" % (time.time() - start_time))
	# print("all_users_dict", all_users_dict)
	return JsonResponse({
		"all_users":all_users_dict,
	})


@login_required
def superadmin(request):
	return render(request, 'superadmin.html')

@login_required
def home(request):
	if request.method == 'POST':
		print("request",request.POST)
		print("role", request.user.profile.role)
		if "Mentor" in request.POST and request.user.profile.role == "":
			request.user.profile.role = "Mentor"
			request.user.save()
		elif "Mentee" in request.POST and request.user.profile.role == "":
			request.user.profile.role = "Mentee"
			request.user.save()
	return render(request, 'home.html')

	# if 'q' in request.GET:
	# 	field = request.GET.get('f')
	# 	query_string = request.GET['q'].strip()
	# 	retrieved_people = people_retrieve(field, query_string)

	# 	return render(request, 'home.html', {"retrieved_people": retrieved_people, "query_string": query_string})
	# else:

	# 	return render(request, 'home.html', {"retrieved_people": None, "query_string": query_string})


