import json
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from apps.shapeteam.models import Connection
from apps.chat.models import Chat


class ChatAPITest(APITestCase):
    fixtures = [
        'fixtures/user/user_fixture.json',
        'fixtures/shapeteam/connection_fixture.json',
        'fixtures/chat/chat_fixture.json'
    ]

    def setUp(self):
        self.connection = Connection.objects.get(pk=1)
        self.user1 = get_user_model().objects.get(pk=self.connection.sender.pk)
        self.user2 = get_user_model().objects.get(pk=self.connection.receiver.pk)
        self.data = {
            "connection": self.connection.pk,
            "user": self.user1.pk,
            "text": "Hello, World!"
        }

    def test_create_chat_success(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(
            reverse('chat-list'),
            data=json.dumps(self.data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Chat.objects.count(), 4)
        self.assertEqual(Chat.objects.last().text, self.data['text'])

    def test_create_chat_error(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(
            reverse('chat-list'),
            data=json.dumps({"text": ""}),
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