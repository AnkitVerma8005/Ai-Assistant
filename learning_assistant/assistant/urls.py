from django.urls import path
from . import views

urlpatterns = [
    path("", views.assistant_home, name="assistant_home"),
    path("api/chat/", views.chat_api, name="chat_api"),
]
