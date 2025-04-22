import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from apps.chat.routing import websocket_urlpatterns
from core.socketauth import QueryAuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": QueryAuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})