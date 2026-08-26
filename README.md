# Track A Runtime Validity

Track A is a bounded experimental component of the broader Governed Execution research program and reference architecture.

This repository isolates one research question: runtime validity and revalidation of prior governance decisions before consequential action.

Track A is deliberately developed and evaluated as a narrow component so its behavior, assumptions, failure modes, and evidence can be examined separately before broader integration.

Results from this repository should not be interpreted as validation of the broader Governed Execution architecture, of other tracks, or of runtime governance generally.

## Relationship to Governed Execution

Governed Execution is the broader runtime-governance research program.

The working architecture separates:

- a control plane for authority, policy, admissibility, placement, budget, and release
- an execution plane for models, retrieval, tools, delegation, and workflows
- an evidence plane for decisions, authorizations, actions, evaluations, failures, and outcomes
- a separate action boundary governing whether system output may create external consequence

Individual tracks isolate bounded mechanisms or research questions so they can be implemented and tested independently before composition.

This repository therefore serves two roles:

1. A bounded experimental artifact for runtime-validity research.
2. A candidate component for later composition into a broader Governed Execution Runtime.

Integration would not imply that results from Track A automatically generalize to other components.

Composition, interaction effects, failure modes, and portability require separate evaluation.

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

For:

```text
revalidation_mode = "none"
```

the authority obligation is not evaluated and the evidence records:

```text
current = null
result = NOT_EVALUATED
outcome = PROCEED
```

The caller does not supply the runtime authority state used for the governance decision.

Current authority is obtained through a server-side dependency.

The experimental harness can also create a controlled process-local authority change before execution-time evaluation.

For the tested transition:

```text
authority_valid:
true -> false
```

full revalidation observes the changed value and produces:

```text
current = false
result = MISMATCH
outcome = HOLD
```

while the no-revalidation baseline produces:

```text
current = null
result = NOT_EVALUATED
outcome = PROCEED
```

The implementation now also retains a separate process-local transition artifact recording the implementation-observed:

```text
previous_authority_valid
current_authority_valid
transition_id
occurred_at
```

That transition artifact can be retrieved during the same process lifetime.

The transition artifact and decision evidence remain separate.

The implementation does not yet establish that a particular decision evaluated the runtime state represented by a particular transition artifact.

This is a reference implementation for controlled experiments.

It is not evidence that the governance mechanism is complete, correct, independently validated, or suitable for production use.

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

The default process-local authority source begins with:

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

under full revalidation, the evaluation records:

```text
expected = true
current = false
result = MISMATCH
outcome = HOLD
```

For this implementation, `HOLD` is a design choice for an authority mismatch.

It is not a research conclusion that every authority change should result in `HOLD`.

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

A `PROCEED` result under this mode means that the authority condition was not re-evaluated.

It does not establish that the intended consequence remained justified.

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

The decision-record store is process-local memory.

Records are lost when the process exits and are not shared between service instances.

## Authority Transition Evidence

Increment 010 adds a separate process-local artifact representing a recorded authority-value change.

The current transition representation contains:

```text
transition_id
occurred_at
previous_authority_valid
current_authority_valid
```

For the controlled change:

```text
true -> false
```

the implementation retains an artifact resembling:

```json
{
  "transition_id": "<uuid>",
  "occurred_at": "<UTC record time>",
  "previous_authority_valid": true,
  "current_authority_valid": false
}
```

This is a recorded transition assertion produced by the implementation.

It is not independent proof that an authentic external authority fact changed.

## Transition Semantics

Increment 010 uses changed-value-only semantics.

The following create transition records:

```text
true -> false
false -> true
```

The following do not:

```text
true -> true
false -> false
```

This is a design choice for the bounded reference implementation.

It is not a general definition of governance-relevant events.

For example, same-value re-attestation, renewal, heartbeat, or validity-refresh events could be meaningful in richer authority models.

## Retrieve an Authority Transition

Given a transition identifier, retrieve the retained artifact while the same process is running:

```bash
curl -s \
  http://127.0.0.1:8000/authority-transitions/<transition_id>
```

A known identifier returns the retained transition artifact.

An unknown valid UUID returns HTTP 404.

A malformed UUID is rejected with HTTP 422.

The transition store is process-local memory.

Transition records are lost when the process exits and are not shared between service instances.

## Transition Evidence Interpretation

The strongest supported interpretation of a retained transition artifact is:

> The Track A implementation recorded that its process-local authority value changed from one Boolean value to another under the recorded identifier and record time.

The artifact alone does not establish:

- source authenticity
- evidence integrity
- semantic correctness
- governance materiality
- causal relevance
- decision-transition binding
- durable retention
- distributed ordering
- external action containment

The implementation that changes process-local state is also the implementation that creates the transition record.

The transition artifact is therefore self-produced evidence, not an independent witness.

## Relationship Between Transition and Decision Evidence

Track A currently retains two conceptually distinct artifacts.

### Authority transition evidence

Answers:

> What process-local authority change did this implementation record?

### Decision evidence

Answers:

> What authority condition did the execution-time decision evaluate, and what disposition resulted?

The implementation does not yet answer:

> Which exact retained authority transition or state version supplied the runtime authority value evaluated by this exact decision?

Timestamp proximity or matching Boolean values are not treated as proof of that relationship.

Decision-to-state binding is a candidate next experiment.

## Run Tests

Run:

```bash
git diff --check
python -m pytest -v
```

Current locally verified test suite:

```text
20 passed
```

The suite retains the 13 tests from Increments 001 through 009 and adds coverage for Increment 010.

Current coverage includes:

- matching server-side authority
- mismatching server-side authority
- skipped revalidation
- rejection of caller-supplied runtime state
- structured decision evidence
- decision-record UUID and UTC timestamp metadata
- invalid revalidation modes
- unsupported obligation kinds
- empty obligation sets
- decision-record retrieval
- unknown and malformed decision-record identifiers
- controlled authority change before full revalidation
- equivalent authority-change scenario without revalidation
- authority-transition creation for a controlled value change
- transition UUID and UTC record-time metadata
- transition retrieval
- unknown transition identifier handling
- malformed transition identifier handling
- same-value assignment behavior
- retained transition stability after a later authority change
- rejection of caller-supplied transition evidence
- transition-store isolation between tests

The 20-test result is an internal evaluation result.

It is not independent validation.

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

Increment 010 remains `In Progress` until its pull-request CI verification succeeds.

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
010  Authority transition evidence
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
│       ├── 009-authority-change-revalidation.md
│       └── 010-authority-transition-evidence.md
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
- UUID and UTC decision-record metadata
- process-local decision-record retention and retrieval
- controlled process-local authority changes for experimental tests
- comparison of full revalidation against a no-revalidation authority-change baseline
- structured process-local authority-transition evidence
- changed-value-only transition semantics
- UUID and UTC transition-record metadata
- process-local transition retention and retrieval
- rejection of caller-supplied transition evidence
- automated tests and GitHub Actions CI

## Current Limitations

The current authority source is process-local.

Authority is represented only as:

```text
authority_valid: bool
```

This does not represent:

- subject
- protected resource
- action
- scope
- delegation
- policy basis
- credential
- provenance
- validity interval
- authority source

The implementation does not establish that the process-local authority state came from an authenticated or independently authoritative enterprise source such as an IAM, delegation, credential, or policy system.

The authority transition artifact records what this implementation observed and retained.

It does not prove that the represented authority values were authentic or semantically correct.

Decision records and transition records are retained only in process memory and are not durable across restarts.

The implementation does not structurally bind a decision record to a specific transition record or authority-state version.

Only the `authority_valid` obligation is implemented.

The implementation does not yet provide:

- authenticated authority mutation
- authority provenance
- external IAM or policy integration
- decision-to-state binding
- transition causality
- multiple governance-material change classes
- state-version identifiers
- multi-transition ordering guarantees
- durable evidence storage
- distributed-state guarantees
- concurrency guarantees
- external action-boundary enforcement
- `DENY` or `ESCALATE` dispositions
- cryptographic integrity
- policy, model, tool, or runtime version tracking
- experimental comparison against the broader research baselines

Structured evidence records what this implementation evaluated or recorded.

It does not prove that the observed authority state was correct or that the resulting governance decision was semantically justified.

## Research Position

Track A is an engineering reference implementation used to test bounded hypotheses about runtime validity, revalidation, and evidence.

The implementation currently supports two related engineering observations.

First, under a controlled process-local authority change from valid to invalid, full revalidation observes the changed state and produces `MISMATCH` and `HOLD`, while the no-revalidation baseline leaves the authority obligation `NOT_EVALUATED` and returns `PROCEED`.

Second, the same process-local implementation can retain and retrieve a structured transition artifact containing the implementation-recorded previous authority value, resulting value, UUID identifier, and UTC record time.

These are bounded engineering observations supported by internal tests.

They do not establish:

- that `authority_valid` is a complete representation of authority
- that every authority change is governance-material
- that `HOLD` is the correct response to every authority mismatch
- that the transition artifact is independently verified
- that the four-field transition representation is necessary or sufficient for governance reconstruction
- that a particular transition caused or invalidated a particular decision
- that the mechanism is sufficient for runtime governance generally
- that the results generalize beyond this implementation

## Next Research Question

The next candidate experiment concerns decision-to-state binding:

> What retained evidence is required to establish that a specific execution-time governance decision evaluated a specific runtime state or transition representation?

Candidate mechanisms may include an explicit:

```text
state_version
```

or:

```text
transition reference
```

The experiment should not assume that timestamp proximity, matching values, or knowledge from the test procedure establishes causality.

## License

Licensed under the Apache License, Version 2.0. See `LICENSE`.
