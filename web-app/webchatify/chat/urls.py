from django.urls import path

from . import views

urlpatterns = [
    path('', views.ChatView.as_view(), name='chat'),
    path('create_group/', views.CreateGroupView.as_view(), name='create_group'),
    path("<int:room_id>/", views.RoomView.as_view(), name="room"),
    path("invite/<str:invite_link>", views.JoinChatRoomView.as_view(), name='invite'),
    path("get_invite_link/", views.GetInviteLinkView.as_view(), name='get_invite_link'),
    path("leave_chat_room/<int:room_id>/", views.LeaveChatRoomView.as_view(), name='leave_chat_room'),
]
