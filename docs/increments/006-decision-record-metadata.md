# Increment 006: Decision Record Metadata

Status: Complete

## Objective

Give each decision response a unique record identity and minimal metadata needed to reference the evaluation later.

The uncertainty being removed is:

> Can an individual decision result be uniquely identified and tied to when and under which evidence schema it was produced?

## Observable Behavior

Each valid decision response includes:

```text
record_id = valid UUID
created_at = timezone-aware UTC timestamp
schema_version = "1"
```

The metadata is generated for both `PROCEED` and `HOLD` responses.

## Acceptance Criteria

- [x] Each decision response contains a `record_id`.
- [x] `record_id` is a valid UUID.
- [x] Each decision response contains an explicit creation timestamp.
- [x] The timestamp is timezone-aware UTC.
- [x] Each decision response identifies its evidence schema version.
- [x] Existing decision and evidence behavior remains unchanged.
- [x] Automated tests validate the metadata without depending on fixed UUID or timestamp values.

## Verification

Command:

```bash
python -m pytest -v
```

Observed result:

```text
9 passed in 0.19s
```

Verified behaviors:

- generated `record_id` parses as a UUID
- generated timestamp is timezone-aware UTC
- evidence schema version is `"1"`
- matching authority still returns `PROCEED`
- mismatching authority still returns `HOLD`
- skipped revalidation still records `NOT_EVALUATED`
- existing request-validation failures remain covered

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

Persist decision records so a previously returned `record_id` can be retrieved after the decision request completes.
