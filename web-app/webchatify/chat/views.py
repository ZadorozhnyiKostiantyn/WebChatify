import secrets

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .forms import CreateNewGroupForm
from .models import (
    ChatRoom,
    GroupMember,
)


@login_required(login_url='login')
def chat(request):
    context = {
        'group': CreateNewGroupForm(),
        'chat_rooms': get_all_chat_rooms_by_user(User.objects.get(id=request.user.id)),
        'user': request.user
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
            post.invite_link = secrets.token_hex(6).upper()
            post.save()

            GroupMember.objects.create(
                user=User.objects.filter(id=request.user.id)[0],
                chat_room=ChatRoom.objects.filter(invite_link=post.invite_link)[0]
            )

            return redirect(to='chat')

    return render(
        request=request,
        template_name='chat/chat.html')


@login_required(login_url='login')
def room(request, room_name, room_id):
    if not ChatRoom.objects.filter(id=room_id).exists():
        return render(
            request=request,
            template_name='chat/404.html'
        )

    if not ChatRoom.objects.filter(name=room_name).exists():
        return render(
            request=request,
            template_name='chat/404.html'
        )

    chat_room = ChatRoom.objects.get(id=room_id)
    user = User.objects.filter(id=request.user.id)[0]

    if not GroupMember.objects.filter(user=user, chat_room=chat_room).exists():
        return render(
            request=request,
            template_name='chat/404.html')

    context = {
        'group': CreateNewGroupForm(),
        'chat_rooms': get_all_chat_rooms_by_user(User.objects.get(id=request.user.id)),
        'room': chat_room,
        'username': request.user.username,
    }
    return render(
        request=request,
        template_name="chat/room.html",
        context=context
    )


def get_invite_link(request):
    chatId = request.GET.get('chatId', None)
    data = {
        'link': ChatRoom.objects.get(id=chatId).invite_link
    }
    return JsonResponse(data)


@login_required(login_url='login')
def join_chat_room(request, invite_link):
    chat_room = ChatRoom.objects.get(invite_link=invite_link)
    user = User.objects.filter(id=request.user.id)[0]

    if not GroupMember.objects.filter(user=user, chat_room=chat_room).exists():
        GroupMember.objects.create(
            user=User.objects.filter(id=request.user.id)[0],
            chat_room=chat_room
        )

        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            f'chat_{chat_room.name}',
            {
                'type': 'join_message',
                'username': user.username,
            }
        )

    return redirect(
        to='room',
        room_name=chat_room.name,
        room_id=chat_room.id
    )


def get_all_chat_rooms_by_user(user):
    return ChatRoom.objects.filter(groupmember__user=user)
