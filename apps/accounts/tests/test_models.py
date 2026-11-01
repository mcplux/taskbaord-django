import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from apps.accounts.models import User

pytestmark = pytest.mark.django_db


class TestUserManager:
    def test_create_user(self, user: User, user_password: str) -> None:
        assert user.email == "user@example.com"
        assert user.check_password(user_password)
        assert user.is_active
        assert not user.is_staff
        assert not user.is_superuser
        assert not user.is_verified

    def test_create_user_without_email_raises(self) -> None:
        with pytest.raises(ValueError, match="email must be set"):
            User.objects.create_user(email="", password="x")

    def test_create_user_without_password_is_unusable(self) -> None:
        user = User.objects.create_user(email="nopass@example.com")
        assert not user.has_usable_password()

    def test_create_superuser(self, superuser: User) -> None:
        assert superuser.is_staff
        assert superuser.is_superuser
        assert superuser.is_verified

    @pytest.mark.parametrize("flag", ["is_staff", "is_superuser", "is_verified"])
    def test_create_superuser_with_false_flag_raises(self, flag: str) -> None:
        with pytest.raises(ValueError, match=f"{flag}=True"):
            User.objects.create_superuser(email="admin@example.com", password="x", **{flag: False})

    def test_normalize_email_lowercases_and_strips(self) -> None:
        assert User.objects.normalize_email("  Foo.Bar@Example.COM ") == "foo.bar@example.com"

    def test_get_by_natural_key_is_case_insensitive(self, user: User) -> None:
        assert User.objects.get_by_natural_key("USER@Example.com") == user


class TestUserEmailLowercase:
    def test_create_user_stores_lowercase(self) -> None:
        user = User.objects.create_user(email="Mixed.Case@Example.COM", password="x")
        user.refresh_from_db()
        assert user.email == "mixed.case@example.com"

    def test_save_stores_lowercase(self, user: User) -> None:
        user.email = "New.Email@Example.COM"
        user.save()
        user.refresh_from_db()
        assert user.email == "new.email@example.com"

    def test_clean_lowercases(self) -> None:
        user = User(email="Clean@Example.COM")
        user.clean()
        assert user.email == "clean@example.com"

    def test_email_unique_regardless_of_case(self, user: User) -> None:
        with pytest.raises(IntegrityError), transaction.atomic():
            User.objects.create_user(email="USER@example.com", password="x")

    def test_db_constraint_rejects_uppercase(self, user: User) -> None:
        with pytest.raises(IntegrityError), transaction.atomic():
            User.objects.filter(pk=user.pk).update(email="UPPER@example.com")

    def test_validate_constraints_rejects_uppercase(self) -> None:
        user = User(email="UPPER@example.com")
        with pytest.raises(ValidationError, match="Email must be lowercase"):
            user.validate_constraints()


class TestUserModel:
    def test_str_returns_email(self, user: User) -> None:
        assert str(user) == "user@example.com"

    def test_get_full_name(self) -> None:
        user = User(email="a@example.com", first_name=" Jane", last_name="Doe ")
        assert user.get_full_name() == "Jane Doe"

    def test_get_full_name_empty(self) -> None:
        assert User(email="a@example.com").get_full_name() == ""

    def test_get_short_name(self) -> None:
        assert User(email="a@example.com", first_name="Jane").get_short_name() == "Jane"
