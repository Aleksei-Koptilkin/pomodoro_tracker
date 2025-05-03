from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db_session
from dependency import get_user_service
from schema import UserLoginSchema, UserCreateSchema
from service import UserService

router = APIRouter(prefix="/user", tags=["user"])


@router.post("", response_model=UserLoginSchema)
async def create_user(
        user: UserCreateSchema,
        user_service: UserService = Depends(get_user_service),
        session: AsyncSession = Depends(get_db_session)
    ):
    return await user_service.create_user(user, session)
