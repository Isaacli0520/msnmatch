from django.urls import path
from . import views
from django.contrib.auth import logout, login

urlpatterns = [
  path('', views.courses, name='courses'),
  path('departments/', views.departments, name="departments"),
  path('<course_number>/', views.course, name='course'),
  path('departments/<department_number>/', views.department, name="department"),
  path('ajax/save_take/', views.save_take, name='save_take'),
  path('ajax/course_search_result/', views.course_search_result, name='course_search_result'),
  path('ajax/get_course/', views.get_course, name='get_course'),
  path('ajax/get_course_instructor/', views.get_course_instructor, name='get_course_instructor'),
  path('ajax/get_basic_info/', views.get_basic_info, name='get_basic_info'),
  path('ajax/get_department/', views.get_department, name='get_department'),
  path('ajax/get_trending_courses/', views.get_trending_courses, name='get_trending_courses'),
  path('ajax/get_recommendations/', views.get_recommendations, name='get_recommendations'),
  path('ajax/get_major_options/', views.get_major_options, name='get_major_options'),
  path('ajax/get_departments/', views.get_departments, name='get_departments'),
  path('ajax/submit_review/', views.submit_review, name='submit_review'),
  path('<course_number>/<instructor_number>/', views.course_instructor, name='course_instructor'),
]
