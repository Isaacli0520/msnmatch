from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User
from courses.models import CourseUser, Course
from friendship.exceptions import AlreadyExistsError
from django.contrib import messages
from friendship.models import Friend, Follow, FriendshipRequest, Block
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity
from users.models import User, Profile
from django.db.models import Q
import requests
from users.models import MatchingHistory
from .forms import UserForm, ProfileForm
from .models import MatchRequest
from msnmatch import settings

@login_required
def update_profile(request, username):
	if request.user.username != username:
		return redirect(reverse('update_profile', kwargs={"username": request.user.username, }))
	if request.method == 'POST':
		profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
		user_form = UserForm(request.POST, instance=request.user)
		if profile_form.is_valid() and user_form.is_valid():
			profile_form.save()
			user_form.save()
			return redirect(reverse('profile', kwargs={"username": request.user.username, }))
	else:
		profile_form = ProfileForm(instance=request.user.profile)
		user_form = UserForm(instance=request.user)
	return render(request, 'update_profile.html', {
		'user_form': user_form,
		'profile_form': profile_form,
	})

@login_required
def profile(request, username):
	user = User.objects.get(username=username)
	# print(user_taken_courses)
	from_user = request.user

	all_skills = user.skill_set.all()

	skill_set = {}
	skill_list = []
	for skill in all_skills:
		if skill.skill_type not in skill_set:
			skill_set[skill.skill_type] = []
		skill_set[skill.skill_type].append(skill)
	for k in skill_set:
		skill_list += skill_set[k]

	show_cal = False
	if request.user.username == username:
		editable = True
		show_cal = True
	else:
		editable = False
	email_html = user.email.split('@')
	calendar_url = "https://calendar.google.com/calendar/embed?src=" +email_html[0] + "%40" + email_html[1]+ "&ctz=America%2FNew_York"
	
	ctx = {
	"from_user": from_user,
		"to_username": username,
		"user": user,
		"editable": editable,
		"user_skills":skill_list,
		"calendar_url": calendar_url,
		"show_cal": show_cal,
		# "real_year": user.real_year(),
	}

	return render(request, 'profile.html', ctx)

