# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from recipes.models import *


# class ChatConsumer(AsyncWebsocketConsumer):

#     async def connect(self):
#         self.room_name = f"room_{self.scope['url_route']['kwargs']['room_name']}"
#         await self.channel_layer.group_add(self.room_name, self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(self.room_name, self.channel_name)

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json

#         event = {
#             "type": "send_message",
#             "message": message,
#         }

#         await self.channel_layer.group_send(self.room_name, event)

#     async def send_message(self, event):
#         data = event["message"]
#         await self.create_message(data=data)
#         response_data = {"sender": data["sender"], "message": data["message"]}
#         await self.send(text_data=json.dumps({"message": response_data}))

#     @database_sync_to_async
#     def create_message(self, data):
#         get_room_by_name = Room.objects.get(room_name=data["room_name"])
#         if not Message.objects.filter(message=data["message"]).exists():
#             new_message = Message(
#                 room=get_room_by_name, sender=data["sender"], message=data["message"]
#             )
#             new_message.save()



import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from recipes.models import Room, Message
from django.contrib.auth.models import User


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_username = text_data_json['sender']
        room_name = text_data_json['room_name']

        # Save message to the database
        await self.create_message(sender_username, room_name, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender_username,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
        }))

    @database_sync_to_async
    def create_message(self, sender_username, room_name, message):
        room = Room.objects.get(room_name=room_name)
        sender = User.objects.get(username=sender_username)
        Message.objects.create(room=room, sender=sender, message=message)
