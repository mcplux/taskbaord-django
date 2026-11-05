from typing import Any

from django import forms
from django.contrib.auth.forms import AuthenticationForm, BaseUserCreationForm
from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import User
from apps.core.forms import TailwindFormMixin


class RegisterForm(TailwindFormMixin, BaseUserCreationForm[User]):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {
                "autocomplete": "email",
                "placeholder": "your-email@example.com",
                "autofocus": True,
            }
        )

    def clean_email(self) -> str:
        return User.objects.normalize_email(self.cleaned_data["email"])


class LoginForm(TailwindFormMixin, AuthenticationForm):
    remember_me = forms.BooleanField(label=_("Remember me"), required=False)

    error_messages = {  # noqa: RUF012
        "invalid_login": _("Please enter a correct email and password."),
        "inactive": _("This account is inactive."),
        "unverified": _(
            "Please verify your email address before signing in. "
            "Check your inbox for the verification link."
        ),
    }

    def __init__(self, request: HttpRequest | None = None, *args: Any, **kwargs: Any) -> None:
        super().__init__(request, *args, **kwargs)
        username = self.fields["username"]
        username.widget.input_type = "email"
        username.widget.attrs.update(
            {
                "autocomplete": "email",
                "placeholder": "your-email@example.com",
            }
        )

    def get_invalid_login_error(self) -> ValidationError:
        email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        try:
            user = User.objects.get_by_natural_key(email)
        except User.DoesNotExist:
            return super().get_invalid_login_error()
        if user.is_active and not user.is_verified and user.check_password(password):
            return ValidationError(self.error_messages["unverified"], code="unverified")
        return super().get_invalid_login_error()
