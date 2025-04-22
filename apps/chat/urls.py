from django.urls import path
from . import views

urlpatterns = [
    path('', views.ChatListAPIView.as_view(), name='chat-list'),
    path('<str:username>/', views.ChatAPIView.as_view(), name='chat-detail'),
    path('<str:username>/messages/', views.ChatMessagesAPIView.as_view(), name='chat-messages'),
    path('send/', views.MessageSendAPIView.as_view(), name='send-message'),
]