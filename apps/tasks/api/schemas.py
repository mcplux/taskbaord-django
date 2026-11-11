from datetime import date, datetime
from typing import Any

from ninja import Schema

from apps.tasks.models import TaskActivityAction, TaskPriority, TaskStatus


class TaskBase(Schema):
    title: str
    description: str
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.LOW
    due_date: date | None = None


class TaskIn(TaskBase):
    pass


class TaskOut(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime


class TaskPatch(Schema):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    due_date: date | None = None


class TaskActivityOut(Schema):
    actor_id: int | None = None
    action: TaskActivityAction
    changes: dict[str, Any]
    created_at: datetime
