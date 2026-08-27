# Runtime Validity Demo Runbook

## Purpose

This runbook describes a bounded live demonstration of Runtime Validity - Track A.

The demonstration exercises one implemented scenario:

1. a prior-decision fixture contains an obligation requiring authority to remain valid;
2. the current process-local runtime state initially reports that authority as valid;
3. full revalidation produces `PROCEED` with `MATCH`;
4. a guarded experimental endpoint changes the process-local authority state from `true` to `false`;
5. the implementation retains a structured authority-transition record;
6. the transition can be retrieved by identifier;
7. full revalidation of an authority-valid obligation observes the changed state;
8. the resulting decision is `HOLD` with `MISMATCH`;
9. the demo restores the authority state to `true`.

This is an engineering demonstration of the current implementation. It is not independent validation of the broader Governed Execution research program.

## Scope

The demonstrated mechanism is process-local and intentionally narrow.

The scripted demonstration exercises the implementation's ability to:

- represent an authority-valid obligation;
- compare an expected authority state with current runtime state;
- produce `MATCH` or `MISMATCH`;
- produce `PROCEED` or `HOLD` under the implemented decision rule;
- retain a structured authority-state transition;
- retrieve that transition during the same process lifetime;
- expose the exercised mechanism through an HTTP API;
- restore the experimental authority state after the demonstration.

The implementation also retains decision evidence records and exposes a decision-record retrieval endpoint, but decision-record retrieval is not exercised by this scripted demonstration.

## What this demo does not establish

The demo does not establish:

- authentic external authority revocation;
- production identity or authentication;
- production authorization;
- authority provenance;
- correctness of the authority-state value;
- semantic correctness of retained evidence;
- tamper-resistant evidence;
- durable persistence across process restart;
- distributed-system correctness;
- binding between a specific authority transition and a specific prior decision;
- enforcement at a real external consequential-action boundary;
- effectiveness across other governance-material change classes;
- portability across agent frameworks or runtimes;
- general effectiveness of the broader Governed Execution architecture.

The experimental control token is only a narrow guard for the demonstration endpoint. It is not a production authentication, authorization, identity, or authority-provenance mechanism.

## Preconditions

The Runtime Validity service must be running and reachable from the machine executing the demonstration.

The demo script accepts the service base URL as its first argument.

For a local service using the script default:

```text
http://127.0.0.1:8000
```

The experimental authority-control configuration must exist locally at:

```text
~/.config/runtime-validity/runtime-validity.env
```

The file must not be committed to the repository.

Expected permissions:

```text
600
```

Do not print or copy the token into logs, documentation, terminal transcripts intended for publication, or repository history.

## Run the demonstration

From the repository root:

```bash
./scripts/demo-authority-revalidation.sh
```

To exercise a service at another reachable address:

```bash
./scripts/demo-authority-revalidation.sh \
  http://<runtime-validity-host>:8000
```

## Expected baseline

The first decision should report:

```text
outcome = PROCEED
expected = true
current = true
result = MATCH
```

Interpretation:

Under the implemented fixture and decision rule, the current process-local authority state matches the authority-valid obligation contained in the prior-decision fixture.

This does not prove that the prior decision was independently authorized or that an intended external consequence is justified in a real deployment.

## Expected authority transition

The demonstration then changes the experimental process-local authority state from:

```text
true -> false
```

The returned transition record should contain:

```text
transition_id
occurred_at
previous_authority_valid = true
current_authority_valid = false
```

The script subsequently retrieves the retained transition through:

```text
GET /authority-transitions/{transition_id}
```

In the exercised scenario, the retrieved representation contains the same recorded transition identifier and authority-state values produced when the transition was created.

The transition record is self-produced process-local evidence. It is not an independent witness of an external authority change.

## Expected revalidation result

After the controlled authority-state change, full revalidation should report:

```text
outcome = HOLD
expected = true
current = false
result = MISMATCH
```

Interpretation:

The represented authority-valid obligation no longer matches the current process-local runtime state, and the implemented rule therefore produces `HOLD`.

`HOLD` for this mismatch is a design choice of the current implementation. It is not presented as a universal governance rule.

## Cleanup behavior

The demo script attempts to restore:

```text
authority_valid = true
```

when it exits.

A cleanup failure is reported as a warning.

For an independent post-demo check, submit a full revalidation with an authority-valid obligation expecting `true`.

The clean state should produce:

```text
outcome = PROCEED
current = true
result = MATCH
```

## API surface

The current implementation exposes FastAPI documentation at:

```text
<base-url>/docs
```

Relevant endpoints are:

```text
POST /experimental/authority-state
POST /decide
GET  /records/{record_id}
GET  /authority-transitions/{transition_id}
```

The experimental endpoint is disabled unless explicitly enabled through local runtime configuration.

`GET /records/{record_id}` is part of the implementation but is not exercised by the scripted authority-revalidation demonstration described in this runbook.

## Suggested live narrative

A concise explanation during the demonstration is:

> Runtime Validity is testing a narrow question: whether conditions that mattered to an earlier governance decision still hold when that decision is re-evaluated before a proposed consequential action.
>
> Here the prior-decision fixture requires authority to remain valid. Initially the process-local runtime state agrees, so revalidation returns `MATCH` and the implemented decision is `PROCEED`.
>
> I then use a guarded experimental control to change that represented runtime condition. This is a controlled internal state change, not an authentic external authority revocation. The implementation records the transition from `true` to `false`.
>
> When an authority-valid obligation is evaluated again, the current state no longer matches what the fixture requires. The result becomes `MISMATCH` and the implemented decision is `HOLD`.
>
> The research question is broader than this demonstration: which runtime changes should invalidate earlier governance decisions, what should trigger revalidation before consequential action, and what evidence should let an external reviewer reconstruct why the resulting action proceeded, was held, denied, or escalated?

## Claim classification

### Engineering observation

In the current process-local implementation, a controlled authority-state change can be retained as a structured transition and retrieved later during the same process lifetime.

### Internal evaluation result

The exercised live scenario produced:

```text
PROCEED / MATCH
-> authority state true -> false
-> retained transition retrieval
-> HOLD / MISMATCH
-> reset
-> PROCEED / MATCH
```

### Design choice

The implementation maps the exercised authority mismatch to `HOLD`.

### Research hypothesis

Changes in authority are a candidate class of governance-material runtime change that may invalidate obligations supporting an earlier governance decision.

The current demonstration does not establish when that hypothesis generalizes, which authority changes are material, or whether the proposed representation is sufficient.

## Current evidence boundary

The strongest claim supported by this demonstration is:

> In the current Runtime Validity process-local implementation, an experimentally controlled change to the represented authority-valid state can be retained as structured transition evidence, observed during full revalidation of an authority-valid obligation, and result in the implemented decision changing from `PROCEED` with `MATCH` to `HOLD` with `MISMATCH`.

Anything stronger requires additional experiments, external state sources, stronger provenance, action-boundary enforcement, and broader evaluation.
