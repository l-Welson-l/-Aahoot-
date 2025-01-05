from django.urls import path
from . import views
from .views import UserLogin, logged_out, Home, RegisterPage, UserLogout, CreateQuiz, QuizView, QuizDelete, QuestionCreate, QuestionDelete, QuizUpdate, AnswerCreate, QuizPlayView, QuizResultView, QuizParticipantResultsView, dashboard
urlpatterns = [
    path('', Home.as_view(), name="home" ),
    path('login/',UserLogin.as_view(), name="login" ),
    path('register/',RegisterPage.as_view(), name="register"),
    path('logout/', UserLogout.as_view(), name="logout"),
    path('create-quiz/', CreateQuiz.as_view(), name="create_quiz"),
    path('quiz/<int:pk>/', QuizView.as_view(), name="quiz"),
    path('delete-quiz/<int:pk>/', QuizDelete.as_view(), name="delete_quiz"),
    path('quiz/<int:quiz_id>/create-question', QuestionCreate.as_view(), name="create_question"),
    path('delete-question/<int:pk>/', QuestionDelete.as_view(), name="delete_question"),
    path('quiz-update/<int:pk>/', QuizUpdate.as_view(), name="update_quiz"),
    path('<int:pk>/answer-create/', AnswerCreate.as_view(), name="create_answer"),
    path('quiz/<int:pk>/play/', QuizPlayView.as_view(), name='quiz_play'),
    path('quiz/<int:quiz_id>/result/', QuizResultView.as_view(), name="quiz_results"),
    path('quiz/<int:pk>/participant-results/', QuizParticipantResultsView.as_view(), name='quiz_participant_result'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logged_out/', views.logged_out, name='logged_out'),

]
