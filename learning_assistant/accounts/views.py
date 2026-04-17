from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from .forms import EmailSignUpForm, EmailLoginForm

class CustomLoginView(LoginView):
    authentication_form = EmailLoginForm
    template_name = 'registration/login.html'

class SignUpView(CreateView):
    form_class = EmailSignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
