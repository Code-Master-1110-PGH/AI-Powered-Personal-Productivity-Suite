"""
Resume Analysis Repository.

Handles persistence and querying for structured resume analyses.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.resume_analysis import ResumeAnalysis
from app.repositories.base import BaseRepository


class ResumeAnalysisRepository(BaseRepository[ResumeAnalysis]):
    """Repository for ResumeAnalysis entity operations."""

    def __init__(self, db: Session):
        super().__init__(ResumeAnalysis, db)

    def get_by_user_id(self, user_id: int) -> List[ResumeAnalysis]:
        """Fetch all resume analyses belonging to a specific user, ordered latest first."""
        return (
            self.db.query(ResumeAnalysis)
            .filter(ResumeAnalysis.user_id == user_id)
            .order_by(desc(ResumeAnalysis.created_at))
            .all()
        )

    def get_latest_by_user_id(self, user_id: int) -> Optional[ResumeAnalysis]:
        """Fetch the single most recent resume analysis for a user."""
        return (
            self.db.query(ResumeAnalysis)
            .filter(ResumeAnalysis.user_id == user_id)
            .order_by(desc(ResumeAnalysis.created_at))
            .first()
        )

