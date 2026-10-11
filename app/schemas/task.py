"""
Task Pydantic Schemas.

Validation and serialization models for Task creation, status updates,
and Natural Language Understanding (NLU) extraction.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from app.models.task import TaskStatus, TaskPriority


class TaskBase(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    estimated_duration_minutes: int = Field(default=60, ge=5, le=1440)
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    user_id: int
    raw_prompt: Optional[str] = None


class TaskResponse(TaskBase):
    id: int
    user_id: int
    raw_prompt: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SmartTaskRequest(BaseModel):
    user_id: int = Field(..., description="Target user identifier")
    natural_language_input: str = Field(
        ...,
        min_length=3,
        description="Natural language request (e.g. 'Schedule a mock interview tomorrow at 5 PM')",
        examples=["Schedule a mock interview tomorrow at 5 PM"]
    )
    reference_datetime: Optional[datetime] = Field(
        default=None,
        description="Optional base datetime to resolve relative dates against. Defaults to UTC now."
    )


class ExtractedTaskIntent(BaseModel):
    raw_input: str
    intent: str = Field(..., description="Detected user intent, e.g., 'CREATE_EVENT', 'SCHEDULE_TASK'")
    extracted_title: str
    priority: TaskPriority
    target_start_time: datetime
    target_end_time: datetime
    duration_minutes: int
    confidence_score: float = Field(..., ge=0.0, le=1.0)

