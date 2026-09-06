# Technical Specification v0.1 — LOCKED

**Status:** Locked for MVP implementation
**Product:** AI Lead Qualification & Outreach Operations Agent
**Track:** Best Apps & Agents

## 1. Architecture

React/Vite frontend → FastAPI backend → Agent Orchestrator → Tool/Service layer → Nebius Token Factory → NVIDIA Nemotron.

The backend owns the model credential and all consequential actions.

## 2. Stack

### Frontend
- React
- Vite
- TypeScript
- Lightweight dashboard UI

### Backend
- Python
- FastAPI
- Pydantic
- SQLAlchemy or SQLModel

### Database
- SQLite for MVP
- Schema designed for later PostgreSQL migration

### AI
- Nebius Token Factory
- NVIDIA Nemotron model selected from the models available to the project at implementation time
- OpenAI-compatible client interface

### Packaging/deployment
- Docker-compatible application
- Nebius AI Cloud / supported Nebius deployment path for the final hosted demo

## 3. Agent workflow

1. Normalize lead data.
2. Retrieve relevant lead context.
3. Qualify the lead.
4. Calculate priority score.
5. Produce recommended action.
6. Generate outreach draft if appropriate.
7. Create an approval request.
8. Execute only an approved action.
9. Verify and record the outcome.

## 4. Service boundaries

### AIProvider
Abstracts model inference from application logic.

Implementation:
`NebiusProvider`

Environment:
- `NEBIUS_API_KEY`
- `NEBIUS_BASE_URL`
- `NEBIUS_MODEL`

### AgentOrchestrator
Coordinates deterministic services and model calls.

### LeadService
CRUD, import and normalization.

### QualificationService
Structured AI qualification.

### ScoringService
Deterministic weighted scoring.

Initial weights:
- ICP fit: 30%
- Company potential: 20%
- Role relevance: 20%
- Buying signal: 20%
- Data quality: 10%

Thresholds:
- 80–100 HIGH
- 60–79 MEDIUM
- 40–59 LOW
- 0–39 NOT QUALIFIED

### OutreachService
Generates and stores editable outreach drafts.

### ApprovalService
Controls proposed → approved/rejected → executed state transitions.

### AuditService
Stores agent runs and action history.

## 5. Tool interface

Initial tools:

`lead.list()`
`lead.get()`
`lead.create()`
`lead.update()`
`qualification.evaluate()`
`lead.score()`
`outreach.generate()`
`action.propose()`
`action.approve()`
`action.reject()`
`action.execute()`
`activity.log()`

The model must never receive unrestricted database or shell access.

## 6. API

`POST /api/leads/import`
`GET /api/leads`
`GET /api/leads/{id}`
`POST /api/leads/{id}/qualify`
`POST /api/leads/{id}/score`
`POST /api/leads/{id}/outreach`
`GET /api/leads/{id}/outreach`
`POST /api/actions/{id}/approve`
`POST /api/actions/{id}/reject`
`POST /api/actions/{id}/execute`
`GET /api/activity`
`GET /api/agent-runs`
`GET /health`

## 7. Data model

Core entities:
- users
- leads
- lead_scores
- qualification_results
- outreach_drafts
- actions
- action_approvals
- activity_logs
- agent_runs

A Lead can have multiple qualification results, scores, drafts and activity records.

## 8. Agent run record

Minimum fields:
- id
- lead_id
- operation
- model
- prompt_version
- input_hash
- output
- status
- latency_ms
- created_at

## 9. Structured model outputs

Qualification:

```json
{
  "lead_id": "lead_001",
  "qualification": "HIGH",
  "score": 87,
  "fit_reasons": [],
  "risks": [],
  "recommended_action": "PERSONALIZED_OUTREACH",
  "confidence": 0.89
}
```

Outreach:

```json
{
  "subject": "...",
  "message": "...",
  "personalization_points": [],
  "confidence": 0.91
}
```

## 10. Safety and security

- Never commit API keys.
- Keep Nebius credentials server-side.
- Validate tool arguments.
- Require explicit approval for consequential actions.
- Log action state transitions.
- Do not allow arbitrary model-generated code execution.
- Do not fabricate lead facts.
- Clearly distinguish supplied facts, retrieved facts and AI inferences.

## 11. Implementation constraint

Do not expand the MVP into a general CRM or autonomous sales platform. New functionality requires an explicit scope decision.

## 12. Definition of done

The technical specification is implemented when the golden-path demo works end-to-end using Nebius Token Factory and an NVIDIA Nemotron model, with lead import, qualification, scoring, outreach generation, approval, execution logging and reporting.
