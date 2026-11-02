from django.conf import settings
from django.contrib import admin
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from .models import HomePage


@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin[HomePage]):
    list_display = ("title", "language", "updated_at")
    list_filter = ("language",)
    readonly_fields = ("updated_at",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "language",
                    "meta_description",
                )
            },
        ),
        (
            _("Hero"),
            {
                "fields": (
                    "hero_title",
                    "hero_subtitle",
                    "hero_image",
                    "hero_image_alt",
                    "hero_cta_label",
                    "hero_cta_url",
                )
            },
        ),
        (
            _("About"),
            {"fields": ("about_title", "about_body")},
        ),
        (
            _("Login"),
            {"fields": ("login_title", "login_body", "login_button_label")},
        ),
        (_("Important dates"), {"fields": ("updated_at",)}),
    )

    def has_add_permission(self, request: HttpRequest) -> bool:
        has_free_language = HomePage.objects.count() < len(settings.LANGUAGES)
        return super().has_add_permission(request) and has_free_language

    def has_delete_permission(self, request: HttpRequest, obj: HomePage | None = None) -> bool:
        return False
