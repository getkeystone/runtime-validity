# Track A Runtime Validity

Reference implementation for experiments in runtime validity and revalidation before consequential AI actions.

## Current Status

Early engineering and research implementation.

The current implementation evaluates a narrow runtime-governance case:

```text
prior decision
    |
    | contains authority_valid obligation
    v
POST /decide
    |
    | compare prior expected authority
    | with current supplied runtime authority
    v
MATCH       MISMATCH
  |             |
PROCEED        HOLD
```

For `revalidation_mode: "none"`, the authority obligation is not evaluated and the result records `NOT_EVALUATED`.

The implementation also returns structured evidence for the decision and retains the resulting record in process-local memory so it can be retrieved by `record_id`.

This is a reference implementation for controlled experiments. It is not evidence that the governance mechanism is complete, correct, or suitable for production use.

## Requirements

Python 3.12 or newer.

## Setup

Clone the repository and enter the project directory:

```bash
git clone https://github.com/getkeystone/track-a-runtime-validity.git
cd track-a-runtime-validity
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install the project and development dependencies:

```bash
python -m pip install -e ".[dev]"
```

## Run the API

Start the development server:

```bash
python -m uvicorn track_a.api:app --reload
```

The API is available at:

```text
http://127.0.0.1:8000
```

FastAPI interactive documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Exercise `/decide`

Send a request where the current authority condition still matches the prior obligation:

```bash
curl -s \
  -X POST \
  http://127.0.0.1:8000/decide \
  -H "Content-Type: application/json" \
  -d '{
    "action_proposal": "send customer notification",
    "prior_decision": {
      "decision_id": "decision-123",
      "outcome": "PROCEED",
      "obligations": [
        {
          "obligation_id": "authority-1",
          "kind": "authority_valid",
          "expected": true
        }
      ]
    },
    "runtime_state": {
      "authority_valid": true
    },
    "revalidation_mode": "full"
  }'
```

The response contains `PROCEED` and structured evidence:

```json
{
  "outcome": "PROCEED",
  "evidence": {
    "record_id": "<uuid>",
    "created_at": "<UTC timestamp>",
    "schema_version": "1",
    "action_proposal": "send customer notification",
    "prior_decision_id": "decision-123",
    "revalidation_mode": "full",
    "obligation_evaluations": [
      {
        "obligation_id": "authority-1",
        "kind": "authority_valid",
        "expected": true,
        "current": true,
        "result": "MATCH"
      }
    ]
  }
}
```

If the same request supplies:

```json
{
  "runtime_state": {
    "authority_valid": false
  }
}
```

under `revalidation_mode: "full"`, the authority evaluation records `MISMATCH` and the decision outcome becomes `HOLD`.

For this implementation, `HOLD` is a design choice for an authority mismatch. It is not a research conclusion that every authority change should result in `HOLD`.

## Retrieve a Decision Record

A successful `/decide` request produces a `record_id`.

Retrieve that record while the same service process is running:

```bash
curl -s \
  http://127.0.0.1:8000/records/<record_id>
```

A known record returns the same decision outcome and evidence.

An unknown valid UUID returns HTTP 404.

A malformed UUID is rejected with HTTP 422.

The record store is process-local memory. Records are lost when the process exits and are not shared between service instances.

## Run Tests

```bash
git diff --check
python -m pytest -v
```

Current verified test suite:

```text
12 passed
```

The tests currently cover matching authority, authority mismatch, skipped revalidation, structured evidence, record metadata, request validation, record retrieval, unknown records, and malformed record identifiers.

## Current Increment Progression

```text
001  Executable decision boundary
002  Prior decision obligations
003  Current authority state representation
004  Authority obligation comparison
005  Structured decision evidence
006  Decision record metadata
007  Process-local decision record retrieval
```

Detailed increment records are under:

```text
docs/increments/
```

## Project Structure

```text
track-a-runtime-validity/
├── docs/
│   └── increments/
│       ├── 001-executable-boundary.md
│       ├── 002-prior-decision-obligations.md
│       ├── 003-current-authority-state.md
│       ├── 004-authority-obligation-comparison.md
│       ├── 005-decision-evidence-response.md
│       ├── 006-decision-record-metadata.md
│       └── 007-decision-record-retrieval.md
├── src/
│   └── track_a/
│       ├── __init__.py
│       └── api.py
├── tests/
│   └── test_api.py
├── .gitignore
├── pyproject.toml
└── README.md
```

## Implemented Scope

The implementation currently provides an executable HTTP decision boundary, explicit prior-decision obligations, caller-supplied runtime authority state, obligation comparison under full revalidation, `PROCEED` and `HOLD` outcomes, structured obligation-evaluation evidence, UUID and UTC record metadata, and process-local record retrieval.

## Current Limitations

The current authority state is supplied directly by the caller. The implementation does not yet establish that this value came from an authoritative source.

Decision records are retained only in process memory and are not durable across restarts.

Only the `authority_valid` obligation is implemented.

The implementation does not yet provide external action-boundary enforcement, durable evidence storage, cryptographic integrity, policy or tool version tracking, distributed-state guarantees, or a general material-change taxonomy.

Structured evidence records what this implementation evaluated. It does not prove that the supplied evidence was correct or that the resulting governance decision was semantically justified.
