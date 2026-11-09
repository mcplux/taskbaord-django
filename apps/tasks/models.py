from typing import Any

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    """
    Unit of work on the board
    """

    class Status(models.TextChoices):
        TODO = "todo", _("To do")
        IN_PROGRESS = "in_progress", _("In progress")
        DONE = "done", _("Done")

    class Priority(models.IntegerChoices):
        LOW = 1, _("Low")
        MEDIUM = 2, _("Medium")
        HIGH = 3, _("High")
        URGENT = 4, _("Urgent")

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

    def __str__(self) -> str:
        return self.title


class TaskActivity(models.Model):
    class Action(models.TextChoices):
        CREATED = "created", _("Created")
        UPDATED = "updated", _("Updated")

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
