import re
import time
import os
import json
import hmac
import random
import numpy as np
import datetime
from collections import Counter, defaultdict

from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity
from django.db.models import Q, F, Count
from django.db.models.functions import Lower, Substr, Length
from django.http import JsonResponse, Http404
from django.forms.models import model_to_dict
from django.utils import timezone

from msnmatch import settings
from msnmatch.utils import custom_md5, cmp_semester, val_required, js_boolean, _get_not_allowed, _post_not_allowed, _success_response, _error_response
from functools import cmp_to_key

from users.models import MAJOR_CHOICES, PlanProfile, PlanProfileVersion, Authenticator
from .models import Course, CourseUser, CourseInstructor, Instructor, Department, Bug

courseTypes = [
    'Clinical',
    'Discussion',
    'Drill',
    'Independent Study',
    'Laboratory',
    'Lecture',
    'Practicum',
    'Seminar',
    'Studio',
    'Workshop',
]

mnemonics = ['AAS', 'MATH', 'ANTH', 'SWAH', 'MDST', 'ARAD', 'ARAH', 'ARTH', 'ARTS',
'ARAB', 'ARTR', 'HEBR', 'HIND', 'MESA', 'MEST', 'PERS', 'SANS', 'SAST', 'SATR', 'URDU', 'ASTR',
'MUBD', 'MUEN', 'MUPF', 'MUSI', 'BIOL', 'HBIO', 'PHIL', 'CHEM', 'PHYS', 'CLAS', 'GREE', 'LATI',
'PLAD', 'PLAP', 'PLCP', 'PLIR', 'PLPT', 'DANC', 'DRAM', 'PHS', 'PHSE', 'CHIN', 'CHTR', 'EAST',
'JAPN', 'JPTR', 'KOR', 'TBTN', 'PSYC', 'ECON', 'RELA', 'RELB', 'RELC', 'RELG', 'RELH', 'RELI',
'RELJ', 'RELS', 'CPLT', 'ENAM', 'ENCR', 'ENCW', 'ENEC', 'ENGL', 'ENGN', 'ENLP', 'ENLT', 'ENMC',
 'ENMD', 'ENNC', 'ENPG', 'ENPW', 'ENRN', 'ENSP', 'ENWR', 'POL', 'RUSS', 'RUTR', 'SLAV', 'SLTR',
 'EVAT', 'EVEC', 'EVGE', 'EVHY', 'EVSC', 'SOC', 'CREO', 'FRTR', 'FREN', 'ITAL', 'ITTR', 'KICH',
 'PORT', 'POTR', 'SPAN', 'GERM', 'GETR', 'STAT', 'HIAF', 'HIEA', 'HIEU', 'HILA', 'HIME', 'HISA',
 'HIST', 'HIUS', 'EDHS', 'USEM', 'WGS', 'ASL', 'INST', 'AMST', 'JWST', 'ARCY', 'LAST', 'COGS',
 'COLA', 'LASE', 'CS', 'LING', 'LNGS', 'ARH', 'ELA', 'NESC', 'ARCH', 'PLAN', 'EURS', 'PST',
 'GDS', 'GSGS', 'GSMS', 'GSSJ', 'GSVS', 'PAVS', 'FORU', 'EGMT', 'ES', 'NUCO', 'APMA', 'CPE',
 'ECE', 'BME', 'EP', 'MSE', 'CHE', 'MAE', 'CE', 'STS', 'SYS', 'ENGR', 'EDIS', 'EDLF', 'KINE',
 'ALAR', 'LAR', 'PLAC', 'SARC', 'AM', 'LAW', 'GBUS', 'BIMS', 'BIOC', 'BIOP', 'CELL', 'MED',
 'GCOM', 'MICR', 'PATH', 'PHAR', 'PHY', 'COMM', 'GCNL', 'GNUR', 'NUIP', 'NURS', 'ENTP', 'LPPA',
 'LPPL', 'LPPP', 'LPPS', 'DS', 'AIR', 'AIRS', 'CASS', 'EDNC', 'HSCI', 'IMP', 'MISC', 'NAS',
 'NASC', 'PPL', 'UNST', "ESL",]

@login_required
def courses(request):
    return render(request, 'courses.html')

@login_required
def course_v2(request, course_number):
    try:
        mnemonic = re.search('(^[a-zA-Z]+)\d+$', course_number).group(1).upper()
        number_type = course_number[len(mnemonic):]
        if len(number_type) < 2:
            raise Http404
        cs_num, cs_type = number_type[:-1], int(number_type[-1])
        if cs_type >= len(courseTypes):
            raise Http404
        course = get_object_or_404(Course, mnemonic=mnemonic, number=cs_num, type=courseTypes[cs_type])
        return redirect(reverse('course', kwargs={"course_number": course.pk }))
    except:
        raise Http404

@login_required
def course(request, course_number):
    get_object_or_404(Course, pk=course_number)
    return render(request, 'course.html')

@login_required
def course_instructor(request, course_number, instructor_number):
    get_object_or_404(Course, pk=course_number)
    get_object_or_404(Instructor, pk=instructor_number)
    return render(request, 'course_instructor.html')

@login_required
def departments(request):
    return render(request, 'departments.html')

@login_required
def reviews(request):
    return render(request, 'reviews.html')

@login_required
def instructor(request, instructor_number):
    get_object_or_404(Instructor, pk=instructor_number)
    return render(request, 'instructor.html')

@login_required
def department(request, department_number):
    get_object_or_404(Department, pk=department_number)
    return render(request, 'department.html')

@login_required
def my_courses(request):
    return render(request, "mycourses.html")

@login_required
def get_current_semester(request):
    return _success_response({
        "year":settings.CURRENT_SEMESTER[:4],
        "semester":settings.CURRENT_SEMESTER[4:],
    })

# @login_required
def get_basic_info(request):
    info = {}
    if request.user.is_authenticated:
        info = {
            "profile": reverse('profile', args=[request.user.username]),
            "update_profile":reverse('update_profile', args=[request.user.username]),
        }
    return _success_response({
        "all_info":info,
    })

@login_required
def get_roll_result(request):
    date = request.GET.get("date")
    tot_winners = int(request.GET.get("tot_winners"))
    dt = datetime.datetime.strptime(date, '%Y-%m-%d')
    users = []
    for user in User.objects.all():
        user_review_num = user.courseuser_set.annotate(length=Length("text")).filter(length__gt=15, date__gt=dt).count()
        if user_review_num > 0 and user.username != "admin":
            users.append({
                "pk":user.pk,
                "username":user.username,
                "name":user.first_name + " " + user.last_name,
                "reviews":user_review_num,
            })
    random.shuffle(users)
    total_num = sum([u["reviews"] for u in users])
    num_try, MAX_TRY = 0, 1000
    result = []
    while len(result) != tot_winners and num_try < MAX_TRY:
        num_try += 1
        result = []
        lottery = sorted([random.randint(0, total_num - 1) for i in range(tot_winners)])
        pointer = 0
        left, right = 0, users[0]["reviews"] - 1
        for i, user in enumerate(users):
            if lottery[pointer] >= left and lottery[pointer] <= right:
                result.append(user)
                pointer += 1
            if i == len(users) - 1 or pointer >= tot_winners:
                break
            left = right + 1
            right = right + users[i + 1]["reviews"]
    return _success_response({
        "users":result
    })

@login_required
def report_bug(request):
    if request.method == "POST":
        post = json.loads(request.body)
        title, text = post.get("title"), post.get("text")
        if len(title) > 0 and len(text) > 0:
            Bug.objects.create(user=request.user, title=title, text=text)
            return _success_response()
        else:
            return _error_response("Missing title or text field")	
    return _error_response("Get method not allowed")

@login_required
def get_top_reviews(request):
    # time_start = time.time()
    reviews = CourseUser.objects.annotate(length=Length("text")).filter(Q(length__gt=45) & Q(take="taken"))
    tot = sum([review.length for review in reviews])
    reviews_prob = [review.length * 1.0 / tot for review in reviews]
    K = 10
    reviews = np.random.choice(reviews, K if K < len(reviews_prob) else len(reviews_prob), False, reviews_prob)
    reviews = [get_json_of_review(review) for review in reviews]
    # print("---------------get top reviews time--------------", time.time() - time_start)
    return _success_response({
        "reviews":reviews,
    })
    

@login_required
def get_top_review_users(request):
    date = request.GET.get("date")
    dt = datetime.datetime.strptime(date, '%Y-%m-%d')
    users = []
    for user in User.objects.all():
        user_review_num = user.courseuser_set.annotate(length=Length("text")).filter(length__gt=15, date__gt=dt).count()
        if user_review_num > 0:
            users.append({
                "pk":user.pk,
                "username":user.username,
                "name":user.first_name + " " + user.last_name,
                "reviews":user_review_num,
            })
    users = sorted(users, key=lambda x:x["reviews"], reverse=True)
    return _success_response({
        "review_users":users,
    })

@login_required
def get_course_instructors(request):
    course_pk, instructor_pk = request.GET.get("course_pk"), request.GET.get("instructor_pk")
    course = get_object_or_404(Course, pk=course_pk)
    instructor = get_object_or_404(Instructor, pk=instructor_pk)

    course_instructor_relations = []
    course_instructor_query = CourseInstructor.objects.filter(course=course, instructor=instructor)
    for course_instructor in course_instructor_query:
        course_instructor_relations.append({
            "course_instructor_pk":course_instructor.pk,
            "semester":course_instructor.semester,
            "topic":course_instructor.topic,
            })

    return _success_response({
        "course_instructors":course_instructor_relations,
    })

@login_required
def get_reviews(request):
    cs_users = CourseUser.objects.filter(user=request.user, take="taken")
    reviews_arr = [cs_user for cs_user in cs_users if cs_user.text]
    return _success_response({
        "reviews":[get_json_of_review(review) for review in reviews_arr]
    })

@login_required
def get_instructor(request):
    instructor_pk = request.GET.get("instructor_pk")
    instructor = get_object_or_404(Instructor, pk=instructor_pk)
    cs_instr_query = CourseInstructor.objects.filter(instructor=instructor)
    all_courses = {}
    for cs_instr in cs_instr_query:
        tmp_course_number = cs_instr.course.mnemonic + cs_instr.course.number
        if tmp_course_number not in all_courses:
            all_courses[tmp_course_number] = {
                "course_pk":cs_instr.course.pk,
                "mnemonic":cs_instr.course.mnemonic,
                "number":cs_instr.course.number,
                "title":cs_instr.course.title,
                "rating":get_rating_of_instructor_with_course(instructor, cs_instr.course)[0],
                "semesters":[]
            }
        if cs_instr.semester not in all_courses[tmp_course_number]["semesters"]:
            all_courses[tmp_course_number]["semesters"].append(cs_instr.semester)
    tmp_rating, tmp_counter = get_rating_of_instructor(instructor)
    return _success_response({
        "name":instructor.__str__(),
        "rating":tmp_rating,
        "rating_counter":tmp_counter,
        "rating_users_count":sum(tmp_counter),
        "courses":all_courses,
    })

@login_required
def get_user_hmp_header(request):
    return _success_response({
        "user":{
            "first_name":request.user.first_name,
            "last_name":request.user.last_name,
            "role":request.user.profile.role,
            "num_reviews":request.user.courseuser_set.annotate(length=Length("text")).filter(length__gt=15).count(),
        },
        "taking_courses":get_take_courses(request.user, "taking")
    })

@login_required
def get_my_courses(request):
    return _success_response({
        "taking_courses":get_take_courses(request.user, "taking"),
        "taken_courses":get_take_courses(request.user, "taken"),
    })

def get_take_courses(user, take):
    final_courses = []
    cs_users = CourseUser.objects.filter(user=user, take=take)
    for cs_user in cs_users:
        final_courses.append({
            "course_pk":cs_user.course.pk,
            "mnemonic":cs_user.course.mnemonic,
            "number":cs_user.course.number,
            "title":cs_user.course.title,
            "take":take,
            "type":cs_user.course.type,
            "semester":cs_user.course_instructor.semester,
        })
    return final_courses

@login_required
def get_credential(request):
    if request.method == "GET":
        auths = Authenticator.objects.filter(username=request.user.username)
        access_token = None
        if auths.first() != None:
            for auth in auths:
                diff = timezone.now() - auth.date_created
                if diff.total_seconds() > 86400 * 7:
                    auth.delete()
                elif access_token == None:
                    access_token = auth.access_token
        if access_token == None:
            access_token = hmac.new(key = settings.SECRET_KEY.encode('utf-8'), msg = os.urandom(32), digestmod = 'sha256',).hexdigest()
            Authenticator.objects.create(access_token=access_token, username=request.user.username)
        return _success_response({
            "credential":access_token,
            "username":request.user.username,
        })
    if request.method == "POST":
        return _post_not_allowed()

def get_versions_of_profile(profile):
    return [{
        "modified":int(p.modified.timestamp()*1000),
        "userAgent":p.user_agent,
        "version":p.version,
    } for p in profile.planprofileversion_set.all()] 

@csrf_exempt
@val_required
def edit_plannable_profile(request):
    if request.method == "POST":
        post = json.loads(request.body)
        username, credential = post["username"], post["credential"]
        try:
            user = User.objects.get(username=username)
        except:
            return _error_response("User doesn't exist")
        auth = authenticate_credential(credential, username)
        if auth["success"]:
            user_agent = request.META['HTTP_USER_AGENT']
            action = post["action"]
            # Rename profile and delete all previous versions
            if action == "rename":
                oldName, newName, content = post["oldName"], post["newName"], post["profile"]
                try:
                    profile = PlanProfile.objects.get(user=user ,name=oldName)
                except:
                    return _error_response("Profile doesn't exist")
                new_profile = PlanProfile.objects.filter(user=user, name=newName).first()
                # newName already exists, delete old profile and add new version to new profile it
                if new_profile != None:
                    for p_v in profile.planprofileversion_set.all():
                        p_v.delete()
                    profile.delete()
                    PlanProfileVersion.objects.create(version=new_profile.latest + 1, content=content, plan_profile=new_profile, user_agent=user_agent)
                    new_profile.latest += 1
                    new_profile.save()
                    return _success_response({"versions":get_versions_of_profile(new_profile)})
                # Delete(detach) previous versions
                for p_v in profile.planprofileversion_set.all():
                    p_v.delete()
                PlanProfileVersion.objects.create(version=1, content=content, plan_profile=profile, user_agent=user_agent)
                profile.name = newName
                profile.latest = 1
                profile.save()
                return _success_response({"versions":get_versions_of_profile(profile)})
            # Delete profile and corresponding versions
            elif action == "delete":
                if "name" not in post:
                    return _error_response("Missing name field")
                name = post["name"]
                try:
                    profile = PlanProfile.objects.get(user=user ,name=name)
                except:
                    return _error_response("Profile doesn't exist")
                for p_v in profile.planprofileversion_set.all():
                    p_v.delete()
                profile.delete()
                return _success_response()
            else:
                return _error_response("Action not recognized")
        else:
            return _error_response(auth["message"])
    if request.method == "GET":
        return _get_not_allowed()

@csrf_exempt
@val_required
def get_plannable_profile(request):
    if request.method == "POST":
        post = json.loads(request.body)
        username, credential= post["username"], post["credential"]
        try:
            user = User.objects.get(username=username)
        except:
            return _error_response("User doesn't exist")
        auth = authenticate_credential(credential, username)
        if auth["success"]:
            ret_profile = []
            # Return a specific profile
            if "name" in post:
                profile = PlanProfile.objects.filter(name=post["name"], user=user).first()
                if profile == None:
                    return _error_response("Profile doesn't exist")
                # Return a specific version of the profile
                if "version" in post:
                    try:
                        version = int(post["version"])
                    except:
                        return _error_response("Version should be a number")
                    real_profile = profile.planprofileversion_set.filter(version=version).first()
                # Return the latest version of the profile 
                else:
                    real_profile = profile.planprofileversion_set.filter(version=profile.latest).first()
                ret_profile.append({
                    "versions":get_versions_of_profile(profile),
                    "profile":real_profile.content,
                })
            # Return all profiles
            else:
                profiles = PlanProfile.objects.filter(user=user)
                for profile in profiles:
                    ret_profile.append({
                        "versions":get_versions_of_profile(profile),
                        "profile":profile.planprofileversion_set.filter(version=profile.latest).first().content,
                    })
            return JsonResponse({
                    "success":True,
                    "message":"Nice",
                    "profiles":ret_profile,
                }, safe=False)
        else:
            return _error_response(auth["message"])
    if request.method == "GET":
        return _get_not_allowed()

@csrf_exempt
@val_required
def save_plannable_profile(request):
    if request.method == "POST":
        post = json.loads(request.body)
        username, credential, profiles = post["username"], post["credential"], post["profiles"]
        try:
            user = User.objects.get(username=username)
        except:
            return _error_response("User doesn't exist")
        auth = authenticate_credential(credential, username)
        if auth["success"]:
            user_agent = request.META['HTTP_USER_AGENT']
            versions = []
            for profile in profiles:
                name, content = profile["name"], profile["profile"]
                plan_profile = PlanProfile.objects.filter(user=user, name=name).first()
                new_flag = plan_profile == None
                if new_flag:
                    plan_profile = PlanProfile.objects.create(user=user, name=name)
                # Force to create a new version
                if "new" in profile or new_flag:
                    PlanProfileVersion.objects.create(version=plan_profile.latest + 1, content=content, plan_profile=plan_profile, user_agent=user_agent)
                    plan_profile.latest += 1
                    plan_profile.save()
                # Server decide whether to create a new version
                else:
                    latest_version = plan_profile.planprofileversion_set.filter(version=plan_profile.latest).first()
                    if latest_version == None:
                        return _error_response("Dirty profile")
                    diff = timezone.now() - latest_version.modified
                    # Latest version is more than 5min old, create new version
                    if diff.total_seconds() > 300:
                        PlanProfileVersion.objects.create(version=plan_profile.latest + 1, content=content, plan_profile=plan_profile, user_agent=user_agent)
                        plan_profile.latest += 1
                        plan_profile.save()
                    # Latest version is still young, update latest version
                    else:
                        latest_version.user_agent = user_agent
                        latest_version.content = content
                        latest_version.save()
                versions.append(get_versions_of_profile(plan_profile))
            return _success_response({"versions":versions})
        else:
            return _error_response(auth["message"])
    if request.method == "GET":
        return _get_not_allowed()
    

@login_required
def get_recommendations(request):
    year, semester, major = request.GET.get('year'), request.GET.get('semester'), request.GET.get('major')
    users_pk = [sth.pk for sth in User.objects.filter(profile__major=major).exclude(username="admin")]
    if len(users_pk) == 0:
        return _success_response({
            "rcm_courses":[],
        })
        
    cs_users = CourseUser.objects.filter(user__pk__in=users_pk, take="taken")
    final_cs_users = []
    courses_dict = {}
    for cs_user in cs_users:
        if cs_user.user.profile.graduate_year:
            tmp_year, tmp_semester = year_and_semester(cs_user.course_instructor.semester)
            if tmp_year + 4 - int(cs_user.user.profile.graduate_year) == int(year) and tmp_semester == semester:
                final_cs_users.append(cs_user)

    for cs_user in final_cs_users:
        if cs_user.course.pk not in courses_dict:
            courses_dict[cs_user.course.pk] = 1
        else:
            courses_dict[cs_user.course.pk] += 1

    courses = []
    for pk, num in courses_dict.items():
        tmp_course = get_object_or_404(Course, pk=pk)
        courses.append({
            "course_pk":pk,
            "mnemonic":tmp_course.mnemonic,
            "number":tmp_course.number,
            "title":tmp_course.title,
            "taken":num,
            })
    return _success_response({
        "rcm_courses":courses,
    })

@login_required
def get_major_options(request):
    major = ""
    semester = settings.CURRENT_SEMESTER[4:]
    year = 0
    majors = [{"text":item[0], "value":item[0]} for item in MAJOR_CHOICES]

    if request.user.profile.major:
        major = request.user.profile.major
    if request.user.profile.graduate_year:
        year = int(settings.CURRENT_YEAR) + 4 - int(request.user.profile.graduate_year)

    return _success_response({
        "major_options":majors,
        "major":major,
        "year":year,
        "semester":semester,
    })

"""
Seperate the year and semester of the input string, and the year is incremented if semester is Fall

Parameters:
    ys(String): String with format like "2019Fall"

Returns:
    int: The year part of ys
    string: The semester part of ys
"""
def year_and_semester(ys):
    year, semester = ys[:4], ys[4:]
    if semester == "Fall":
        return int(year) + 1, semester
    else:
        return int(year), semester

@login_required
def get_trending_courses(request):
    # time_start = time.time()
    tmp_courses = Course.objects.annotate(num_taken=Count('courseuser', filter=Q(courseuser__take__iexact = "taken"))).annotate(num_taking=Count('courseuser', filter=Q(courseuser__take__iexact = "taking")))
    taken_courses = sorted(tmp_courses, key=lambda c: c.num_taken, reverse=True)[:20]
    final_taken_courses = []
    for cs in taken_courses:
        if cs.num_taken > 0:
            final_taken_courses.append({
                "course_pk":cs.pk,
                "title":cs.title,
                "mnemonic":cs.mnemonic,
                "number":cs.number,
                "description":cs.description,
                "taking":cs.num_taking,
                "taken":cs.num_taken,
                "last_taught":cs.last_taught,
            })

    # time_end = time.time()
    # print("GET TRENDING TIME SPENT:", time_end - time_start)
    return _success_response({
        "taken_courses":final_taken_courses[:10],
    })

@login_required
def get_departments(request):
    return _success_response({
        "departments":[model_to_dict(department) for department in Department.objects.all().exclude(name="")],
    })

@login_required
def get_department(request):
    start_time = time.time()
    department_pk = request.GET.get("department_pk")
    department = get_object_or_404(Department, pk=department_pk)
    ret_courses = [get_detailed_json_of_course(cs, request.user, with_take=True) for cs in department.course_set.all().exclude(units="0")]
    print("Time Spent:", time.time()-start_time)
    return _success_response({
        "department":{
            "name":department.name,
            "school":department.school,
        },
        "courses":ret_courses,
    })

@login_required
def submit_review(request):
    if request.method == "POST":
        post = json.loads(request.body)
        text, rating_course, rating_instructor = post["text"], post["rating_course"], post["rating_instructor"]
        course_instructor_pk =  post["course_instructor_pk"]
        if len(text.strip()) == 0 or rating_course == 0 or rating_instructor == 0:
            return _error_response()
        course_instructor = get_object_or_404(CourseInstructor, pk=course_instructor_pk)
        cs_user_query = CourseUser.objects.filter(course=course_instructor.course, user=request.user)
        if cs_user_query.first() != None:
            cs_user = cs_user_query.first()
            cs_user.text = text
            cs_user.instructor = course_instructor.instructor
            cs_user.take = "taken"
            cs_user.rating_course = rating_course
            cs_user.rating_instructor = rating_instructor
            cs_user.course_instructor = course_instructor
            cs_user.save()
        else:
            CourseUser.objects.create(course=course_instructor.course,
                user=request.user, 
                instructor=course_instructor.instructor,
                course_instructor=course_instructor,
                text=text,
                take="taken",
                rating_course=rating_course,
                rating_instructor=rating_instructor)
        return _success_response()
    if request.method == "GET":
        return _get_not_allowed()

@login_required
def save_take(request):
    now_instructor_pk, now_semester, now_take = "", "", ""
    if request.method == "POST":
        post = json.loads(request.body)
        take, semester, delete = post['take'], post['semester'], post['delete']
        course = get_object_or_404(Course, pk=post['course_pk'])
        past_query = CourseUser.objects.filter(user=request.user, course = course)
        if delete:
            if past_query.first() != None:
                past_query.first().delete()
            return _success_response()
        instructor = get_object_or_404(Instructor, pk=post['instructor_pk'])
    
        cs_instr = get_object_or_404(CourseInstructor, pk=post["course_instructor_pk"])

        if past_query.first() != None:
            past_query.first().delete()
        if not delete:
            cs_user = CourseUser.objects.create(user=request.user, course = course, instructor = instructor, course_instructor = cs_instr)
            now_instructor_pk, now_semester, now_take = cs_user.course_instructor.instructor.pk, cs_user.course_instructor.semester, cs_user.take
        return _success_response({
            "now":{
                "instructor_pk":now_instructor_pk,
                "semester":now_semester,
                "take":now_take,
            },
        })
    if request.method == "GET":
        return _get_not_allowed()

@login_required
def get_course(request):
    pk = request.GET.get("pk")
    course = get_object_or_404(Course, pk=pk)
    return _success_response({
        "course":get_detailed_json_of_course(course, request.user,with_take=True, with_instructors=True),
    })

@login_required
def get_course_instructor(request):
    course_pk, instructor_pk = request.GET.get("course_pk"), request.GET.get("instructor_pk")
    course = get_object_or_404(Course, pk=course_pk)
    instructor = get_object_or_404(Instructor, pk=instructor_pk)
    return _success_response(get_detailed_json_of_course_instructor(course, instructor, request.user))

@login_required
def course_search_result(request):
    query = request.GET.get("query")
    query_time = request.GET.get("time")
    search_course = js_boolean(request.GET.get('cs'))
    search_instructor = js_boolean(request.GET.get('instr'))
    if not query or not query_time:
        return _error_response("Query or Time not provided")
    search_queryset = course_and_instructor_retrieve(query, search_course, search_instructor)
    course_result = []
    for query in search_queryset:
        if query[1] == "instructor":
            course_result.append(get_json_of_instructor(query[0]))
        if query[1] == "course":
            course_result.append(get_json_of_course(query[0]))
    return _success_response({
        "course_result": course_result,
        "time":query_time,
    })

# --------------------------- Helper Functions ---------------------------

def course_and_instructor_retrieve(query, search_course, search_instructor):
    query = query.strip().lower()

    nums = re.findall(r'\d+', query)
    strs = []
    for s in re.findall(r'[^\d.]+', query):
        strs += s.split()
    strs = [s.strip() for s in strs]

    # Extract the mnemonics from the non-num strings
    tmp_mn = [strs[i] for i in range(len(strs)) if strs[i].upper() in mnemonics]
    tmp_ix = [i for i in range(len(strs)) if strs[i].upper() in mnemonics]
    new_strs = [strs[i] for i in range(len(strs)) if i not in tmp_ix]

    # Get the extracted queries of mnemonics, nums, and other non-num strings
    query_string_mn = " ".join(tmp_mn)
    query_string_str = " ".join([s.strip() for s in new_strs])
    query_string_num = nums[0] if len(nums) > 0 else ""

    # print(query, "----", query_string_mn, "----", query_string_num, "----",query_string_str, "----")

    exact_course_query = Course.objects.filter(mnemonic__iexact=query_string_mn, number__iexact=query_string_num)
    
    if len(query.split()) == 2:
        tmp_a, tmp_b = query.split()[0], query.split()[1]
        exact_instructor_query = Instructor.objects.filter(first_name__iexact = tmp_a, last_name__iexact = tmp_b) | Instructor.objects.filter(first_name__iexact = tmp_b, last_name__iexact = tmp_a)

    if query.upper() in mnemonics and search_course:
        return [(course, "course") for course in sorted(Course.objects.filter(mnemonic=query.upper()).exclude(units="0"), key=lambda c:(c.mnemonic, c.number))]
    elif exact_course_query.first() != None and search_course:
        return [(course, "course") for course in exact_course_query.exclude(units="0")]
    elif len(query.split()) == 2 and exact_instructor_query.first() != None and search_instructor:
        return [(tmp_instructor, "instructor") for tmp_instructor in exact_instructor_query]
    else:
        retrieved_courses, retrieved_instructors = [], []
        if search_course:
            tmp_course_queryset = Course.objects.exclude(units="0").annotate(
                similarity_prefix=TrigramSimilarity('mnemonic',query_string_mn),
                similarity_number=TrigramSimilarity('number',query_string_num),
                similarity_name=TrigramSimilarity('title', query_string_str)).filter((Q(similarity_prefix__gt=0.5) & (Q(number__startswith=query_string_num)|Q(similarity_number__gt=0.3)|Q(similarity_name__gt=0.2))) | Q(similarity_name__gt=0.25))
            retrieved_courses = sorted(tmp_course_queryset, key=lambda c: (-c.similarity_prefix,-c.similarity_number, -c.similarity_name,c.mnemonic,c.number))
            retrieved_courses = [(tmp_r_c, "course") for tmp_r_c in retrieved_courses[:20]]
        if search_instructor:
            tmp_instructor_queryset = Instructor.objects.annotate(
                similarity_first_name=TrigramSimilarity('first_name', query_string_str),
                similarity_last_name=TrigramSimilarity('last_name', query_string_str),
            ).filter(Q(similarity_first_name__gt=0.35)|Q(similarity_last_name__gt=0.35))
            retrieved_instructors = sorted(tmp_instructor_queryset, key=lambda c: (-c.similarity_first_name,-c.similarity_last_name))
            retrieved_instructors = [(tmp_r_i, "instructor") for tmp_r_i in retrieved_instructors[:20]]
        
        return retrieved_courses + retrieved_instructors

def cmp_semester_key(a,b):
    return cmp_semester(a["semester"], b["semester"])

def get_json_of_instructor(instructor):
    return {
        "pk":instructor.pk,
        "name": instructor.__str__(),
        "type":"instructor",
        "last_taught":instructor.last_taught,
    }

def get_json_of_course(course):
    return {
        "pk":course.pk,
        "mnemonic":course.mnemonic,
        "number":course.number,
        "title":course.title,
        "last_taught":course.last_taught,
        "type":"course",
    }

def get_detailed_json_of_course_instructor(course, instructor, user):
    course_instructor_relations = []
    course_instructor_query = CourseInstructor.objects.filter(course=course, instructor=instructor)
    for course_instructor in course_instructor_query:
        if course_instructor.semester != settings.CURRENT_SEMESTER:
            course_instructor_relations.append({
                "course_instructor_pk":course_instructor.pk,
                "topic":course_instructor.topic,
                "semester":course_instructor.semester,
                })

    # duplicated_keys = []
    # course_users = []
    # for course_user in CourseUser.objects.filter(course=course, instructor=instructor):
    # 	if course_user.user.pk not in duplicated_keys:
    # 		duplicated_keys.append(course_user.user.pk)
    # 		course_users.append(get_detailed_json_of_course_user(course_user))
    course_users = [get_detailed_json_of_course_user(course_user) for course_user in CourseUser.objects.filter(course=course, instructor=instructor) ]
    tmp_query, tmp_counter = get_rating_of_instructor_with_course(instructor, course)
    return {
        "course":get_detailed_json_of_course(course, user),
        "instructor":{
            "instructor_pk":instructor.pk,
            "name":instructor.__str__(),
            "rating_instructor":tmp_query,
            "rating_instructor_counter":tmp_counter,
            "rating_instructor_users_count":sum(tmp_counter),
            "counter":tmp_counter,
        },
        "course_instructors":course_instructor_relations,
        "course_users":course_users,
    }

def get_json_of_review(review):
    return {
        "course":{
            "mnemonic":review.course.mnemonic,
            "number":review.course.number,
            "title":review.course.title,
            "pk":review.course.pk,
        },
        "instructor":{
            "pk":review.instructor.pk,
            "name":review.instructor.__str__(),
        },
        "semester":review.course_instructor.semester,
        "take":review.take,
        "text":review.text,
        "rating_instructor":review.rating_instructor,
        "rating_course":review.rating_course,
        "instructor_pk":review.instructor.pk,
        "course_instructor_pk":review.course_instructor.pk,
    }

def get_detailed_json_of_course_user(course_user):
    return {
        "course_pk":course_user.course.pk,
        "mnemonic":course_user.course.mnemonic,
        "number":course_user.course.number,
        "title":course_user.course.title,
        "course_user_pk":course_user.pk,
        "instructor_pk":course_user.instructor.pk,
        "instructor_name":course_user.instructor.__str__(),
        "course_instructor_pk":course_user.course_instructor.pk,
        "user_pk":course_user.user.pk,
        "username":course_user.user.username,
        "name":course_user.user.first_name + " " + course_user.user.last_name,
        "take":course_user.take,
        "text":course_user.text,
        "semester":course_user.course_instructor.semester,
        "rating_course":course_user.rating_course,
        "rating_instructor":course_user.rating_instructor,
    }

def get_detailed_json_of_course(course, user, with_instructors=False, with_take=False):
    courseUser_query = CourseUser.objects.filter(user=user, course=course).first()
    take = {"instructor_pk":"", "course_pk":"", "semester":"", "take":""}

    rating_course, rating_course_counter = get_rating_of_course(course)
    if courseUser_query != None:
        take = {
            "instructor_pk":courseUser_query.course_instructor.instructor.pk,
            "course_pk":courseUser_query.course.pk,
            "semester":courseUser_query.course_instructor.semester,
            "take":courseUser_query.take,
            "course_instructor_pk":courseUser_query.course_instructor.pk,
        }
    course_dict = {
        "course_pk":course.pk,
        "mnemonic":course.mnemonic,
        "number":course.number,
        "title":course.title,
        "description":course.description,
        "prerequisite":course.prerequisite,
        "type":course.type,
        "take":take,
        "last_taught":course.last_taught,
        "department":{
            "name":course.department.name,
            "department_pk":course.department.pk,
        },
        "rating_course":rating_course,
        "rating_course_counter":rating_course_counter,
    }
    if with_instructors:
        course_dict["instructors"] = get_instructors_of_course(course)
    if with_take:
        course_dict["taking"] = course.courseuser_set.filter(take="taking").count()
        course_dict["taken"] = course.courseuser_set.filter(take="taken").count()
    return course_dict

def get_instructors_of_course(course):
    courseInstructor_query = CourseInstructor.objects.filter(course=course)
    final_instructors = []
    if courseInstructor_query.first() != None:
        instructors = {}
        for cs_instructor in courseInstructor_query:
            tmp_name = cs_instructor.instructor.__str__()
            rating_instructor, _ = get_rating_of_instructor_with_course(cs_instructor.instructor, course)
            if tmp_name not in instructors:
                tmp_cs_user_query = CourseUser.objects.filter(course=course, instructor=cs_instructor.instructor)
                instructors[tmp_name] = {
                    "semesters":[],
                    "pk":cs_instructor.instructor.pk,
                    "rating_instructor":rating_instructor,
                    "taking":tmp_cs_user_query.filter(take="taking").count(),
                    "taken":tmp_cs_user_query.filter(take="taken").count(),
                }
            instructors[tmp_name]["semesters"].append({
                "semester":cs_instructor.semester,
                "course_instructor_pk":cs_instructor.pk,
                "topic":cs_instructor.topic,
            })
        for instructor_name,v in instructors.items():
            topic = ""
            if len(v["semesters"]) > 0:
                v["semesters"] = sorted(v["semesters"], key=cmp_to_key(cmp_semester_key), reverse=True)
                topic = v["semesters"][0]["topic"]
            
            final_instructors.append({
                "name":instructor_name,
                "semesters":v["semesters"],
                "topic":topic,
                "pk":v["pk"],
                "rating_instructor":v["rating_instructor"],
                "taking":v["taking"],
                "taken":v["taken"],
            })
    return final_instructors

def get_rating_of_course(course):
    return get_rating(CourseUser.objects.filter(course=course), "rating_course")

def get_rating_of_instructor_with_course(instructor, course):
    return get_rating(CourseUser.objects.filter(course=course, instructor = instructor), "rating_instructor")

def get_rating_of_instructor(instructor):
    return get_rating(CourseUser.objects.filter(instructor = instructor), "rating_instructor")

def get_rating(course_user_queryset, attr_name):
    rating_arr = []
    rating_instructor = 0
    counter = [0] * 6
    for cs_user in course_user_queryset:
        tmp_user_rating = getattr(cs_user, attr_name)
        if tmp_user_rating != None and tmp_user_rating > 0 and tmp_user_rating <= 5:
            rating_arr.append(int(tmp_user_rating))
    if len(rating_arr) > 0:
        rating_instructor = sum(rating_arr)/len(rating_arr)
    for k, v in Counter(rating_arr).items():
        counter[k] = v
    return round(rating_instructor,2), counter