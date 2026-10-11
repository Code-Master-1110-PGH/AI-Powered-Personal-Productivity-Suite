"""
Smart Task & Scheduling Endpoints.

Handles natural language task input, AI extraction, automatic task generation,
and schedule block reservation.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.api.deps import get_scheduler_service
from app.core.database import get_db
from app.core.exceptions import EntityNotFoundException, SchedulingConflictException
from app.models.task import TaskStatus
from app.repositories.task_repository import TaskRepository
from app.services.scheduler_service import SchedulerService
from app.schemas.task import (
    SmartTaskRequest,
    TaskResponse,
)
from app.schemas.schedule import SmartTaskSchedulingResponse

router = APIRouter()


@router.post(
    "/smart-tasks",
    response_model=SmartTaskSchedulingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create & Schedule Task from Natural Language",
    description=(
        "Processes natural language commands (e.g., 'Schedule a mock interview tomorrow at 5 PM'), "
        "extracts the intent, task title, priority, target time, and duration, creating both the Task "
        "and corresponding Daily Schedule entry."
    ),
)
def create_smart_task(
    request: SmartTaskRequest,
    allow_overlap: bool = Query(True, description="Whether to permit overlapping schedule blocks"),
    service: SchedulerService = Depends(get_scheduler_service),
) -> SmartTaskSchedulingResponse:
    try:
        task, schedule, nlu_metadata = service.process_smart_task(
            request=request, allow_overlap=allow_overlap
        )
        return SmartTaskSchedulingResponse(
            message=f"Successfully extracted and scheduled task: '{task.title}'",
            task=task,
            schedule=schedule,
            nlu_metadata=nlu_metadata,
        )
    except EntityNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e.message),
        )
    except SchedulingConflictException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e.message),
        )


@router.get(
    "/tasks/user/{user_id}",
    response_model=List[TaskResponse],
    summary="Get user tasks",
    description="Lists all tasks created by or extracted for a user.",
)
def get_user_tasks(
    user_id: int,
    status_filter: Optional[TaskStatus] = Query(None, alias="status"),
    db: Session = Depends(get_db),
) -> List[TaskResponse]:
    repo = TaskRepository(db)
    return repo.get_by_user_id(user_id=user_id, status=status_filter)

