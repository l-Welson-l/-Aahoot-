from django.urls import path
from . import views
from .views import UserLogin, home, RegisterPage, UserLogout, CreateQuestion, QuestionView
urlpatterns = [
    path('', home.as_view(), name="home" ),
    path('login/',UserLogin.as_view(), name="login" ),
    path('register/',RegisterPage.as_view(), name="register"),
    path('logout/', UserLogout.as_view(), name="logout"),
    path('create-question/', CreateQuestion.as_view(), name="create_question"),
    path('question/<int:pk>/', QuestionView.as_view(), name="question"),
]
