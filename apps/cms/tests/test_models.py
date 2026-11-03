import pytest
from django.core.exceptions import ValidationError
from django.utils import translation

from apps.cms.models import HomePage
from apps.cms.validators import validate_link


class TestValidateLink:
    @pytest.mark.parametrize(
        "value",
        [
            "/",
            "/about/",
            "/search/?q=tasks#results",
            "#login",
            "http://example.com",
            "https://example.com/pricing/?plan=team",
        ],
    )
    def test_accepts(self, value: str) -> None:
        validate_link(value)

    @pytest.mark.parametrize(
        "value",
        [
            "javascript:alert(1)",
            "JaVaScRiPt:alert(1)",
            " javascript:alert(1)",
            "java\tscript:alert(1)",
            "data:text/html,<script>alert(1)</script>",
            "vbscript:msgbox(1)",
            "mailto:team@example.com",
            "ftp://example.com",
            "about",
            "example.com",
            "//example.com",
            "/\\example.com",
            "/about us/",
            "/about/\n",
            "/\tabout/",
        ],
    )
    def test_rejects(self, value: str) -> None:
        with pytest.raises(ValidationError):
            validate_link(value)

    def test_field_uses_validator(self) -> None:
        page = HomePage(
            title="Title",
            hero_title="Title",
            login_title="Login",
            hero_cta_label="Go",
            hero_cta_url="javascript:alert(1)",
        )
        with pytest.raises(ValidationError) as exc_info:
            page.clean_fields()
        assert list(exc_info.value.message_dict) == ["hero_cta_url"]


@pytest.mark.django_db
class TestForActiveLanguage:
    @pytest.fixture
    def page(self) -> HomePage:
        return HomePage.objects.create(language="en", hero_title="Title", login_title="Login")

    def test_returns_page_for_language(self, page: HomePage) -> None:
        with translation.override("en"):
            assert HomePage.for_active_language() == page

    def test_resolves_language_variant(self, page: HomePage) -> None:
        with translation.override("en-us"):
            assert HomePage.for_active_language() == page

    def test_uses_default_language_when_translations_are_deactivated(self, page: HomePage) -> None:
        with translation.override(None):
            assert HomePage.for_active_language() == page

    def test_returns_none_without_page(self) -> None:
        with translation.override("en"):
            assert HomePage.for_active_language() is None

    @pytest.mark.usefixtures("page")
    def test_returns_none_for_unsupported_language(self) -> None:
        with translation.override("fr"):
            assert HomePage.for_active_language() is None
