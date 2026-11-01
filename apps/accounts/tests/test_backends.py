import pytest
from django.contrib.auth import authenticate

from apps.accounts.models import User

pytestmark = pytest.mark.django_db


class TestVerifiedUserBackend:
    def test_unverified_user_cannot_authenticate(self, user: User, user_password: str) -> None:
        assert authenticate(email=user.email, password=user_password) is None

    def test_verified_user_can_authenticate(self, user: User, user_password: str) -> None:
        user.is_verified = True
        user.save()
        assert authenticate(email=user.email, password=user_password) == user

    def test_inactive_verified_user_cannot_authenticate(
        self, user: User, user_password: str
    ) -> None:
        user.is_verified = True
        user.is_active = False
        user.save()
        assert authenticate(email=user.email, password=user_password) is None

    def test_superuser_can_authenticate(self, superuser: User, user_password: str) -> None:
        assert authenticate(email=superuser.email, password=user_password) == superuser
