from django.urls import path
from . import views
from django.contrib.auth import logout, login

urlpatterns = [
	path('', views.courses, name='courses'),
	path('me/', views.my_courses, name='my_courses'),
	path('departments/', views.departments, name="departments"),
	path('reviews/', views.reviews, name="reviews"),
	path('instructors/<int:instructor_number>/', views.instructor, name="instructor"),
	path('<int:course_number>/', views.course, name='course'),
	path('departments/<int:department_number>/', views.department, name="department"),

	path('api/get_departments/', views.get_departments, name='get_departments'),
	path('api/get_department/', views.get_department, name='get_department'),
	path('api/get_course_instructor/', views.get_course_instructor, name='get_course_instructor'),
	path('api/get_course_instructors/', views.get_course_instructors, name='get_course_instructors'),
	path('api/get_user_hmp_header/', views.get_user_hmp_header, name='get_user_hmp_header'),
	path('api/get_top_reviews/', views.get_top_reviews, name='get_top_reviews'),

	path('api/submit_review/', views.submit_review, name='submit_review'),
	path('api/report_bug/', views.report_bug, name='report_bug'),

	path('api/get_roll_result/', views.get_roll_result, name='get_roll_result'),
	path('api/get_top_review_users/', views.get_top_review_users, name='get_top_review_users'),
	path('api/get_basic_info/', views.get_basic_info, name='get_basic_info'),
	path('api/get_my_courses/', views.get_my_courses, name='get_my_courses'),
	path('ajax/save_take/', views.save_take, name='save_take'),
	path('ajax/course_search_result/', views.course_search_result, name='course_search_result'),
	path('ajax/get_current_semester/', views.get_current_semester, name='get_current_semester'),
	path('ajax/get_course/', views.get_course, name='get_course'),
	path('ajax/get_instructor/', views.get_instructor, name='get_instructor'),
	path('ajax/get_trending_courses/', views.get_trending_courses, name='get_trending_courses'),
	path('ajax/get_recommendations/', views.get_recommendations, name='get_recommendations'),
	path('ajax/get_major_options/', views.get_major_options, name='get_major_options'),
	path('ajax/get_credential/', views.get_credential, name='get_credential'),
	path('ajax/get_reviews/', views.get_reviews, name='get_reviews'),

	path('<int:course_number>/<int:instructor_number>/', views.course_instructor, name='course_instructor'),

	path('api/get_plannable_profile/', views.get_plannable_profile, name='get_plannable_profile'),
	path('api/save_plannable_profile/', views.save_plannable_profile, name='save_plannable_profile'),
    path('api/edit_plannable_profile/', views.edit_plannable_profile, name="edit_plannable_profile"),
]
