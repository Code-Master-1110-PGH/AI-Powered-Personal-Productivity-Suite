"""
Resume Reviewer Endpoints.

Handles unstructured resume text ingestion, AI extraction of skills and metrics,
and retrieval of historical resume evaluations.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.api.deps import get_resume_service
from app.core.exceptions import EntityNotFoundException
from app.services.resume_service import ResumeService
from app.schemas.resume import (
    ResumeAnalysisRequest,
    ResumeAnalysisResponse,
)

router = APIRouter()


@router.post(
    "/analyze-resume",
    response_model=ResumeAnalysisResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Analyze Resume Text with AI NLU",
    description=(
        "Accepts unstructured resume text, executes the Resume NLU pipeline to extract "
        "skills, quantified metrics, summary, and calculates an overall score, storing the "
        "structured record in the database."
    ),
)
def analyze_resume(
    request: ResumeAnalysisRequest,
    service: ResumeService = Depends(get_resume_service),
) -> ResumeAnalysisResponse:
    try:
        return service.analyze_and_store(request)
    except EntityNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e.message),
        )


@router.get(
    "/resumes/user/{user_id}",
    response_model=List[ResumeAnalysisResponse],
    summary="Get user's analyzed resumes",
    description="Retrieves all past resume analyses and scored extractions for a user.",
)
def get_user_resumes(
    user_id: int,
    service: ResumeService = Depends(get_resume_service),
) -> List[ResumeAnalysisResponse]:
    try:
        return service.get_user_resumes(user_id)
    except EntityNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e.message),
        )

