from django.urls import path

from apps.accounts.views.auth import LoginView, RegisterView

app_name = "auth"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
]
