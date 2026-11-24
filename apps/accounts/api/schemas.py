from ninja import Schema
from pydantic import EmailStr

from apps.accounts.models import User


class UserOut(Schema):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    full_name: str
    is_staff: bool

    @staticmethod
    def resolve_full_name(obj: User):
        return obj.get_full_name()
