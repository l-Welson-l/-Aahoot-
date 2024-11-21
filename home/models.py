from django.db import models 
from django.contrib.auth.models import User


class Quiz(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    question = models.CharField(max_length=200)
    def __str__ (self):
        return self.question

class Answer(models.Model):
    answer = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    def __str__ (self):
        return self.text
    
class CorrectAnswer(models.Model):
    correct_answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    unique_correct_answer = models.UniqueConstraint(fields = ["correct_answer", "quiz"], name="unique_correct_answer")
    def __str__ (self):
        return self.correct_answer.text

class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    unique_user_answer = models.UniqueConstraint(fields = ["user", "quiz", "answer"], name="unique_user_answer")
    created_at = models.DateTimeField(auto_now_add = True)
    def __str__ (self):
        return self.user.username



    