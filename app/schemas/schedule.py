"""
Daily Schedule Pydantic Schemas.

Validation and serialization models for schedule time-blocks and daily itinerary retrieval.
"""

from typing import List, Optional
from datetime import date, datetime
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.task import TaskResponse, ExtractedTaskIntent


class DailyScheduleBase(BaseModel):
    scheduled_date: date
    start_time: datetime
    end_time: datetime
    time_block_title: str = Field(..., max_length=255)
    is_completed: bool = False


class DailyScheduleCreate(DailyScheduleBase):
    user_id: int
    task_id: Optional[int] = None


class DailyScheduleResponse(DailyScheduleBase):
    id: int
    user_id: int
    task_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    task: Optional[TaskResponse] = None

    model_config = ConfigDict(from_attributes=True)


class DailyItineraryResponse(BaseModel):
    user_id: int
    scheduled_date: date
    total_blocks: int
    itinerary: List[DailyScheduleResponse] = Field(default_factory=list)


class SmartTaskSchedulingResponse(BaseModel):
    message: str
    task: TaskResponse
    schedule: DailyScheduleResponse
    nlu_metadata: ExtractedTaskIntent

