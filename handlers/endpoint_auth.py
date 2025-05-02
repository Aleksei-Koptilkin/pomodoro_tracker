from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import  RedirectResponse

from sqlalchemy.ext.asyncio import AsyncSession

from client import GoogleClient
from database import get_db_session
from dependency import get_auth_service, get_google_client
from exception import UserNotFoundException, UserNotCorrectPasswordException
from schema import UserLoginSchema, UserCreateSchema
from service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=UserLoginSchema)
async def login(
        user: UserCreateSchema,
        auth: AuthService = Depends(get_auth_service),
        session: AsyncSession = Depends(get_db_session)
    ):
    try:
        user_login = await auth.login(
            username=user.username,
            password=user.password,
            session=session
        )
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except UserNotCorrectPasswordException as e:
        raise HTTPException(status_code=401, detail=e.detail)
    return user_login


@router.get("/login/google", response_class=RedirectResponse)
async def google_login(auth: AuthService = Depends(get_auth_service)):
    google_redirect_url = auth.google_redirect()
    print(google_redirect_url)
    return RedirectResponse(google_redirect_url)


@router.get("/google_auth")
async def google_auth(
        code: str,
        auth: AuthService = Depends(get_auth_service),
        session: AsyncSession = Depends(get_db_session)
    ):
    return await auth.google_auth(code=code, session=session)

@router.get("/login/yandex", response_class=RedirectResponse)
async def yandex_login(auth_service: AuthService = Depends(get_auth_service)):
    yandex_redirect_url = auth_service.yandex_redirect()
    print(yandex_redirect_url)
    return RedirectResponse(yandex_redirect_url)

@router.get("/yandex_auth")
async def yandex_auth(
        code: str,
        auth: AuthService = Depends(get_auth_service),
        session: AsyncSession = Depends(get_db_session)
    ):
    return await auth.yandex_auth(code=code, session=session)