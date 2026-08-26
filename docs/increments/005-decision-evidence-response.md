# Increment 005: Decision Evidence Response

Status: In Progress

## Objective

Return enough structured evidence with each decision to explain why the current request produced `PROCEED` or `HOLD`.

The uncertainty being removed is:

> Can the system expose the inputs and obligation evaluation that directly produced the current decision outcome?

## Observable Behavior

A full revalidation with matching authority should return evidence resembling:

```json
{
  "outcome": "PROCEED",
  "evidence": {
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

An authority mismatch should record:

```text
expected = true
current = false
result = MISMATCH
outcome = HOLD
```

For `revalidation_mode: "none"`:

```text
result = NOT_EVALUATED
outcome = PROCEED
```

`NOT_EVALUATED` is distinct from `MATCH`. A skipped governance check must not be represented as a successful evaluation.

## Acceptance Criteria

- [ ] Decision responses include structured evidence.
- [ ] Evidence identifies the action proposal and prior decision.
- [ ] Evidence records the revalidation mode.
- [ ] Full revalidation records expected and current authority state.
- [ ] Matching authority records `MATCH`.
- [ ] Mismatching authority records `MISMATCH`.
- [ ] Skipped revalidation records `NOT_EVALUATED`.
- [ ] Existing `PROCEED` and `HOLD` behavior remains unchanged.
- [ ] Automated tests verify evidence for each decision path.

## Out of Scope

This increment does not yet:

- persist decision evidence
- assign evidence record IDs
- add timestamps or version metadata
- cryptographically protect evidence
- fetch authoritative state externally
- evaluate multiple obligation kinds
- enforce decisions at an external action boundary

## Known Limitations

The evidence is returned synchronously with the API response and is not persisted.

The current runtime authority value is still supplied by the caller.

This increment provides structured evidence for the implemented comparison only. It is not yet a complete evidence-plane implementation or proof that the decision was correct.

## Next Step

Implement the minimal evidence response for `MATCH`, `MISMATCH`, and `NOT_EVALUATED`.
