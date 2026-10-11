"""
API v1 Router Aggregator.

Consolidates all v1 endpoint sub-routers under unified prefixes and tags.
"""

from fastapi import APIRouter
from app.api.v1.endpoints import users, resume, tasks, schedules

api_router = APIRouter()

# Health check
@api_router.get("/health", tags=["Health"], summary="System health check")
def health_check():
    return {"status": "healthy", "service": "AI-Powered Personal Productivity Suite"}

api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(resume.router, tags=["Resume Reviewer"])
api_router.include_router(tasks.router, tags=["Smart Scheduler & Tasks"])
api_router.include_router(schedules.router, prefix="/schedules", tags=["Daily Schedules & Itineraries"])

