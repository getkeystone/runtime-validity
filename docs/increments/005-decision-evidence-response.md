# Increment 005: Decision Evidence Response

Status: Complete

## Objective

Return enough structured evidence with each decision to explain why the current request produced `PROCEED` or `HOLD`.

The uncertainty being removed is:

> Can the system expose the inputs and obligation evaluation that directly produced the current decision outcome?

## Observable Behavior

A full revalidation with matching authority returns:

```text
expected = true
current = true
result = MATCH
outcome = PROCEED
```

An authority mismatch returns:

```text
expected = true
current = false
result = MISMATCH
outcome = HOLD
```

For `revalidation_mode: "none"`:

```text
current = null
result = NOT_EVALUATED
outcome = PROCEED
```

`NOT_EVALUATED` is distinct from `MATCH`. A skipped check is not represented as a successful evaluation.

## Acceptance Criteria

- [x] Decision responses include structured evidence.
- [x] Evidence identifies the action proposal and prior decision.
- [x] Evidence records the revalidation mode.
- [x] Full revalidation records expected and current authority state.
- [x] Matching authority records `MATCH`.
- [x] Mismatching authority records `MISMATCH`.
- [x] Skipped revalidation records `NOT_EVALUATED`.
- [x] Existing `PROCEED` and `HOLD` behavior remains unchanged.
- [x] Automated tests verify evidence for each decision path.

## Verification

Command:

```bash
python -m pytest -v
```

Observed result:

```text
8 passed in 0.19s
```

Verified behaviors:

- matching authority returns `PROCEED` with `MATCH` evidence
- mismatching authority returns `HOLD` with `MISMATCH` evidence
- skipped revalidation returns `PROCEED` with `NOT_EVALUATED` evidence
- existing request-validation failures remain covered

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

This increment provides structured evidence for the implemented comparison only. It is not a complete evidence-plane implementation or proof that the decision was correct.

## Next Step

Introduce a stable decision/evidence record identity and minimal metadata so individual decisions can be referenced and reconstructed across runs.
