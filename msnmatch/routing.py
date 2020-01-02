from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.sessions import SessionMiddlewareStack
import comments.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack( # SessionMiddlewareStack
        URLRouter(
            comments.routing.websocket_urlpatterns
        )
    ),
})