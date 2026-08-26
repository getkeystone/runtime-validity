# Increment 010: Authority Transition Evidence

Status: In Progress

## Objective

Introduce a minimal retained artifact representing a process-local authority value change so that the implementation's recorded claim about the change becomes inspectable without relying on the test procedure to supply the before-and-after values.

Increment 009 established the controlled sequence:

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

Increment 009 decision evidence records the authority value observed during execution-time revalidation.

It does not retain:

- the earlier process-local authority value
- a record asserting that a mutation occurred
- when the implementation recorded that mutation
- a stable identifier for the recorded mutation

Increment 010 addresses that specific evidence gap.

The uncertainty being examined is:

> Can a minimal retained transition artifact make the implementation's recorded before-and-after authority values and record time inspectable without requiring the test procedure to supply those values?

This increment concerns evidence representation, retention, and retrieval.

It does not establish that the retained artifact independently proves that the represented transition actually occurred, came from an authentic authority source, was governance-material, or caused a particular governance decision.

## Relationship to Increment 009

Increment 009 demonstrated the following bounded engineering behavior:

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

The retained decision evidence supports reconstruction of the execution-time comparison:

```text
expected = true
current = false
result = MISMATCH
outcome = HOLD
```

It does not independently contain an artifact representing:

```text
authority_valid:
true -> false
```

The before-and-after transition is therefore currently established by the controlled test procedure.

Increment 010 introduces a separate process-local artifact representing what the implementation recorded as that transition.

## Research Role of This Increment

Recording a state transition is not itself a novel mechanism.

Transition logs, authorization audit records, revocation records, state-version references, provenance systems, and tamper-evident logs have substantial prior art.

Increment 010 should therefore not be interpreted as proposing transition recording as a new governance primitive.

Its narrower role in Track A is to establish a candidate evidence representation that can later participate in controlled experiments about governance-decision reconstruction.

The contribution of the broader research program, if supported by later evidence, is more likely to be compositional and empirical:

- which runtime changes are governance-material
- which prior obligations those changes invalidate
- when revalidation is needed
- what retained evidence supports reconstruction of the resulting governance decision

Increment 010 addresses only one small part of that larger question.

## Terminology and Epistemic Boundary

The following distinctions are required throughout this increment.

### Recorded transition assertion

A structured artifact produced by this implementation asserting that its process-local authority value changed from one value to another.

This is what Increment 010 directly implements.

### Process-local state transition

A change in the implementation's in-memory authority value.

The mutation function and transition-recording function are colocated in this bounded implementation, but the retained record is still self-produced evidence.

### Authentic authority transition

A transition corresponding to a real change in an authoritative external authorization or delegation system.

Increment 010 does not establish this.

### Governance-material transition

A runtime change that makes a prior governance decision stale or otherwise invalid for an intended consequence.

Increment 010 does not establish this.

### Causally relevant transition

A transition whose occurrence explains or changes a particular governance decision or consequential action.

Increment 010 does not establish this.

The increment operates directly at the level of a recorded transition assertion.

It tests process-local transition-recording mechanics under controlled conditions.

It does not collapse recorded evidence into independent proof of the underlying authority fact.

## Research Hypothesis

For this bounded implementation:

> If a process-local authority value change produces a retained artifact containing the previous value, resulting value, transition identifier, and transition record time, then those recorded before-and-after values and metadata can be recovered from retained evidence without consulting the mutation step that supplied them.

This is a narrow research hypothesis about the candidate evidence representation.

Passing tests may establish that the implementation creates, retains, and retrieves the specified fields under controlled conditions.

Passing tests would not establish that:

- the underlying authority fact was correct
- the transition was authentic
- the transition record was independently witnessed
- the record was tamper-resistant
- the transition was governance-material
- the transition was causally relevant to a decision
- the representation is sufficient for external governance assurance

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

From that record alone, a reviewer can determine that execution-time evaluation observed:

```text
authority_valid = false
```

against an expected value of:

```text
authority_valid = true
```

The decision record does not contain a separate retained artifact asserting that the process-local runtime state itself changed:

```text
true -> false
```

The controlled experimental procedure currently supplies that information.

Increment 010 adds that missing representation.

## Candidate Transition Record

The candidate artifact is intentionally minimal:

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

The record preserves both values directly rather than requiring the previous value to be inferred from another mutable object.

### transition_id

A freshly generated UUID used to identify and retrieve this particular retained transition record.

UUID generation is an implementation mechanism.

The tests can establish that retained records receive identifiers and that specific generated identifiers differ where exercised.

They do not prove global uniqueness as a mathematical property.

### occurred_at

The UTC time at which this implementation creates the transition record.

It is record-time metadata.

It must not be interpreted as independent proof of when an external authority fact changed.

### previous_authority_valid

The process-local authority value read immediately before the mutation performed by the controlled mutation function.

### current_authority_valid

The process-local authority value resulting from the mutation represented by the record.

## Why No Sequence Number Yet

Prior systems commonly use state versions, sequence numbers, counters, snapshot identifiers, or other temporal markers.

Increment 010 does not introduce one.

The primary controlled experiment contains one authority transition:

```text
true -> false
```

It therefore does not test multi-transition ordering.

Adding a sequence number without evaluating ordering would introduce a field whose necessity is not exercised by the experiment.

Ordering, state versioning, and decision-to-state binding remain important later questions.

A subsequent increment may introduce a state-version or transition reference when the experiment requires a governance decision to identify the exact runtime state it evaluated.

## Initial State

The module-level initial runtime state:

```text
authority_valid = true
```

is treated as the experimental baseline state.

Import-time initialization does not create an authority transition record.

Increment 010 records changes from an already established process-local state.

This is a design choice for the reference implementation.

It is not a general definition of how system initialization should be represented in governance evidence.

## Transition Semantics

Increment 010 uses changed-value-only semantics.

A transition record represents a change in the process-local authority value.

Therefore:

```text
true -> false
```

creates a transition record.

```text
false -> true
```

creates a transition record.

```text
true -> true
```

does not create a transition record.

```text
false -> false
```

does not create a transition record.

This is a design choice for this experiment.

It does not establish that same-value assertions, renewals, heartbeats, re-attestations, or validity refreshes are never governance-relevant events.

Those cases require richer semantics than the current Boolean model provides.

## Controlled Scenario

The primary scenario is:

```text
T0
authority_valid = true
        |
        | controlled process-local mutation
        v
T1
authority_valid = false
```

The mutation should create a retained artifact resembling:

```text
transition_id = <uuid>
occurred_at = <UTC record time>
previous_authority_valid = true
current_authority_valid = false
```

The artifact should remain retrievable during the same process lifetime.

## Expected Behavior

### Before mutation

The process-local runtime state is:

```text
authority_valid = true
```

### Mutation

The experimental harness changes authority to:

```text
authority_valid = false
```

### Recorded transition assertion

The implementation creates and retains:

```text
previous_authority_valid = true
current_authority_valid = false
```

with:

```text
transition_id
occurred_at
```

### Retrieval

Given the transition identifier:

```text
GET /authority-transitions/{transition_id}
```

returns the retained artifact during the same service-process lifetime.

### Same-value assignment

Given:

```text
authority_valid = true
```

followed by:

```text
set_current_runtime_state(authority_valid=True)
```

no transition record is produced because the process-local value did not change.

## Independent Variable

For the primary scenario:

```text
process-local authority mutation:
true -> false
```

For the same-value control scenario:

```text
process-local authority assignment:
true -> true
```

This increment does not compare multiple governance-material change classes.

## Dependent Variables

Observed outputs include:

- whether a transition object is returned for an actual value change
- whether no transition object is returned for a same-value assignment
- recorded previous authority value
- recorded resulting authority value
- presence of a UUID transition identifier
- presence of UTC record-time metadata
- retained transition retrieval behavior
- unknown transition identifier behavior
- malformed transition identifier behavior
- regression behavior of existing decision and revalidation tests

## Acceptance Criteria

- [x] Changing process-local authority from `true` to `false` creates a structured transition record.
- [x] The transition record contains `previous_authority_valid = true`.
- [x] The transition record contains `current_authority_valid = false`.
- [x] The transition record receives a UUID identifier.
- [x] The transition record contains UTC record-time metadata.
- [x] The retained transition record remains unchanged when the mutable runtime state changes later.
- [x] The transition can be retrieved by identifier during the same process lifetime.
- [x] An unknown valid transition identifier returns HTTP 404.
- [x] A malformed transition identifier is rejected with HTTP 422.
- [x] Assigning the existing authority value does not create a transition record.
- [x] Caller input to `POST /decide` cannot supply a transition artifact as server-retained transition evidence.
- [x] Existing full-revalidation behavior remains unchanged.
- [x] Existing no-revalidation behavior remains unchanged.
- [x] Existing decision-record retrieval remains unchanged.
- [x] Existing caller-supplied runtime-state rejection remains unchanged.
- [x] Transition-store state is isolated between tests.
- [x] The complete existing test suite continues to pass.

## Failure Criteria

The increment fails its intended engineering test if:

- a `true -> false` process-local change produces no transition record
- the retained previous value is not `true`
- the retained current value is not `false`
- the transition lacks an identifier
- the transition lacks UTC record-time metadata
- a later state mutation changes an already retained transition record
- a retained transition cannot be retrieved by its identifier
- an unknown identifier is treated as an existing transition
- a malformed identifier bypasses API validation
- a same-value assignment is incorrectly represented as a transition under the chosen semantics
- caller-supplied transition data is accepted as server transition evidence
- existing full-revalidation behavior changes
- existing no-revalidation behavior changes
- existing decision-record behavior changes
- mutable transition-store state causes test-order dependence
- existing tests regress

## Evidence Requirements

A retained transition artifact should allow inspection of the implementation's recorded answers to:

1. What process-local authority value did the mutation function read immediately before the recorded change?
2. What process-local authority value resulted from the recorded change?
3. Which retained artifact identifies the recorded change?
4. When did this implementation create the transition artifact?

For the primary scenario, the retained artifact should therefore contain:

```text
previous_authority_valid = true
current_authority_valid = false
```

without requiring the test mutation statement itself to supply those values to the reviewer.

This is evidence of what the implementation recorded.

It is not independent verification of the underlying authority fact.

## Reconstruction Target

The minimum reconstruction target is:

```text
retained transition artifact
        |
        +-- previous = true
        |
        +-- current = false
        |
        +-- occurred_at
        |
        +-- transition_id
```

The strongest supported statement should be:

> The retained Track A artifact records that the process-local authority value changed from `true` to `false`, under the recorded transition identifier and record time.

The artifact alone does not support the stronger statement:

> An authentic external authority fact was proven to have changed from valid to invalid at this time.

The second statement requires evidence that Increment 010 does not provide.

## Baseline Comparison

The relevant comparison is conceptual and structural.

### Increment 009 baseline

Available retained evidence:

```text
expected authority = true
observed execution-time authority = false
MISMATCH
HOLD
```

Missing retained transition artifact:

```text
previous runtime state
current runtime state
transition identifier
transition record time
```

### Increment 010 treatment

Available retained evidence additionally includes:

```text
transition_id
occurred_at
previous_authority_valid
current_authority_valid
```

The treatment therefore makes the implementation's recorded before-and-after transition assertion directly inspectable.

This increment does not claim that the four fields are necessary or sufficient for general authorization reconstruction.

Field necessity and human reconstruction sufficiency remain candidate future evaluation questions.

## Scope and Non-Goals

This increment does not:

- implement an external authoritative authority source
- integrate with IAM
- model identities
- model resources
- model actions
- model authority scope
- model delegation chains
- model authorization policy
- authenticate authority mutations
- identify who caused the transition
- identify why the transition occurred
- sign transition records
- hash-chain transition records
- establish record integrity
- provide durable transition storage
- provide cross-process transition history
- provide distributed-state consistency
- establish distributed ordering
- introduce sequence numbers
- introduce state-version vectors
- introduce logical clocks
- introduce event sourcing
- introduce an evidence ledger
- establish transition causality
- bind a transition identifier to a decision record
- bind a transition identifier to a prior decision
- establish that a transition invalidates a governance decision
- establish which transitions are governance-material
- establish semantic correctness of authority values
- prove absence of unrecorded transitions
- prove that no mutation path can bypass recording
- enforce an external consequential action
- demonstrate portability
- demonstrate composition with other Governed Execution tracks
- establish sufficiency for regulatory, legal, audit, or compliance review
- establish sufficiency for independent human reconstruction

## Threats to Validity

### Self-produced evidence

The implementation that changes process-local state also creates the transition record.

The record is therefore self-reported evidence.

A defect could cause the runtime state and retained record to disagree.

Increment 010 does not provide an independent witness.

### Process-local mutation

The transition is produced by a process-local experimental control.

The experiment therefore tests transition-recording mechanics, not integration with a real authority system.

### Simplified authority representation

Authority remains:

```text
authority_valid: bool
```

The transition artifact does not represent:

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
- source identity

The reconstruction is syntactic rather than semantically complete.

### No source authenticity

A retained transition record shows what this implementation recorded.

It does not prove that either authority value came from an authentic or authoritative source.

### No integrity guarantee

A UUID and timestamp provide identity and record-time metadata.

They do not demonstrate tamper resistance.

### No semantic correctness guarantee

Correctly recording:

```text
true -> false
```

does not establish that either Boolean correctly represented real-world authority.

### No decision binding

The transition artifact remains separate from `DecisionEvidence`.

The implementation does not yet structurally establish that a particular execution-time decision evaluated the runtime state represented by a particular transition.

### No causal claim

Timestamp proximity or matching Boolean values do not establish that a transition caused a decision result.

### No ordering claim

The experiment contains one primary transition and does not evaluate histories with multiple competing transitions.

`occurred_at` is therefore record-time metadata, not a validated total-order mechanism.

### No completeness guarantee

The absence of a transition record is not general evidence that no transition occurred.

The tests exercise known mutation paths under controlled conditions.

They do not prove that all possible mutation paths are mediated by the recording function.

### Internal evaluation only

The implementation and repository tests are produced within the same research project.

Passing tests are internal evaluation results.

They are not independent validation.

### Deterministic environment

The experiment does not test:

- concurrency
- partial writes
- process crashes
- clock rollback
- network failure
- stale replicas
- distributed race conditions
- adversarial record suppression
- adversarial record modification

## Confounds

Potential confounds include:

- shared process-local mutable state
- test execution order
- fixture setup or teardown creating incidental transitions
- transition records surviving across tests
- repeated same-value assignments
- accidental dependence on wall-clock ordering
- later mutations changing retained objects
- tests inspecting global record counts rather than records created by the scenario
- evaluator logic containing knowledge supplied by the test mutation procedure

The test design should isolate transition-store state and avoid relying on aggregate store counts unless a particular count is explicitly part of the scenario.

## Test Isolation

The existing test fixture resets process-local authority state before and after each test.

Once transition recording exists, a cleanup mutation such as:

```text
false -> true
```

may itself generate a transition.

Increment 010 should therefore explicitly clear process-local transition records as part of test isolation.

The intended test fixture behavior is conceptually:

```text
establish authority baseline
clear transition records
run test
restore authority baseline
clear transition records
```

This prevents fixture-generated transition artifacts from affecting later scenarios.

This is test isolation.

It is not evidence persistence behavior for the runtime itself.

## Reproducibility Requirements

The test suite must:

- start from a known process-local authority state
- start from an isolated process-local transition store
- perform an explicit `true -> false` mutation
- verify the returned transition artifact
- verify retained previous and resulting values
- verify transition identity metadata
- verify UTC record-time metadata
- retrieve the same retained transition
- verify unknown transition behavior
- verify malformed identifier behavior
- verify same-value assignment behavior
- verify retained artifact stability across a later state change
- retain existing revalidation tests
- retain existing decision-record tests
- retain existing API-validation tests
- remain deterministic under normal test-order variation
- run successfully through the documented project setup
- run successfully through repository CI

## Proposed Implementation Boundary

The smallest useful implementation should remain colocated in:

```text
src/track_a/api.py
```

No new service, repository, persistence, or event abstractions are justified yet.

### Candidate Pydantic model

```python
class AuthorityTransition(BaseModel):
    transition_id: UUID
    occurred_at: datetime
    previous_authority_valid: StrictBool
    current_authority_valid: StrictBool
```

### Candidate process-local store

```python
authority_transitions: dict[UUID, AuthorityTransition] = {}
```

### Candidate mutation behavior

The existing:

```python
set_current_runtime_state(authority_valid=...)
```

should:

1. read the existing process-local authority value
2. compare it with the requested value
3. create no transition when the values are equal
4. when different, create a transition record containing the previous and resulting values
5. retain that record in the process-local transition store
6. update the current runtime state
7. return the created transition, or `None` for a same-value assignment

Conceptually:

```text
set_current_runtime_state(false)
        |
        v
previous = current runtime authority
        |
        v
compare previous and requested
        |
        +--> equal
        |      |
        |      v
        |   no transition
        |
        +--> different
               |
               v
        create transition record
               |
               +-- transition_id
               +-- occurred_at
               +-- previous
               +-- current
               |
               v
        retain transition
               |
               v
        update RuntimeState
```

The exact operation order should be documented by the implementation.

Increment 010 does not claim atomicity under concurrency or process failure.

## Retrieval Boundary

The increment should expose:

```text
GET /authority-transitions/{transition_id}
```

This follows the existing process-local decision-record retrieval pattern.

A known transition identifier should return the retained transition.

An unknown valid UUID should return:

```text
404
```

A malformed UUID should be rejected by FastAPI validation with:

```text
422
```

The endpoint exposes a bounded experimental artifact.

It must not be described as an enterprise audit ledger.

## Proposed Tests

The smallest useful new test set should cover the following.

### Transition creation

```text
true -> false
```

should create a transition with:

```text
previous_authority_valid = true
current_authority_valid = false
```

and valid identifier/time metadata.

### Transition retrieval

A created transition should be retrievable using:

```text
GET /authority-transitions/{transition_id}
```

### Unknown identifier

A valid UUID that does not identify a retained transition should return:

```text
404
```

### Malformed identifier

A malformed transition identifier should return:

```text
422
```

### Same-value assignment

```text
true -> true
```

should return no transition artifact under the chosen semantics.

### Artifact stability

After retaining:

```text
true -> false
```

a later:

```text
false -> true
```

mutation must not alter the already retained first transition artifact.

### Caller boundary

Supplying an `authority_transition` field through `POST /decide` should remain rejected by the existing extra-field validation boundary.

### Regression

All existing tests from Increments 001 through 009 must continue to pass.

The expected suite size will be determined after the final reviewed test set is implemented.

It should not be fixed in advance merely to satisfy an expected number.

## Relationship to Decision Evidence

Increment 010 intentionally retains two separate concepts:

```text
AuthorityTransition
```

and:

```text
DecisionEvidence
```

The transition artifact answers:

> What process-local authority change did this implementation record?

The decision evidence answers:

> What authority condition did the execution-time governance decision evaluate, and what disposition resulted?

Increment 010 does not yet answer:

> Which exact retained transition or state version supplied the runtime authority evaluated by this exact decision?

That missing relationship is deliberate.

## Prior-Art Implication for Later Work

Prior work suggests that stronger authorization reconstruction commonly requires concepts such as:

- subject
- object or protected resource
- action
- policy or authority-state version
- provenance
- issuer
- sequence or temporal marker
- delegation or causal references
- integrity protection

Increment 010 intentionally does not import those mechanisms wholesale.

The four-field candidate record is a bounded experimental representation for one process-local Boolean authority transition.

Later experiments should add richer fields only when a specific falsifiable question requires them.

## Interpretation Boundary

If the acceptance criteria pass, the strongest supported engineering observation will be:

> In the process-local Track A implementation, a controlled authority value change can produce a retained structured artifact containing the implementation-recorded previous value, resulting value, transition identifier, and UTC record time, and that artifact can be retrieved independently of the test statement that requested the mutation.

This establishes the implemented representation and retrieval behavior under controlled conditions.

It does not establish:

- that the retained artifact independently proves the transition occurred
- source authenticity
- evidence integrity
- semantic correctness
- governance materiality
- causal relevance
- decision-transition binding
- durable retention
- multi-transition ordering
- distributed correctness
- external action containment
- independent reviewer sufficiency
- broader runtime-governance effectiveness

## Claim Classification

### Definition

A recorded authority transition assertion is the structured artifact used by this implementation to represent a change between two process-local Boolean authority values.

### Design choice

The following are design choices:

- four-field transition representation
- changed-value-only transition semantics
- UUID identifiers
- UTC record-time metadata
- process-local retention
- HTTP retrieval boundary
- omission of sequence numbers in this increment
- test-store isolation behavior

### Engineering observation

If tests pass, the implementation can create, retain, and retrieve the specified transition representation under the controlled scenarios.

### Internal evaluation result

The repository test suite may establish that the expected representation and retrieval behaviors occur in the exercised scenarios.

### External evidence

Prior authorization, audit, state-continuity, revocation, and provenance work establishes that transition recording and evidence retention are existing mechanism families.

That prior art constrains novelty claims.

### Research hypothesis

Explicitly retained transition representations may contribute to later reconstruction of governance-material runtime change when composed with decision evidence and evaluated against stronger baselines.

### Not yet a research conclusion

Increment 010 alone cannot establish that the four-field representation is:

- necessary
- sufficient
- authentic
- tamper-resistant
- semantically correct
- portable
- generally appropriate for runtime governance
- sufficient for external governance assurance

## Verification

Local verification completed on the Increment 010 feature branch with:

```bash
git diff --check
python -m pytest -v
```

Observed local result:

```text
20 passed in 0.24s
```

The 20-test suite includes the 13 tests retained from Increments 001 through 009 and 7 Increment 010 tests covering:

- transition creation for a controlled `true -> false` authority change
- UUID and UTC record-time metadata
- retrieval by transition identifier
- HTTP 404 for an unknown valid transition identifier
- HTTP 422 for a malformed transition identifier
- no transition record for a same-value assignment
- retained transition stability across a later authority change
- rejection of caller-supplied transition evidence

The test fixture also isolates the process-local transition store before and after each test.

This is an internal evaluation result under controlled process-local conditions.

It establishes that the implementation exhibits the specified transition-recording and retrieval behavior in the exercised scenarios.

It does not independently establish:

- authenticity of the represented authority transition
- integrity or tamper resistance of the retained artifact
- semantic correctness of the authority values
- completeness of transition capture outside the exercised mutation path
- governance materiality
- causal relevance to a particular decision
- decision-transition binding
- correctness under concurrency or distributed execution
- durability across process restart
- independent validation
- broader runtime-governance effectiveness

GitHub Actions verification through the pull-request workflow remains pending.

The increment should remain `In Progress` until that repository-level verification succeeds.

## Next Step

After Increment 010 is implemented and reviewed, the next candidate experiment should examine decision-to-state binding:

> What retained evidence is required to establish that a specific execution-time governance decision evaluated a specific runtime state or transition representation?

That experiment should consider whether a decision requires an explicit:

```text
state_version
```

or:

```text
transition reference
```

rather than relying on:

- timestamp proximity
- matching Boolean values
- test-procedure knowledge

A later experiment can then ask whether such binding improves reconstruction of why a consequential action proceeded, was held, denied, or escalated.
