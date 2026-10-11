"""
Task Natural Language Understanding (NLU) Service.

Parses natural language scheduling requests (e.g., "Schedule a mock interview tomorrow at 5 PM")
into structured intents, clean task titles, priorities, timestamps, and durations.
"""

import re
from datetime import datetime, timedelta, time, timezone
from typing import Any, Dict, Optional, Tuple
from app.services.ai.base import BaseNLUService
from app.models.task import TaskPriority
from app.schemas.task import ExtractedTaskIntent


class TaskNLUService(BaseNLUService):
    """
    Inference service for parsing natural language scheduling inputs.
    """

    WEEKDAYS = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6,
    }

    def parse(self, text: str, **kwargs: Any) -> ExtractedTaskIntent:
        """
        Parse unstructured task prompt into structured ExtractedTaskIntent.

        :param text: Natural language input prompt (e.g. "Schedule a mock interview tomorrow at 5 PM").
        :param kwargs: reference_datetime: datetime (defaults to current UTC datetime).
        :return: ExtractedTaskIntent domain object.
        """
        ref_dt: datetime = kwargs.get("reference_datetime") or datetime.now(timezone.utc)
        
        # 1. Detect Intent
        intent = self._detect_intent(text)

        # 2. Extract Priority
        priority = self._extract_priority(text)

        # 3. Extract Duration
        duration_minutes = self._extract_duration(text)

        # 4. Extract Date & Time
        target_start_time, temporal_confidence = self._extract_datetime(text, ref_dt)
        target_end_time = target_start_time + timedelta(minutes=duration_minutes)

        # 5. Extract Clean Task Title
        extracted_title = self._extract_clean_title(text)

        confidence_score = min(max(temporal_confidence * 0.95, 0.65), 1.0)

        return ExtractedTaskIntent(
            raw_input=text,
            intent=intent,
            extracted_title=extracted_title,
            priority=priority,
            target_start_time=target_start_time,
            target_end_time=target_end_time,
            duration_minutes=duration_minutes,
            confidence_score=round(confidence_score, 2),
        )

    def _detect_intent(self, text: str) -> str:
        """Classify user intent based on primary directive."""
        lower = text.lower()
        if any(w in lower for w in ["interview", "mock interview"]):
            return "SCHEDULE_INTERVIEW"
        if any(w in lower for w in ["meeting", "sync", "1:1", "standup", "call"]):
            return "SCHEDULE_MEETING"
        if any(w in lower for w in ["review", "code review", "pr review"]):
            return "SCHEDULE_REVIEW"
        if any(w in lower for w in ["reminder", "remind me"]):
            return "SET_REMINDER"
        return "SCHEDULE_TASK"

    def _extract_priority(self, text: str) -> TaskPriority:
        """Determine task priority from urgent / critical keywords."""
        lower = text.lower()
        if any(w in lower for w in ["urgent", "asap", "emergency", "critical", "highest priority"]):
            return TaskPriority.URGENT
        if any(w in lower for w in ["high priority", "important", "vital", "crucial"]):
            return TaskPriority.HIGH
        if any(w in lower for w in ["low priority", "optional", "someday", "when free"]):
            return TaskPriority.LOW
        return TaskPriority.MEDIUM

    def _extract_duration(self, text: str) -> int:
        """Detect duration expressions (e.g. 'for 45 mins', 'for 2 hours'). Default: 60 mins."""
        match_hours = re.search(r"(?:for|duration)\s+(\d+(?:\.\d+)?)\s*(?:hour|hours|hr|hrs)", text, re.IGNORECASE)
        if match_hours:
            return int(float(match_hours.group(1)) * 60)

        match_mins = re.search(r"(?:for|duration)\s+(\d+)\s*(?:minute|minutes|min|mins)", text, re.IGNORECASE)
        if match_mins:
            return int(match_mins.group(1))

        return 60  # Standard default 1 hour slot

    def _extract_datetime(self, text: str, ref_dt: datetime) -> Tuple[datetime, float]:
        """Extract target calendar date and clock time from natural language."""
        lower = text.lower()
        target_date = ref_dt.date()
        date_matched = False
        time_matched = False

        # --- Date Resolution ---
        if "day after tomorrow" in lower:
            target_date = ref_dt.date() + timedelta(days=2)
            date_matched = True
        elif "tomorrow" in lower:
            target_date = ref_dt.date() + timedelta(days=1)
            date_matched = True
        elif "today" in lower:
            target_date = ref_dt.date()
            date_matched = True
        else:
            # Check for weekday (e.g., "on friday", "next monday")
            for day_name, day_idx in self.WEEKDAYS.items():
                if day_name in lower:
                    current_idx = ref_dt.weekday()
                    days_ahead = (day_idx - current_idx) % 7
                    if days_ahead == 0 or "next" in lower:
                        days_ahead += 7
                    target_date = ref_dt.date() + timedelta(days=days_ahead)
                    date_matched = True
                    break

        # --- Time Resolution ---
        # Match "at 5 PM", "at 5:30 pm", "5pm", "17:00"
        time_match = re.search(r"(?:at\s+)?(\d{1,2})(?::(\d{2}))?\s*(am|pm)\b", lower)
        target_hour = 17  # Default 5:00 PM if unspecified
        target_minute = 0

        if time_match:
            hour = int(time_match.group(1))
            minute = int(time_match.group(2)) if time_match.group(2) else 0
            meridiem = time_match.group(3)

            if meridiem == "pm" and hour != 12:
                hour += 12
            elif meridiem == "am" and hour == 12:
                hour = 0
            target_hour = hour
            target_minute = minute
            time_matched = True
        elif "noon" in lower:
            target_hour = 12
            target_minute = 0
            time_matched = True
        elif "morning" in lower:
            target_hour = 9
            target_minute = 0
            time_matched = True
        elif "afternoon" in lower:
            target_hour = 14
            target_minute = 0
            time_matched = True
        elif "evening" in lower:
            target_hour = 18
            target_minute = 0
            time_matched = True

        target_time = time(hour=target_hour, minute=target_minute)
        combined_dt = datetime.combine(target_date, target_time)
        # Ensure UTC timezone awareness if reference was tz-aware
        if ref_dt.tzinfo:
            combined_dt = combined_dt.replace(tzinfo=ref_dt.tzinfo)

        confidence = 0.95 if (date_matched and time_matched) else (0.80 if (date_matched or time_matched) else 0.65)
        return combined_dt, confidence

    def _extract_clean_title(self, text: str) -> str:
        """Strip filler commands and temporal clauses to yield a crisp task title."""
        cleaned = text.strip()

        # 1. Remove leading imperative verbs like "schedule", "please set up", "add"
        cleaned = re.sub(r"^(?:please\s+)?(?:schedule|create|add|set\s+up|book|arrange)\b\s*", "", cleaned, flags=re.IGNORECASE)

        # 2. Remove priority labels (e.g. urgent, asap, critical)
        cleaned = re.sub(r"\b(?:urgent|asap|critical|high priority|low priority)\b", "", cleaned, flags=re.IGNORECASE)

        # 3. Remove leading articles if left orphaned (e.g. "an", "a", "the")
        cleaned = re.sub(r"^(?:an|a|the)\b\s*", "", cleaned, flags=re.IGNORECASE)

        # 4. Remove temporal clauses like "tomorrow at 5 PM", "next monday", "at 10am"
        cleaned = re.sub(r"\b(?:tomorrow|today|day after tomorrow|yesterday)\b", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\b(?:at\s+)?\d{1,2}(?::\d{2})?\s*(?:am|pm)\b", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\b(?:for|duration)\s+\d+(?:\.\d+)?\s*(?:hours?|hrs?|minutes?|mins?)\b", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\b(?:on\s+)?(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\b(?:next\s+week|this\s+week|in\s+the\s+(?:morning|afternoon|evening)|at\s+noon)\b", "", cleaned, flags=re.IGNORECASE)

        # 5. Clean trailing/leading prepositions or punctuation
        cleaned = re.sub(r"^(?:for|at|on|to)\b\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s+\b(?:for|at|on|to)\b\s*$", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s+", " ", cleaned).strip(" .,-")

        if not cleaned:
            return "Scheduled Task"

        return cleaned[0].upper() + cleaned[1:]
