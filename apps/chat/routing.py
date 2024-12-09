from django.urls import path
from apps.chat import consumers

websocket_urlpatterns = [
	path('chat/', consumers.ChatConsumer.as_asgi())
]