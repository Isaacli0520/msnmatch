
from django.core.asgi import get_asgi_application
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "msnmatch.settings")
django_asgi_app = get_asgi_application()

from channels.layers import get_channel_layer
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import comments.routing

# django.setup()
channel_layer = get_channel_layer()
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            comments.routing.websocket_urlpatterns
        )
    ),
})