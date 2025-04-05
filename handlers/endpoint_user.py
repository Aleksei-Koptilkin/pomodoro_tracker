from fastapi import APIRouter, Depends

from dependency import get_user_service
from schema import UserLoginSchema, UserCreateSchema
from service import UserService

router = APIRouter(prefix="/user", tags=["user"])


@router.post("", response_model=UserLoginSchema)
def create_user(
        user: UserCreateSchema,
        user_service: UserService = Depends(get_user_service)
    ):
    return user_service.create_user(username=user.username, password=user.password)
