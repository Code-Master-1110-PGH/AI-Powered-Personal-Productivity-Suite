"""
Resume Analysis ORM Model.

Stores raw resume text and AI-extracted structured information such as
candidate details, categorized skills, quantified metrics, and evaluation scores.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class ResumeAnalysis(Base):
    """
    SQLAlchemy ORM model storing structured extraction results from unstructured resume text.
    """
    __tablename__ = "resume_analyses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Raw unstructured text
    raw_text = Column(Text, nullable=False)
    
    # Extracted structured metadata
    candidate_name = Column(String(255), nullable=True)
    summary = Column(Text, nullable=True)
    
    # Structured JSON data:
    # skills format: [{"category": "Languages", "skills": ["Python", "SQL"]}, ...]
    skills = Column(JSON, nullable=False, default=list)
    
    # metrics format: [{"metric": "Latency reduced by 40%", "category": "Performance", "quantified_value": "40%"}, ...]
    metrics = Column(JSON, nullable=False, default=list)
    
    # Quantitative quality score (0.0 to 100.0)
    overall_score = Column(Float, nullable=False, default=0.0)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationship to user
    user = relationship("User", back_populates="resume_analyses")

    def __repr__(self) -> str:
        return f"<ResumeAnalysis(id={self.id}, user_id={self.user_id}, score={self.overall_score})>"

