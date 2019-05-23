from django.urls import path
from . import views

urlpatterns = [
  path('manage/', views.groups_manage, name='groups_manage'),
  path('family/', views.family, name='family'),
  path('<group_pk>/', views.group, name='group'),
  path('<group_pk>/edit/', views.update_group, name='update_group'),
  path('<group_pk>/tags/', views.update_group_tags, name='update_group_tags'),
  path('ajax/get_all_families/', views.get_all_families, name='get_all_families'),
  path('ajax/get_all_groups/', views.get_all_groups, name='get_all_groups'),
  path('ajax/get_manager_groups/', views.get_manager_groups, name='get_manager_groups'),
  path('ajax/get_member_groups/', views.get_member_groups, name='get_member_groups'),
  path('ajax/get_group/', views.get_group, name='get_group'),
  path('ajax/get_group_edit/', views.get_group_edit, name='get_group_edit'),
  path('ajax/get_family_page_basic_info/',views.get_family_page_basic_info, name='get_family_page_basic_info'),
]
