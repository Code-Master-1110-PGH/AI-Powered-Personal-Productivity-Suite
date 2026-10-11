"""
Daily Schedule & Itinerary Endpoints.

Provides chronological itinerary lookup for specific dates based on database records.
"""

from datetime import date, datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.api.deps import get_scheduler_service
from app.core.exceptions import EntityNotFoundException
from app.services.scheduler_service import SchedulerService
from app.schemas.schedule import DailyItineraryResponse, DailyScheduleResponse

router = APIRouter()


@router.get(
    "/daily/{user_id}",
    response_model=DailyItineraryResponse,
    summary="Retrieve User's Daily Itinerary",
    description=(
        "Retrieves a user's chronological itinerary for a target date, ordered by start time. "
        "If date is omitted, defaults to the current date."
    ),
)
def get_daily_itinerary(
    user_id: int,
    target_date: Optional[date] = Query(
        None,
        alias="date",
        description="Target calendar date (YYYY-MM-DD). Defaults to current date if omitted.",
    ),
    service: SchedulerService = Depends(get_scheduler_service),
) -> DailyItineraryResponse:
    query_date = target_date or datetime.now(timezone.utc).date()
    try:
        schedule_blocks = service.get_daily_itinerary(user_id=user_id, target_date=query_date)
        return DailyItineraryResponse(
            user_id=user_id,
            scheduled_date=query_date,
            total_blocks=len(schedule_blocks),
            itinerary=[DailyScheduleResponse.model_validate(block) for block in schedule_blocks],
        )
    except EntityNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e.message),
        )

