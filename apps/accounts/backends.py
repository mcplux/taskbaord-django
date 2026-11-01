from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import AnonymousUser

from .models import User


class VerifiedUserBackend(ModelBackend):
    """
    Authentication backend that rejects users who have not verified their email.
    """

    def user_can_authenticate(self, user: User | AnonymousUser | None) -> bool:
        return super().user_can_authenticate(user) and getattr(user, "is_verified", False)
