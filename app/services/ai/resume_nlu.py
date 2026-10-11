"""
Resume Natural Language Understanding (NLU) Service.

Analyzes raw unstructured resume text, extracting technical competencies,
quantifiable achievements/metrics, candidate identifiers, and computes
an evaluation score based on metric density and skill breadth.
"""

import re
from typing import Any, Dict, List
from app.services.ai.base import BaseNLUService
from app.schemas.resume import SkillCategory, QuantifiedMetric


class ResumeNLUService(BaseNLUService):
    """
    Inference service for parsing unstructured resume texts into structured analytics.
    """

    SKILL_TAXONOMY = {
        "Languages": [
            "Python", "JavaScript", "TypeScript", "Go", "Golang", "Java", "C++", "C#",
            "Rust", "SQL", "Ruby", "PHP", "Swift", "Kotlin", "Scala", "Bash", "Shell",
        ],
        "Frameworks & Libraries": [
            "FastAPI", "Django", "Flask", "React", "Next.js", "Vue.js", "Angular",
            "Spring Boot", "Express", "Node.js", "PyTorch", "TensorFlow", "Pandas",
            "NumPy", "SQLAlchemy", "LangChain", "Celery",
        ],
        "Cloud & Infrastructure": [
            "AWS", "Amazon Web Services", "Azure", "GCP", "Google Cloud", "Docker",
            "Kubernetes", "K8s", "Terraform", "CI/CD", "GitHub Actions", "Jenkins",
            "Prometheus", "Grafana", "Linux",
        ],
        "Databases & Storage": [
            "PostgreSQL", "Postgres", "MySQL", "Redis", "MongoDB", "Elasticsearch",
            "Cassandra", "DynamoDB", "SQLite", "Kafka", "RabbitMQ",
        ],
        "Architecture & Concepts": [
            "REST", "RESTful", "GraphQL", "Microservices", "System Design",
            "Distributed Systems", "Event-Driven Architecture", "OOP", "Object-Oriented Design",
            "gRPC", "Clean Architecture",
        ],
    }

    METRIC_PATTERNS = [
        # Percentage changes (e.g. "improved latency by 45%", "reduced costs by 30%")
        (
            re.compile(r"([^.\n]*?(?:increased|decreased|reduced|improved|boosted|optimized|accelerated|cut)\b[^.\n]*?\b(\d+(?:\.\d+)?%)[^.\n]*)", re.IGNORECASE),
            "Efficiency",
        ),
        # Latency / speed / throughput (e.g. "under 150ms", "50,000 QPS", "10k requests/sec")
        (
            re.compile(r"([^.\n]*?\b(\d+(?:\.\d+)?\s*(?:ms|seconds|qps|rps|tps))\b[^.\n]*)", re.IGNORECASE),
            "Performance",
        ),
        # Monetary impact (e.g. "$1.5M in annual savings", "$250K budget")
        (
            re.compile(r"([^.\n]*?(\$(?:\d+(?:\.\d+)?)\s*(?:[KkMmBb]|million|thousand|billion)?)[^.\n]*)", re.IGNORECASE),
            "Financial/Cost",
        ),
        # Scale & user metrics (e.g. "10M+ daily active users", "500K records", "99.99% uptime")
        (
            re.compile(r"([^.\n]*?\b(\d+(?:\.\d+)?\s*(?:[KkMmBb]\+?|million|thousand|billion|users|customers|queries|requests|uptime))\b[^.\n]*)", re.IGNORECASE),
            "Scale",
        ),
        # Team leadership & mentorship (e.g. "led team of 8 engineers", "mentored 5 junior devs")
        (
            re.compile(r"([^.\n]*?(?:led|managed|mentored|guided)\s+(?:a\s+)?team\s+of\s+(\d+)[^.\n]*)", re.IGNORECASE),
            "Leadership",
        ),
    ]

    def parse(self, text: str, **kwargs: Any) -> Dict[str, Any]:
        """
        Execute information extraction on resume text.
        """
        candidate_name = self._extract_candidate_name(text)
        summary = self._extract_summary(text)
        skills = self._extract_skills(text)
        metrics = self._extract_metrics(text)
        overall_score = self._compute_score(skills, metrics, text)

        return {
            "candidate_name": candidate_name,
            "summary": summary,
            "skills": [s.model_dump() for s in skills],
            "metrics": [m.model_dump() for m in metrics],
            "overall_score": overall_score,
        }

    def _extract_candidate_name(self, text: str) -> str:
        """Heuristic name extraction: usually top 1-2 non-empty lines without digits or emails."""
        lines = [line.strip() for line in text.strip().split("\n") if line.strip()]
        for line in lines[:3]:
            # If line is short, doesn't contain email or digits or special chars, it's likely a name
            if "@" not in line and not any(char.isdigit() for char in line) and len(line.split()) <= 4:
                # remove labels like "Name:" if present
                clean_name = re.sub(r"^(name\s*:\s*)", "", line, flags=re.IGNORECASE).strip()
                if clean_name:
                    return clean_name
        return "Anonymous Candidate"

    def _extract_summary(self, text: str) -> str:
        """Extract opening profile summary or first descriptive block."""
        match = re.search(r"(?:summary|profile|about\s+me)[\s:]*\n?(.*?)(?:\n\s*\n|\bexperience\b|\bskills\b|\beducation\b)", text, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()[:500]
        # Fallback: first 200 characters of substantive text
        cleaned = " ".join(text.split()[:40])
        return cleaned[:250] + "..." if len(cleaned) > 250 else cleaned

    def _extract_skills(self, text: str) -> List[SkillCategory]:
        """Extract taxonomy skills based on exact word boundary regex matches."""
        categorized_skills: List[SkillCategory] = []

        for category, skill_list in self.SKILL_TAXONOMY.items():
            matched_for_category = []
            for skill in skill_list:
                pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"
                if re.search(pattern, text, re.IGNORECASE):
                    matched_for_category.append(skill)
            if matched_for_category:
                categorized_skills.append(
                    SkillCategory(category=category, skills=matched_for_category)
                )

        return categorized_skills

    def _extract_metrics(self, text: str) -> List[QuantifiedMetric]:
        """Extract statements containing quantified impact numbers and impact verbs."""
        extracted: List[QuantifiedMetric] = []
        seen_sentences = set()

        for pattern, category in self.METRIC_PATTERNS:
            for match in pattern.finditer(text):
                full_sentence = match.group(1).strip().strip("•-* \t")
                quant_value = match.group(2).strip()

                # Deduplicate similar sentences
                sentence_key = full_sentence.lower()
                if sentence_key in seen_sentences or len(full_sentence) < 15:
                    continue
                seen_sentences.add(sentence_key)

                extracted.append(
                    QuantifiedMetric(
                        metric=full_sentence,
                        category=category,
                        quantified_value=quant_value,
                    )
                )

        return extracted

    def _compute_score(
        self, skills: List[SkillCategory], metrics: List[QuantifiedMetric], raw_text: str
    ) -> float:
        """
        Compute an enterprise resume readiness score from 0.0 to 100.0.
        Factors:
        - Quantified impact metrics (up to 40 pts)
        - Skill domain coverage (up to 30 pts)
        - Specificity and text depth (up to 30 pts)
        """
        # Baseline score for valid structured resume text
        base_score = 20.0

        # Metric score: each strong quantified metric yields 10 points, capped at 40
        metric_score = min(len(metrics) * 10.0, 40.0)

        # Skill score: each recognized skill yields 4 points, capped at 25
        total_skills_count = sum(len(c.skills) for c in skills)
        skill_score = min(total_skills_count * 4.0, 25.0)

        # Domain diversity bonus
        domain_bonus = 5.0 if len(skills) >= 2 else 0.0

        # Word count & depth score (up to 10 points)
        word_count = len(raw_text.split())
        depth_score = min((word_count / 100.0) * 10.0, 10.0)

        total_score = round(base_score + metric_score + skill_score + domain_bonus + depth_score, 1)
        return min(max(total_score, 10.0), 100.0)
