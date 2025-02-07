from django.urls import path
from . import views

urlpatterns = [
    path('', views.ChatsAPIView.as_view(), name='chat-list'),
    path('<str:username>/', views.ChatAPIView.as_view(), name='chat-detail'),
]