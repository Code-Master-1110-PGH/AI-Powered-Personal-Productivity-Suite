<div align="center">

# ⚡ SYNAPSE OS: AI-POWERED PRODUCTIVITY SUITE
### *Full-Stack Enterprise Monorepo • Next.js 14 • FastAPI • SQLAlchemy • Dual-NLU*

<p align="center">
  <a href="https://git.io/typing-svg">
    <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=21&duration=2800&pause=1000&color=00F0FF&center=true&vCenter=true&width=750&lines=Bridging+Daily+Tasks+with+Long-Term+Career+Growth;Dual-Engine+NLU+Pipelines+(Micro-Temporal+%2B+Macro-Career);Sub-Millisecond+Relational+SQL+Indexing+%26+FastAPI+Async+Core;Fluid+Framer+Motion+Physics+%26+Obsidian+Glassmorphism" alt="Typing SVG" />
  </a>
</p>

[![GitHub repo](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Code-Master-1110-PGH/AI-Powered-Personal-Productivity-Suite)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.style?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/Build-Passing-10B981?style=for-the-badge&logo=checkmarx&logoColor=white)]()
[![Test Coverage](https://img.shields.io/badge/Pytest-10%2F10%20Passed-00F0FF?style=for-the-badge&logo=pytest&logoColor=white)]()

<br />

<!-- ======================================================================= -->
<!-- TECH STACK SHIELDS -->
<!-- ======================================================================= -->

### 🛠️ Full-Stack Technology Stack

| Architecture Tier | Technology Badges |
| :--- | :--- |
| **Frontend UI / UX** | ![Next.js 14](https://img.shields.io/badge/Next.js%2014-000000?style=flat-square&logo=nextdotjs&logoColor=white) ![React 18](https://img.shields.io/badge/React%2018-20232A?style=flat-square&logo=react&logoColor=61DAFB) ![Framer Motion](https://img.shields.io/badge/Framer%20Motion%2011-0055FF?style=flat-square&logo=framer&logoColor=white) ![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS%203-38B2AC?style=flat-square&logo=tailwind-css&logoColor=white) ![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=flat-square&logo=typescript&logoColor=white) |
| **Backend & Services** | ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white) ![Python 3.13](https://img.shields.io/badge/Python%203.13-3776AB?style=flat-square&logo=python&logoColor=white) ![Pydantic v2](https://img.shields.io/badge/Pydantic%20v2-E92063?style=flat-square&logo=pydantic&logoColor=white) ![Uvicorn](https://img.shields.io/badge/Uvicorn-499848?style=flat-square&logo=gunicorn&logoColor=white) ![REST API](https://img.shields.io/badge/REST-OpenAPI%203.1-blue?style=flat-square) |
| **Database & AI Inference** | ![SQLAlchemy 2.0](https://img.shields.io/badge/SQLAlchemy%202.0-D71F00?style=flat-square&logo=sqlalchemy&logoColor=white) ![SQLite / PostgreSQL](https://img.shields.io/badge/Relational%20SQL-336791?style=flat-square&logo=postgresql&logoColor=white) ![Dual NLU](https://img.shields.io/badge/Dual%20NLU%20Engines-8B5CF6?style=flat-square&logo=openai&logoColor=white) ![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white) |

</div>

---

<!-- ======================================================================= -->
<!-- HERO VISUALS -->
<!-- ======================================================================= -->

## 🎬 Hero Visuals & Product Walkthrough

<div align="center">

### 🖥️ Dual-Pane UI/UX Interactive Experience
```
+--------------------------------------------------------------------------------------------------+
|                                    SYNAPSE OS: COMMAND CENTER                                    |
|   [Career Index: 86/100]    [Skills: 18 Indexed]    [Metrics: 5 KPIs]    [Agenda: 3 Active]      |
|                                                                                                  |
|      <<< MICRO-PRODUCTIVITY: SCHEDULER >>>         |         <<< MACRO-PRODUCTIVITY: VAULT >>>   |
|                                                    |                                             |
|   ⚡ Glowing Natural Language Chat Input           |   📁 Drag & Drop Resume Upload Zone         |
|   "Schedule mock interview tomorrow at 5 PM"       |   "Reduced API latency by 45% on AWS"       |
|                                                    |                                             |
|   📅 Interactive Chronological Agenda:             |   🔬 Neural Document Scanner Active:        |
|   • 15:00 - 17:00 Architecture Review              |   • Circular SVG Career Readiness Gauge     |
|   • 17:00 - 18:30 Mock Interview [URGENT]          |   • Categorized Floating Skill Tags         |
|   • 19:00 - 19:45 Team Retrospective               |   • Quantified KPI Achievement Cards        |
+--------------------------------------------------------------------------------------------------+
```
> *Tip: Drop an animated GIF demo of your dashboard here (`docs/assets/demo.gif`).*

<br/>

### 📐 End-to-End Multi-Tiered System Architecture
```
[Client Web Browser / Next.js 14]
               │
               ▼  HTTP REST (JSON Payloads)
┌─────────────────────────────────────────────────────────────────┐
│ FastAPI Presentation Tier (Port 8000)                           │
│   • Pydantic v2 Contract Validation & Serialization             │
│   • Scoped Dependency Injection (get_db, Service Factories)     │
└──────────────┬──────────────────────────────────┬───────────────┘
               │                                  │
               ▼                                  ▼
┌───────────────────────────────┐  ┌───────────────────────────────┐
│ ResumeService                 │  │ SchedulerService              │
│   └─► ResumeNLUService        │  │   └─► TaskNLUService          │
│       • Taxonomy Matching     │  │       • Relative Date Parsing │
│       • Metric Tokenizer      │  │       • Priority & Intent NLU │
│       • Executive Scoring     │  │       • Conflict Detection    │
└──────────────┬────────────────┘  └──────────────┬────────────────┘
               │ (Repository Call)                │ (Repository Call)
               ▼                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│ Data Access Layer (Repository Pattern: BaseRepository[T])       │
│   UserRepository • ResumeRepo • TaskRepo • ScheduleRepo         │
└──────────────────────────────┬──────────────────────────────────┘
                               ▼  SQLAlchemy 2.0 ORM Session
┌─────────────────────────────────────────────────────────────────┐
│ Relational Database Storage (SQLite / PostgreSQL)               │
│   • users (1:N) resume_analyses • tasks (1:N) daily_schedules   │
│   • ON DELETE CASCADE • Composite B-Tree Indexes                │
└─────────────────────────────────────────────────────────────────┘
```
> *Tip: Drop a high-resolution export of your system diagram here (`docs/assets/architecture.png`).*

</div>

---

<!-- ======================================================================= -->
<!-- DUAL-ENGINE BREAKDOWN -->
<!-- ======================================================================= -->

## 💎 The "Dual-Engine" Architectural Paradigm

Most productivity suites either handle short-term tasks or long-term career planning. **Synapse OS** bridges this divide by unifying **tactical daily execution** (Micro) and **strategic career capital** (Macro) into a single relational graph:

<table width="100%">
  <thead>
    <tr>
      <th width="50%" align="center"><h3>🔵 AI Smart Scheduler (Micro-Productivity)</h3></th>
      <th width="50%" align="center"><h3>🟣 Smart Resume Reviewer (Macro-Productivity)</h3></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td valign="top">
        <b>Primary Mission:</b> Frictionless daily execution via natural language intent extraction.<br/><br/>
        <b>Core Capabilities:</b>
        <ul>
          <li><b>Temporal Resolver:</b> Translates colloquial expressions (<code>"tomorrow at 5 PM"</code>, <code>"next Monday for 90 mins"</code>, <code>"at noon"</code>) into UTC timestamps.</li>
          <li><b>Priority Classifier:</b> Maps urgency indicators (<code>"critical"</code>, <code>"urgent"</code>, <code>"when free"</code>) to strict enums (<code>URGENT</code>, <code>HIGH</code>, <code>MEDIUM</code>, <code>LOW</code>).</li>
          <li><b>Atomic SQL Reservation:</b> Creates a <code>Task</code> entity and maps it into a <code>DailySchedule</code> block within an atomic database unit of work.</li>
          <li><b>Collision Detection:</b> Validates schedule boundaries against existing calendar blocks to avoid overlaps.</li>
        </ul>
        <pre><code>POST /api/v1/smart-tasks
"Schedule an urgent mock interview tomorrow at 5 PM for 90 mins"
⬇️
[Task: 'Mock interview' | URGENT | 17:00 - 18:30]</code></pre>
      </td>
      <td valign="top">
        <b>Primary Mission:</b> Continuous career benchmarking, skills indexing, and metric parsing.<br/><br/>
        <b>Core Capabilities:</b>
        <ul>
          <li><b>Multi-Domain Skill Taxonomy:</b> Automatically indexes keywords across 5 technical tiers (Languages, Frameworks, Cloud & DevOps, Databases, Architecture).</li>
          <li><b>Quantified Impact Parser:</b> Extracts measurable achievements (<code>"reduced latency by 45%"</code>, <code>"$250K cost savings"</code>, <code>"10M+ users"</code>, <code>"team of 8"</code>).</li>
          <li><b>Executive Readiness Gauge:</b> Algorithmic readiness score (0–100) weighting metric density, domain diversity, and depth.</li>
          <li><b>Hybrid Relational/JSON Schema:</b> Stores structured candidate metadata with native JSON columns for historical trend analysis.</li>
        </ul>
        <pre><code>POST /api/v1/analyze-resume
"Reduced API latency by 45% for 10M+ users on AWS"
⬇️
[Score: 86/100 | Category: Performance | Value: 45%]</code></pre>
      </td>
    </tr>
  </tbody>
</table>

---

<!-- ======================================================================= -->
<!-- END-TO-END DATA LIFECYCLE -->
<!-- ======================================================================= -->

## 🔄 End-to-End Data Flow & Architecture

1. **Client Event Ingestion**:
   - The user submits an instruction via the Next.js Framer Motion UI (e.g. natural language command or unstructured resume text).
2. **FastAPI Transport Layer**:
   - Strict Pydantic v2 models validate data types, string constraints, and datetime schemas.
   - Decoupled dependency injection (`deps.py`) handles transaction-safe database sessions (`get_db`).
3. **Dual AI Inference Engines**:
   - `TaskNLUService`: Normalizes verbs, strips filler tokens, resolves relative dates to UTC timestamps, and classifies priority.
   - `ResumeNLUService`: Scans for word-boundary taxonomy matches and regex metric patterns, computing an overall readiness score.
4. **Data Access Layer (Repository Pattern)**:
   - Specialized repositories (`TaskRepository`, `DailyScheduleRepository`, `ResumeAnalysisRepository`) encapsulate raw ORM queries behind domain abstractions.
5. **Relational Database Persistence (SQL)**:
   - Atomic unit of work persists data with foreign key cascades and composite indexing (`idx_daily_schedule_user_date`) for fast itinerary queries.

---

<!-- ======================================================================= -->
<!-- LOCAL SETUP GUIDE -->
<!-- ======================================================================= -->

## 🚀 Quickstart & Local Setup Guide

### Prerequisites
- **Python 3.10+** (Python 3.13 recommended)
- **Node.js 18+** (Node.js 22 recommended) & npm
- **Git**

### 1. Clone Monorepo
```bash
git clone https://github.com/Code-Master-1110-PGH/AI-Powered-Personal-Productivity-Suite.git
cd AI-Powered-Personal-Productivity-Suite
```

### 2. Backend Setup (FastAPI & SQLAlchemy)
```bash
# Install Python dependencies
pip install -r requirements.txt

# Start the FastAPI server
python main.py

# 🚀 Server listening on: http://127.0.0.1:8000
# 📖 Interactive Swagger UI: http://127.0.0.1:8000/docs
# 📄 ReDoc Documentation: http://127.0.0.1:8000/redoc
```

### 3. Frontend Setup (Next.js 14 & Framer Motion)
```bash
# In a separate terminal, navigate to frontend/
cd frontend

# Install npm packages
npm install

# Start Next.js development server
npm run dev

# 🌐 Application UI live at: http://localhost:3000
```

### 4. Run Test Suite
```bash
# Execute unit and integration test suite (100% passing)
python -m pytest -v
```

---

<!-- ======================================================================= -->
<!-- COLLAPSIBLE REST API REFERENCE -->
<!-- ======================================================================= -->

<details>
<summary><b>📡 Collapsible REST API Specification & Sample Payloads</b></summary>
<br/>

### `POST /api/v1/smart-tasks`
Extracts intent and schedules a task from natural language.

**Request:**
```json
{
  "user_id": 1,
  "natural_language_input": "Schedule an urgent mock interview tomorrow at 5 PM for 90 mins"
}
```

**Response (`201 Created`):**
```json
{
  "message": "Successfully extracted and scheduled task: 'Mock interview'",
  "task": {
    "id": 1,
    "user_id": 1,
    "title": "Mock interview",
    "status": "PENDING",
    "priority": "URGENT",
    "estimated_duration_minutes": 90
  },
  "schedule": {
    "id": 1,
    "scheduled_date": "2026-10-13",
    "start_time": "2026-10-13T17:00:00Z",
    "end_time": "2026-10-13T18:30:00Z",
    "time_block_title": "Mock interview",
    "is_completed": false
  },
  "nlu_metadata": {
    "intent": "SCHEDULE_INTERVIEW",
    "confidence_score": 0.95
  }
}
```

---

### `POST /api/v1/analyze-resume`
Extracts technical competencies, quantified metrics, and scores candidate readiness.

**Request:**
```json
{
  "user_id": 1,
  "resume_text": "Alex Mercer. Senior Architect. Reduced API latency by 45% for 10M+ users. Led team of 8 on AWS."
}
```

**Response (`201 Created`):**
```json
{
  "id": 1,
  "user_id": 1,
  "candidate_name": "Alex Mercer",
  "overall_score": 86.0,
  "skills": [
    { "category": "Cloud & Infrastructure", "skills": ["AWS"] },
    { "category": "Architecture & Concepts", "skills": ["Microservices", "REST"] }
  ],
  "metrics": [
    {
      "metric": "Reduced API latency by 45% for 10M+ users",
      "category": "Performance",
      "quantified_value": "45%"
    }
  ]
}
```

---

### `GET /api/v1/schedules/daily/{user_id}?date=YYYY-MM-DD`
Retrieves a chronological itinerary of all scheduled time blocks for a given date.

</details>

---

<div align="center">
  <sub>Architected with ❤️ by <b>Code-Master-1110-PGH</b> • Engineered for Distributed Systems & Tier-One Tech Roles</sub>
</div>
