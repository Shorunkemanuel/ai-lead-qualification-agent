# Security

## Secrets

All API credentials are environment variables. `.env` is ignored by Git.

## Authorization boundary

The frontend never receives the Nebius API key.

## AI safety

The model cannot directly:
- run shell commands;
- write arbitrary files;
- execute arbitrary code;
- send uncontrolled bulk messages.

## Approval boundary

Consequential actions require an explicit user approval state.

## Data integrity

All imported data is validated before persistence. Tool inputs are validated again at the service boundary.

## Auditability

Every AI operation and consequential action is recorded.
