from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User
from courses.models import Relation, Course
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

# Create your views here.


@login_required
def update_profile(request, username):
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
def people(request):
	list_of_people = User.objects.all().exclude(
			first_name="").exclude(username=request.user.username)
	return render(request, 'people.html', {
		"list_of_people": list_of_people,
		})


@login_required
def profile(request, username):
	user = User.objects.get(username=username)
	user_taking_courses = user.course_set.filter(relation__take="taking")
	user_taken_courses = user.course_set.filter(relation__take="taken")
	# print(user_taken_courses)
	friends = Friend.objects.friends(user)
	friend_requests = FriendshipRequest.objects.filter(to_user=user)
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

	current_matching = user.matching_requests_received.filter(finished=False)
	past_matching_received = user.matching_requests_received.filter(finished=True).order_by("created").reverse()
	past_matching_sent = user.matching_requests_sent.filter(finished=True)
	sent_matching = user.matching_requests_sent.all()
	# past_sent_matching = user.matching_requests_sent.filter(finished=True)
	to_user = user
	ctx = {'to_username': username}
	try:
		request_exist = FriendshipRequest.objects.get(from_user=from_user, to_user=to_user)
	except FriendshipRequest.DoesNotExist:
		request_exist = None
	show_cal = False
	if request.method == 'POST':
		if "review" in request.POST:

			match = get_object_or_404(MatchingHistory, id=request.POST['review'])
			match.reviewed = True
			match.comment = request.POST['comment']
			match.display_name = request.POST['user_name']
			match.rating = int(request.POST['rate'])
			match.save()

		elif "mark" in request.POST:
			match = get_object_or_404(MatchingHistory, id=request.POST['match'])
			match.finished = True
			match.save()
			Friend.objects.remove_friend(match.from_user, match.to_user)

		elif "match_request" in request.POST and request_exist == None:
			try:
					Friend.objects.add_friend(from_user, to_user)
					request_exist = FriendshipRequest.objects.get(from_user=from_user, to_user=to_user)
					request_exist.matchrequest.title = request.POST['match_title']
					request_exist.matchrequest.reason = request.POST['match_reason']
					request_exist.save()
			except AlreadyExistsError as e:
					ctx['errors'] = ["%s" % e]
					messages.info(request, e)

	try:
		other_user = User.objects.get(username=request.user.username)
		friendship_exist = Friend.objects.filter(Q(from_user=user, to_user=other_user) | Q(from_user=other_user, to_user=user)).first()
		show_cal = True
	except Friend.DoesNotExist:
		friendship_exist = None
		show_cal = False
	if friendship_exist == None:
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
		"user_taking_courses": user_taking_courses,
		"user_taken_courses": user_taken_courses,
		"friends": friends,
		"requests": friend_requests,
		"request_exist": request_exist,
		"current_matching": current_matching,
		"past_matching_received": past_matching_received,
		"past_matching_sent": past_matching_sent,
		"sent_matching":sent_matching,
		"calendar_url": calendar_url,
		"show_cal": show_cal,
			"cal_act" : False,
	}

	return render(request, 'profile.html', ctx)


@login_required
def friendship_accept(request, username):
	user = User.objects.get(username=username)
	friend_requests = FriendshipRequest.objects.filter(to_user=user)

	ctx = {'requests': friend_requests}
	if request.method == 'POST':
		frequest = get_object_or_404(FriendshipRequest, id=request.POST['r_id'])
		if "accept" in request.POST:
			MatchingHistory.objects.create(from_user=frequest.from_user, to_user=frequest.to_user)
			frequest.accept()

		if "reject" in request.POST:
			frequest.delete()
	return render(request, 'request.html', ctx)

@login_required
def match(request):
	user = User.objects.get(username=request.user.username)

	match_received_request = FriendshipRequest.objects.filter(to_user=user).order_by("created").reverse()
	match_received_ongoing = user.matching_requests_received.filter(finished=False).order_by("created").reverse()
	match_received_finished = user.matching_requests_received.filter(finished=True).order_by("created").reverse()
	
	match_sent_request = FriendshipRequest.objects.filter(from_user=user).order_by("created").reverse()
	match_sent_ongoing = user.matching_requests_sent.filter(finished=False).order_by("created").reverse()
	match_sent_finished = user.matching_requests_sent.filter(finished=True, reviewed=True).order_by("created").reverse()
	match_sent_to_be_reviewed = user.matching_requests_sent.filter(finished=True, reviewed=False).order_by("created").reverse()
	
	match_request = match_received_request | match_sent_request
	match_ongoing = match_received_ongoing | match_sent_ongoing
	match_finished = match_received_finished | match_sent_finished
	match_to_be_reviewed = match_sent_to_be_reviewed
	
	ctx = {
			# 'match_received_ongoing': match_received_ongoing,
			# 'match_received_finished': match_received_finished,
			# 'match_sent_ongoing': match_sent_ongoing,
			# 'match_sent_finished': match_sent_finished,
			# 'match_sent_to_be_reviewed': match_sent_to_be_reviewed,
			# 'match_sent_request': match_sent_request,
			# 'match_received_request': match_received_request,
			"match_request":match_request,
			"match_ongoing":match_ongoing,
			"match_finished":match_finished,
			"match_to_be_reviewed":match_to_be_reviewed,
			}
	if request.method == 'POST':
			if "accept" in request.POST:
					frequest = get_object_or_404(FriendshipRequest, id=request.POST['r_id'])
					tmp_m_hst = MatchingHistory.objects.create(from_user=frequest.from_user, to_user=frequest.to_user)
					tmp_m_hst.title = frequest.matchrequest.title
					tmp_m_hst.reason = frequest.matchrequest.reason
					tmp_m_hst.save()
					frequest.accept()
			elif "reject" in request.POST:
					frequest = get_object_or_404(FriendshipRequest, id=request.POST['r_id'])
					frequest.delete()
			elif "Finish" in request.POST:
					match = get_object_or_404(MatchingHistory, id=request.POST['match'])
					match.finished = True
					match.save()
					Friend.objects.remove_friend(match.from_user, match.to_user)
			elif "review" in request.POST:
					match = get_object_or_404(MatchingHistory, id=request.POST['review'])
					match.reviewed = True
					match.comment = request.POST['comment']
					match.display_name = request.POST['user_name']
					match.rating = int(request.POST['rate'])
					match.save()
	return render(request, 'match.html', ctx)


	# # Get the exact match class (if there is no such class, exact_match_first_course == None)
	# # return User.objects.all()

	# exact_match_people = User.objects.filter(
	#     Q(profile__major=query_string) | Q(profile__major_two=query_string)).exclude(first_name="")
	# exact_match_first_people = exact_match_people.first()
	# print("hello")
	# print(exact_match_people)

	# # if DEBUGGG == True:
	# # 	print(query_string, "----", query_string_mn, "----",
	# # 	      query_string_num, "----", query_string_str, "----")

	# if exact_match_first_people != None:
	# 	retrieved_people = exact_match_people
	# else:
	# 	tmp_queryset = User.objects.annotate(
	# 	similarity_major=TrigramSimilarity('profile__major', query_string),
	# 	similarity_major_two = TrigramSimilarity('profile__major_two', query_string)).filter(Q(similarity_major__gt=0.25) | Q(similarity_major_two__gt=0.23))
	# 	retrieved_people=sorted(tmp_queryset, key = lambda c: (-c.similarity_major, -c.similarity_major_two, c.first_name, c.last_name)[0])

	# 	# retrieved_people= retrieved_people[:MAXIMUM_PEOPLE]
	# 	# retrieved_people = tmp_queryset

	# 	# if DEBUGGG == True:
	# 	# 	for person in retrieved_people:
	# 	# 		print(person.similarity_name,"  ", re.findall(r'[.]+', person.first_name)[0])

	# return retrieved_people
