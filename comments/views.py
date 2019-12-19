from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
# from django.db.models import Q

@login_required
def comments(request):
    req_user = User.objects.get(username=request.user.username)
    return render(request, 'comments.html', {
        # "req_user_avatar_url":req_user_avatar_url,
    })

@login_required
def comments_send(request):
    req_user = User.objects.get(username=request.user.username)
    return render(request, 'commentsend.html', {
        # "req_user_avatar_url":req_user_avatar_url,
    })

@login_required
def comments_filter(request):
    req_user = User.objects.get(username=request.user.username)
    return render(request, 'commentfilter.html', {
        # "req_user_avatar_url":req_user_avatar_url,
    })
