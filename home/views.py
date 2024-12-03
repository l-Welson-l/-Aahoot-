from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView, UpdateView, CreateView, DeleteView
from django.views.generic import DetailView
from django.views.generic import View 
from django.urls import reverse_lazy, reverse
from .models import Quiz, Answer, UserAnswer, Question
from .forms import QuizForm, QuestionForm, AnswerForm

class home(ListView):
    template_name = 'home/home.html'
    model = Quiz
    context_object_name = 'home'

class UserLogin (LoginView):
    template_name = 'home/login.html'
    def get_success_url(self):
        next_url = self.request.GET.get('next', reverse_lazy('home'))
        return next_url

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


class CreateQuiz(CreateView):
    model = Quiz
    template_name = 'home/quiz_create.html'
    form_class = QuizForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            return super().form_valid(form)
        else:
            return redirect('login')

class QuizView(DetailView):
    model = Quiz
    template_name = 'home/quiz_detail.html'
    context_object_name = 'quiz'

class QuizDelete(DeleteView):
    model = Quiz
    template_name = 'home/quiz_delete.html'
    success_url = reverse_lazy('home')
    def get_queryset(self):
        return Quiz.objects.filter(user=self.request.user)

class QuestionCreate(CreateView):
    model = Question
    template_name = 'home/question_create.html'
    form_class = QuestionForm
    def form_valid(self, form):
        form.instance.quiz_id = self.kwargs['quiz_id']
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('quiz', kwargs={'pk': self.kwargs['quiz_id']})

class QuestionDelete(DeleteView):
    model = Question
    def get_success_url(self):
        question = self.get_object()
        return reverse('quiz', kwargs={'pk': question.quiz.id})

class QuizUpdate(UpdateView):
    model = Quiz
    template_name = 'home/quiz_update.html'
    form_class = QuizForm
    def get_success_url(self):
        quiz = self.get_object()
        return reverse('quiz', kwargs={'pk': quiz.id})

class AnswerCreate(CreateView):
    model = Answer
    template_name = 'home/answer_create.html'
    form_class = AnswerForm
    def form_valid(self, form):
        question = get_object_or_404(Question, pk=self.kwargs['pk'])
        form.instance.question = question
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('quiz', kwargs={'pk': self.object.question.quiz.id})