import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        nickname = text_data_json['nickname']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {'type': 'chat_message','message': message, 'nickname':nickname})

    def chat_message(self,event):
        message = event['message']
        nickname = event['nickname']

        self.send(text_data= json.dumps({
            "type" : 'chat',
            'message': message,
            'nickname': nickname,
        }))
