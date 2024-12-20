from django import forms
from .models import Quiz, Question, Answer, UserAnswer


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'time_limit']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'is_correct']

class UserAnswerForm(forms.ModelForm):
    class Meta:
        model = UserAnswer
        fields = ['selected_answer']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['selected_answer'].queryset = Answer.objects.all()
        