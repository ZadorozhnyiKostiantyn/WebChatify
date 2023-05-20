from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE
    )
    profile_photo = models.CharField(max_length=500)
    profile_number = models.CharField(max_length=15)
    color = models.CharField(max_length=50)


class GroupMember(models.Model):
    joined_datetime = models.DateTimeField()
    left_datetime = models.DateTimeField()
    users = models.ManyToManyField(to=User)


class Conversation(models.Model):
    conversation_name = models.CharField(max_length=100)


class Message(models.Model):
    from_user = models.CharField(max_length=100)
    send_datetime = models.TimeField()
    message = models.TextField()
    conversation = models.ForeignKey(
        to=Conversation,
        on_delete=models.CASCADE
    )

