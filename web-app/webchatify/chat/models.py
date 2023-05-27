import datetime
import shutil
import os

from django.contrib.auth.models import User
from django.db import models
from model_utils import Choices
from webchatify import settings


def get_upload_chat_path(instance, filename):
    return f'{instance.owner.username}/group/{instance.invite_link}/icon/{filename}'


def get_upload_profile_path(instance, filename):
    return f'{instance.user.username}/profile/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE
    )
    photo = models.ImageField(null=True, upload_to=get_upload_profile_path)
    number = models.CharField(max_length=15)
    color_session = models.CharField(max_length=50)


class ChatRoom(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    invite_link = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    photo = models.ImageField(null=True, blank=True, upload_to=get_upload_chat_path)

    def delete_folder(self):
        if self.photo:
            shutil.rmtree(os.path.join(settings.MEDIA_ROOT, f'{self.owner.username}/group/{self.invite_link}'))


class GroupMember(models.Model):
    joined_datetime = models.DateTimeField(default=datetime.datetime.now)
    left_datetime = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE
    )
    chat_room = models.ForeignKey(
        to=ChatRoom,
        on_delete=models.CASCADE
    )


class Message(models.Model):
    MESSAGE = "MESSAGE"
    JOIN = "JOIN"
    LEAVE = "LEAVE"
    TYPE = Choices(
        (MESSAGE, "message"),
        (JOIN, "join"),
        (LEAVE, "leave"),
    )

    author = models.ForeignKey(
        to=User,
        related_name='author_message',
        on_delete=models.CASCADE,
    )
    timestamp = models.DateTimeField(default=datetime.datetime.now)
    message = models.TextField()
    chat_room = models.ForeignKey(
        to=ChatRoom,
        on_delete=models.CASCADE
    )
    type = models.CharField(
        max_length=10,
        choices=TYPE,
        default=MESSAGE
    )

    def __str__(self):
        return self.author.username
