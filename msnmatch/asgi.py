from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.layers import get_channel_layer
from channels.auth import AuthMiddlewareStack

import os
import django
import comments.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "msnmatch.settings")
# django.setup()
# channel_layer = get_channel_layer()
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            comments.routing.websocket_urlpatterns
        )
    ),
})