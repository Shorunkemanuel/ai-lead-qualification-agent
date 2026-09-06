# Architecture

## High-level flow

```text
React/Vite UI
    |
    v
FastAPI API
    |
    v
Agent Orchestrator
    |
    +--> Lead Service
    +--> Qualification Service
    +--> Scoring Service
    +--> Outreach Service
    +--> Approval Service
    +--> Audit Service
    |
    v
AI Provider
    |
    v
Nebius Token Factory
    |
    v
NVIDIA Nemotron
```

## Architectural rule

The model reasons and proposes. Application services validate and execute.

This prevents the LLM from becoming the authority over database mutations or external actions.
