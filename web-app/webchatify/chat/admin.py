from django.contrib import admin
from .models import (
    Profile,
    GroupMember,
    ChatRoom,
    Message
)


admin.site.register(Profile)
admin.site.register(GroupMember)
admin.site.register(ChatRoom)
admin.site.register(Message)