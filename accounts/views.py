from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import CustomUser
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .forms import UserProfileForm, LoginForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'login.html'
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')
