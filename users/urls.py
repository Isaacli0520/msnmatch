from django.urls import path
from . import views
from django.contrib.auth import logout, login

urlpatterns = [
    path('match/', views.match, name="match"),
    path('<username>/', views.profile, name='profile'),
    path('<username>/request', views.friendship_accept, name='request'),
    path('<username>/edit/', views.update_profile, name='update_profile'),
]
