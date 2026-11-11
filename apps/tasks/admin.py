from typing import Any, cast

from django.contrib import admin
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import User
from apps.core.admin import ReadOnlyAdminMixin
from apps.tasks.models import Task, TaskActivity


class TaskActivityInline(ReadOnlyAdminMixin, admin.TabularInline[TaskActivity, Task]):
    model = TaskActivity
    extra = 0
    fields = ("created_at", "action", "actor", "changes")
    readonly_fields = fields
    ordering = ("-created_at",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin[Task]):
    list_display = ("title", "owner", "status", "priority", "due_date", "updated_at")
    list_filter = ("status", "priority", "due_date")
    search_fields = ("title", "description", "owner__email")
    autocomplete_fields = ("owner",)
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"
    inlines = (TaskActivityInline,)
    fieldsets = (
        (None, {"fields": ("owner", "title", "description")}),
        (_("Planning"), {"fields": ("status", "priority", "due_date")}),
        (_("Important dates"), {"fields": ("created_at", "updated_at")}),
    )

    def save_model(self, request: HttpRequest, obj: Task, form: Any, change: Any) -> None:
        user = cast(User, request.user)
        obj.save(actor=user)
        super().save_model(request, obj, form, change)
