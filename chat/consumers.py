import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from urllib.parse import parse_qs
from rest_framework_simplejwt.tokens import AccessToken, TokenError
from .models import Message, ChatRoom
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        query_string = self.scope['query_string'].decode()
        tokens = parse_qs(query_string).get('token', None)
        if not tokens:
            await self.close()
            return
        token = tokens[0]
        try:
            validated_token = AccessToken(token)
            user_id = validated_token['user_id']  # Ensure token payload has 'user_id'
            self.scope['user'] = await database_sync_to_async(User.objects.get)(id=user_id)
        except (TokenError, KeyError):
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        await self.channel_layer.group_send(
            self.room_group_name,
            {'type': 'chat_message', 'message': f'{self.scope["user"].username} has joined.', 'sender': 'System'}
        )

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_send(
                self.room_group_name,
                {'type': 'chat_message', 'message': f'{self.scope["user"].username} has left.', 'sender': 'System'}
            )
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope['user']

        await self.save_message(message, user)

        await self.channel_layer.group_send(
            self.room_group_name,
            {'type': 'chat_message', 'message': message, 'sender': user.username}
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({'message': event['message'], 'sender': event['sender']}))

    @database_sync_to_async
    def save_message(self, message, user):
        room = ChatRoom.objects.get(name=self.room_name)
        Message.objects.create(room=room, sender=user, content=message)