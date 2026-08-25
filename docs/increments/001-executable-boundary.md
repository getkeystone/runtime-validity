# Increment 001: Executable Decision Boundary

Status: Complete

## Objective

Establish the smallest executable API boundary for Track A.

The uncertainty being removed is:

> Can the project accept a valid decision request through an HTTP API,
> validate its request shape, and return a predictable outcome?

## Observable Behavior

A valid request to:

`POST /decide`

returns:

```json
{"outcome":"PROCEED"}
```

An invalid request that violates the request contract is rejected before
the decision function executes.

## Acceptance Criteria

- [x] FastAPI application starts successfully.
- [x] `POST /decide` accepts a valid request.
- [x] A valid request returns HTTP 200.
- [x] A valid request returns `{"outcome":"PROCEED"}`.
- [x] An invalid `revalidation_mode` is rejected with HTTP 422.
- [x] Automated tests cover the valid and invalid cases.
- [x] A developer can install and run the project using repository documentation.

## Request Contract

The endpoint currently accepts:

- `action_proposal`: string
- `prior_decision_id`: string
- `revalidation_mode`: `"none"` or `"full"`

Example:

```json
{
  "action_proposal": "send customer notification",
  "prior_decision_id": "decision-123",
  "revalidation_mode": "full"
}
```

## Current Implementation

The API boundary is intentionally minimal.

`DecisionRequest` and the `/decide` route are colocated in
`src/track_a/api.py`.

The endpoint currently returns `PROCEED` for every request that passes
request validation.

## Out of Scope

This increment does not implement:

- governance decision logic
- material-change detection
- revalidation logic
- obligation tracking
- state persistence
- decision evidence records
- action-boundary enforcement
- Docker or deployment infrastructure
- CI

## Manual Verification

Valid request:

```bash
curl -i \
  -X POST \
  http://127.0.0.1:8000/decide \
  -H "Content-Type: application/json" \
  -d '{
    "action_proposal": "send customer notification",
    "prior_decision_id": "decision-123",
    "revalidation_mode": "full"
  }'
```

Observed result:

```text
HTTP/1.1 200 OK

{"outcome":"PROCEED"}
```

Invalid request using:

```json
"revalidation_mode": "sometimes"
```

Observed result:

```text
HTTP/1.1 422 Unprocessable Entity
```

## Automated Verification

Command:

```bash
python -m pytest -v
```

Observed result:

```text
2 passed in 0.16s
```

Verified behaviors:

- valid `/decide` request returns HTTP 200 and `PROCEED`
- invalid `revalidation_mode` returns HTTP 422

## Clean-Clone Reproducibility Verification

The repository was cloned into a separate temporary directory and exercised
using the documented setup instructions without relying on the development
working copy.

Verified sequence:

```text
clone repository
→ create fresh virtual environment
→ install project and development dependencies
→ run automated tests
→ start API server
→ exercise POST /decide
```

Automated test result:

```text
2 passed in 0.16s
```

API verification result:

```text
HTTP/1.1 200 OK

{"outcome":"PROCEED"}
```

An initial server start attempt failed because local port `8000` was already
in use by another process. After freeing the port, the API started and the
documented request completed successfully.

## Verification Environment

- Python 3.12.3
- FastAPI 0.141.1
- Pydantic 2.13.4
- pytest 8.4.2

## Known Limitations

`PROCEED` currently demonstrates executable API behavior only.

It is not evidence that the system performs runtime governance,
authorization revalidation, or safe consequential-action enforcement.

## Next Step

Increment 001 is complete.

The next increment should introduce the smallest governance-relevant behavior
needed to move beyond a trivially successful decision boundary.
