from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .models import Quiz, Answer, CorrectAnswer, UserAnswer

class home(ListView):
    template_name = 'home/home.html'
    model = Quiz
    context_object_name = 'home'

class UserLogin (LoginView):
    template_name = 'home/login.html'
    def get_sucess_url(self):
        return reverse_lazy('home')

# class RegisterPage():
#     template_name = 'home/register.html'

