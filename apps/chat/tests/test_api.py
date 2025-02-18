import json, pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from apps.shapeteam.models import Connection
from apps.chat.models import Chat
from channels.testing import WebsocketCommunicator
from core.asgi import application


class ChatAPITest(APITestCase):
    fixtures = [
        'apps/user/fixtures/user_fixture.json',
        'apps/shapeteam/fixtures/connection_fixture.json',
        'apps/chat/fixtures/chat_fixture.json'
    ]

    def setUp(self):
        self.connection = Connection.objects.get(pk=1)
        self.user1 = get_user_model().objects.get(pk=self.connection.sender.pk)
        self.user2 = get_user_model().objects.get(pk=self.connection.receiver.pk)
        self.data = {
            "connection": self.connection.pk,
            "user": self.user1.pk,
            "message": "Hello, World!"
        }

    def test_create_chat_success(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(
            reverse('chat-list'),
            data=json.dumps(self.data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Chat.objects.count(), 3)
        self.assertEqual(Chat.objects.last().message, self.data['message'])

    def test_create_chat_error(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(
            reverse('chat-list'),
            data=json.dumps({"message": ""}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Chat.objects.count(), 3)

    def test_list_chat_success(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(reverse('chat-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_list_chat_error(self):
        response = self.client.get(reverse('chat-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


@pytest.mark.asyncio
async def test_websocket_connect():
    communicator = WebsocketCommunicator(application, "/ws/chat/testroom/")
    connected, subprotocol = await communicator.connect()
    assert connected
    await communicator.disconnect()

@pytest.mark.asyncio
async def test_websocket_receive_message():
    communicator = WebsocketCommunicator(application, "/ws/chat/testroom/")
    await communicator.connect()
    message = {"message": "Hello, World!"}
    await communicator.send_json_to(message)
    response = await communicator.receive_json_from()
    assert response == message
    await communicator.disconnect()

@pytest.mark.asyncio
async def test_websocket_disconnect():
    communicator = WebsocketCommunicator(application, "/ws/chat/testroom/")
    await communicator.connect()
    await communicator.disconnect()