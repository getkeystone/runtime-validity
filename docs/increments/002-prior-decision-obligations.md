# Increment 002: Prior Decision Obligations

Status: In Progress

## Objective

Represent a prior governance decision together with the conditions that
justified that decision.

The uncertainty being removed is:

> Can the system represent why a prior decision was allowed in a form that
> can later be checked against changed runtime state?

## Observable Behavior

A decision request can include a prior decision with explicit obligations.

The system can distinguish between:

- the prior decision outcome
- the obligations that justified that outcome

## Acceptance Criteria

- [ ] A prior decision can be represented explicitly.
- [ ] A prior decision contains one or more explicit obligations.
- [ ] Invalid obligation structures are rejected at the API boundary.
- [ ] A valid request containing obligations is accepted.
- [ ] Automated tests cover valid and invalid obligation input.

## Out of Scope

This increment does not yet implement:

- material-change detection
- obligation invalidation
- revalidation
- PROCEED/HOLD/DENY/ESCALATE logic
- persistence
- action-boundary enforcement
- evidence reconstruction

## Next Step

Define the smallest useful representation for a prior decision and its
obligations.

## Proposed Minimal Data Shape

A prior decision will be represented explicitly rather than only by an ID.

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
