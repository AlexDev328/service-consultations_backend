from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer, AsyncWebsocketConsumer, WebsocketConsumer
import json
import time

from chat.models import Room, Message


class ChatConsumer(AsyncJsonWebsocketConsumer):
    channel_layer_alias = 'chat'

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']

        await self.channel_layer.group_add(self.room_name, self.channel_name)

        print(self.room_name, 'Присоединен')

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        await self.close()

    async def receive_json(self, message, **kwargs):
        users_id = await get_collocutors(message['room_id'])
        from_user = self.room_name  # message.get('from_user')
        t = time.ctime()
        for i in users_id:
            await self.channel_layer.group_send(
                str(i),
                {
                    "type": "chat.message",
                    "event": {
                        'message': message.get('message'),
                        'group': str(self.room_name),
                        'from_user': from_user,
                        'time': t,
                    },
                },
            )

    async def chat_message(self, event):
        print(event)
        await self.send(text_data=json.dumps(event['event']))


class PushConsumer(AsyncWebsocketConsumer):
    channel_layer_alias = 'push'

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['id']

        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def push_message(self, event):
        print(event)
        await self.send(text_data=json.dumps(event))


@sync_to_async
def get_collocutors(room_id):
    res = []
    for i in Room.objects.filter(id=room_id)[0].collocutors.all().values('id'):
        res.append(i['id'])
    return res
