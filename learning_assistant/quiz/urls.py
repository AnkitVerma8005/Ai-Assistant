from django.urls import path
from . import views

urlpatterns = [
    path("", views.quiz_home, name="quiz_home"),
    path("api/generate/", views.generate_quiz, name="generate_quiz"),
]
