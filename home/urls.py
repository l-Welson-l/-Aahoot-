from django.urls import path
from . import views
from .views import UserLogin, home, RegisterPage, UserLogout, CreateQuiz, QuizView, QuizDelete
urlpatterns = [
    path('', home.as_view(), name="home" ),
    path('login/',UserLogin.as_view(), name="login" ),
    path('register/',RegisterPage.as_view(), name="register"),
    path('logout/', UserLogout.as_view(), name="logout"),
    path('create-question/', CreateQuiz.as_view(), name="create_quiz"),
    path('question/<int:pk>/', QuizView.as_view(), name="quiz"),
    path('delete-quiz/<int:pk>/', QuizDelete.as_view(), name="delete_quiz")
]
