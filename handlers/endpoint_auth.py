from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import  RedirectResponse

from client import GoogleClient
from dependency import get_auth_service, get_google_client
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


@router.get("/login/google", response_class=RedirectResponse)
def google_login(auth: AuthService = Depends(get_auth_service)):
    google_redirect_url = auth.google_redirect()
    print(google_redirect_url)
    return RedirectResponse(google_redirect_url)


@router.get("/google_auth")
def google_auth(
        code: str,
        auth: AuthService = Depends(get_auth_service)
    ):
    return auth.google_auth(code=code)
