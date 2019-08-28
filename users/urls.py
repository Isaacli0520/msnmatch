from django.urls import path
from . import views
from django.contrib.auth import logout, login

urlpatterns = [
    path('<username>/', views.profile, name='profile'),
    path('<username>/courses/', views.my_courses, name='my_courses'),
    path('<username>/edit/', views.update_profile, name='update_profile'),
]
