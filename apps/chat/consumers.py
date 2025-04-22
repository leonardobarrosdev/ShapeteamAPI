import json
from django.contrib.auth import get_user_model
from channels.generic.websocket import AsyncWebsocketConsumer
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_string = self.scope["query_string"].decode("utf-8")
        self.room_name = query_string.split("=")[1]
        self.groups.append(f"chat_{self.room_name}")
        try:
            await self.accept()
        except Exception as e:
            logger.error(f"Connection rejected: {e}")
            await self.close()
    
    async def receive(self, text_data=None, bytes_data=None):
        if text_data is not None:
            try:
                data = json.loads(text_data)
                message = data.get("message", "")
                user_id = data.get("user_id", None)
                if user_id:
                    user = await User.objects.aget(id=user_id)
                    await self.send(text_data=json.dumps({"message": f"{user.username}: {message}"}))
                else:
                    await self.send(text_data=json.dumps({"message": "User ID not provided."}))
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {e}")
                await self.send(text_data=json.dumps({"error": "Invalid JSON format."}))
        elif  bytes_data is None:
            try:
                data = json.loads(bytes_data)
                message = data.get("message", "")
                user_id = data.get("user_id", None)
                if user_id:
                    user = await User.objects.aget(id=user_id)
                    await self.send(text_data=json.dumps({"message": f"{user.username}: {message}"}))
                else:
                    await self.send(text_data=json.dumps({"message": "User ID not provided."}))
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {e}")
                await self.send(text_data=json.dumps({"error": "Invalid JSON format."}))
        else:
            logger.error("No text data received.")
            await self.send(text_data=json.dumps({"error": "No text data received."}))

    async def disconnect(self, close_code):
        try:
            await self.close(close_code) if close_code else await self.close()
        except Exception as e:
            logger.error(f"Error during disconnect: {e}")
