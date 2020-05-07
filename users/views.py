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
from .forms import UserForm, ProfileForm, ProfileNewForm
from .models import MatchRequest
from msnmatch import settings
from django.http import JsonResponse

@login_required
def update_profile(request, username):
    if request.user.username != username:
        return redirect(reverse('update_profile', kwargs={"username": request.user.username, }))
    return render(request, 'profile_edit.html')

@login_required
def edit_user(request):
    if request.method == "POST":
        # post = request.POST.copy()
        username = request.POST.get("username")
        if not username:
            return JsonResponse({"success":False, "message":"No username provided"})
        user = User.objects.filter(username=username).first()
        if not user:
            return JsonResponse({"success":False, "message":"User does not exist."})
        if user != request.user:
            return JsonResponse({"success":False, "message":"You can't edit other people's profile."})
        profile_form = ProfileNewForm(request.POST, request.FILES, instance=user.profile)
        user_form = UserForm(request.POST, request.FILES, instance=user)
        if profile_form.is_valid() and user_form.is_valid():
            # print("profile Form cleaned data", profile_form.cleaned_data)
            # print("user Form cleaned data", user_form.cleaned_data)
            profile_form.save()
            user_form.save()
            return JsonResponse({"success":True})
        else:
            print("User Edit Error:", user_form.errors)
            print("Profile Edit Error:", profile_form.errors)
    return JsonResponse({"success":False, "message":"Get request not supported"})

# @login_required
# def update_profile(request, username):
#   if request.user.username != username:
#       return redirect(reverse('update_profile', kwargs={"username": request.user.username, }))
#   if request.method == 'POST':
#       profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
#       user_form = UserForm(request.POST, instance=request.user)
#       if profile_form.is_valid() and user_form.is_valid():
#           profile_form.save()
#           user_form.save()
#           return redirect(reverse('profile', kwargs={"username": request.user.username, }))
#   else:
#       profile_form = ProfileForm(instance=request.user.profile)
#       user_form = UserForm(instance=request.user)
#   return render(request, 'profile_edit.html', {
#       'user_form': user_form,
#       'profile_form': profile_form,
#   })

@login_required
def get_profile(request):
    username = request.GET.get('username')
    if not username:
        return JsonResponse({
            "success":False
        })
    editable = True if request.user.username == username else False
    user = User.objects.filter(username = username).first()
    if not user:
        return JsonResponse({
            "success":False
        })
    return JsonResponse({
        "success":True,
        "editable":editable,
        "user":profile_json(user),
    })

def profile_json(user):
    if user.profile.graduate_year:
        tmp_year = 4 + settings.CURRENT_YEAR - int(user.profile.graduate_year)
    else:
        tmp_year = ""
    if user.profile.picture:
        picture_url = user.profile.picture.url
    else:
        picture_url = settings.STATIC_URL + "css/images/brand.jpg"
    if user.profile.video:
        video_url = user.profile.video.url
    else:
        video_url = ""
    return {
        "pk": user.pk,
        "picture": picture_url,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "role":user.profile.role,
        "bio": user.profile.bio,
        "birth_date": user.profile.birth_date,
        "location": user.profile.location,
        "year": tmp_year,
		"graduate_year":user.profile.graduate_year,
        "major": user.profile.major,
        "sex":user.profile.sex,
        "major_two":user.profile.major_two,
        "minor":user.profile.minor,
        "wechat":user.profile.wechat,
        "username":user.username,
        "video":video_url,
        "rm_bio":user.profile.rm_bio,
        "rm_schedule":user.profile.rm_schedule,
        "rm":user.profile.rm,
    }

@login_required
def my_courses(request, username):
    if request.user.username != username:
        return redirect(reverse('my_courses', kwargs={"username": request.user.username, }))
    return render(request, "mycourses.html")

@login_required
def profile(request, username):
    # user = User.objects.get(username=username)
    # # print(user_taken_courses)
    # from_user = request.user

    # all_skills = user.skill_set.all()

    # skill_set = {}
    # skill_list = []
    # for skill in all_skills:
    #   if skill.skill_type not in skill_set:
    #       skill_set[skill.skill_type] = []
    #   skill_set[skill.skill_type].append(skill)
    # for k in skill_set:
    #   skill_list += skill_set[k]

    # show_cal = False
    # if request.user.username == username:
    #   editable = True
    #   show_cal = True
    # else:
    #   editable = False
    # email_html = user.email.split('@')
    # calendar_url = "https://calendar.google.com/calendar/embed?src=" +email_html[0] + "%40" + email_html[1]+ "&ctz=America%2FNew_York"
    
    # ctx = {
    # "from_user": from_user,
    #   "to_username": username,
    #   "user": user,
    #   "editable": editable,
    #   "user_skills":skill_list,
    #   "calendar_url": calendar_url,
    #   "show_cal": show_cal,
    #   # "real_year": user.real_year(),
    # }

    # return render(request, 'profile.html', ctx)
    return render(request, 'profile.html')

