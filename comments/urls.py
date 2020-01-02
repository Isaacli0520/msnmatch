from django.urls import path
from . import views

urlpatterns = [
    path('test/',views.test, name='test'),
    path('create/',views.create, name='create'),
    path('send/',views.comments_send, name='comments_send'),
    path('filter/',views.comments_filter, name='comments_filter'),

	path('<slide_pk>/',views.comments, name='comments'),

    path('api/set_slide/', views.set_slide, name="set_slide"),
    path('api/create_slide/', views.create_slide, name="create_slide"),
    path('api/get_slide/', views.get_slide, name="get_slide"),
    path('api/get_slides/', views.get_slides, name="get_slides"),
    path('api/get_active_slide/', views.get_active_slide, name="get_active_slide"),
]
