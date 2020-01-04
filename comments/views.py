from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Slide
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
# from django.db.models import Q

@login_required
def test(request):
    return render(request, 'test.html')

@login_required
def create(request):
    return render(request, 'commentcreate.html')

@login_required
def question(request):
    return render(request, 'commentquestion.html')

@login_required
def comments(request, slide_pk):
    return render(request, 'comments.html')

@login_required
def comments_send(request):
    return render(request, 'commentsend.html')

@login_required
def comments_filter(request):
    return render(request, 'commentfilter.html')

@login_required
def set_slide(request):
    if request.method == "POST":
        post = json.loads(request.body)
        slide_pk = post["slide_pk"]
        for slide in Slide.objects.all():
            slide.active = False
            slide.save()
        slide = get_object_or_404(Slide, pk = slide_pk)
        slide.active = True
        slide.save()
        return JsonResponse({
            "success":True
        })

@login_required
def create_slide(request):
    if request.method == "POST":
        post = json.loads(request.body)
        name, url = post["name"], post["url"]
        url = url[:url.find('pub?')]
        Slide.objects.create(user = request.user, name = name, url = url)
        return JsonResponse({"success":True})
    return JsonResponse({"success":False})


@login_required
def delete_slide(request):
    if request.method == "POST":
        post = json.loads(request.body)
        slide_pk= post["slide_pk"]
        slide = get_object_or_404(Slide, pk = slide_pk)
        slide.delete()
        return JsonResponse({"success":True})
    return JsonResponse({"success":False})

@login_required
def get_active_slide(request):
    if request.method == "GET":
        slide = Slide.objects.filter(active=True)
        if slide == None:
            return JsonResponse({
                "success":False,
            })
        return JsonResponse({
            "slide_pk":slide[0].pk,
        })
    return JsonResponse({
        "message":"POST method not supported",
    })

@login_required
def get_slide(request):
    if request.method == "GET":
        slide = get_object_or_404(Slide, pk = request.GET.get('slide_pk'))
        return JsonResponse({
            "pk":slide.pk,
            "url":slide.url,
        })

@login_required
def get_slides(request):
    if request.method == "GET":
        slides = Slide.objects.all()
        if slides != None:
            slides_json = [{
                "name":slide.name,
                "url":slide.url,
                "user":{
                    "first_name":slide.user.first_name,
                    "last_name":slide.user.last_name},
                "pk":slide.pk,
                "active":slide.active,
            }for slide in slides]
        else:
            slides_json = []
        return JsonResponse({
            "slides":slides_json,
        })
    return JsonResponse({
            "message":"POST method not supported",
        })