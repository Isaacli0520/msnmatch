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
from django.db.models import Q
from users.models import ROLE_CHOICES

def handler404(request, exception):
    response = render(request, "404.html")
    response.status_code = 404
    return response

def handler403(request, exception):
    response = render(request, "403.html")
    response.status_code = 403
    return response

def csrf_failure(request, reason=""):
    return render("csrf_failure.html")

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


