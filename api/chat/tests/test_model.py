from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from api.shapeteam.models import Connection
from api.chat.models import Chat


class ChatTest(TestCase):
    fixtures = [
        'fixtures/user/user_fixture.json',
        'fixtures/shapeteam/connection_fixture.json'
    ]

    def setUp(self):
        self.user = get_user_model().objects.get(pk=1)
        self.connection = Connection.objects.get(pk=1)
        self.chat = Chat.objects.create(connection=self.connection, user=self.user, text='Hello, world!')

    def tearDown(self) -> None:
        return super().tearDown()

    def test_chat_success(self):
        self.assertIsInstance(self.chat, Chat)
        self.assertEqual(self.chat.connection, self.connection)
        self.assertEqual(self.chat.user, self.user)
        self.assertEqual(self.chat.text, 'Hello, world!')

    def test_chat_error(self):
        with self.assertRaises(IntegrityError):
            Chat.objects.create(user=self.user, text='Hello, world!')

    def test_chat_obj_field(self):
        chat = Chat.objects.get(pk=1)
        field_label = chat._meta.get_field('connection').verbose_name
        self.assertEqual(field_label, 'connection')
        self.assertEqual(str(chat), f'{chat.user.username}: {chat.text}')

    def test_chat_str(self):
        self.assertEqual(str(self.chat), f"{self.user.username}: Hello, world!")
