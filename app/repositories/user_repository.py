"""
User Repository.

Handles user database operations and email lookups.
"""

from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for User entity operations."""

    def __init__(self, db: Session):
        super().__init__(User, db)

    def get_by_email(self, email: str) -> Optional[User]:
        """Query user by unique email address."""
        return self.db.query(User).filter(User.email == email).first()

