# Increment 006: Decision Record Metadata

Status: In Progress

## Objective

Give each decision response a unique record identity and minimal metadata needed to reference the evaluation later.

The uncertainty being removed is:

> Can an individual decision result be uniquely identified and tied to when and under which evidence schema it was produced?

## Observable Behavior

Each decision response includes metadata resembling:

```json
{
  "outcome": "PROCEED",
  "evidence": {
    "record_id": "4c7729c4-...",
    "created_at": "2026-08-25T22:30:00Z",
    "schema_version": "1",
    "action_proposal": "send customer notification",
    "prior_decision_id": "decision-123",
    "revalidation_mode": "full",
    "obligation_evaluations": []
  }
}
```

The metadata is generated for every valid decision response, including `PROCEED` and `HOLD`.

## Acceptance Criteria

- [ ] Each decision response contains a `record_id`.
- [ ] `record_id` is a valid UUID.
- [ ] Each decision response contains an explicit creation timestamp.
- [ ] The timestamp is timezone-aware UTC.
- [ ] Each decision response identifies its evidence schema version.
- [ ] Existing decision and evidence behavior remains unchanged.
- [ ] Automated tests validate the metadata without depending on fixed UUID or timestamp values.

## Out of Scope

This increment does not yet:

- persist decision records
- retrieve records by ID
- provide idempotency across repeated requests
- cryptographically protect evidence
- establish semantic correctness of the evidence
- fetch authoritative runtime state externally
- enforce the decision at an external action boundary

## Known Limitations

The record exists only in the synchronous API response.

A unique `record_id` makes the result referenceable within the response model, but does not make it durable or retrievable.

The schema version describes the evidence structure only. It does not represent policy, model, tool, or runtime versions.

## Next Step

Implement UUID record identity, UTC creation time, and evidence schema version.
