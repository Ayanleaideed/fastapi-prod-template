from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self._repository = UserRepository(session)

    async def create_user(self, payload: UserCreate) -> User:
        existing = await self._repository.get_by_email(str(payload.email))
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="User with this email already exists"
            )
        return await self._repository.create(email=str(payload.email), full_name=payload.full_name)

    async def get_user(self, user_id: int) -> User | None:
        return await self._repository.get_by_id(user_id)
