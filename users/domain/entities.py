from pydantic import BaseModel
from typing_extensions import Optional


class User(BaseModel):
    id: Optional[int]
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    email: str
    is_active: bool
    is_superuser: bool
    is_staff: bool

    @staticmethod
    def factory(
        username: str,
        first_name: str,
        last_name: str,
        email: str,
        _id: int = None,
        is_active: bool = True,
        is_superuser: bool = False,
        is_staff: bool = False,
    ) -> 'User':
        return User(
            id=_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_active=is_active,
            is_superuser=is_superuser,
            is_staff=is_staff
        )
