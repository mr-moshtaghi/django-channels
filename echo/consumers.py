from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json


class EchoConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        if text_data:
            self.send(text_data=text_data + " - Sent By Server")
        elif bytes_data:
            self.send(bytes_data=bytes_data)


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['username']  # The user who sends the message
        self.group_name = f"chat_{self.user_id}"  # The channel group related to the user who sends the message

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )  # Add channel group that sends messages

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        if text_data:
            text_data_json = json.loads(text_data)
            username = text_data_json['receiver']  # The user who received the message
            user_group_name = f"chat_{username}"  # The channel group related to the user who received the message

            async_to_sync(self.channel_layer.group_send)(
                user_group_name,
                {
                    'type': 'chat_message',  # The function to be called
                    'message': text_data
                }
            )

    def chat_message(self, event):
        message = event['message']

        self.send(text_data=message)
