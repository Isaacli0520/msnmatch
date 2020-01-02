from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/send_to_filter/", consumers.FilterConsumer),
    path("ws/send_to_comments/", consumers.CommentsConsumer),
    # /<from_user_name>/<to_user_name>/
]