"""
Schemas Package.
"""

from app.schemas.user import UserBase, UserCreate, UserResponse
from app.schemas.resume import (
    SkillCategory,
    QuantifiedMetric,
    ResumeAnalysisRequest,
    ResumeAnalysisResponse,
)
from app.schemas.task import (
    TaskBase,
    TaskCreate,
    TaskResponse,
    SmartTaskRequest,
    ExtractedTaskIntent,
)
from app.schemas.schedule import (
    DailyScheduleBase,
    DailyScheduleCreate,
    DailyScheduleResponse,
    DailyItineraryResponse,
    SmartTaskSchedulingResponse,
)

__all__ = [
    "UserBase",
    "UserCreate",
    "UserResponse",
    "SkillCategory",
    "QuantifiedMetric",
    "ResumeAnalysisRequest",
    "ResumeAnalysisResponse",
    "TaskBase",
    "TaskCreate",
    "TaskResponse",
    "SmartTaskRequest",
    "ExtractedTaskIntent",
    "DailyScheduleBase",
    "DailyScheduleCreate",
    "DailyScheduleResponse",
    "DailyItineraryResponse",
    "SmartTaskSchedulingResponse",
]

