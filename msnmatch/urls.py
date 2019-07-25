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
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from . import views
from django.views.generic.base import RedirectView

from django.conf.urls import (
handler400, handler403, handler404, handler500
)

handler404 = 'msnmatch.views.handler404'
handler403 = 'msnmatch.views.handler403'

urlpatterns = [
	path('admin/', admin.site.urls),
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),
	path('', views.home, name='home'),
	path('match/', views.match, name='match'),
	path('users/', include('users.urls')),
	path('auth/', include('social_django.urls', namespace='social')),
	path('login/', auth_views.LoginView.as_view(), name='login'),
	path('courses/', include('courses.urls')),
	path('groups/', include('groups.urls')),
    path('skills/', include('skills.urls')),
    path('friendship/', include('friendship.urls')),
	path('superadmin/', views.superadmin, name="superadmin"),
	path('ajax/get_all_ranked_users/', views.get_all_ranked_users, name="get_all_ranked_users"),
	path('ajax/get_home_page_basic_info/', views.get_home_page_basic_info, name="get_home_page_basic_info"),

]
