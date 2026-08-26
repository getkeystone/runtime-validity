# Track A Runtime Validity

Track A is an experimental component of the broader Governed Execution runtime-governance reference implementation.

This repository isolates one research question: runtime validity and revalidation of prior governance decisions before consequential action.

The broader platform is intended to compose multiple governance mechanisms across control, execution, and evidence planes, with a separate action boundary governing whether system output may create external consequence.

Track A is deliberately developed and evaluated as a narrow component so its behavior, assumptions, failure modes, and evidence can be examined separately before broader integration.

Results from this repository should not be interpreted as validation of the broader platform architecture or of runtime governance generally.

## Relationship to the Broader Platform

Track A is one component in a larger Governed Execution engineering and research program.

Individual tracks isolate governance mechanisms or research questions so they can be implemented and tested independently. The broader platform is intended to study how those mechanisms interact when composed into a runtime system.

This repository therefore serves two roles:

1. A bounded experimental artifact for runtime-validity research.
2. A component intended for later integration with other Governed Execution tracks.

Integration does not imply that results from one track automatically generalize to the others. Composition, interaction effects, failure modes, and portability require separate evaluation.

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
    +------> server-controlled authority source
                 |
                 v
          current authority state
                 |
                 v
       obligation comparison
            /        \
         MATCH      MISMATCH
           |            |
       PROCEED         HOLD
```

For `revalidation_mode: "none"`, the authority obligation is not evaluated and the result records `NOT_EVALUATED`.

The caller no longer supplies the runtime authority state used for the governance decision. Current authority is obtained through a server-side dependency.

The test harness can also create a controlled process-local authority transition before execution-time evaluation. Under the tested `true` to `false` transition, full revalidation observes the changed value and returns `MISMATCH` and `HOLD`, while the no-revalidation baseline leaves the obligation `NOT_EVALUATED` and returns `PROCEED`.

The transition itself is established by the controlled test procedure. The retained decision evidence records the expected authority condition and the execution-time value when evaluated, but it does not currently retain the earlier authority value or the mutation event.

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

Send a valid request:

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
    "revalidation_mode": "full"
  }'
```

The default process-local authority source currently returns:

```text
authority_valid = true
```

so the response contains `PROCEED` and structured evidence resembling:

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

In tests, the server-side authority dependency can be replaced independently of the decision request.

If the server-side authority value is:

```text
authority_valid = false
```

under `revalidation_mode: "full"`, the evaluation records:

```text
expected = true
current = false
result = MISMATCH
outcome = HOLD
```

For this implementation, `HOLD` is a design choice for an authority mismatch. It is not a research conclusion that every authority change should result in `HOLD`.

## Caller-Supplied Runtime State

Current runtime authority is not part of the decision request.

A caller attempting to submit:

```json
{
  "runtime_state": {
    "authority_valid": false
  }
}
```

is rejected with HTTP 422.

This boundary prevents the action request from directly supplying the state used to evaluate its own authority obligation.

It does not establish that the server-side authority source is correct, authenticated, current, or authoritative.

## Revalidation Disabled

For:

```json
{
  "revalidation_mode": "none"
}
```

the authority obligation is not evaluated.

The evidence records:

```text
current = null
result = NOT_EVALUATED
outcome = PROCEED
```

`NOT_EVALUATED` is intentionally distinct from `MATCH`.

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
13 passed
```

The tests currently cover:

- matching server-side authority
- mismatching server-side authority
- skipped revalidation
- rejection of caller-supplied runtime state
- structured decision evidence
- record UUID and UTC timestamp metadata
- invalid revalidation modes
- unsupported obligation kinds
- empty obligation sets
- decision record retrieval
- unknown and malformed record identifiers
- controlled authority change before full revalidation
- equivalent authority-change scenario without revalidation

## Continuous Integration

GitHub Actions runs the test suite on pushes to `main` and on pull requests.

Workflow:

```text
.github/workflows/test.yml
```

The workflow installs the project with its development dependencies and runs:

```bash
python -m pytest -v
```

## Current Increment Progression

```text
001  Executable decision boundary
002  Prior decision obligations
003  Current authority state representation
004  Authority obligation comparison
005  Structured decision evidence
006  Decision record metadata
007  Process-local decision record retrieval
008  Authority source boundary
009  Authority change revalidation
```

Detailed increment records are under:

```text
docs/increments/
```

## Project Structure

```text
track-a-runtime-validity/
├── .github/
│   └── workflows/
│       └── test.yml
├── docs/
│   └── increments/
│       ├── 001-executable-boundary.md
│       ├── 002-prior-decision-obligations.md
│       ├── 003-current-authority-state.md
│       ├── 004-authority-obligation-comparison.md
│       ├── 005-decision-evidence-response.md
│       ├── 006-decision-record-metadata.md
│       ├── 007-decision-record-retrieval.md
│       ├── 008-authority-source-boundary.md
│       └── 009-authority-change-revalidation.md
├── src/
│   └── track_a/
│       ├── __init__.py
│       └── api.py
├── tests/
│   └── test_api.py
├── .gitignore
├── LICENSE
├── pyproject.toml
└── README.md
```

## Implemented Scope

The implementation currently provides:

- an executable HTTP decision boundary
- explicit prior-decision obligations
- a server-side boundary for current authority state
- rejection of caller-supplied runtime authority
- obligation comparison under full revalidation
- `PROCEED` and `HOLD` outcomes
- explicit `MATCH`, `MISMATCH`, and `NOT_EVALUATED` results
- structured obligation-evaluation evidence
- UUID and UTC record metadata
- process-local decision record retention and retrieval
- automated tests and GitHub Actions CI
- controlled process-local authority-state transitions for experimental tests
- comparison of full revalidation against a no-revalidation authority-change baseline

## Current Limitations

The current authority source is process-local.

The retained decision record does not currently contain the authority mutation event or the earlier process-local authority value. The controlled test procedure establishes that temporal transition.

The implementation does not yet establish that authority state came from an authenticated or independently authoritative enterprise source such as an IAM, delegation, credential, or policy system.

Decision records are retained only in process memory and are not durable across restarts.

Only the `authority_valid` obligation is implemented.

The implementation does not yet provide:

- authenticated authority mutation
- authority provenance
- external IAM or policy integration
- multiple governance-material change classes
- durable evidence storage
- distributed-state guarantees
- external action-boundary enforcement
- `DENY` or `ESCALATE` dispositions
- cryptographic integrity
- policy, model, tool, or runtime version tracking
- experimental comparison against the broader research baselines

Structured evidence records what this implementation evaluated. It does not prove that the observed authority state was correct or that the resulting governance decision was semantically justified.

## Research Position

Track A is an engineering reference implementation used to test hypotheses about runtime validity and revalidation.

The current implementation demonstrates a bounded engineering behavior: under a controlled process-local authority change from valid to invalid, full revalidation observes the changed state and produces MISMATCH and HOLD, while the no-revalidation baseline leaves the authority obligation NOT_EVALUATED and returns PROCEED.

It does not establish that this mechanism is sufficient for runtime governance generally, that `authority_valid` is a complete representation of authority, or that `HOLD` is the correct response to every authority change.

## License

Licensed under the Apache License, Version 2.0. See `LICENSE`.
