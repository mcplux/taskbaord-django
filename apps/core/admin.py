from typing import Any

from django.http import HttpRequest


class ReadOnlyAdminMixin:
    def has_add_permission(self, _request: HttpRequest, _obj: Any = None) -> bool:
        return False

    def has_change_permission(self, _request: HttpRequest, _obj: Any = None) -> bool:
        return False

    def has_delete_permission(self, _request: HttpRequest, _obj: Any = None) -> bool:
        return False
