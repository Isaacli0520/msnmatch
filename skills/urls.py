from django.urls import path
from . import views
from django.contrib.auth import logout, login
app_name = "skills"

urlpatterns = [
  path('', views.skills, name="skills"),
  # path('rank/', views.skill_rank, name='skill_rank'),
  path('<int:skill_pk>/', views.skill, name='skill'),

  path('api/get_skill/', views.get_skill, name="get_skill"),
  path('api/get_all_users/', views.get_all_users, name="get_all_users"),
  path('api/get_all_and_user_skills/', views.get_all_and_user_skills, name="get_all_and_user_skills"),
  path('api/get_search_result/', views.get_search_result, name="get_search_result"),
  path('api/user_add_skill/', views.user_add_skill, name="user_add_skill"),
  path('api/user_del_skill/', views.user_del_skill, name="user_del_skill"),
  path('api/get_user_match_header/', views.get_user_match_header, name="get_user_match_header"),

  path('api/add_to_list/', views.add_to_list, name="add_to_list"),
  path('api/get_all_users/', views.get_all_users, name="get_all_users"),
  path('api/get_follow_list/', views.get_follow_list, name="get_follow_list"),
  path('api/del_fav/', views.del_fav, name="del_fav"),
  path('api/choose_role/', views.choose_role, name="choose_role"),
]
