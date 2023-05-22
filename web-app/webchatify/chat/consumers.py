import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message, ChatRoom
from django.contrib.auth.models import User
from .views import get_last_10_messages
import datetime
from django.utils.timezone import utc


class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self, data):
        messages = get_last_10_messages()
        content = {
            'messages': self.messages_to_json(messages)
        }
        return self.send_message(content)


    def new_message(self, data):
        author = data['from']
        print(author)
        author_user = User.objects.filter(username=author)[0]
        print(author_user.username)
        message = Message.objects.create(
            author=author_user,
            message=data['message'],
            chat_room=ChatRoom.objects.filter(name=data['chat_room'])[0]
        )
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result
        # return [self.message_to_json(message) for message in messages]

    def message_to_json(self, message):
        time = datetime.datetime.strptime(str(message.timestamp), '%Y-%m-%d %H:%M:%S.%f').time()
        return {
            'author': message.author.username,
            'message': message.message,
            'timestamp': str(time)[:5]
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
    }

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))