from fastapi import APIRouter, Depends, HTTPException

from dependency import get_auth_service
from exception import UserNotFoundException, UserNotCorrectPasswordException
from schema import UserLoginSchema, UserCreateSchema
from service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=UserLoginSchema)
def login(user: UserCreateSchema, auth: AuthService = Depends(get_auth_service)):
    try:
        user_login = auth.login(username=user.username, password=user.password)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except UserNotCorrectPasswordException as e:
        raise HTTPException(status_code=401, detail=e.detail)
    return user_login