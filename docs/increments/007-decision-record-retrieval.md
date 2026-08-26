# Increment 007: Decision Record Retrieval

Status: In Progress

## Objective

Retain generated decision records inside the running service and allow them to be retrieved by `record_id`.

The uncertainty being removed is:

> Can a decision returned by `/decide` be referenced later by its record identity and retrieved with the same decision and evidence content?

## Observable Behavior

A successful decision request returns a record:

```text
POST /decide
→ 200
→ record_id = <uuid>
```

The same record can then be retrieved:

```text
GET /records/<record_id>
→ 200
→ same decision outcome and evidence
```

An unknown record identifier returns:

```text
GET /records/<unknown-record-id>
→ 404
```

The store used in this increment is process-local memory.

## Acceptance Criteria

- [ ] Every successful `/decide` result is retained in the running service.
- [ ] A record can be retrieved using its `record_id`.
- [ ] Retrieved content preserves the original outcome.
- [ ] Retrieved content preserves the original evidence.
- [ ] An unknown valid UUID returns HTTP 404.
- [ ] An invalid UUID path value is rejected by request validation.
- [ ] Existing decision behavior remains unchanged.
- [ ] Automated tests cover creation, retrieval, unknown records, and malformed record identifiers.

## Out of Scope

This increment does not yet:

- provide durable storage across process restarts
- use a database or external datastore
- provide concurrent or distributed storage guarantees
- provide record mutation or deletion
- provide idempotency for repeated decision requests
- cryptographically protect stored records
- prove that recorded evidence is semantically correct
- fetch authoritative runtime state externally
- enforce decisions at an external action boundary

## Known Limitations

The record store exists only in application memory.

Records disappear when the process exits and are not shared across multiple service instances.

This increment tests record identity and retrieval semantics, not durable evidence storage.

Successful retrieval shows that the service retained what it produced. It does not establish that the decision or evidence was correct.

## Next Step

Implement process-local decision record retention and `GET /records/{record_id}` retrieval.
