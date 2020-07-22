import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class FigmaOrderConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.author_id = self.scope['url_route']['kwargs']['author']
        self.client_auth = self.scope["session"]["client_auth"]
        self.room_group_name = 'order_%s' % self.author_id
        # join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        # accept connection
        self.accept()

    def disconnect(self, close_code):
        # leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # receive message from WebSocket
    def receive(self, text_data):
        data_json = json.loads(text_data)
        product = data_json['product']
        preview_text = data_json['preview_text']
        product_material = data_json['product_material']
        phone_number = data_json['phone_number']

        # send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'preview_text': preview_text,
                'product': product,
                'product_material': product_material,
                'phone_number': phone_number,
                'user': self.user.id,
                'client_auth': self.client_auth
            }
        )

    # receive message from room group
    def chat_message(self, event):
        self.send(text_data=json.dumps(event))
