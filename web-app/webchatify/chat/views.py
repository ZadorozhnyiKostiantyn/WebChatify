import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
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
    group = CreateNewGroupForm()
    chat_rooms = ChatRoom.objects.filter(owner__id=request.user.id)

    context = {
        'group': group,
        'chat_rooms': chat_rooms,
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


def get_chat_room_by_id(request):
    if request.method == 'GET':
        chatId = request.GET.get('chatId', None)
        chat_room = ChatRoom.objects.get(id=chatId)
        messages = Message.objects \
            .filter(chat_room__id=chatId) \
            .order_by('send_datetime') \
            .values()  # Отримуємо QuerySet як список словників

        if not messages:  # Замість порівняння з None використовуйте "not messages"
            messages = []

        data = {
            'room_name': chat_room.name,
            'room_icon': chat_room.photo.url,
            'messages': messages  # Передаємо список повідомлень
        }

        return JsonResponse(data)

    data = {
        'chat': 'None'
    }

    return JsonResponse(data)


def save_massage_to_log(chat_room, message_text):
    message = Message(
        chat_room=chat_room,
        send_datetime=timezone.now(),
        message=message_text
    )
    message.save()


def get_massages_to_log(chat_room, message_text):
    message = Message(
        chat_room=chat_room,
        send_datetime=timezone.now(),
        message=message_text
    )
    message.save()


@login_required(login_url='login')
def index(request):
    group = CreateNewGroupForm()
    chat_rooms = ChatRoom.objects.filter(owner__id=request.user.id)

    context = {
        'group': group,
        'chat_rooms': chat_rooms,
    }
    return render(
        request=request,
        template_name='chat/index.html',
        context=context,
    )


@login_required(login_url='login')
def room(request, room_name):
    context = {
        'group': CreateNewGroupForm(),
        'chat_rooms': ChatRoom.objects.filter(owner__id=request.user.id),
        "room_name": mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.username)),
    }
    return render(
        request=request,
        template_name="chat/room1.html",
        context=context
    )

def get_last_10_messages():
    return Message.objects.order_by('-timestamp').all()[:10]
