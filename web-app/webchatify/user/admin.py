from django.contrib import admin
from .models import (
    Profile,
    GroupMember,
    Conversation,
    Message
)


admin.site.register(Profile)
admin.site.register(GroupMember)
admin.site.register(Conversation)
admin.site.register(Message)