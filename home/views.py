from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.generic.edit import FormView, UpdateView, CreateView, DeleteView
from django.views.generic import DetailView, View, TemplateView
from django.urls import reverse_lazy, reverse
from .models import Quiz, Answer, UserAnswer, Question, Message
from .forms import QuizForm, QuestionForm, AnswerForm
from django.forms import modelformset_factory
from django.db.models import Q

@login_required
def inbox(request):
    user = request.user
    messages = Message.objects.filter(Q(sender=user) | Q(receiver=user))
    contacts = {}
    for msg in messages:
        contact = msg.receiver if msg.sender == user else msg.sender
        if contact not in contacts or msg.timestamp > contacts[contact].timestamp:
            contacts[contact] = msg
    contacts = sorted(contacts.items(), key=lambda x: x[1].timestamp, reverse=True)

    return render(request, 'home/inbox.html', {'contacts': contacts})


@login_required
def chat_view(request, username):
    user = request.user
    other_user = get_object_or_404(User, username=username)

   
    messages = Message.objects.filter(Q(sender=user) | Q(receiver=user))

   
    contacts = {}
    for msg in messages:
        contact = msg.receiver if msg.sender == user else msg.sender
        if contact not in contacts or msg.timestamp > contacts[contact].timestamp:
            contacts[contact] = msg
    contacts = sorted(contacts.items(), key=lambda x: x[1].timestamp, reverse=True)

   
    conversation = messages.filter(
        Q(sender=user, receiver=other_user) |
        Q(sender=other_user, receiver=user)
    ).order_by('timestamp')

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=user, receiver=other_user, content=content)
            return redirect('chat', username=username)

    return render(request, 'home/chat.html', {
        'other_user': other_user,
        'messages': conversation,
        'contacts': contacts, 
    })



@login_required
def start_conversation(request, username):
    recipient = get_object_or_404(User, username=username)
    return redirect('chat', username=recipient.username)
    




def logged_out(request):
    if request.user.is_authenticated:
        return redirect('home')  
    return render(request, 'home/logged_out.html')

def user_search(request):
    query = request.GET.get('q', '')
    users = User.objects.filter(username__icontains=query) if query else []
    return render(request, 'home/user_search.html', {'users': users, 'query': query})

def user_profile(request, username):
    user = User.objects.get(username=username)
    quizzes = Quiz.objects.filter(user=user)
    return render(request, 'home/user_profile.html', {'profile_user': user, 'quizzes': quizzes})

class Home(ListView):
    template_name = 'home/home.html'
    model = Quiz
    context_object_name = 'home'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('logged_out')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('q', '')
        
        created_quizzes = Quiz.objects.filter(user=self.request.user, title__icontains=search_query)
        all_quizzes = Quiz.objects.filter(title__icontains=search_query)

        context['created_quizzes'] = created_quizzes
        context['home'] = all_quizzes 
        context['search_query'] = search_query

        return context


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

@login_required
def dashboard(request):
    user = request.user
    created_quizzes = Quiz.objects.filter(user=user)
    played_quizzes = Quiz.objects.filter(questions__answers__user=user).distinct()

    return render(request, 'home/dashboard.html', {
        'created_quizzes': created_quizzes,
        'played_quizzes': played_quizzes,
    })



class QuizView(DetailView):
    model = Quiz
    template_name = 'home/quiz_detail.html'
    context_object_name = 'quiz'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz = self.get_object()
        user = self.request.user

        context['questions'] = quiz.questions.all()

        if user.is_authenticated:
            user_answers = UserAnswer.objects.filter(user=user, question__quiz=quiz)
            context['answered_all'] = user_answers.count() == quiz.questions.count()
        else:
            context['answered_all'] = False

        return context

    def post(self, request, *args, **kwargs):
        quiz = self.get_object()
        user = self.request.user

        answers = request.POST
        for question_id, selected_answer_id in answers.items():
            if question_id.startswith('answer_'):
                question = Question.objects.get(id=question_id.split('_')[1])
                selected_answer = Answer.objects.get(id=selected_answer_id)

                UserAnswer.objects.update_or_create(
                    user=user,
                    question=question,
                    defaults={'selected_answer': selected_answer}
                )

        quiz.participants.add(user)

        return redirect('quiz_results', quiz.id)





class QuizDelete(DeleteView):
    model = Quiz
    template_name = 'home/quiz_delete.html'
    success_url = reverse_lazy('home')
    def get_queryset(self):
        return Quiz.objects.filter(user=self.request.user)

class QuestionCreate(CreateView):
    template_name = 'home/question_create.html'
    QuestionForm = QuestionForm
    AnswerFormSet = modelformset_factory(Answer, fields=('text', 'is_correct'), extra=3)  

    def get(self, request, *args, **kwargs):
        quiz_id = kwargs['quiz_id']
        quiz = get_object_or_404(Quiz, id=quiz_id)
        question_form = self.QuestionForm()
        answer_formset = self.AnswerFormSet(queryset=Answer.objects.none())
        return render(request, self.template_name, {
            'quiz': quiz,
            'question_form': question_form,
            'answer_formset': answer_formset,
        })

    def post(self, request, *args, **kwargs):
        quiz_id = kwargs['quiz_id']
        quiz = get_object_or_404(Quiz, id=quiz_id)
        question_form = self.QuestionForm(request.POST)
        answer_formset = self.AnswerFormSet(request.POST)

        if question_form.is_valid() and answer_formset.is_valid():
            question = question_form.save(commit=False)
            question.quiz = quiz
            question.save()

            for form in answer_formset:
                if form.cleaned_data: 
                    answer = form.save(commit=False)
                    answer.question = question
                    answer.save()

            return redirect(reverse('quiz', kwargs={'pk': quiz.id}))

        return render(request, self.template_name, {
            'quiz': quiz,
            'question_form': question_form,
            'answer_formset': answer_formset,
        })


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
    
class QuizPlayView(DetailView):
    model = Quiz
    template_name = 'home/quiz_play.html'
    context_object_name = 'quiz'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz = context['quiz']
        user = self.request.user

        context['questions'] = quiz.questions.all()

        user_answers = UserAnswer.objects.filter(user=user, question__quiz=quiz)
        context['answered_all'] = user_answers.count() == quiz.questions.count()

        return context

    def post(self, request, *args, **kwargs):
        quiz = self.get_object()
        user = request.user
        answers = request.POST

        for question_id, selected_answer_id in answers.items():
            if question_id.startswith('question_'):
                question = Question.objects.get(id=question_id.split('_')[1])
                selected_answer = Answer.objects.get(id=selected_answer_id)

                UserAnswer.objects.update_or_create(
                    user=user,
                    question=question,
                    defaults={'selected_answer': selected_answer}
                )

        return redirect('quiz_results', quiz.id)




class QuizResultView(TemplateView):
    template_name = 'home/quiz_results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz_id = kwargs['quiz_id']
        user = self.request.user

        quiz = Quiz.objects.get(id=quiz_id)
        user_answers = UserAnswer.objects.filter(user=user, question__quiz=quiz)

        results = []
        for user_answer in user_answers:
            question = user_answer.question
            selected_answer = user_answer.selected_answer
            correct_answer = question.answers.filter(is_correct=True).first()
            
            results.append({
                'question': question,
                'selected_answer': selected_answer,
                'correct_answer': correct_answer,
                'is_correct': selected_answer == correct_answer
            })

        context['quiz'] = quiz
        context['results'] = results
        context['score'] = user_answers.filter(selected_answer__is_correct=True).count()
        context['total_questions'] = quiz.questions.count()

        return context




class QuizParticipantResultsView(DetailView):
    model = Quiz
    template_name = 'home/quiz_participant_results.html'
    context_object_name = 'quiz'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz = self.get_object()

        if self.request.user != quiz.user:
            raise PermissionDenied("You are not authorized to view this page.")

        user_answers = UserAnswer.objects.filter(question__quiz=quiz)
        participants = User.objects.filter(
            useranswer__question__quiz=quiz
        ).distinct()

        participants_data = []
        for participant in participants:
            user_answers_for_quiz = user_answers.filter(user=participant)
            correct_answers = user_answers_for_quiz.filter(selected_answer__is_correct=True).count()
            total_questions = quiz.questions.count()

            participants_data.append({
                'participant': participant,
                'score': f"{correct_answers}/{total_questions}",
                'answers': user_answers_for_quiz
            })

        context['participants_data'] = participants_data
        return context

