from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.chat, name='chat'),
    path('create_group/', views.create_group, name='create_group'),
    path("<str:room_name>/<str:room_id>/", views.room, name="room"),
    path("invite/<str:invite_link>", views.join_chat_room, name='invite'),
    re_path(r'^get_invite_link/$', views.get_invite_link, name='get_invite_link'),
]
