"""
Task ORM Model.

Represents actionable items, their lifecycle status, and urgency.
Includes the raw natural language prompt that prompted the AI inference.
"""

import enum
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base


class TaskStatus(str, enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class TaskPriority(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"


class Task(Base):
    """
    SQLAlchemy ORM model representing user tasks.
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Traceability: Natural language prompt used by Task NLU to extract this task
    raw_prompt = Column(Text, nullable=True)
    
    status = Column(
        Enum(TaskStatus, native_enum=False, length=50),
        nullable=False,
        default=TaskStatus.PENDING,
        index=True,
    )
    priority = Column(
        Enum(TaskPriority, native_enum=False, length=50),
        nullable=False,
        default=TaskPriority.MEDIUM,
        index=True,
    )
    
    estimated_duration_minutes = Column(Integer, nullable=False, default=60)
    due_date = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    user = relationship("User", back_populates="tasks")
    schedules = relationship(
        "DailySchedule",
        back_populates="task",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status}', priority='{self.priority}')>"

