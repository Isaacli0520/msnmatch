from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.utils import timezone

from msnmatch import settings
from users.models import User, Authenticator
from friendship.models import Follow
from .utils import _get_not_allowed, _post_not_allowed, _success_response, _error_response, val_required

import collections
import time
import hmac
import os
import jwt
import json
import uuid
import datetime
from hashlib import sha256
from urllib.parse import quote, urlencode


@login_required
def superadmin(request):
    return render(request, 'superadmin.html')

@login_required
def match(request):
    return render(request, 'match.html')

@login_required
def roommate_match(request):
    return render(request, 'roommate_match.html')

def home(request):
    return render(request, 'home.html')

def login(request):
    if request.user.is_authenticated:
        return redirect(reverse("home"))
    next_url = request.GET.get("next")
    return render(request, 'registration/login.html', {
        "next": quote(next_url) if next_url != None else ""
    })

def handler404(request, exception):
    response = render(request, "404.html")
    response.status_code = 404
    return response

def handler403(request, exception):
    response = render(request, "403.html")
    response.status_code = 403
    return response

@csrf_exempt
def oauth_authorize(request):
    try:
        response_type, state = request.GET.get("response_type"), request.GET.get("state")
        client_id, redirect_uri = request.GET.get("client_id"), request.GET.get("redirect_uri")
        code_challenge, code_challenge_method = request.GET.get("code_challenge"), request.GET.get("code_challenge_method")
    except:
        return _error_response("Missing params")
    if redirect_uri not in settings.AUTH_REDIRECT_URLS:
        return _error_response("Invalid redirect url")
    if client_id not in settings.AUTH_CLIENT_ID:
        return _error_response("Invalid client id")
    if request.method == "GET":
        if not request.user.is_authenticated:
            return redirect("/login/?next=" + quote(request.get_full_path()))
        return render(request, "authorize.html")
    if request.method == "POST":
        if not request.user.is_authenticated:
            return _error_response("Unauthorized user")
        allow, deny = request.POST.get("allow"), request.POST.get("deny")
        if deny and deny == "Deny":
            resp = {
                "error":"access denied",
                "error_description":"The user denied the request",
                "state":state,
            }
            return redirect(redirect_uri + "?" + urlencode(resp))
        if allow and allow == "Allow":
            expire_date = timezone.now() + datetime.timedelta(minutes=10)
            # print("UTC_NOW:", (datetime.datetime.utcnow() + datetime.timedelta(minutes=10)).timestamp())
            auth = {
                "exp":int(expire_date.timestamp()),
                "client_id":client_id,
                "redirect_uri":redirect_uri,
                "username":request.user.username,
                "code_challenge":code_challenge,
                "code_challenge_method":code_challenge_method,
                "id":uuid.uuid4().hex,
            }
            auth_code = jwt.encode(auth, settings.SECRET_KEY, algorithm="HS256")
            resp = {
                "code":auth_code,
                "state":state,
            }
            return redirect(redirect_uri + "?" + urlencode(resp))
        return _error_response("Invalid Behavior")

@csrf_exempt
def oauth_token(request):
    if request.method == "GET":
        return _get_not_allowed()
    if request.method == "POST":
        post = json.loads(request.body)
        for field in ["grant_type", "code", "code_verifier", "redirect_uri", "client_id"]:
            if field not in post:
                return JsonResponse({"error":"invalid_request"}, status=400)
        if post["grant_type"] != "authorization_code":
            return JsonResponse({"error":"unsupported_grant_type"}, status=400)
        try:
            auth = jwt.decode(post["code"], settings.SECRET_KEY, algorithms="HS256")
        except:
            return _error_response("Authorization code is expired")
        if auth["redirect_uri"] != post["redirect_uri"]:
            return JsonResponse({"error":"invalid_grant"}, status=400)
        if auth["client_id"] != post["client_id"]:
            return JsonResponse({"error":"invalid_client"}, status=401)
        if auth["code_challenge_method"] != "S256":
            return JsonResponse({"error":"invalid_request"}, status=400)
        code_hashed = sha256(post["code_verifier"].encode('utf-8')).hexdigest()
        if auth["code_challenge"] != code_hashed:
            return JsonResponse({"error":"invalid_grant"}, status=400)
        auths = Authenticator.objects.filter(auth_id=auth["id"])
        # Auth code reused
        if auths.first() != None:
            return JsonResponse({"error":"Auth code reused"}, status=400)
        user = User.objects.filter(username=auth["username"])
        if user.first() == None:
            return JsonResponse({"error":"User doesn't exist"}, status=400)
        # Delete expired authenticators
        for auth in auths:
            diff = timezone.now() - auth.date_created
            if diff.total_seconds() > settings.ACCESS_TOKEN_EXPIRATION:
                auth.delete()
        access_token = hmac.new(key = settings.SECRET_KEY.encode('utf-8'), msg = os.urandom(32), digestmod = 'sha256',).hexdigest()
        Authenticator.objects.create(access_token=access_token, auth_id=auth["id"], username=auth["username"])
        resp = JsonResponse({
            "access_token":access_token,
            "expires_in":settings.ACCESS_TOKEN_EXPIRATION,
            "token_type":"Bearer",
        })
        resp['Cache-Control'] = "no-store"
        resp['Pragma'] = "no-cache"
        resp['Access-Control-Allow-Headers'] = "Authorization"
        return resp


def get_all_ranked_users(request):
    all_users = User.objects.all().exclude(username="admin").exclude(profile__role="")
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
            "year": user.profile.graduate_year,
            "major": user.profile.major,
            "matched":user.profile.matched,
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
    return JsonResponse({
        "all_users":all_users_dict,
    })