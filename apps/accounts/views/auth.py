from django.conf import settings
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import resolve_url
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView

from apps.accounts.forms import LoginForm, RegisterForm
from apps.accounts.models import User
from apps.core.mixins import AnonymousRequiredMixin, HtmxMixin


class RegisterView(
    HtmxMixin,
    AnonymousRequiredMixin,
    SuccessMessageMixin[RegisterForm],
    CreateView[User, RegisterForm],
):
    form_class = RegisterForm
    template_name = "accounts/register.html"
    htmx_template = "form"
    success_message = _("Account created successfully!")

    def get_success_url(self) -> str:
        return resolve_url(settings.LOGIN_URL)


class LoginView(HtmxMixin, SuccessMessageMixin[LoginForm], DjangoLoginView[LoginForm]):
    form_class = LoginForm
    template_name = "accounts/login.html"
    htmx_template = "form"
    redirect_authenticated_user = True
    success_message = _("Welcome back!")

    def form_valid(self, form: LoginForm) -> HttpResponse:
        response = super().form_valid(form)
        if not form.cleaned_data["remember_me"]:
            self.request.session.set_expiry(0)
        return response
