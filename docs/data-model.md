# Data Model

## leads

- id
- name
- company
- role
- email
- website
- industry
- company_size
- source
- notes
- created_at
- updated_at

## lead_scores

- id
- lead_id
- icp_fit
- company_potential
- role_relevance
- buying_signal
- data_quality
- overall_score
- rationale
- created_at

## qualification_results

- id
- lead_id
- qualification
- reasons
- risks
- confidence
- model
- agent_run_id
- created_at

## outreach_drafts

- id
- lead_id
- subject
- message
- personalization_points
- confidence
- status
- created_at
- updated_at

## actions

- id
- lead_id
- type
- payload
- status
- proposed_at
- approved_at
- executed_at
- verified_at

## activity_logs

- id
- lead_id
- action_id
- event_type
- metadata
- created_at

## agent_runs

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
