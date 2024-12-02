from django.db import models 
from django.contrib.auth.models import User



class Quiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quizzes")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.quiz.title} - {self.text}"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    def __str__ (self):
        return self.text

class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ("user", "question")
    def __str__(self):
        return f"{self.user.username} - {self.question.text} - {self.selected_answer.text}"



    