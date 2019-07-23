from django.urls import path
from . import views
from django.contrib.auth import logout, login

urlpatterns = [
  path('', views.courses, name='courses'),
  path('search/',views.course_search, name='course_search'),
  path('<course_number>/', views.course, name='course'),
  path('sections/<course_instructor_number>/', views.course_instructor, name='course_instructor'),
  path('ajax/save_take/', views.save_take, name='save_take'),
  path('ajax/course_search_result/', views.course_search_result, name='course_search_result'),
  path('ajax/get_course/', views.get_course, name='get_course'),
  path('ajax/get_course_instructor/', views.get_course_instructor, name='get_course_instructor'),
  path('ajax/get_basic_info/', views.get_basic_info, name='get_basic_info'),
  path('ajax/submit_review/', views.submit_review, name='submit_review'),
  path('ajax/get_course_user/', views.get_course_user, name='get_course_user'),
]
