from django.db import models
from django.contrib.auth.models import User


def get_upload_chat_path(instance, filename):
    return f'{instance.owner.username}/group/{instance.name}/icon/{filename}'



def get_upload_profile_path(instance, filename):
    return f'{instance.user.username}/profile/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE
    )
    profile_photo = models.ImageField(null=True, upload_to=get_upload_profile_path)
    profile_number = models.CharField(max_length=15)
    color = models.CharField(max_length=50)


class ChatRoom(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    photo = models.ImageField(null=True, upload_to=get_upload_chat_path)


class GroupMember(models.Model):
    joined_datetime = models.DateTimeField()
    left_datetime = models.DateTimeField()
    users = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE
    )
    chat_room = models.ForeignKey(
        to=ChatRoom,
        on_delete=models.CASCADE
    )


class Message(models.Model):
    from_user = models.CharField(max_length=100)
    send_datetime = models.TimeField()
    message = models.TextField()
    chat_room = models.ForeignKey(
        to=ChatRoom,
        on_delete=models.CASCADE
    )
