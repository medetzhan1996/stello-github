import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class FigmaConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['id']
        self.author_id = self.scope['url_route']['kwargs']['author_id']
        self.client_auth = self.scope["session"]["client_auth"]
        self.room_group_name = 'shop_%s' % self.id
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
        text_data_json = json.loads(text_data)
        product = text_data_json['product']
        preview_text = text_data_json['preview_text']
        product_material = text_data_json['product_material']
        phone_number = text_data_json['phone_number']
        image_src = text_data_json['image_src']

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
                'client_auth': self.client_auth,
                'image_src': image_src
            }
        )

    # receive message from room group
    def chat_message(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps(event))
