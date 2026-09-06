# Product Requirements Document

## 1. Problem

Lead-generation work is fragmented across lead lists, company information, notes and outreach activity. Users need to decide which leads deserve attention and what to do next.

## 2. Goal

Build an agent that transforms lead records into qualified opportunities, ranked priorities, recommended actions and personalized outreach drafts, with explicit human approval before consequential execution.

## 3. Primary user story

> As a sales operator, I want to give the agent my lead list and have it identify the most promising leads, explain its reasoning, recommend next actions, and prepare outreach that I can approve or edit.

## 4. MVP requirements

### Lead intake
- Import CSV.
- Add/edit a lead manually.
- View normalized lead records.

### Qualification
- Evaluate ICP fit.
- Identify relevant and missing information.
- Produce structured qualification reasoning.

### Scoring
- Calculate a configurable 0–100 priority score.
- Show score factors and rationale.

### Action planning
- Recommend a next action and objective.
- Show confidence and supporting context.

### Outreach
- Generate personalized outreach.
- Use only supplied or retrieved facts.
- Allow editing and regeneration.

### Approval
- Approve, reject or edit proposed actions.
- Prevent consequential execution without approval.

### Activity
- Record recommendations, approvals, executions and outcomes.
- Make agent runs auditable.

## 5. Golden-path demo

1. Import a demo lead list.
2. Ask the agent to find the five leads worth contacting today.
3. Agent qualifies and scores leads.
4. Agent explains the ranking.
5. Agent drafts personalized outreach.
6. User edits or approves a draft.
7. System records the approved action.
8. Agent reports the completed workflow.

## 6. MVP non-requirements

- Full CRM replacement
- Autonomous bulk outreach
- Payment processing
- Complex multi-tenant administration
- Large-scale web scraping
- Custom model training

## 7. Success criteria

A judge should understand the complete agent loop within a short demo: observe context, reason, prioritize, propose, obtain approval, execute and report.
