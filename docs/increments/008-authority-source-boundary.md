# Increment 008: Authority Source Boundary

Status: In Progress

## Objective

Separate current authority state from the decision request so the caller cannot directly supply the value used to determine whether its prior authority obligation still holds.

The uncertainty being removed is:

> Can the decision boundary obtain current authority state from a server-controlled source rather than trusting the action request to provide the state being evaluated?

## Observable Behavior

Before this increment, the caller provides:

```text
POST /decide
    |
    +-- prior decision
    +-- runtime_state.authority_valid
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

The decision request no longer owns `runtime_state`.

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

A caller attempting to supply `runtime_state` is rejected rather than silently overriding or being confused with server-controlled state.

## Acceptance Criteria

- [ ] `DecisionRequest` no longer accepts current runtime authority state as a decision input.
- [ ] Full revalidation obtains current authority state from a server-side source.
- [ ] Matching server-provided authority returns `PROCEED`.
- [ ] Mismatching server-provided authority returns `HOLD`.
- [ ] Evidence records the authority value obtained from the server-side source.
- [ ] A caller-supplied `runtime_state` field is rejected.
- [ ] `revalidation_mode: "none"` remains explicitly `NOT_EVALUATED`.
- [ ] Existing decision-record metadata and retrieval behavior remains intact.
- [ ] Automated tests control the authority source independently of the decision request.

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

The initial authority source remains process-local and controlled by the service/test harness.

Separating the source from the decision request reduces one trust-boundary problem, but does not establish that the source itself is correct, current, authenticated, or authoritative.

Tests may substitute authority-source values in order to exercise runtime-change scenarios. Test control over the source is not equivalent to production authority acquisition.

`HOLD` on authority mismatch remains an implementation design choice for this experiment.

## Next Step

Implement a server-side authority source boundary and remove caller ownership of current authority state.
