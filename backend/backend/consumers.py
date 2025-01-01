import json

from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
            self.group_name = f'notifications_group'
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
    
    async def receive(self, text_data=None, bytes_data=None):
        pass

    async def send_notification(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = f'chat_group'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
             self.group_name,
             self.channel_name
        )

    async def receive(self, text_data):
        json_text = json.loads(text_data)
        message = json_text.get("message")

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat_message",
                "message": message
            }
        )

    async def chat_message(self, event):
        data = {
            "id": str(event['data'].conversation.id),
            "sent_to": str(event['data'].sent_to.id)
        }
        await self.send(text_data=json.dumps(
            {
                "data": data
            }
            )
        )