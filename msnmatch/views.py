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
	all_users = User.objects.all().exclude(username=request.user.username)
	return render(request, 'home.html', {
		"all_users":all_users,
	})

	# if 'q' in request.GET:
	# 	field = request.GET.get('f')
	# 	query_string = request.GET['q'].strip()
	# 	retrieved_people = people_retrieve(field, query_string)

	# 	return render(request, 'home.html', {"retrieved_people": retrieved_people, "query_string": query_string})
	# else:

	# 	return render(request, 'home.html', {"retrieved_people": None, "query_string": query_string})


def people_retrieve(field, query_string):
	exact_match_people = User.objects.all()
	retrieved_people = None
	if field == 'all':
		exact_match_people = User.objects.filter(Q(profile__major=query_string) | Q(profile__major_two=query_string) |
			Q(first_name=query_string) | Q(last_name=query_string) | Q(profile__year=query_string) | Q(profile__minor=query_string)).exclude(username="admin")
		if exact_match_people.exists():
			retrieved_people = exact_match_people
		else:
			tmp_queryset = User.objects.annotate(
				similarity_firstname=TrigramSimilarity('first_name', query_string),
				similarity_lastname=TrigramSimilarity('last_name', query_string),
				similarity_major=TrigramSimilarity('profile__major', query_string),
				similarity_major_two=TrigramSimilarity('profile__major_two', query_string),
				similarity_minor=TrigramSimilarity('profile__minor', query_string),
				similarity_year=TrigramSimilarity('profile__year', query_string)).filter(Q(similarity_firstname__gt=.3) | Q(similarity_lastname__gt=.3) | Q(similarity_major__gt=.2) | 
				Q(similarity_major_two__gt=.2) | Q(similarity_minor__gt=.2) | Q(similarity_year__gt=.1))
			retrieved_people=sorted(tmp_queryset, key = lambda c: (-c.similarity_firstname, -c.similarity_lastname, -c.similarity_major, -c.similarity_major_two, -c.similarity_minor, -c.similarity_year))
	elif field == 'name':
		exact_match_people = User.objects.filter(Q(first_name=query_string) | Q(last_name=query_string)).exclude(username="admin")
		if exact_match_people.exists():
			retrieved_people = exact_match_people
		else:
			tmp_queryset = User.objects.annotate(
				similarity_firstname=TrigramSimilarity('first_name', query_string),
				similarity_lastname=TrigramSimilarity('last_name', query_string)).filter(Q(similarity_firstname__gt=.3) | Q(similarity_lastname__gt=.3))
			retrieved_people=sorted(tmp_queryset, key = lambda c: (-c.similarity_firstname, -c.similarity_lastname))
	elif field == 'major':
		exact_match_people = User.objects.filter(Q(profile__major=query_string) | Q(profile__major_two=query_string)).exclude(username="admin")
		if exact_match_people.exists():
			retrieved_people = exact_match_people
		else:
			tmp_queryset = User.objects.annotate(similarity_major=TrigramSimilarity('profile__major', query_string),
				similarity_major_two=TrigramSimilarity('profile__major_two', query_string)).filter(Q(similarity_major__gt=.2) | Q(similarity_major_two__gt=.2))
			retrieved_people=sorted(tmp_queryset, key = lambda c: (-c.similarity_major, -c.similarity_major_two))
	elif field == 'minor':
		exact_match_people = User.objects.filter(Q(profile__minor=query_string)).exclude(username="admin").exclude(username="admin")
		if exact_match_people.exists():
			retrieved_people = exact_match_people
		else:
			tmp_queryset = User.objects.annotate(similarity_minor=TrigramSimilarity('profile__minor', query_string)).filter(similarity_minor__gt=.2)
			retrieved_people=sorted(tmp_queryset, key = lambda c: (-c.similarity_minor))
	elif field == 'year':
		exact_match_people = User.objects.filter(Q(profile__year=query_string)).exclude(username="admin")
		if exact_match_people.exists():
			retrieved_people = exact_match_people
		else:
			tmp_queryset = User.objects.annotate(similarity_year=TrigramSimilarity('profile__year', query_string)).filter(similarity_year__gt=.1)
			retrieved_people=sorted(tmp_queryset, key = lambda c: (-c.similarity_year))
	if retrieved_people != None:
		return retrieved_people[:25]
	else:
		return None
