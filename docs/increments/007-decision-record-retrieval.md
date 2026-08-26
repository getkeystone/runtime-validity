# Increment 007: Decision Record Retrieval

Status: Complete

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

- [x] Every successful `/decide` result is retained in the running service.
- [x] A record can be retrieved using its `record_id`.
- [x] Retrieved content preserves the original outcome.
- [x] Retrieved content preserves the original evidence.
- [x] An unknown valid UUID returns HTTP 404.
- [x] An invalid UUID path value is rejected by request validation.
- [x] Existing decision behavior remains unchanged.
- [x] Automated tests cover creation, retrieval, unknown records, and malformed record identifiers.

## Verification

Commands:

```bash
git diff --check
python -m pytest -v
```

Observed result:

```text
12 passed in 0.20s
```

`git diff --check` completed without warnings after removing trailing blank lines from `tests/test_api.py`.

Verified behaviors:

- `/decide` retains each successful decision response in process-local memory
- a retained record can be retrieved using its `record_id`
- retrieved content matches the originally returned decision and evidence
- an unknown valid UUID returns HTTP 404
- a malformed UUID is rejected with HTTP 422
- existing `PROCEED`, `HOLD`, `MATCH`, `MISMATCH`, and `NOT_EVALUATED` behavior remains covered
- existing request validation behavior remains covered

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

Determine whether durable evidence storage is required for the next research question, or whether the next increment should move toward authoritative runtime state acquisition.
