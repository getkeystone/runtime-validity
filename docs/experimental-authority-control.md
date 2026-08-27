# Experimental Authority Control

## Purpose

Runtime Validity normally obtains current authority state through an internal server-side boundary.

The HTTP decision endpoint does not allow a caller to supply the runtime authority state used for revalidation.

For controlled demonstrations and experiments, this repository also provides:

```text
POST /experimental/authority-state
```

This endpoint exists only to exercise the process-local authority transition and revalidation mechanisms through the running HTTP service.

It is experimental harness plumbing, not a production authority-management interface.

## Default State

The experimental control is disabled by default.

It is enabled only when the runtime process is configured with:

```text
RUNTIME_VALIDITY_ENABLE_EXPERIMENTAL_CONTROL=1
```

The process must also define:

```text
RUNTIME_VALIDITY_EXPERIMENTAL_CONTROL_TOKEN
```

Requests must provide the configured token through:

```text
X-Experimental-Control-Token
```

The token is a narrow access guard for the experimental endpoint.

It should not be interpreted as production authentication, authorization, identity verification, or authority provenance.

## Controlled Flow

A controlled experiment can exercise:

```text
authority_valid = true

        |
        | POST /experimental/authority-state
        | authority_valid = false
        v

process-local authority transition
true -> false

        |
        v

retained AuthorityTransition
transition_id
occurred_at
previous_authority_valid = true
current_authority_valid = false

        |
        | GET /authority-transitions/{transition_id}
        v

retrieved transition artifact

        |
        | POST /decide
        | revalidation_mode = "full"
        v

current = false
result = MISMATCH
outcome = HOLD
```

This flow exercises the same process-local transition store and execution-time revalidation mechanism used by the existing Runtime Validity implementation.

## Claim Boundary

The experimental endpoint demonstrates that a controlled HTTP request can invoke the implementation's process-local authority-state mutation path.

It does not establish:

- authentic external authority change
- identity of the party changing authority
- authorization to change authority
- authority provenance
- correctness of the authority value
- production-grade authentication
- production-grade authorization
- tamper resistance
- durable state
- distributed-state correctness
- decision-to-transition binding
- external consequential-action containment
- broader runtime-governance effectiveness

The resulting transition artifact remains self-produced process-local evidence.

The experimental control should not be exposed on an untrusted network or enabled in a production deployment.

## Scope

This mechanism exists to support controlled Runtime Validity experiments and demonstrations.

It is not a new research result or a separate research increment.
