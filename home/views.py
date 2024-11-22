from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from .models import Quiz, Answer, CorrectAnswer, UserAnswer

class home(ListView):
    template_name = 'home/home.html'
    model = Quiz
    context_object_name = 'home'

class UserLogin (LoginView):
    template_name = 'home/login.html'
    success_url = reverse_lazy('home')

class RegisterPage(FormView):
    template_name = 'home/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)
        return super().form_valid(form)

    

