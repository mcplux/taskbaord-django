from typing import cast

from django.db.models import QuerySet
from ninja import Status
from ninja.security import django_auth
from ninja_extra import ControllerBase, api_controller, route, status
from ninja_extra.permissions import IsAuthenticated

from apps.accounts.models import User
from apps.tasks.models import Task, TaskActivity

from .schemas import TaskActivityOut, TaskIn, TaskOut, TaskPatch


@api_controller("/tasks", tags=["tasks"], auth=django_auth, permissions=[IsAuthenticated])
class TaskController(ControllerBase):
    @property
    def user(self) -> User:
        assert self.context is not None
        assert self.context.request is not None
        return cast(User, self.context.request.user)

    def get_queryset(self) -> QuerySet[Task]:
        return Task.objects.filter(owner=self.user)

    def get_task(self, task_id: int) -> Task:
        return self.get_object_or_exception(
            self.get_queryset(), error_message=f"task with id {task_id} not found", pk=task_id
        )

    @route.post("", response={status.HTTP_201_CREATED: TaskOut})
    def create_task(self, payload: TaskIn) -> Status[Task]:
        task = Task(owner=self.user, **payload.model_dump())
        task.save(actor=self.user)
        return Status(status.HTTP_201_CREATED, task)

    @route.get("", response={status.HTTP_200_OK: list[TaskOut]})
    def list_task(self) -> Status[QuerySet[Task]]:
        return Status(status.HTTP_200_OK, self.get_queryset())

    @route.get("/{task_id}", response={status.HTTP_200_OK: TaskOut})
    def retrieve_task(self, task_id: int) -> Task:
        return self.get_task(task_id)

    @route.put("/{task_id}", response={status.HTTP_200_OK: TaskOut})
    def update_task(self, task_id: int, payload: TaskIn) -> Task:
        task = self.get_task(task_id)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(task, field, value)
        task.save(actor=self.user)
        return task

    @route.patch("/{task_id}", response={status.HTTP_200_OK: TaskOut})
    def update_task_partially(self, task_id: int, payload: TaskPatch) -> Task:
        task = self.get_task(task_id)
        for field, value in payload.model_dump(exclude_unset=True).items():
            if value is None and field != "due_date":
                continue
            setattr(task, field, value)
        task.save(actor=self.user)
        return task

    @route.delete("/{task_id}", response={status.HTTP_204_NO_CONTENT: None})
    def delete_task(self, task_id: int) -> Status[None]:
        self.get_task(task_id).delete()
        return Status(status.HTTP_204_NO_CONTENT, None)

    @route.get("/{task_id}/activities", response={status.HTTP_200_OK: list[TaskActivityOut]})
    def get_task_activities(self, task_id: int) -> QuerySet[TaskActivity]:
        return self.get_task(task_id).activities.all()
