"""
Resume Service Layer.

Orchestrates resume analysis business logic, interacting with the AI NLU
inference engine and the persistence repositories.
"""

from typing import List
from sqlalchemy.orm import Session
from app.core.exceptions import EntityNotFoundException
from app.models.resume_analysis import ResumeAnalysis
from app.repositories.resume_repository import ResumeAnalysisRepository
from app.repositories.user_repository import UserRepository
from app.services.ai.resume_nlu import ResumeNLUService
from app.schemas.resume import ResumeAnalysisRequest


class ResumeService:
    """Service orchestrating resume analysis and persistence workflows."""

    def __init__(self, db: Session, ai_engine: ResumeNLUService = None):
        self.db = db
        self.resume_repo = ResumeAnalysisRepository(db)
        self.user_repo = UserRepository(db)
        self.ai_engine = ai_engine or ResumeNLUService()

    def analyze_and_store(self, request: ResumeAnalysisRequest) -> ResumeAnalysis:
        """
        Validate user existence, run AI NLU extraction, and persist structured record.

        :param request: Validated ResumeAnalysisRequest schema.
        :return: Created ResumeAnalysis ORM entity.
        :raises EntityNotFoundException: If user_id is invalid.
        """
        user = self.user_repo.get_by_id(request.user_id)
        if not user:
            raise EntityNotFoundException(f"User with ID {request.user_id} does not exist.")

        # Run AI NLU extraction
        extraction_result = self.ai_engine.parse(request.resume_text)

        # Map to persistence model
        analysis_data = {
            "user_id": request.user_id,
            "raw_text": request.resume_text,
            "candidate_name": extraction_result["candidate_name"],
            "summary": extraction_result["summary"],
            "skills": extraction_result["skills"],
            "metrics": extraction_result["metrics"],
            "overall_score": extraction_result["overall_score"],
        }

        return self.resume_repo.create(analysis_data)

    def get_user_resumes(self, user_id: int) -> List[ResumeAnalysis]:
        """Retrieve all resume analyses submitted by a user."""
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise EntityNotFoundException(f"User with ID {user_id} does not exist.")
        return self.resume_repo.get_by_user_id(user_id)

