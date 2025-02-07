from knox.auth import TokenAuthentication
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Chat
from .serializers import ChatSerializer


class ChatsAPIView(generics.ListCreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]


class ChatAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
