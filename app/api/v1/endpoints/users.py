from fastapi import APIRouter, HTTPException, status

from app.db.session import SessionDependency
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import UserService

router = APIRouter()


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, session: SessionDependency) -> UserRead:
    service = UserService(session)
    return await service.create_user(payload)  # type: ignore


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, session: SessionDependency) -> UserRead:
    service = UserService(session)
    user = await service.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user  # type: ignore
