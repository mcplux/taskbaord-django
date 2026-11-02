from django.urls import path

from .views import HomePageView

app_name = "cms"

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
]
