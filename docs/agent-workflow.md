# Agent Workflow

## State machine

```text
PROPOSED
  |  | +--> REJECTED
  |
  +--> EDITED --> APPROVED --> EXECUTED --> VERIFIED
```

## Agent loop

1. Observe available lead context.
2. Reason over qualification criteria.
3. Produce structured result.
4. Recommend a next action.
5. Generate outreach where applicable.
6. Wait for human approval.
7. Execute approved action through a deterministic tool.
8. Verify result.
9. Record the run and outcome.

## Prompt policy

Prompts must:
- require structured output;
- prohibit unsupported factual claims;
- identify missing context;
- avoid autonomous consequential actions;
- carry a version identifier for auditability.
