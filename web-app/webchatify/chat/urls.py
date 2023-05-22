from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    # path('', views.chat, name='chat'),
    path('', views.index, name='chat'),
    path('create_group/', views.create_group, name='create_group'),
    path("<str:room_name>/", views.room, name="room"),
    re_path(r'^ajax/get_chat_room_by_id/$', views.get_chat_room_by_id, name='get_chat_room_by_id'),
]

