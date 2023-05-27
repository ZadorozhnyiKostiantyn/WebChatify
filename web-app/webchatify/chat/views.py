import secrets

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from .forms import CreateNewGroupForm
from .models import ChatRoom, GroupMember


class ChatView(LoginRequiredMixin, View):
    login_url = 'login'
    template_name = 'chat/chat.html'
    form_class = CreateNewGroupForm

    def get(self, request):
        context = {
            'group': self.form_class(),
            'chat_rooms': self.get_all_chat_rooms_by_user(User.objects.get(id=request.user.id)),
            'user': request.user
        }
        return render(request, self.template_name, context)

    def get_all_chat_rooms_by_user(self, user):
        return ChatRoom.objects.filter(groupmember__user=user)


class CreateGroupView(LoginRequiredMixin, View):
    login_url = 'login'
    template_name = 'chat/chat.html'
    form_class = CreateNewGroupForm

    def post(self, request):
        group = self.form_class(request.POST, request.FILES)
        if group.is_valid():
            post = group.save(commit=False)
            post.owner = request.user
            post.invite_link = secrets.token_hex(6).upper()
            post.save()

            GroupMember.objects.create(
                user=User.objects.filter(id=request.user.id)[0],
                chat_room=ChatRoom.objects.filter(invite_link=post.invite_link)[0]
            )

            return redirect(reverse('chat'))

        return render(request, self.template_name, {'group': group})

    def get(self, request):
        group = self.form_class()
        return render(request, self.template_name, {'group': group})


class RoomView(LoginRequiredMixin, View):
    login_url = 'login'
    template_name = 'chat/room.html'
    form_class = CreateNewGroupForm

    def get(self, request, room_id):
        if not ChatRoom.objects.filter(id=room_id).exists():
            return render(request, 'chat/404.html')

        chat_room = ChatRoom.objects.get(id=room_id)
        user = User.objects.filter(id=request.user.id)[0]

        if not GroupMember.objects.filter(user=user, chat_room=chat_room).exists():
            return render(request, 'chat/404.html')

        context = {
            'group': self.form_class(),
            'chat_rooms': self.get_all_chat_rooms_by_user(User.objects.get(id=request.user.id)),
            'room': chat_room,
            'username': request.user.username,
        }
        return render(request, self.template_name, context)

    def get_all_chat_rooms_by_user(self, user):
        return ChatRoom.objects.filter(groupmember__user=user)


class GetInviteLinkView(View):
    def get(self, request):
        chat_id = request.GET.get('chatId', None)
        data = {
            'link': ChatRoom.objects.get(id=chat_id).invite_link
        }
        return JsonResponse(data)


class JoinChatRoomView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, invite_link):
        chat_room = ChatRoom.objects.get(invite_link=invite_link)
        user = User.objects.filter(id=request.user.id)[0]

        if not GroupMember.objects.filter(user=user, chat_room=chat_room).exists():
            GroupMember.objects.create(
                user=User.objects.filter(id=request.user.id)[0],
                chat_room=chat_room
            )

            channel_layer = get_channel_layer()

            async_to_sync(channel_layer.group_send)(
                f'chat_{chat_room.id}',
                {
                    'type': 'join_message',
                    'username': user.username,
                }
            )

        return redirect(reverse('room', kwargs={'room_id': chat_room.id}))
