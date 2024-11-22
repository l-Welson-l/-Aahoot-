from django.urls import path
from . import views
from .views import UserLogin, home
urlpatterns = [
    path('', home.as_view(), name="home" ),
    path('login/',UserLogin.as_view(), name="login" ),

]
