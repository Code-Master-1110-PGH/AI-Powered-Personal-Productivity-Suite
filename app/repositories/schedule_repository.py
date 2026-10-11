"""
Daily Schedule Repository.

Handles persistence and chronological itinerary queries for daily calendar blocks.
"""

from typing import List
from datetime import date, datetime
from sqlalchemy.orm import Session
from sqlalchemy import asc, and_
from app.models.daily_schedule import DailySchedule
from app.repositories.base import BaseRepository


class DailyScheduleRepository(BaseRepository[DailySchedule]):
    """Repository for DailySchedule entity operations."""

    def __init__(self, db: Session):
        super().__init__(DailySchedule, db)

    def get_itinerary(self, user_id: int, scheduled_date: date) -> List[DailySchedule]:
        """
        Fetch chronological itinerary for a specific user and date.
        Leverages composite index idx_daily_schedule_user_date.
        """
        return (
            self.db.query(DailySchedule)
            .filter(
                and_(
                    DailySchedule.user_id == user_id,
                    DailySchedule.scheduled_date == scheduled_date,
                )
            )
            .order_by(asc(DailySchedule.start_time))
            .all()
        )

    def find_conflicts(
        self, user_id: int, start_time: datetime, end_time: datetime
    ) -> List[DailySchedule]:
        """
        Check for any overlapping time blocks for the given user.
        Overlaps occur when: (Existing.start < New.end) AND (Existing.end > New.start).
        """
        return (
            self.db.query(DailySchedule)
            .filter(
                and_(
                    DailySchedule.user_id == user_id,
                    DailySchedule.start_time < end_time,
                    DailySchedule.end_time > start_time,
                )
            )
            .all()
        )

