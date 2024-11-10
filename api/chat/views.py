from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Chat
from .serializers import ChatSerializer


class ChatAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]
    permissions = ['view_chat', 'change_chat', 'delete_chat']


class ChatsAPIView(generics.ListCreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]
    permissions = ['add_chat', 'view_chat']