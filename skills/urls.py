from django.urls import path
from . import views
from django.contrib.auth import logout, login

urlpatterns = [
  path('search/', views.skill_search, name='skill_search'),
  path('rank/', views.skill_rank, name='skill_rank'),
  path('<skill_pk>/', views.skill, name='skill'),
  path('ajax/result/', views.skill_search_result, name="skill_search_result"),
  path('ajax/add_del_skill/', views.add_del_skill, name="add_del_skill"),
  path('ajax/get_all_user_skills/', views.get_all_user_skills, name="get_all_user_skills"),
  path('ajax/get_all_skills/', views.get_all_skills, name="get_all_skills"),
  path('ajax/add_to_list/', views.add_to_list, name="add_to_list"),
  path('ajax/get_all_users/', views.get_all_users, name="get_all_users"),
  path('ajax/retrieve_users/', views.retrieve_users, name="retrieve_users"),
  path('ajax/get_follow_list/', views.get_follow_list, name="get_follow_list"),
  path('ajax/del_fav/', views.del_fav, name="del_fav"),
  path('ajax/get_users_by_sim/', views.get_users_by_sim, name="get_users_by_sim"),
  
#   path('ajax/course_taking_add_delete/', views.course_taking_add_delete, name='course_taking_add_delete'),
#   path('ajax/course_taken_add_delete/', views.course_taken_add_delete, name='course_taken_add_delete'),
#   path('ajax/course_search_result/', views.course_search_result, name='course_search_result'),
]
