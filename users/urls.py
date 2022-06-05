from django.urls import path
from django.contrib.auth import logout, login
from . import views

urlpatterns = [
    path('<username>/', views.profile, name='profile'),
    path('<username>/edit/', views.update_profile, name='update_profile'),

    path('api/signup_user/', views.signup_user,name="signup_user"),
    path('api/match_user/', views.match_user,name="match_user"),
    path('api/edit_user/',views.edit_user, name='edit_user'),
    path('api/check_mentor_requirements/', views.check_mentor_requirements, name="check_mentor_requirements"),
    path('api/choose_role/', views.choose_role, name="choose_role"),
    path('api/choose_roommate_role/', views.choose_roommate_role, name="choose_roommate_role"),
    path('api/add_fav/', views.add_fav, name="add_fav"),
    path('api/del_fav/', views.del_fav, name="del_fav"),

    path('api/get_match_header/', views.get_match_header, name="get_match_header"),
    path('api/get_profile/',views.get_profile, name='get_profile'),
    path('api/get_user_match_header/', views.get_user_match_header, name="get_user_match_header"),
    path('api/get_all_users/', views.get_all_users, name="get_all_users"),
    path('api/get_all_users_roommate/', views.get_all_users_roommate, name="get_all_users_roommate"),
    path('api/get_all_and_user_skills/', views.get_all_and_user_skills, name="get_all_and_user_skills"),
    path('api/get_follow_list/', views.get_follow_list, name="get_follow_list"),
]
