# Increment 002: Prior Decision Obligations

Status: Complete

## Objective

Represent a prior governance decision together with the conditions that justified that decision.

The uncertainty being removed is:

> Can the system represent why a prior decision was allowed in a form that can later be checked against changed runtime state?

## Observable Behavior

A decision request can include a prior decision with explicit obligations.

The system can distinguish between:

* the prior decision outcome
* the obligations that justified that outcome

## Acceptance Criteria

* [x] A prior decision can be represented explicitly.
* [x] A prior decision contains one or more explicit obligations.
* [x] Invalid obligation structures are rejected at the API boundary.
* [x] A valid request containing obligations is accepted.
* [x] Automated tests cover valid and invalid obligation input.

## Request Representation

A prior decision is represented explicitly rather than only by an ID.

Example:

```json
{
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
}
```

The first supported obligation kind is intentionally narrow:

`authority_valid`

This is not intended to define a complete obligation ontology.

## Verification

Command:

```bash
python -m pytest -v
```

Observed result:

```text
4 passed in 0.17s
```

Verified behaviors:

* valid prior decision with an `authority_valid` obligation is accepted
* invalid `revalidation_mode` is rejected
* unsupported obligation kinds are rejected
* a prior decision without obligations is rejected

## Out of Scope

This increment does not yet implement:

* material-change detection
* obligation invalidation
* revalidation
* PROCEED/HOLD/DENY/ESCALATE logic
* persistence
* action-boundary enforcement
* evidence reconstruction

## Known Limitations

This increment represents prior decision obligations only.

It does not determine whether an obligation remains valid against current runtime state.

The `authority_valid` obligation is a deliberately narrow initial representation, not a claim that authority alone captures decision justification.

## Next Step

Introduce the smallest representation of current runtime state needed to compare against the `authority_valid` obligation.
