import datetime
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User

from .models import Message, GroupMember, ChatRoom
from django.db.models import Value, CharField, ExpressionWrapper, DateTimeField, F, TextField


class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self, data):
        messages = self.get_chat_history(data['chatId'])
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        return self.send_message(content)

    def new_message(self, data):
        author = data['from']
        author_user = User.objects.filter(username=author)[0]
        message = Message.objects.create(
            author=author_user,
            message=data['message'],
            chat_room=ChatRoom.objects.filter(id=data['chatId'])[0]
        )
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    def join_message(self, data):
        author = data['from']
        author_user = User.objects.filter(username=author)[0]
        Message.objects.create(
            author=author_user,
            message=f'{author} has joined the group',
            chat_room=ChatRoom.objects.filter(id=data['chatId'])[0],
            type="JOIN"
        )
        content = {
            'command': 'join_message',
            'message': {
                'message': f'{author} has joined the group',
            }
        }
        self.send_message(content)

    def leave_message(self, data):
        author = User.objects.filter(username=data['from'])[0]
        content = {
            'command': 'leave_message',
            'message': {
                'message': f'{author.username} has leaved the group',
            }
        }
        self.send_message(content)

    def messages_to_json(self, messages):
        return [self.message_to_json(message) for message in messages]

    def message_to_json(self, message):
        time = message.timestamp.strftime('%H:%M')
        return {
            'id': message.id,
            'author': message.author.username,
            'message': message.message,
            'timestamp': time,
            'type': message.get_type_display(),
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
        'join_message': join_message,
        'leave_message': leave_message,
    }

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_id"]

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

    def get_chat_history(self, chatId):
        return Message.objects.filter(chat_room__id=chatId).order_by('-timestamp')
