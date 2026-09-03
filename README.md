# Runtime Validity - Track A

Runtime Validity is the bounded reference implementation for research identifier Track A within the broader Governed Execution research program.

Track A's controlling research question is stated in full under [Track A Research Question](#track-a-research-question) below. In short, it studies which controlled runtime interventions invalidate which obligations in a prior decision's justification, and under what conditions revalidating only the affected obligations preserves the same disposition as fully reevaluating the decision, at lower revalidation work.

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

This repository is a bounded experimental artifact for Track A's runtime-validity research. A separate experiment/evaluation environment, `governed-execution-lab`, is where controlled Track A experiments are expected to run; this repository does not itself claim that such composition has already occurred.

A future composed Governed Execution Runtime does not currently exist. Future composition of Runtime Validity with other governed-execution mechanisms is separate work that would require its own integration and evaluation; it is not implied by anything in this repository.

Composition, interaction effects, failure modes, and portability require separate evaluation.

## Track A Research Question

Orchestration determines how work proceeds. Governance determines whether the intended consequence remains justified to proceed. Track A studies a specific piece of that governance question: whether a justification that was valid when a decision was made is still valid when the decision's consequence is about to execute.

The controlling Track A research question is:

> Given a prior decision justification composed of heterogeneous governance obligations, which controlled runtime interventions invalidate which obligations, and under what conditions does obligation-scoped revalidation preserve the same policy-expected disposition as full commit-boundary reevaluation with lower revalidation work?

This is a research question, not yet a research conclusion. Research priority within it is ordered as follows, and the ordering is deliberate:

1. **Primary: intervention-to-obligation invalidation mapping.** Which controlled runtime interventions invalidate which obligations?
2. **Secondary: disposition preservation.** When does obligation-scoped revalidation produce the same policy-expected disposition as full commit-boundary reevaluation of the same decision?
3. **Tertiary, conditional on (2): revalidation work and latency.** Only once equivalent disposition is established does it become meaningful to ask whether scoped revalidation requires less work or less time than full reevaluation.

Revalidation work and latency are not the primary Track A contribution. Neither is transition evidence, nor decision-to-state binding: both are candidate enabling mechanisms for later controlled experiments on the primary and secondary questions, not substitutes for them. See [Relationship of the Current Implementation to the Track A Research Question](#relationship-of-the-current-implementation-to-the-track-a-research-question) for what the current repository does and does not yet evaluate against this question.

Two terms in the research question carry specific meaning here and should not be collapsed into each other:

- **Permission governance** asks who is allowed to do what.
- **Decision justification** asks why this particular decision was appropriate for this context, evidence, affected party, and consequence level.

The research question above concerns a prior *decision justification* composed of heterogeneous obligations, not a single permission bit. The current implementation, described next, does not yet model that richer justification: it models one bounded obligation representation.

A closely related idea, useful background for the question above: **currency** asks whether the original justification still legitimately authorizes the intended consequence at the point of execution. This repository does not currently operationalize currency as a measured experimental variable; it is offered here only to explain the shape of the question.

## Current Status

Early engineering and research implementation.

The current implementation evaluates one bounded case toward the Track A research question above, not the question itself: a single Boolean obligation, one controlled intervention (a process-local authority change), and a comparison against a no-revalidation baseline rather than against full commit-boundary reevaluation of a heterogeneous decision. See [Relationship of the Current Implementation to the Track A Research Question](#relationship-of-the-current-implementation-to-the-track-a-research-question) below for the full boundary.

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

## Relationship of the Current Implementation to the Track A Research Question

Increments 001 through 010 construct prerequisites and one bounded experimental case. Increment 011 is in-progress research toward grounding a future obligation universe. Neither constitutes evaluation of the full Track A research question stated above.

| Increment(s) | What it establishes |
|---|---|
| 001 | Executable decision/action-admission boundary (`POST /decide`). |
| 002 | Representation of a prior decision's obligations. |
| 003 | Representation of current process-local authority state. |
| 004 | Comparison between a prior obligation and current state. |
| 005-007 | Structured decision evidence, record metadata, process-local retention and retrieval. |
| 008 | Server-controlled authority-source boundary (the caller cannot supply the state used to evaluate its own obligation). |
| 009 | A controlled authority change and a comparison of full revalidation against no revalidation. |
| 010 | Process-local authority-transition evidence, retained and retrievable separately from decision evidence. |
| 011 (in progress) | Prior-art research toward grounding an initial heterogeneous obligation universe in published mechanisms. No obligation set has been selected. No evaluated result exists yet. |

These increments construct mechanisms and research prerequisites for Track A. They do not constitute the Track A invalidation-mapping experiment.

As of this increment, Runtime Validity has **not yet evaluated**:

1. heterogeneous governance obligations (only one Boolean obligation kind, `authority_valid`, is implemented);
2. a final, externally grounded obligation universe (Increment 011 is in progress toward one, not complete);
3. multiple controlled runtime intervention classes (only one controlled intervention, a process-local authority change, is implemented);
4. intervention-to-obligation invalidation mappings (the Track A primary question);
5. obligation-scoped or selective revalidation (not implemented; only whole-decision full revalidation and no revalidation exist);
6. disposition preservation between scoped and full commit-boundary revalidation (the Track A secondary question);
7. a policy-expected-disposition oracle defined independently of the mechanism under test;
8. revalidation-work reduction from scoped revalidation;
9. latency differences between scoped and full revalidation;
10. conditions under which scoped revalidation would be unsafe or disposition-divergent;
11. authentic external authority revocation;
12. production authentication or authorization;
13. independently witnessed transition evidence;
14. durable persistence of decision or transition records;
15. structural binding between a transition record and the exact decision state it was evaluated against;
16. distributed ordering or concurrency guarantees;
17. real external consequence enforcement.

Items 1 through 10 are research questions and experiments not yet conducted, not defects in the current implementation: Increments 001-010 were not designed to answer them, and Increment 011 is in-progress groundwork for later addressing the first two.

## Requirements

Python 3.12 or newer.

## Setup

Clone the repository and enter the project directory:

```bash
git clone https://github.com/getkeystone/runtime-validity.git
cd runtime-validity
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
python -m uvicorn runtime_validity.api:app --reload
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
23 passed
```

The suite retains the 13 tests from Increments 001 through 009, adds 7 tests for Increment 010, and adds 3 further tests for a guarded, disabled-by-default experimental authority-control endpoint added after Increment 010.

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
- the experimental authority-control endpoint is disabled unless explicitly enabled
- the experimental authority-control endpoint rejects an invalid control token
- the experimental authority-control endpoint, when enabled with a valid token, drives the same live revalidation path exercised above

The 23-test result is an internal evaluation result for this commit.

It is not independent validation, and it is not evidence toward the Track A research question above: none of these tests exercise more than one obligation, more than one intervention class, or a comparison against full commit-boundary reevaluation of a heterogeneous decision.

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

Increment 010 is complete after local verification and successful GitHub Actions verification on `main`.

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
011  Externally grounded obligation universe (in progress; no evaluated result yet)
012  Track A research alignment (this documentation increment)
```

Detailed increment records are under:

```text
docs/increments/
```

## Project Structure

```text
runtime-validity/
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
│       ├── 010-authority-transition-evidence.md
│       ├── 011-externally-grounded-obligation-universe.md
│       └── 012-track-a-research-alignment.md
├── src/
│   └── runtime_validity/
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

Track A is an engineering reference implementation used to test bounded hypotheses about runtime validity, revalidation, and evidence. See [Track A Research Question](#track-a-research-question) for the controlling question this work is building toward, and [Relationship of the Current Implementation to the Track A Research Question](#relationship-of-the-current-implementation-to-the-track-a-research-question) for the full list of what is not yet evaluated.

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

Decision-to-state binding is a candidate enabling engineering experiment for later Track A evaluation. It is not a replacement for the Track A invalidation-mapping research question stated in [Track A Research Question](#track-a-research-question); it is scaffolding that a later invalidation-mapping or disposition-preservation experiment may need.

The candidate experiment concerns decision-to-state binding:

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

This is not necessarily the next numbered increment. Increment 011 (obligation-universe grounding) is already in progress toward the Track A primary question and is independent of this one.

## License

Licensed under the Apache License, Version 2.0. See `LICENSE`.
