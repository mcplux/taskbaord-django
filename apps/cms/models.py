from typing import Self

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from django.utils.translation.trans_real import get_supported_language_variant
from django_ckeditor_5.fields import CKEditor5Field

from .validators import validate_link


def language_choices() -> list[tuple[str, str]]:
    """
    Callable so that changing settings.LANGUAGES doesn't require a migration
    """
    return list(settings.LANGUAGES)


def default_language() -> str:
    return get_supported_language_variant(settings.LANGUAGE_CODE)


class PageModel(models.Model):
    """
    Abstract class for CMS pages.
    """

    language = models.CharField(
        _("language"), choices=language_choices, default=default_language(), unique=True
    )
    title = models.CharField(_("seo title"), max_length=100)
    meta_description = models.CharField(_("meta description"), max_length=160, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"{self.title} ({self.language})"


class HomePage(PageModel):
    """
    Home page content.
    """

    hero_title = models.CharField(_("title"), max_length=200)
    hero_subtitle = models.TextField(_("subtitle"), blank=True)
    hero_image = models.ImageField(_("image"), upload_to="cms/", blank=True)
    hero_image_alt = models.CharField(_("image alt text"), max_length=200, blank=True)
    hero_cta_label = models.CharField(_("button label"), max_length=50, blank=True)
    hero_cta_url = models.CharField(
        _("button link"),
        max_length=200,
        blank=True,
        validators=[validate_link],
    )

    about_title = models.CharField(_("title"), max_length=200, blank=True)
    about_body = CKEditor5Field(_("body"), blank=True)

    login_title = models.CharField(_("title"), max_length=200)
    login_body = CKEditor5Field(_("body"), blank=True)
    login_button_label = models.CharField(_("button label"), max_length=50, default="Log in")

    class Meta:
        verbose_name = _("home page")
        verbose_name_plural = _("home page")

    def __str__(self) -> str:
        return f"{self.hero_title} ({self.language})"

    def clean(self) -> None:
        super().clean()
        if bool(self.hero_cta_label) != bool(self.hero_cta_url):
            field = "hero_cta_url" if self.hero_cta_label else "hero_cta_label"
            raise ValidationError(
                {field: _("A hero button needs both a label and a link.")},
            )

    @classmethod
    def for_active_language(cls) -> Self | None:
        try:
            language = get_supported_language_variant(get_language() or settings.LANGUAGE_CODE)
        except LookupError:
            return None
        return cls.objects.filter(language=language).first()
