"""
Daily Schedule ORM Model.

Links Tasks to specific chronological time blocks and dates.
Includes composite indexing for efficient itinerary querying.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.core.database import Base


class DailySchedule(Base):
    """
    SQLAlchemy ORM model mapping tasks and events to temporal schedule slots.
    """
    __tablename__ = "daily_schedules"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=True, index=True)

    scheduled_date = Column(Date, nullable=False, index=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    
    time_block_title = Column(String(255), nullable=False)
    is_completed = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    user = relationship("User", back_populates="schedules")
    task = relationship("Task", back_populates="schedules")

    # Composite indexes for high-throughput queries
    __table_args__ = (
        Index("idx_daily_schedule_user_date", "user_id", "scheduled_date"),
        Index("idx_daily_schedule_user_time", "user_id", "start_time", "end_time"),
    )

    def __repr__(self) -> str:
        return (
            f"<DailySchedule(id={self.id}, user_id={self.user_id}, "
            f"date={self.scheduled_date}, time='{self.start_time} - {self.end_time}')>"
        )

