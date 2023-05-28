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
from .models import ChatRoom, GroupMember, Message


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

            chat_room = ChatRoom.objects.filter(invite_link=post.invite_link)[0]

            GroupMember.objects.create(
                user=User.objects.filter(id=request.user.id)[0],
                chat_room=chat_room
            )

            message = Message.objects.create(
                author=request.user,
                message=f"'{chat_room.name}' was created",
                chat_room=chat_room,
                type="JOIN"
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
        try:
            chat_room = ChatRoom.objects.get(id=room_id)
            user = User.objects.get(id=request.user.id)

            if not GroupMember.objects.filter(user=user, chat_room=chat_room).exists():
                return render(request, 'chat/404.html')

            context = {
                'group': self.form_class(),
                'chat_rooms': self.get_all_chat_rooms_by_user(User.objects.get(id=request.user.id)),
                'room': chat_room,
                'username': request.user.username,
            }
            return render(request, self.template_name, context)
        except ChatRoom.DoesNotExist:
            return render(request, 'chat/404.html')

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
        try:
            chat_room = ChatRoom.objects.get(invite_link=invite_link)
            user = User.objects.get(id=request.user.id)

            if not GroupMember.objects.filter(user=user, chat_room=chat_room).exists():
                GroupMember.objects.create(
                    user=user,
                    chat_room=chat_room
                )

                channel_layer = get_channel_layer()

                async_to_sync(channel_layer.group_send)(
                    f'chat_{chat_room.id}',
                    {
                        'type': 'join_message',
                        'from': user.username,
                        'chatId': chat_room.id
                    }
                )

            return redirect(reverse('room', kwargs={'room_id': chat_room.id}))
        except ChatRoom.DoesNotExist:
            return redirect('chat')


class LeaveChatRoomView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, room_id):
        try:
            chat_room = ChatRoom.objects.get(id=room_id)
            user = User.objects.get(id=request.user.id)

            if GroupMember.objects.filter(user=user, chat_room=chat_room).exists():
                GroupMember.objects.get(user=user, chat_room=chat_room).delete()

                Message.objects.create(
                    author=user,
                    message=f'{user.username} has leaved the group',
                    chat_room=chat_room,
                    type="LEAVE"
                )

                channel_layer = get_channel_layer()

                async_to_sync(channel_layer.group_send)(
                    f'chat_{chat_room.id}',
                    {
                        'type': 'leave_message',
                        'from': user.username,
                        'chatId': chat_room.id
                    }
                )

                if GroupMember.objects.filter(chat_room=chat_room).count() == 0:
                    chat_room.delete_folder()
                    chat_room.delete()

            return redirect('chat')
        except ChatRoom.DoesNotExist:
            return redirect('chat')


class SearchChatsView(View):
    def get(self, request):
        query = request.GET.get('query', '')
        if query is None:
            chats = ChatRoom.objects.filter(groupmember__user=user)
            return JsonResponse({[{'name': chat.name, 'id': chat.id, 'photoUrl': chat.photo.url} for chat in chats]})

        chats = ChatRoom.objects.filter(name__icontains=query, groupmember__user_id=request.user.id)
        results = [{'name': chat.name, 'id': chat.id, 'photoUrl': chat.photo.url} for chat in chats]
        return JsonResponse({'results': results})


