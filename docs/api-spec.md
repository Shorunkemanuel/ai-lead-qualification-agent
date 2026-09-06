# API Specification

## Lead import

`POST /api/leads/import`

Accept CSV and return import summary.

## List leads

`GET /api/leads`

Supports basic filtering and sorting.

## Qualify

`POST /api/leads/{id}/qualify`

Runs qualification and returns structured qualification result.

## Score

`POST /api/leads/{id}/score`

Calculates and persists the lead priority score.

## Generate outreach

`POST /api/leads/{id}/outreach`

Generates an editable outreach draft.

## Approval

`POST /api/actions/{id}/approve`
`POST /api/actions/{id}/reject`

Updates the action state after validating the current state.

## Execution

`POST /api/actions/{id}/execute`

Only approved actions may be executed.

## Activity

`GET /api/activity`

Returns audit events.

## Agent runs

`GET /api/agent-runs`

Returns model-operation records for debugging and transparency.
