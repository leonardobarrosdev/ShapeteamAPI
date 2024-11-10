from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.ChatsAPIView.as_view(), name='chat-list'),
    path('chat/<int:pk>/', views.ChatAPIView.as_view(), name='chat-detail'),
]