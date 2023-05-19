from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User

from django.contrib.auth import (
    authenticate,
    login,
    logout
)

from django.contrib.auth.decorators import login_required


def index(request):
    return redirect(to='login')

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request=request,
            username=username,
            password=password
        )

        if user is not None:
            login(
                request=request,
                user=user
            )
            return redirect('chat')
        else:
            messages.info(
                request=request,
                message='Username or password is incorrect'
            )

    return render(
        request=request,
        template_name='user/login.html',
    )


def logout_user(request):
    logout(request)
    return redirect('login')


def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request=request, message='Account created successfully')
            return redirect('login')
    context = {'form': form}
    return render(
        request=request,
        template_name='user/register.html',
        context=context
    )


# @csrf_exempt
def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username=username).exists()
    }
    return JsonResponse(data)


@login_required(login_url='login')
def chat(request):
    return render(
        request=request,
        template_name='user/chat.html'
    )
