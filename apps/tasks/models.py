from typing import Any

from django.conf import settings
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import User


class TaskStatus(models.TextChoices):
    TODO = "todo", _("To do")
    IN_PROGRESS = "in_progress", _("In progress")
    DONE = "done", _("Done")


class TaskPriority(models.IntegerChoices):
    LOW = 1, _("Low")
    MEDIUM = 2, _("Medium")
    HIGH = 3, _("High")
    URGENT = 4, _("Urgent")


class Task(models.Model):
    """
    Unit of work on the board
    """

    TRACKED_FIELDS = (
        "title",
        "description",
        "status",
        "priority",
        "due_date",
    )

    Status = TaskStatus
    Priority = TaskPriority

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name=_("owner"),
    )
    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"), blank=True)
    status = models.CharField(
        _("status"), max_length=20, choices=Status, default=Status.TODO, db_index=True
    )
    priority = models.PositiveSmallIntegerField(
        _("priority"), choices=Priority, default=Priority.LOW, db_index=True
    )
    due_date = models.DateField(_("due date"), null=True, blank=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        verbose_name = _("task")
        verbose_name_plural = _("tasks")
        ordering = ("-created_at",)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._snapshot = self._tracked_values()

    def __str__(self) -> str:
        return self.title

    def save(self, *args: Any, actor: User | None = None, **kwargs: Any) -> None:
        """Override save method to create automatically a TaskActivity record"""
        is_new = self._state.adding
        changes: dict[str, Any] = {} if is_new else self._changes()

        with transaction.atomic():
            super().save(*args, **kwargs)
            if is_new:
                TaskActivity.objects.create(
                    task=self, actor=actor, action=TaskActivity.Action.CREATED
                )
            elif changes:
                TaskActivity.objects.create(
                    task=self,
                    actor=actor,
                    action=TaskActivity.Action.UPDATED,
                    changes=TaskActivity.serialize_data(changes),
                )

        self._snapshot = self._tracked_values()  # Update snapshot

    def _tracked_values(self) -> dict[str, Any]:
        """Convert the instance to a dictionary with the tracked values"""
        return {field: getattr(self, field) for field in self.TRACKED_FIELDS}

    def _changes(self) -> dict[str, dict[str, Any]]:
        """Return dictionary with changes"""
        current = self._tracked_values()
        return {
            field: {"old": self._snapshot[field], "new": value}
            for field, value in current.items()
            if self._snapshot[field] != value
        }


class TaskActivityAction(models.TextChoices):
    CREATED = "created", _("Created")
    UPDATED = "updated", _("Updated")


class TaskActivity(models.Model):
    Action = TaskActivityAction

    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name="activities", verbose_name=_("task")
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="task_activities",
        verbose_name=_("actor"),
    )
    action = models.CharField(_("action"), max_length=20, choices=Action)
    changes = models.JSONField(_("changes"), default=dict, blank=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    class Meta:
        verbose_name = _("task activity")
        verbose_name_plural = _("task activities")
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.task} - {self.get_action_display()}"

    @staticmethod
    def serialize_data(data: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
        """Make data JSON-safe"""

        def to_json(value: Any) -> Any:
            if value is None or isinstance(value, str | int | float | bool):
                return value

            if hasattr(value, "isoformat"):
                return value.isoformat()

            return str(value)

        return {
            field: {"old": to_json(diff["old"]), "new": to_json(diff["new"])}
            for field, diff in data.items()
        }
