from typing import cast

from django.contrib.auth import logout as auth_logout
from django.http.request import HttpRequest
from ninja import Status
from ninja.security import django_auth
from ninja_extra import ControllerBase, api_controller, route, status
from ninja_extra.permissions import IsAuthenticated

from apps.accounts.api.schemas import UserOut
from apps.accounts.models import User


@api_controller("/auth", tags=["auth"], auth=django_auth, permissions=[IsAuthenticated])
class AuthController(ControllerBase):
    @property
    def request(self) -> HttpRequest:
        assert self.context is not None
        assert self.context.request is not None
        return self.context.request

    @route.get("/me", response={status.HTTP_200_OK: UserOut}, operation_id="get_me")
    def get_me(self) -> User:
        return cast(User, self.request.user)

    @route.post("/logout", response={status.HTTP_204_NO_CONTENT: None}, operation_id="logout")
    def logout(self) -> Status[None]:
        auth_logout(self.request)
        return Status(status.HTTP_204_NO_CONTENT, None)
