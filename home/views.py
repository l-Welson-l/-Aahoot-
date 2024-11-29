from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView, UpdateView, CreateView, DeleteView
from django.views.generic import View 
from django.urls import reverse_lazy
from .models import Quiz, Answer, CorrectAnswer, UserAnswer

class home(ListView):
    template_name = 'home/home.html'
    model = Quiz
    context_object_name = 'home'

class UserLogin (LoginView):
    template_name = 'home/login.html'
    def get_success_url(self):
        return reverse_lazy('home')


class RegisterPage(FormView):
    template_name = 'home/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)
        return super().form_valid(form)

class UserLogout(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')

class CreateQuestion(CreateView):
    model = Quiz
    template_name = 'home/question_create.html'
    fields = ['question']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
