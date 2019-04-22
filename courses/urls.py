from django.urls import path
from . import views
from django.contrib.auth import logout, login

urlpatterns = [
  path('', views.list, name='courses'),
  path('search/',views.course_search, name='course_search'),
  path('search_auto/', views.course_search_auto, name='course_search_auto'),
  path('<course_number>/', views.course, name='course'),
  path('ajax/course_taking_add_delete/', views.course_taking_add_delete, name='course_taking_add_delete'),
  path('ajax/course_taken_add_delete/', views.course_taken_add_delete, name='course_taken_add_delete'),
  path('ajax/course_search_result/', views.course_search_result, name='course_search_result'),
]
