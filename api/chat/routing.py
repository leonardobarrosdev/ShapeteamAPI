from django.urls import path
from api.chat import consumers

websocket_urlpatterns = [
	path('chat/', consumers.ChatConsumer.as_asgi())
]