from django.urls import path, include
from .views import SignUpView, CustomLoginView

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("", include("django.contrib.auth.urls")),
]
