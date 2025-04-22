from django.contrib.auth import get_user_model
from channels.testing import WebsocketCommunicator, ChannelsLiveServerTestCase
from knox.models import AuthToken
from apps.shapeteam.models import Connection
from apps.chat.models import Message, Chat
from apps.chat.consumers import ChatConsumer


class ChatConsumerTest(ChannelsLiveServerTestCase):
    fixtures = [
        'apps/user/fixtures/goal_fixture.json',
        'apps/user/fixtures/user_fixture.json',
        'apps/shapeteam/fixtures/connection_fixture.json',
        'apps/chat/fixtures/message_fixture.json',
        'apps/chat/fixtures/chat_fixture.json',
    ]

    def setUp(self):
        self.connection = Connection.objects.get(pk=2)
        self.user1 = get_user_model().objects.get(pk=self.connection.sender.pk)
        self.user2 = get_user_model().objects.get(pk=self.connection.receiver.pk)
        self.chat = Chat.objects.get(participant=self.connection)
        # _, token = AuthToken.objects.create(self.user1)
        # self.token = token
        # self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

    async def test_consumer(self):
        communicator = WebsocketCommunicator(
            ChatConsumer.as_asgi(),
            f"/ws/chat/?room_name={self.chat.id}",
            # headers=[(b'Authorization', f'Token {self.token}'.encode())]
        )
        # Connect to the WebSocket
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)
        # Send a message
        message_data = {'message': "Hello, World!", 'user_id': self.user1.id}
        await communicator.send_json_to(message_data)
        # Receive the message
        response = await communicator.receive_json_from()
        self.assertIn('message', response)
        self.assertEqual(
            response['message'],
            f"{self.user1.username}: {message_data['message']}"
        )
        await communicator.disconnect()