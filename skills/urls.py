from django.urls import path
from . import views
from django.contrib.auth import logout, login
app_name = "skills"

urlpatterns = [
    path('', views.skills, name="skills"),
    # path('rank/', views.skill_rank, name='skill_rank'),
    path('<int:skill_pk>/', views.skill, name='skill'),

    path('api/get_search_result/', views.get_search_result, name="get_search_result"),
    
    path('api/user_add_skill/', views.user_add_skill, name="user_add_skill"),
    path('api/user_del_skill/', views.user_del_skill, name="user_del_skill"),
]
