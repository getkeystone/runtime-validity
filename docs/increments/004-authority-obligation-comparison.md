# Increment 004: Authority Obligation Comparison

Status: In Progress

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

For this increment, `HOLD` is the chosen disposition when the prior authority condition no longer matches current runtime state. It means the prior decision is not sufficient to proceed without further governance handling.

For `revalidation_mode: "none"`, the comparison is not performed and the current baseline behavior remains `PROCEED`.

## Acceptance Criteria

- [ ] Full revalidation compares prior expected authority with current authority state.
- [ ] Matching authority state returns `PROCEED`.
- [ ] Mismatched authority state returns `HOLD`.
- [ ] `revalidation_mode: "none"` does not perform the comparison.
- [ ] Existing request validation behavior remains intact.
- [ ] Automated tests cover matching, mismatching, and no-revalidation paths.

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

Implement and test the authority obligation comparison.
