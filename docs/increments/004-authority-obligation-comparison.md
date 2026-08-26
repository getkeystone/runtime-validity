# Increment 004: Authority Obligation Comparison

Status: Complete

## Objective

Compare the prior `authority_valid` obligation against current runtime authority state.

The uncertainty being removed is:

> Can the system detect when the authority condition that justified a prior decision no longer holds at execution time?

## Observable Behavior

For `revalidation_mode: "full"`:

```text
prior expected authority = true
current authority = true
→ PROCEED
```

```text
prior expected authority = true
current authority = false
→ HOLD
```

For this increment, `HOLD` is the chosen disposition when the prior authority condition no longer matches current runtime state.

For `revalidation_mode: "none"`, the comparison is not performed and the baseline behavior remains `PROCEED`.

## Acceptance Criteria

- [x] Full revalidation compares prior expected authority with current authority state.
- [x] Matching authority state returns `PROCEED`.
- [x] Mismatched authority state returns `HOLD`.
- [x] `revalidation_mode: "none"` does not perform the comparison.
- [x] Existing request validation behavior remains intact.
- [x] Automated tests cover matching, mismatching, and no-revalidation paths.

## Verification

Command:

```bash
python -m pytest -v
```

Observed result:

```text
8 passed in 0.17s
```

Verified behaviors:

- matching authority under full revalidation returns `PROCEED`
- mismatching authority under full revalidation returns `HOLD`
- `revalidation_mode: "none"` bypasses the authority comparison and returns `PROCEED`
- missing runtime state remains rejected
- malformed runtime authority state remains rejected
- invalid revalidation mode remains rejected
- unsupported obligation kinds remain rejected
- prior decisions without obligations remain rejected

## Out of Scope

This increment does not yet:

- determine a final `DENY` disposition
- fetch authority from an external authoritative source
- persist state
- generate decision evidence records
- evaluate multiple obligation kinds
- enforce the resulting decision at an external action boundary

## Known Limitations

The runtime authority value is still supplied directly in the request.

This increment tests comparison behavior, not authoritative state acquisition.

The use of `HOLD` for an authority mismatch is an explicit design choice for this increment, not a general conclusion that all authority changes should result in `HOLD`.

## Next Step

Represent enough decision evidence to explain why the request returned `PROCEED` or `HOLD`.
