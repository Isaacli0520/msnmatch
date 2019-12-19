from django.urls import path
from . import views

urlpatterns = [
	path('',views.comments, name='comments'),
    path('send/',views.comments_send, name='comments_send'),
    path('filter/',views.comments_filter, name='comments_filter'),
]
