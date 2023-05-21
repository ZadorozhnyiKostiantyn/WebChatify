from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .forms import CreateNewGroupForm
from django.contrib.auth.models import User
from .models import ChatRoom


@login_required(login_url='login')
def chat(request):
    print(request.user.id)
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
