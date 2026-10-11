"""
API Dependency Injection Helpers.

Provides decoupled factory dependencies for FastAPI endpoint path operations.
"""

from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.resume_service import ResumeService
from app.services.scheduler_service import SchedulerService


def get_resume_service(db: Session = Depends(get_db)) -> ResumeService:
    """Dependency provider for ResumeService."""
    return ResumeService(db=db)


def get_scheduler_service(db: Session = Depends(get_db)) -> SchedulerService:
    """Dependency provider for SchedulerService."""
    return SchedulerService(db=db)

