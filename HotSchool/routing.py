from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import communicate.routing
from communicate.extra import QueryAuthMiddleware

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': QueryAuthMiddleware(
        URLRouter(
            communicate.routing.websocket_urlpatterns
        )
    ),
})