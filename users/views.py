from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity
from django.db.models import Q
from django.db.models.functions import Length

import json
import random
import datetime
import time

from friendship.models import Friend, Follow
from skills.models import Skill
from courses.models import CourseUser, Course
from .models import User, Profile
from .forms import UserForm, ProfileForm, ProfileNewForm
from skills.views import skills_as_dict
from msnmatch import settings
from msnmatch.utils import _get_not_allowed, _post_not_allowed, _success_response, _error_response

@login_required
def profile(request, username):
    return render(request, 'profile.html')

@login_required
def update_profile(request, username):
    if request.user.username != username:
        return redirect(reverse('update_profile', kwargs={"username": request.user.username, }))
    return render(request, 'profile_edit.html')

@login_required
def get_match_header(request):
    following = Follow.objects.following(request.user)
    flw_ret = []
    for flw in following:
        if flw.profile.picture:
            picture_url = flw.profile.picture.url
        else:
            picture_url = settings.STATIC_URL + "css/images/brand.jpg"
        new_flw = {
            "pk": flw.pk,
            "picture": picture_url,
            "user_url": "/users/"+flw.username+"/",
            "first_name": flw.first_name,
            "last_name": flw.last_name,
        }
        flw_ret.append(new_flw)
    return _success_response({
        "user":{
            "first_name":request.user.first_name,
            "last_name":request.user.last_name,
            "role":request.user.profile.role,
        },
        "profile_urls":{
            "profile": reverse('profile', args=[request.user.username]),
            "update_profile":reverse('update_profile', args=[request.user.username]),
        },
        "following":flw_ret,
    })

@login_required
def get_user_match_header(request):
    return _success_response({
        "user":{
            "first_name":request.user.first_name,
            "last_name":request.user.last_name,
            "role":request.user.profile.role,
        }
    })

@login_required
def get_all_and_user_skills(request):
    return _success_response({
        "all_skills":skills_as_dict(Skill.objects.all().exclude(type="Custom").exclude(users=request.user), empty_list = True),
        "user_skills":skills_as_dict(request.user.skill_set.all(), empty_list = True),
    })

@login_required
def get_all_users(request):
    start_time = time.time()
    users = sorted(User.objects.all().exclude(username="admin").exclude(profile__role=""), key=lambda x: random.random())
    resp = {
        "users":[user_json(user, request) for user in users],
        "request_user":user_json(request.user, request),
    }
    print("DEBUG GET ALL USERS TIME:", time.time() - start_time)
    return _success_response(resp)

@login_required
def get_all_users_roommate(request):
    users = sorted(User.objects.filter(profile__rm=True).exclude(username="admin").exclude(profile__role=""), key=lambda x: random.random())
    return _success_response({
        "users":[user_json(user, request) for user in users],
        "request_user":user_json(request.user, request),
    })

@login_required
def get_profile(request):
    username = request.GET.get('username')
    if not username:
        return _error_response()
    editable = request.user.username == username
    user = User.objects.filter(username = username).first()
    if not user:
        return _error_response()
    return _success_response({
        "editable":editable,
        "user":user_json(user, request, personal_profile=True),
    })

@login_required
def match_user(request):
    if request.method == "POST":
        post = json.loads(request.body)
        user_1_pk, user_2_pk = post["user_1"], post["user_2"]
        try:
            user_1, user_2 = User.objects.get(pk=user_1_pk), User.objects.get(pk=user_2_pk)
            user_1.profile.matched = True
            user_1.save()
            user_2.profile.matched = True
            user_2.save()
            return _success_response()
        except:
            return _error_response("User doesn't exist")
    if request.method == "GET":
        return _get_not_allowed()

@login_required
def edit_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        if not username:
            return _error_response("No username provided")
        user = User.objects.filter(username=username).first()
        if not user:
            return _error_response("User does not exist.")
        if user != request.user:
            return _error_response("You can't edit other people's profile.")
        profile_form = ProfileNewForm(request.POST, request.FILES, instance=user.profile)
        user_form = UserForm(request.POST, request.FILES, instance=user)
        if profile_form.is_valid() and user_form.is_valid():
            # print("profile Form cleaned data", profile_form.cleaned_data)
            # print("user Form cleaned data", user_form.cleaned_data)
            profile_form.save()
            user_form.save()
            return _success_response()
        else:
            print("User Edit Error:", user_form.errors)
            print("Profile Edit Error:", profile_form.errors)
    if request.method == "GET":
        return _get_not_allowed()

@login_required
def choose_roommate_role(request):
    if request.method == "POST":
        post = json.loads(request.body)
        rm = post.get("rm")
        if rm != True and rm != False:
            return _error_response("Unknown Rm")
        request.user.profile.rm = rm
        request.user.save()
        return _success_response({
            "rm":request.user.profile.rm,
        })
    if request.method == "GET":
        return _get_not_allowed()

@login_required
def check_mentor_requirements(request):
    if request.method == "GET":
        dt = datetime.datetime.strptime(settings.HMP_CHECK_TIME, '%Y-%m-%d')
        user_review_num = request.user.courseuser_set.annotate(length=Length("text")).filter(length__gt=15, date__gt=dt).count()
        if user_review_num < 3:
            return _success_response({"valid":False})
        return _success_response({"valid":True}) 
    if request.method == "POST":
        return _post_not_allowed()

@login_required
def choose_role(request):
    if request.method == "POST":
        post = json.loads(request.body)
        tmp_role = post.get("role")
        if tmp_role == "Mentor" and request.user.profile.role == "":
            dt = datetime.datetime.strptime(settings.HMP_CHECK_TIME, '%Y-%m-%d')
            user_review_num = request.user.courseuser_set.annotate(length=Length("text")).filter(length__gt=15, date__gt=dt).count()
            if user_review_num < 3:
                return _error_response("You don't have enough course comments.")
            request.user.profile.role = "Mentor"
            request.user.save()
        elif tmp_role == "Mentee" and request.user.profile.role == "":
            # return _error_response("Mentee registration not yet started.")
            request.user.profile.role = "Mentee"
            request.user.save()
        else:
            return _error_response("Unknown Reason")
        return _success_response({
            "role":request.user.profile.role,
        })
    if request.method == "GET":
        return _get_not_allowed()

def add_fav(request):
    if request.method == "POST":
        post = json.loads(request.body)
        user_pk = post.get("user_pk")
        try:
            to_user = User.objects.get(pk=user_pk)
        except:
            return _error_response("User does not exist")
        if request.user.profile.role == '' or request.user.profile.role == to_user.profile.role:
            return _error_response("False Role")
        if not Follow.objects.filter(follower=request.user, followee=to_user).exists() and Follow.objects.filter(follower=request.user).count() < 3:
            Follow.objects.add_follower(request.user, to_user)
            return _success_response()
        return _error_response("You either have already followed this person or have already followed three users")
    if request.method == "GET":
        return _get_not_allowed() 

def del_fav(request):
    if request.method == "POST":
        post = json.loads(request.body)
        user_pk = post.get("user_pk")
        try:
            to_user = User.objects.get(pk=user_pk)
        except:
            return _error_response("User does not exist")
        if Follow.objects.filter(follower=request.user, followee=to_user).exists():
            Follow.objects.remove_follower(follower=request.user, followee=to_user)
            return _success_response()
        else:
            return _error_response("Following relationship does not exist")
    if request.method == "GET":
        return _get_not_allowed()

def get_follow_list(request):
    following = Follow.objects.following(request.user)
    flw_ret = []
    for flw in following:
        if flw.profile.picture:
            picture_url = flw.profile.picture.url
        else:
            picture_url = settings.STATIC_URL + "css/images/brand.jpg"
        new_flw = {
            "pk": flw.pk,
            "picture": picture_url,
            "user_url": "/users/"+flw.username+"/",
            "first_name": flw.first_name,
            "last_name": flw.last_name,
        }
        flw_ret.append(new_flw)
    return _success_response({
        "following":flw_ret,
    })

def user_json(user, request, personal_profile = False):
    picture_url = settings.STATIC_URL + "css/images/brand.jpg"
    avatar_url = settings.STATIC_URL + "css/images/brand_blur.jpg"
    video_url = ""
    year = ""
    if user.profile.picture:
        picture_url = user.profile.picture.url
    if user.profile.avatar:
        avatar_url = user.profile.avatar.url
    if user.profile.video:
        video_url = user.profile.video.url
    if user.profile.graduate_year:
        year = 4 + settings.CURRENT_YEAR - int(user.profile.graduate_year)
    user_dict = {
        "pk": user.pk,
        "username":user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "bio": user.profile.bio,
        "location": user.profile.location,
        "year": year,
        "graduate_year": user.profile.graduate_year,
        "sex":user.profile.sex,
        "role":user.profile.role,
        "major": user.profile.major,
        "major_two":user.profile.major_two,
        "minor":user.profile.minor,
        "wechat":user.profile.wechat,
        "video": video_url,
        "picture": picture_url,
        "avatar":avatar_url,
        "rm_bio":user.profile.rm_bio,
        "rm_schedule":user.profile.rm_schedule,
        "rm":user.profile.rm,
    }
    if not personal_profile:
        user_dict["skills"] = skills_as_dict(user.skill_set.all(), empty_list=True)
        user_dict["follow"] = Follow.objects.filter(follower=request.user, followee=user).exists()
    return user_dict

