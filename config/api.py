from ninja_extra import NinjaExtraAPI

from apps.tasks.api.controllers import TaskController

api = NinjaExtraAPI(title="Taskboard Django API", version="0.0.1", urls_namespace="api")
api.register_controllers(TaskController)
