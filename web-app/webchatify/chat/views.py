import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.forms.models import model_to_dict
from django.core import serializers
from django.utils import timezone
from django.utils.safestring import mark_safe
from .forms import CreateNewGroupForm
from .models import (
    ChatRoom,
    Message,
)


@login_required(login_url='login')
def chat(request):
    context = {
        'group': CreateNewGroupForm(),
        'chat_rooms': ChatRoom.objects.filter(owner__id=request.user.id),
    }
    return render(
        request=request,
        template_name='chat/chat.html',
        context=context
    )


def create_group(request):
    group = CreateNewGroupForm()
    if request.method == 'POST':

        group = CreateNewGroupForm(
            request.POST,
            request.FILES,
        )
        if group.is_valid():
            post = group.save(commit=False)
            post.owner = request.user
            post.save()
            return redirect(to='chat')

    return render(
        request=request,
        template_name='chat/chat.html')


@login_required(login_url='login')
def room(request, room_name, room_id):
    context = {
        'group': CreateNewGroupForm(),
        'chat_rooms': ChatRoom.objects.filter(owner__id=request.user.id),
        'room': ChatRoom.objects.get(id=room_id),
        'username': request.user.username,
    }
    return render(
        request=request,
        template_name="chat/room.html",
        context=context
    )


# def get_last_10_messages(chatId):
#     messages =  Message.objects.filter(chat_room__id=chatId)
#     return messages.filter(chat_room__id=chatId).order_by('-timestamp').all()[:10]

def get_all_messages(chatId):
    messages =  Message.objects.filter(chat_room__id=chatId)
    return messages.filter(chat_room__id=chatId).order_by('-timestamp').all()
