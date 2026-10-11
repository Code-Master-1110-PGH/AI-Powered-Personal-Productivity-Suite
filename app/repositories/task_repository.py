"""
Task Repository.

Handles persistence, status queries, and priority updates for tasks.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.task import Task, TaskStatus
from app.repositories.base import BaseRepository


class TaskRepository(BaseRepository[Task]):
    """Repository for Task entity operations."""

    def __init__(self, db: Session):
        super().__init__(Task, db)

    def get_by_user_id(
        self, user_id: int, status: Optional[TaskStatus] = None
    ) -> List[Task]:
        """Fetch tasks belonging to a user, optionally filtered by status."""
        query = self.db.query(Task).filter(Task.user_id == user_id)
        if status:
            query = query.filter(Task.status == status)
        return query.order_by(desc(Task.created_at)).all()

