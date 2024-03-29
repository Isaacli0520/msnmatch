"""mango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

from django.conf.urls import (handler400, handler403, handler404, handler500)

handler404 = 'msnmatch.views.handler404'
handler403 = 'msnmatch.views.handler403'

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset/done', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/complete', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),  
    path('admin/', admin.site.urls),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', views.login_view, name='login'),
    path('auth/', include('social_django.urls', namespace='social')),
    path('superadmin/', views.superadmin, name="superadmin"),

    # Match
    path('match/', views.match, name='match'),
    path('roommate/', views.roommate_match, name='roommate_match'),

    # URLs for other apps
    path('users/', include('users.urls')),
    path('courses/', include('courses.urls')),
    path('comments/', include('comments.urls', namespace='comments')),
    path('market/', include('market.urls', namespace='market')),
    path('skills/', include('skills.urls')),
    path('friendship/', include('friendship.urls')),

    # APIs
    path('api/get_skill/', views.get_skill, name="get_skill"),
    path('api/get_all_ranked_users/', views.get_all_ranked_users, name="get_all_ranked_users"),
    path('oauth/authorize/', views.oauth_authorize, name="oauth_authorize"),
    path('oauth/api/token/', views.oauth_token, name="oauth_token"),
]
