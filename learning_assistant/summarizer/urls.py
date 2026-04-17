from django.urls import path
from . import views

urlpatterns = [
    path("", views.summarizer_home, name="summarizer_home"),
    path("api/generate/", views.generate_summary, name="generate_summary"),
]
