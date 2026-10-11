"""
Resume Pydantic Schemas.

Validation and serialization models for Resume text input and structured extraction results.
"""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class SkillCategory(BaseModel):
    category: str = Field(..., description="Skill domain, e.g. Languages, Frameworks, Cloud & DevOps, Databases")
    skills: List[str] = Field(default_factory=list, description="Extracted skill keywords")


class QuantifiedMetric(BaseModel):
    metric: str = Field(..., description="Actionable sentence containing numerical impact")
    category: str = Field(..., description="Category, e.g. Performance, Scale, Revenue, Efficiency")
    quantified_value: str = Field(..., description="The quantitative impact, e.g. '40%', '$1.2M', '10k QPS'")


class ResumeAnalysisRequest(BaseModel):
    user_id: int = Field(..., description="ID of the user uploading the resume")
    resume_text: str = Field(..., min_length=20, description="Raw unstructured resume text")


class ResumeAnalysisResponse(BaseModel):
    id: int
    user_id: int
    candidate_name: Optional[str] = None
    summary: Optional[str] = None
    skills: List[SkillCategory] = Field(default_factory=list)
    metrics: List[QuantifiedMetric] = Field(default_factory=list)
    overall_score: float = Field(..., description="Calculated resume quality and impact score (0-100)")
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

