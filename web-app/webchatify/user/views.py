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
        """
        Handles the GET request for the login page.

        If the user is already authenticated, redirects to the chat page.
        Otherwise, renders the login page template.

        Parameters:
        - request: The HTTP request object.

        Returns:
        - If the user is already authenticated, a redirect response to the chat page.
        - Otherwise, a rendered login page template.
        """
        if request.user.is_authenticated:
            return redirect('chat')
        return render(request, self.template_name)

    def post(self, request):
        """
        Handles the POST request for the login page.

        Authenticates the user based on the provided username and password.
        If the user is authenticated, logs them in, generates a random color for the user's profile session,
        and redirects to the chat page.
        If the authentication fails, displays an error message.

        Parameters:
        - request: The HTTP request object.

        Returns:
        - If the authentication is successful, a redirect response to the chat page.
        - Otherwise, a rendered login page template with an error message.
        """
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request=request, username=username, password=password)

        if user is not None:
            login(request=request, user=user)
            profile = Profile.objects.get(user__id=request.user.id)
            profile.color_session = self.generate_light_color_hex()
            profile.save()
            return redirect('chat')
        else:
            messages.info(request=request, message='Username or password is incorrect')

        return render(request, self.template_name)

    def generate_light_color_hex(self):
        """
        Generates a random hexadecimal color code in a light color range.

        Returns:
        - A string representing a hexadecimal color code.
        """
        r = random.randint(120, 255)
        g = random.randint(120, 255)
        b = random.randint(120, 255)
        return "#{:02x}{:02x}{:02x}".format(r, g, b)


class LogoutView(View):
    def get(self, request):
        """
        Handles the GET request for logging out.

        Logs out the user and redirects to the login page.

        Parameters:
        - request: The HTTP request object.

        Returns:
        - A redirect response to the login page.
        """
        logout(request)
        return redirect('login')


class RegisterView(FormView):
    template_name = 'user/register.html'
    form_class = CreateUserForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        """
        Handles the form submission for user registration.

        Creates a new user based on the submitted form data, creates a profile for the user,
        displays a success message, and redirects to the login page.

        Parameters:
        - form: The form instance containing the submitted data.

        Returns:
        - A redirect response to the login page.
        """
        form.save()
        Profile.objects.create(
            user=User.objects.get(username=form.cleaned_data['username']),
        )
        messages.success(request=self.request, message='Account created successfully')
        return super().form_valid(form)


class ValidateUsernameView(View):
    def get(self, request):
        """
        Handles the GET request to validate a username.

        Checks if the given username already exists and returns a JSON response indicating whether it is taken.

        Parameters:
        - request: The HTTP request object.

        Returns:
        - A JSON response containing the 'is_taken' field indicating if the username is taken.
        """
        username = request.GET.get('username', None)
        data = {'is_taken': User.objects.filter(username=username).exists()}
        return JsonResponse(data)
