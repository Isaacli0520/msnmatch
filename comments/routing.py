from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/send_to_filter/", consumers.FilterConsumer.as_asgi()),
    path("ws/send_to_comments/", consumers.CommentsConsumer.as_asgi()),
    # /<from_user_name>/<to_user_name>/
]