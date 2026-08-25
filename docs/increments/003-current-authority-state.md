# Increment 003: Current Authority State

Status: In Progress

## Objective

Represent the current runtime authority state independently from the prior decision obligation.

The uncertainty being removed is:

> Can the system represent the current authority condition that will later be compared against the prior `authority_valid` obligation?

## Observable Behavior

A decision request includes current runtime state:

```json
{
  "runtime_state": {
    "authority_valid": true
  }
}
```

The API accepts a valid authority state and rejects malformed or missing authority state.

## Acceptance Criteria

* [] Current runtime authority state can be represented explicitly.
* [] `authority_valid` accepts boolean values.
* [] A valid request containing runtime state is accepted.
* [] Missing or malformed runtime authority state is rejected.
* [] Automated tests cover valid and invalid runtime state input.

## Out of Scope

This increment does not yet:

* compare current state with prior obligations
* determine whether an obligation is stale or invalid
* trigger revalidation
* return HOLD, DENY, or ESCALATE
* enforce an action boundary
* persist runtime state

## Next Step

Compare the prior `authority_valid` obligation against current runtime `authority state`.
