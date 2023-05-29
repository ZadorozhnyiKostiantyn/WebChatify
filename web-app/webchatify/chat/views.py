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
    """
    Handles the chat view.

    Displays the chat page with the list of available chat rooms for the user.

    Requires the user to be logged in.

    Attributes:
    - login_url (str): The URL to redirect to if the user is not logged in.
    - template_name (str): The name of the template to render.
    - form_class (class): The form class for creating a new group.

    Methods:
    - get: Handles the GET request for the chat page.
    """
    login_url = 'login'
    template_name = 'chat/chat.html'
    form_class = CreateNewGroupForm

    def get(self, request):
        """
        Handles the GET request for the chat page.

        Renders the chat page template with the list of chat rooms and the create new group form.

        Parameters:
        - request: The HTTP request object.

        Returns:
        - A rendered chat page template.
        """
        context = {
            'group': self.form_class(),
            'chat_rooms': self.get_all_chat_rooms_by_user(User.objects.get(id=request.user.id)),
            'user': request.user
        }
        return render(request, self.template_name, context)

    def get_all_chat_rooms_by_user(self, user):
        """
        Retrieves all chat rooms associated with a user.

        Parameters:
        - user: The User object.

        Returns:
        - QuerySet: A queryset of ChatRoom objects.
        """
        return ChatRoom.objects.filter(groupmember__user=user)


class CreateGroupView(LoginRequiredMixin, View):
    """
    Handles the creation of a new group.

    Requires the user to be logged in.

    Attributes:
    - login_url (str): The URL to redirect to if the user is not logged in.
    - template_name (str): The name of the template to render.
    - form_class (class): The form class for creating a new group.

    Methods:
    - get: Handles the GET request for creating a new group.
    - post: Handles the POST request for creating a new group.
    """
    login_url = 'login'
    template_name = 'chat/chat.html'
    form_class = CreateNewGroupForm

    def post(self, request):
        """
        Handles the POST request for creating a new group.

        Creates a new group based on the submitted form data, adds the current user as a group member,
        and redirects to the chat page.

        Parameters:
        - request: The HTTP request object.

        Returns:
        - A redirect response to the chat page.
        """
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


class RoomView(LoginRequiredMixin, View):
    """
    Handles the room view.

    Displays the chat room page with the messages and group details.

    Requires the user to be logged in.

    Attributes:
    - login_url (str): The URL to redirect to if the user is not logged in.
    - template_name (str): The name of the template to render.
    - form_class (class): The form class for creating a new group.

    Methods:
    - get: Handles the GET request for the chat room page.
    """

    login_url = 'login'
    template_name = 'chat/room.html'
    form_class = CreateNewGroupForm

    def get(self, request, room_id):
        """
        Handles the GET request for the chat room page.

        Renders the chat room page template with the chat room details and messages.

        Parameters:
        - request: The HTTP request object.
        - room_id (int): The ID of the chat room.

        Returns:
        - A rendered chat room page template.
        """
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
        """
        Retrieves all chat rooms associated with a user.

        Parameters:
        - user: The User object.

        Returns:
        - QuerySet: A queryset of ChatRoom objects.
        """
        return ChatRoom.objects.filter(groupmember__user=user)


class GetInviteLinkView(View):
    """
    Handles the retrieval of an invite link for a chat room.

    Methods:
    - get: Handles the GET request for retrieving the invite link.
    """
    def get(self, request):
        """
        Handles the GET request for retrieving the invite link.

        Retrieves the invite link for the specified chat room ID.

        Parameters:
        - request: The HTTP request object.

        Returns:
        - A JSON response containing the invite link.
        """
        chat_id = request.GET.get('chatId', None)
        data = {
            'link': ChatRoom.objects.get(id=chat_id).invite_link
        }
        return JsonResponse(data)


class JoinChatRoomView(LoginRequiredMixin, View):
    """
    Handles joining a chat room.

    Requires the user to be logged in.

    Attributes:
    - login_url (str): The URL to redirect to if the user is not logged in.

    Methods:
    - get: Handles the GET request for joining a chat room.
    """

    login_url = 'login'
    def get(self, request, invite_link):
        """
        Handles the GET request for joining a chat room.

        Joins the specified chat room by adding the current user as a group member
        and sends a join message to the chat room's channel.

        Parameters:
        - request: The HTTP request object.
        - invite_link (str): The invite link of the chat room.

        Returns:
        - A redirect response to the chat room page.
        """
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
    """
    Handles leaving a chat room.

    Requires the user to be logged in.

    Attributes:
    - login_url (str): The URL to redirect to if the user is not logged in.

    Methods:
    - get: Handles the GET request for leaving a chat room.
    """
    login_url = 'login'

    def get(self, request, room_id):
        """
        Handles the GET request for leaving a chat room.

        Leaves the specified chat room by removing the current user as a group member,
        sends a leave message to the chat room's channel, and deletes the chat room if no
        other group members are present.

        Parameters:
        - request: The HTTP request object.
        - room_id (int): The ID of the chat room.

        Returns:
        - A redirect response to the chat page.
        """
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
    """
    Handles the search for chat rooms.

    Methods:
    - get: Handles the GET request for searching chat rooms.
    """
    def get(self, request):
        """
        Handles the GET request for searching chat rooms.

        Searches for chat rooms based on the provided query parameter.

        Parameters:
        - request: The HTTP request object.

        Returns:
        - A JSON response containing the search results.
        """
        query = request.GET.get('query', '')
        if query is None:
            chats = ChatRoom.objects.filter(groupmember__user=user)
            return JsonResponse({[{'name': chat.name, 'id': chat.id, 'photoUrl': chat.photo.url} for chat in chats]})

        chats = ChatRoom.objects.filter(name__icontains=query, groupmember__user_id=request.user.id)
        results = [{'name': chat.name, 'id': chat.id, 'photoUrl': chat.photo.url} for chat in chats]
        return JsonResponse({'results': results})
