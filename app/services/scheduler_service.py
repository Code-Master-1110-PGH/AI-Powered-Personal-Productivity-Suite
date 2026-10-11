"""
Smart Scheduler Service Layer.

Orchestrates natural language task extraction, automatic task generation,
and calendar conflict detection & time slot allocation.
"""

from typing import List, Tuple
from datetime import date
from sqlalchemy.orm import Session
from app.core.exceptions import EntityNotFoundException, SchedulingConflictException
from app.models.task import Task
from app.models.daily_schedule import DailySchedule
from app.repositories.task_repository import TaskRepository
from app.repositories.schedule_repository import DailyScheduleRepository
from app.repositories.user_repository import UserRepository
from app.services.ai.task_nlu import TaskNLUService
from app.schemas.task import SmartTaskRequest, ExtractedTaskIntent


class SchedulerService:
    """Service orchestrating natural language task scheduling and itinerary retrieval."""

    def __init__(self, db: Session, ai_engine: TaskNLUService = None):
        self.db = db
        self.task_repo = TaskRepository(db)
        self.schedule_repo = DailyScheduleRepository(db)
        self.user_repo = UserRepository(db)
        self.ai_engine = ai_engine or TaskNLUService()

    def process_smart_task(
        self, request: SmartTaskRequest, allow_overlap: bool = True
    ) -> Tuple[Task, DailySchedule, ExtractedTaskIntent]:
        """
        Extract task intent from natural language, generate a Task record,
        and schedule it into DailySchedule within an atomic database unit of work.

        :param request: SmartTaskRequest containing the natural language text.
        :param allow_overlap: Whether to allow scheduling overlapping events or raise conflict.
        :return: Tuple of created Task, DailySchedule, and ExtractedTaskIntent.
        :raises EntityNotFoundException: If user does not exist.
        :raises SchedulingConflictException: If an unresolvable overlap occurs and allow_overlap is False.
        """
        # 1. Verify User
        user = self.user_repo.get_by_id(request.user_id)
        if not user:
            raise EntityNotFoundException(f"User with ID {request.user_id} does not exist.")

        # 2. Run Task NLU Engine
        extracted_intent: ExtractedTaskIntent = self.ai_engine.parse(
            request.natural_language_input,
            reference_datetime=request.reference_datetime,
        )

        # 3. Check for Scheduling Conflicts (if strict overlap checking desired)
        if not allow_overlap:
            conflicts = self.schedule_repo.find_conflicts(
                user_id=request.user_id,
                start_time=extracted_intent.target_start_time,
                end_time=extracted_intent.target_end_time,
            )
            if conflicts:
                conflicting_titles = [c.time_block_title for c in conflicts]
                raise SchedulingConflictException(
                    f"Scheduling conflict detected with existing slot(s): {', '.join(conflicting_titles)}"
                )

        # 4. Create Task Entity
        task_data = {
            "user_id": request.user_id,
            "title": extracted_intent.extracted_title,
            "description": f"Auto-scheduled from prompt: '{request.natural_language_input}'",
            "raw_prompt": request.natural_language_input,
            "priority": extracted_intent.priority,
            "estimated_duration_minutes": extracted_intent.duration_minutes,
            "due_date": extracted_intent.target_end_time,
        }
        task = self.task_repo.create(task_data)

        # 5. Create DailySchedule Linked Entity
        schedule_data = {
            "user_id": request.user_id,
            "task_id": task.id,
            "scheduled_date": extracted_intent.target_start_time.date(),
            "start_time": extracted_intent.target_start_time,
            "end_time": extracted_intent.target_end_time,
            "time_block_title": task.title,
            "is_completed": False,
        }
        schedule = self.schedule_repo.create(schedule_data)

        return task, schedule, extracted_intent

    def get_daily_itinerary(self, user_id: int, target_date: date) -> List[DailySchedule]:
        """
        Retrieve all chronologically ordered schedule blocks for a user on a given date.

        :param user_id: Target user ID.
        :param target_date: Target calendar date.
        :return: List of DailySchedule ORM entities.
        """
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise EntityNotFoundException(f"User with ID {user_id} does not exist.")

        return self.schedule_repo.get_itinerary(user_id=user_id, scheduled_date=target_date)

