from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('', views.index),
    path('login/', views.login_page, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('chat/', views.chat, name='chat'),
    re_path(r'^ajax/validate_username/$', views.validate_username, name='validate_username'),
    # path('ajax/validate_username/', views.validate_username, name = "validate_username"),
]
