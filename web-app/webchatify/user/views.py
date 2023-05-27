from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from .forms import CreateUserForm
from chat.models import Profile
import random


class IndexView(View):
    def get(self, request):
        return redirect(reverse_lazy('login'))


class LoginPageView(View):
    template_name = 'user/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('chat')
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request=request, username=username, password=password)

        if user is not None:
            login(request=request, user=user)
            profile = Profile.objects.get(user__id=request.user.id)
            profile.color_session = "#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
            profile.save()
            return redirect('chat')
        else:
            messages.info(request=request, message='Username or password is incorrect')

        return render(request, self.template_name)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


class RegisterView(FormView):
    template_name = 'user/register.html'
    form_class = CreateUserForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        Profile.create(
            user=User.objects.get(username=form.username),
        )
        messages.success(request=self.request, message='Account created successfully')
        return super().form_valid(form)


class ValidateUsernameView(View):
    def get(self, request):
        username = request.GET.get('username', None)
        data = {'is_taken': User.objects.filter(username=username).exists()}
        return JsonResponse(data)
