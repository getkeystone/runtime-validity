# Increment 010: Authority Transition Evidence

Status: In Progress

## Objective

Retain explicit evidence of a process-local authority-state transition so the transition itself can be reconstructed from a stored artifact rather than relying only on the controlled test procedure.

Increment 009 established the following controlled sequence:

```text
authority_valid = true
        |
        | controlled mutation
        v
authority_valid = false
        |
        v
execution-time revalidation
```

The execution-time decision evidence records the authority value observed during revalidation.

It does not record:

- the earlier authority value
- the mutation event
- when that mutation occurred
- a stable identifier for the transition

Increment 010 addresses that specific evidence gap.

The uncertainty being tested is:

> Can a minimal retained transition record make the process-local authority change itself reconstructable without requiring the experimental test procedure to establish that the transition occurred?

This increment concerns evidence representation and retrieval.

It does not yet establish that a particular transition caused, invalidated, or was correctly associated with a particular governance decision.

## Relationship to Increment 009

Increment 009 demonstrated a bounded engineering behavior:

```text
prior expected authority = true

runtime authority:
true -> false

full revalidation:
current = false
result = MISMATCH
outcome = HOLD

no revalidation:
current = null
result = NOT_EVALUATED
outcome = PROCEED
```

However, the retained decision record cannot independently establish that:

```text
authority_valid
true -> false
```

actually occurred.

That temporal transition is currently known because the test performs it explicitly.

Increment 010 introduces a separate retained evidence artifact for the transition itself.

## Research Hypothesis

For this bounded implementation:

> If each process-local authority mutation retains a structured record containing the previous value, resulting value, transition identifier, and transition time, then the authority transition can be reconstructed from retained evidence without relying on the test procedure to supply the before-and-after values.

This is a research hypothesis about evidence representation in this implementation.

Passing tests would establish that the implementation retains and retrieves the specified transition fields.

Passing tests would not establish that the transition record is authentic, tamper-resistant, causally relevant to a particular decision, or sufficient for external governance assurance.

## Evidence Baseline

The baseline is the evidence available after Increment 009.

Increment 009 retains decision evidence containing:

```text
prior expected authority
execution-time observed authority
evaluation result
decision outcome
```

For example:

```text
expected = true
current = false
result = MISMATCH
outcome = HOLD
```

That record supports reconstruction of the execution-time comparison.

It does not independently demonstrate that the runtime state previously held:

```text
authority_valid = true
```

or that a mutation occurred between the earlier and later states.

The transition is therefore established by the controlled experimental procedure.

Increment 010 should remove that specific dependency for reconstructing the transition itself.

## Candidate Transition Record

The smallest useful transition artifact should represent:

```text
transition_id
occurred_at
previous_authority_valid
current_authority_valid
```

Conceptually:

```text
AuthorityTransition
    |
    +-- transition_id
    +-- occurred_at
    +-- previous_authority_valid
    +-- current_authority_valid
```

The exact implementation may use a Pydantic model consistent with the existing Track A code.

The transition identifier should be unique within the implementation.

The timestamp should use UTC, consistent with existing decision-record metadata.

The record should preserve both values rather than requiring a reviewer to infer the previous value from another mutable object.

## Controlled Scenario

The primary scenario remains:

```text
T0
authority_valid = true
        |
        | controlled process-local mutation
        v
T1
authority_valid = false
```

The mutation should produce a retained artifact resembling:

```text
transition_id = <uuid>
occurred_at = <UTC timestamp>
previous_authority_valid = true
current_authority_valid = false
```

The artifact should remain retrievable after the mutation while the same process is running.

## Expected Behavior

### Before mutation

The known process-local state is:

```text
authority_valid = true
```

### Mutation

The experimental harness changes authority to:

```text
authority_valid = false
```

### Transition evidence

The implementation retains:

```text
previous_authority_valid = true
current_authority_valid = false
```

along with:

```text
transition_id
occurred_at
```

### Retrieval

Given the transition identifier, the retained artifact can be retrieved during the same process lifetime.

The retrieved representation should contain the same transition values and metadata.

## Independent Variable

For the primary controlled test:

```text
process-local authority mutation:
true -> false
```

This increment does not yet compare multiple categories of governance-material change.

Additional transitions may be tested only where needed to verify the mechanics of transition recording and isolation.

## Dependent Variables

Observed outputs include:

- whether a transition record is created
- recorded previous authority value
- recorded resulting authority value
- presence of a unique transition identifier
- presence of a UTC transition timestamp
- ability to retrieve the retained transition
- behavior for unknown or malformed transition identifiers

## Acceptance Criteria

- [ ] Changing process-local authority from `true` to `false` creates a structured transition record.
- [ ] The transition record contains the previous authority value.
- [ ] The transition record contains the resulting authority value.
- [ ] The transition record contains a unique transition identifier.
- [ ] The transition record contains a UTC timestamp.
- [ ] The transition record is retained independently of the mutable current-state object.
- [ ] A retained transition can be retrieved by identifier while the same process is running.
- [ ] An unknown valid transition identifier returns an explicit not-found result.
- [ ] A malformed transition identifier is rejected by the API boundary if an HTTP retrieval endpoint is used.
- [ ] Caller input to `POST /decide` cannot fabricate or replace the server-retained transition record.
- [ ] Existing authority revalidation behavior remains unchanged.
- [ ] Existing decision-record behavior remains unchanged.
- [ ] Existing caller-supplied runtime-state rejection remains unchanged.
- [ ] Mutable transition evidence is reset or isolated between tests.
- [ ] The full existing test suite continues to pass.

## Failure Criteria

The increment fails its intended engineering test if:

- the previous authority value cannot be recovered from retained evidence
- the resulting authority value cannot be recovered from retained evidence
- a transition identifier is absent or unstable
- transition time is absent
- the retained artifact changes when the current runtime state later changes
- an unknown identifier is treated as an existing transition
- a caller can submit a transition record through the decision request and have it treated as server evidence
- adding transition evidence changes the existing full-revalidation outcome
- adding transition evidence changes the existing no-revalidation baseline
- transition artifacts leak unpredictably between tests
- existing tests regress

## Evidence Requirements

A retained transition artifact should allow a reviewer to answer:

1. What authority value existed immediately before this recorded mutation?
2. What authority value resulted from the mutation?
3. Which retained transition artifact represents the mutation?
4. When did the implementation record the mutation?

For the primary scenario, the artifact should therefore support reconstruction of:

```text
authority_valid:
true -> false
```

without requiring the reviewer to inspect the test procedure to obtain those two values.

The artifact does not yet need to prove which decision depended on that transition.

That binding remains outside the scope of this increment.

## Reconstruction Target

The minimum reconstruction target for Increment 010 is:

```text
transition record
      |
      +-- previous = true
      |
      +-- current = false
      |
      +-- occurred_at
      |
      +-- transition_id
```

A reviewer with the retained artifact should be able to state:

> The implementation recorded a process-local authority transition from `true` to `false` at the recorded time under the recorded transition identifier.

That is the maximum supported interpretation.

The reviewer should not infer from this artifact alone that:

- the transition was authentic
- the transition came from an authoritative IAM system
- the transition was governance-material
- the transition invalidated a particular prior decision
- the resulting decision was correct
- an external action was prevented

## Scope and Non-Goals

This increment does not:

- implement an external authoritative authority source
- integrate with IAM
- authenticate authority mutations
- sign transition records
- hash-chain transition records
- provide durable transition storage
- provide cross-process transition history
- provide distributed-state consistency
- establish transition causality
- bind a transition identifier to a decision record
- bind a transition identifier to a prior decision
- establish that a transition invalidates a governance decision
- establish which transitions are governance-material
- establish transition ordering across distributed systems
- implement state-version vectors
- implement logical clocks
- implement event sourcing
- implement a general evidence ledger
- establish semantic correctness of the recorded authority values
- enforce an external consequential action
- demonstrate portability
- demonstrate composition with other Governed Execution tracks

## Threats to Validity

### Process-local mutation

The transition is still produced by a process-local experimental control.

The experiment therefore demonstrates transition recording mechanics, not integration with a real authority system.

### Simplified authority model

Authority remains represented by:

```text
authority_valid: bool
```

The transition artifact therefore captures only a Boolean state change.

It does not represent:

- subject
- resource
- action
- scope
- delegation
- policy basis
- affected party
- credential
- provenance
- validity interval
- authority source

### No source authenticity

A retained transition record shows what this implementation recorded.

It does not prove that the recorded authority state came from an authentic or authoritative source.

### No integrity guarantee

A UUID and timestamp provide identity and timing metadata.

They do not prove that the transition record has not been altered.

This increment does not introduce cryptographic integrity.

### No semantic correctness guarantee

Correctly recording:

```text
true -> false
```

does not establish that either Boolean value correctly represented real-world authority.

Structural authenticity and semantic correctness remain distinct.

### No decision binding

The transition record is intentionally separate from the decision record in this increment.

A reviewer may be able to reconstruct both artifacts independently, but the implementation does not yet establish a structural relationship showing that a particular decision evaluated a particular transition or state version.

That is a candidate subsequent increment.

### Process lifetime

Transition evidence remains process-local unless the implementation explicitly introduces persistence.

Process-local retention is not durable evidence.

## Confounds

Potential confounds include:

- tests relying on shared mutable process state
- test execution order
- transition records created during fixture cleanup
- repeated assignment of the same Boolean value
- transition identifiers reused accidentally
- timestamps generated from inconsistent clocks
- transition stores not cleared between tests
- later mutations changing previously retained transition objects

The implementation and tests should make these behaviors explicit.

## Same-Value Assignment

The behavior of:

```text
true -> true
```

or:

```text
false -> false
```

must be explicitly chosen and documented.

Two reasonable designs are:

1. Treat only value changes as transitions.
2. Record every state assignment as an event.

For Increment 010, prefer the narrower transition semantics:

> A transition record represents a change in authority value.

Under that design:

```text
true -> true
```

does not create an authority transition.

This is a design choice for the reference implementation, not a general definition of governance events.

## Reproducibility Requirements

The test suite must:

- start from a known process-local authority state
- isolate transition records between tests
- perform an explicit `true` to `false` mutation
- retain the transition artifact
- verify previous and resulting values
- verify transition identity
- verify UTC time metadata
- retrieve the same retained transition
- verify unknown-record behavior
- retain existing runtime-revalidation tests
- retain existing decision-record tests
- retain existing API validation tests
- run successfully through the documented project setup
- run successfully through repository CI

## Proposed Implementation Boundary

The smallest useful implementation should add:

1. A structured authority-transition model.
2. Process-local retention of authority-transition records.
3. Transition creation when the server-controlled authority value actually changes.
4. Retrieval of a retained transition by identifier.

Conceptually:

```text
set_current_runtime_state(false)
        |
        v
read existing state
        |
        v
previous = true
current  = false
        |
        +--> update current RuntimeState
        |
        +--> create AuthorityTransition
                 |
                 +-- transition_id
                 +-- occurred_at
                 +-- previous = true
                 +-- current = false
                 |
                 v
            retain record
```

A retrieval boundary may then expose:

```text
GET /authority-transitions/{transition_id}
```

if that remains the smallest implementation consistent with the existing decision-record retrieval pattern.

The final endpoint name should remain simple and should not imply an enterprise-wide event ledger.

## Relationship to Decision Evidence

Increment 010 deliberately keeps two evidence artifacts conceptually separate:

```text
AuthorityTransition
```

and:

```text
DecisionEvidence
```

The transition artifact answers:

> What authority mutation did this implementation record?

The decision artifact answers:

> What authority condition did the execution-time decision evaluate, and what disposition resulted?

This increment does not yet answer:

> Which exact retained authority transition or state version supplied the authority value used by this exact decision?

That missing relationship should remain explicit.

## Interpretation Boundary

If the acceptance criteria pass, the supported engineering observation will be:

> In the process-local Track A implementation, an authority value change can be retained as a structured transition artifact containing the previous value, resulting value, transition identifier, and transition time, and that artifact can be retrieved independently of the experimental procedure that caused the mutation.

This would improve reconstruction of the state transition itself.

It would not establish:

- source authenticity
- evidence integrity
- semantic correctness
- causal relevance
- governance materiality
- decision-transition binding
- durable retention
- distributed ordering
- external action containment
- broader runtime-governance effectiveness

## Claim Classification

The following classifications should be preserved when this increment is completed.

### Definition

An authority transition record is the structured artifact used by this implementation to represent a change between two process-local authority values.

### Design choice

The selected fields, storage mechanism, retrieval API, UUID identifiers, and treatment of same-value assignments are implementation choices.

### Engineering observation

If tests pass, the implementation can retain and retrieve the specified transition representation under controlled conditions.

### Internal evaluation result

The repository test suite may establish that expected transition fields and retrieval behavior are produced for the controlled scenarios.

### Research hypothesis

Explicit transition evidence may improve reconstruction of governance-material runtime change.

### Not yet a research conclusion

This increment alone cannot establish that the proposed transition representation is sufficient, necessary, portable, or generally appropriate for runtime governance.

## Verification

Verification will require:

```bash
git diff --check
python -m pytest -v
```

The final observed suite result should be recorded here only after implementation, review, and successful execution.

GitHub Actions should independently execute the completed test suite through the pull-request workflow.

## Next Step

After this increment is implemented and evaluated, the next research question should examine binding:

> What evidence is required to establish that a specific execution-time governance decision evaluated a specific retained runtime state or state transition?

That would move from independently reconstructable transition evidence toward governance-decision reconstruction without assuming that timestamps or matching values alone establish causality.
