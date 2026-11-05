import pytest
from django.test import Client
from django.urls import reverse

from apps.accounts.models import User

pytestmark = pytest.mark.django_db

HTMX = {"HX-Request": "true"}


@pytest.mark.parametrize(
    ("url_name", "fields"),
    [
        ("auth:login", ["username", "password", "remember_me"]),
        ("auth:register", ["email", "first_name", "last_name", "password1", "password2"]),
    ],
)
def test_full_page_renders_every_field_inside_the_layout(
    client: Client, url_name: str, fields: list[str]
) -> None:
    html = client.get(reverse(url_name)).content.decode()

    assert "<aside" in html
    for field in fields:
        assert f'name="{field}"' in html


@pytest.mark.parametrize("url_name", ["auth:login", "auth:register"])
def test_htmx_post_returns_only_the_form_with_errors(client: Client, url_name: str) -> None:
    response = client.post(reverse(url_name), {}, headers=HTMX)
    html = response.content.decode()

    assert response.status_code == 200
    assert html.strip().startswith("<form")
    assert "<aside" not in html
    assert "csrfmiddlewaretoken" in html
    assert 'aria-invalid="true"' in html
    assert "_error" in html


def test_login_keeps_next_across_failed_htmx_submit(client: Client) -> None:
    response = client.post(reverse("auth:login"), {"next": "/somewhere/"}, headers=HTMX)

    assert 'name="next" value="/somewhere/"' in response.content.decode()


def test_invalid_credentials_show_non_field_error(client: Client) -> None:
    User.objects.create_user("user@example.com", "s3cret-pass-123", is_verified=True)

    response = client.post(
        reverse("auth:login"),
        {"username": "user@example.com", "password": "wrong"},
        headers=HTMX,
    )

    assert 'role="alert"' in response.content.decode()


def test_register_success_shows_message_on_login_page(client: Client) -> None:
    response = client.post(
        reverse("auth:register"),
        {
            "email": "new@example.com",
            "password1": "s3cret-pass-123",
            "password2": "s3cret-pass-123",
        },
        headers=HTMX,
    )

    assert response.headers["HX-Redirect"] == reverse("auth:login")
    assert "Account created successfully!" in client.get(reverse("auth:login")).content.decode()
