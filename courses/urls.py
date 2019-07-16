from django.urls import path
from . import views
from django.contrib.auth import logout, login

urlpatterns = [
  path('', views.courses, name='courses'),
  path('search/',views.course_search, name='course_search'),
  path('<course_number>/', views.course, name='course'),
  path('ajax/course_search_result/', views.course_search_result, name='course_search_result'),
  path('ajax/get_course/', views.get_course, name='get_course'),
]
