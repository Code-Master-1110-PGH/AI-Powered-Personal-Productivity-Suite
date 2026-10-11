"""
User Management Endpoints.

Handles registration and lookup of suite users.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Registers a new user in the system with a unique email.",
)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
) -> UserResponse:
    repo = UserRepository(db)
    existing = repo.get_by_email(user_in.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email '{user_in.email}' already exists.",
        )
    return repo.create(user_in)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user profile",
    description="Fetches user account details by ID.",
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
) -> UserResponse:
    repo = UserRepository(db)
    user = repo.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found.",
        )
    return user

