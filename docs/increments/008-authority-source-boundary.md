# Increment 008: Authority Source Boundary

Status: Complete

## Objective

Separate current authority state from the decision request so the caller cannot directly supply the value used to determine whether its prior authority obligation still holds.

The uncertainty being removed is:

> Can the decision boundary obtain current authority state from a server-controlled source rather than trusting the action request to provide the state being evaluated?

## Observable Behavior

Before this increment:

```text
caller
  |
  +-- action proposal
  +-- prior decision
  +-- runtime_state.authority_valid
  |
  v
POST /decide
```

After this increment:

```text
caller
  |
  | action proposal + prior decision
  v
POST /decide
  |
  +------> server-side authority source
                 |
                 v
          current authority state
                 |
                 v
          obligation comparison
```

The decision request no longer contains `runtime_state`.

For full revalidation:

```text
prior expected authority = true
server-provided authority = true
→ MATCH
→ PROCEED
```

```text
prior expected authority = true
server-provided authority = false
→ MISMATCH
→ HOLD
```

A caller attempting to submit `runtime_state` is rejected with HTTP 422.

For `revalidation_mode: "none"`:

```text
current = null
result = NOT_EVALUATED
outcome = PROCEED
```

## Acceptance Criteria

- [x] `DecisionRequest` no longer accepts current runtime authority state as a decision input.
- [x] Full revalidation obtains current authority state from a server-side source.
- [x] Matching server-provided authority returns `PROCEED`.
- [x] Mismatching server-provided authority returns `HOLD`.
- [x] Evidence records the authority value obtained from the server-side source.
- [x] A caller-supplied `runtime_state` field is rejected.
- [x] `revalidation_mode: "none"` remains explicitly `NOT_EVALUATED`.
- [x] Existing decision-record metadata and retrieval behavior remains intact.
- [x] Automated tests control the authority source independently of the decision request.

## Verification

Commands:

```bash
git diff --check
python -m pytest -v
```

Observed result:

```text
11 passed in 0.21s
```

Verified behaviors:

- server-side authority `true` produces `MATCH` and `PROCEED`
- server-side authority `false` produces `MISMATCH` and `HOLD`
- the evidence records the server-provided observed authority value
- `revalidation_mode: "none"` records `NOT_EVALUATED`
- caller-supplied `runtime_state` is rejected with HTTP 422
- invalid revalidation modes remain rejected
- unsupported obligation kinds remain rejected
- prior decisions without obligations remain rejected
- decision metadata remains generated
- decision records remain retrievable by `record_id`
- unknown and malformed record identifiers retain their existing behavior

## Implementation Note

The current boundary is implemented using FastAPI dependency injection.

Tests replace the authority dependency using `app.dependency_overrides`, allowing authority state to vary independently from the decision request.

This is an engineering mechanism for separating trust boundaries. It does not establish that the underlying source is authoritative.

## Out of Scope

This increment does not yet:

- claim that the process-local source is an authoritative enterprise identity or authorization system
- authenticate or authorize changes to authority state
- fetch authority from an external IAM, policy, delegation, or credential service
- persist authority state across process restarts
- provide distributed authority-state consistency
- establish authority provenance
- evaluate multiple obligation kinds
- enforce the resulting decision at an external action boundary

## Known Limitations

The initial authority source remains process-local and controlled by the service or test harness.

Separating the source from the decision request removes one trust-boundary problem, but does not establish that the source itself is correct, current, authenticated, or authoritative.

Test control over the source is not equivalent to production authority acquisition.

`HOLD` on authority mismatch remains an implementation design choice for this experiment.

## Next Step

Define the next runtime-change experiment using authority state that can change independently between prior authorization and execution.
