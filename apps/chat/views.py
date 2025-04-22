import ipdb
from knox.auth import TokenAuthentication
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .pagination import MessagePagination, ChatPagination
from .serializers import ChatSerializer, MessageSerializer
from apps.shapeteam.models import Connection
from .models import Chat, Message


User = get_user_model()

class ChatListAPIView(generics.ListCreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    authentication_classes = (TokenAuthentication,)
    pagination_class = ChatPagination


class ChatAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    authentication_classes = (TokenAuthentication,)


class ChatMessagesAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer
    authentication_classes = (TokenAuthentication,)
    pagination_class = MessagePagination

    def get_queryset(self):
        chat_id = self.kwargs['chatId']
        chat = get_object_or_404(Chat, id=chat_id)
        return chat.messages.order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

class MessageSendAPIView(generics.GenericAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    async def get(self, request):
        channel_layer = await get_channel_layer()
        await channel_layer.group_send(
            'chat_1', {
                'type': 'chat_message',
                'text': {'status': 'done'}
            }
        )
        return Response({'status': True}, status=status.HTTP_200_OK)

    async def post(self, request):
        msg = await Message.objects.create(
            contact=request.user,
            content=request.data['message']
        )
        channel_layer = await get_channel_layer()
        await channel_layer.group_send(
            'chat_1', {
                'type': 'chat_message',
                'text': {'message': msg.content}
            }
        )
        return Response({'status': True}, status=status.HTTP_201_CREATED)


async def get_user_contact(username1, username2):
    contact = await Connection.objects.filter(
        Q(sender__username=username1) | Q(receiver=username1) &
        Q(sender__username=username2) | Q(receiver=username2)
    ).first()
    return contact

async def get_current_chat(chat_id):
    return await get_object_or_404(Chat, id=chat_id)