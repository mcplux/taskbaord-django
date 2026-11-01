import pytest

from apps.accounts.models import User


@pytest.fixture
def user_password() -> str:
    return "S3cure-Passw0rd!"


@pytest.fixture
def user(user_password: str) -> User:
    return User.objects.create_user(email="user@example.com", password=user_password)


@pytest.fixture
def superuser(user_password: str) -> User:
    return User.objects.create_superuser(email="admin@example.com", password=user_password)
