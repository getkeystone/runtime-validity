# Increment 009: Authority Change Revalidation

Status: In Progress

## Objective

Test whether execution-time revalidation detects a change in server-controlled authority state that conflicts with the authority assumption attached to a prior decision.

The uncertainty being tested is:

> When authority is represented as valid for a prior decision but becomes invalid before execution, does full revalidation detect the mismatch while a no-revalidation baseline leaves the changed authority condition unevaluated?

This increment introduces an explicit runtime-change scenario rather than only testing independently supplied matching and mismatching authority values.

## Scenario

The controlled scenario is:

```text
T0
authority_valid = true
        |
        | prior decision represents
        | an authority-valid assumption
        v
prior decision
        |
        | runtime authority changes
        v
T1
authority_valid = false
        |
        v
POST /decide
        |
        +-----------------------+
        |                       |
 revalidation=full       revalidation=none
        |                       |
        v                       v
 expected=true             NOT_EVALUATED
 current=false                  |
 MISMATCH                       |
        |                       |
       HOLD                  PROCEED
```

The comparison between `full` and `none` is central to this increment.

The `none` case represents a baseline in which the prior authority assumption is not re-evaluated at execution time.

The `full` case represents the current execution-time revalidation mechanism.

## Research Hypothesis

For this bounded implementation:

> If server-controlled authority changes from valid to invalid after the state represented by a prior decision, full revalidation will detect the resulting mismatch, while the no-revalidation baseline will not evaluate the changed authority state.

This is a research hypothesis for this implementation and scenario.

It is not a conclusion about runtime governance generally, nor does it establish that all authority changes should invalidate all prior governance decisions.

## Independent Variable

Revalidation mode:

- `full`
- `none`

The controlled authority-change scenario remains otherwise equivalent.

## Dependent Variables

Observed outputs include:

- decision outcome
- obligation evaluation result
- current authority value recorded during evaluation
- whether the changed authority condition was evaluated

## Controlled Runtime Change

The process-local authority source supports controlled state mutation for the experimental test harness.

The test sequence explicitly establishes:

```text
authority_valid = true
```

followed by:

```text
authority_valid = false
```

before the execution-time decision is evaluated.

The decision request itself does not control this mutation.

The mutation mechanism is an internal process-local test mechanism. It is not exposed as an HTTP authority-management API.

## Expected Behavior

### Full revalidation

After the authority change:

```text
expected = true
current = false
result = MISMATCH
outcome = HOLD
```

For this implementation, `HOLD` is the selected response to an authority-obligation mismatch.

That is a design choice for the experiment, not a general conclusion that every authority mismatch should produce `HOLD`.

### No-revalidation baseline

Under the same changed authority condition:

```text
current = null
result = NOT_EVALUATED
outcome = PROCEED
```

`PROCEED` in the no-revalidation case does not mean the action is justified.

It means this implementation did not re-evaluate the changed authority condition.

The experiment does not currently enforce an external consequential action after the returned decision.

## Acceptance Criteria

- [ ] The server-controlled authority source can be changed independently of the decision request.
- [ ] Tests establish an authority-valid state before the simulated runtime change.
- [ ] Tests change authority to invalid before execution-time evaluation.
- [ ] Full revalidation observes the changed authority state.
- [ ] Full revalidation records `MISMATCH`.
- [ ] Full revalidation returns `HOLD`.
- [ ] The same changed-state scenario under `revalidation_mode: "none"` records `NOT_EVALUATED`.
- [ ] The no-revalidation baseline does not record the changed authority value as evaluated.
- [ ] Caller-supplied runtime authority remains rejected.
- [ ] Existing decision evidence and record retrieval behavior remains intact.
- [ ] Runtime state is reset between tests so scenarios remain isolated and reproducible.

## Baseline

The primary baseline in this increment is:

```text
revalidation_mode = none
```

This baseline represents execution without re-evaluating the authority obligation.

It should not be interpreted as a complete implementation of admission-time authorization.

The prior decision remains a controlled fixture representing an earlier `PROCEED` decision with an authority-valid obligation.

## Failure Criteria

The increment fails its intended behavioral test if:

- full revalidation returns `PROCEED` despite observing the changed authority state
- full revalidation does not record the authority mismatch
- no-revalidation unexpectedly evaluates the changed authority state
- the decision request can directly control the authority value used for revalidation
- mutable runtime state leaks between tests
- test outcomes depend on test execution order

## Evidence Requirements

A successful execution-time decision record must make it possible to reconstruct:

- the prior expected authority condition
- whether revalidation occurred
- the current authority value when evaluated
- whether the obligation matched or mismatched
- the resulting `PROCEED` or `HOLD` disposition

The current decision evidence records the prior expected authority condition and the authority value observed during revalidation.

It does not record the earlier process-local authority value or the mutation event that changed authority from valid to invalid.

In this increment, the temporal transition is established by the controlled test procedure rather than reconstructed from the retained decision record alone.

Recording governance-material state transitions as evidence remains a separate research and engineering question.

The current evidence also does not prove that the observed authority state is correct, authentic, authoritative, or semantically sufficient for the intended consequence.

## Scope and Non-Goals

This increment does not:

- implement an admission-time authorization service
- prove that the prior decision was correctly issued
- prove that authority was valid when the prior decision was issued
- authenticate authority mutations
- integrate with an external IAM or delegation system
- model multiple identities, resources, actions, or scopes
- model delegation chains or conditional authority
- establish authority provenance
- retain durable authority-state history
- retain the authority mutation event in the decision record
- provide distributed state consistency
- enforce an external consequential action
- establish that `HOLD` is the correct response for every authority mismatch
- establish a general theory of governance-material change
- demonstrate that the broader Governed Execution platform is validated

## Threats to Validity

### Simulated prior decision

The prior decision remains a controlled test fixture rather than an artifact issued by an independently implemented admission-time authorization mechanism.

The experiment therefore does not demonstrate an end-to-end authorization lifecycle.

### Simplified authority representation

Authority is represented by a single Boolean:

```text
authority_valid
```

This does not capture:

- subject identity
- resource
- action
- scope
- delegation chain
- policy conditions
- affected party
- provenance
- validity interval
- authority source authenticity

The experiment therefore tests the mechanics of detecting one bounded authority-state mismatch, not the adequacy of the authority model.

### Process-local state

The authority source remains process-local.

The experiment does not test:

- external authoritative state
- distributed consistency
- concurrent updates
- stale replicas
- network partitions
- source authentication
- source availability

### Transition evidence

The controlled test establishes a `true` to `false` transition, but the retained decision record does not itself contain evidence of the mutation event.

A reviewer can reconstruct the execution-time comparison from the decision record, but reconstructing the complete temporal transition currently requires the controlled test procedure.

### Outcome semantics

`HOLD` is the response selected by this implementation for a detected mismatch.

The experiment tests whether the mechanism produces the expected configured response.

It does not independently establish that `HOLD` is the substantively correct governance decision for every real-world authority change.

### No external consequence

The current implementation returns a governance decision but does not yet bind that decision to an external action boundary.

A returned `HOLD` therefore demonstrates decision behavior, not containment of a real external consequence.

## Reproducibility Requirements

The test suite must:

- start from a known authority state
- explicitly establish the pre-change authority condition
- explicitly perform the authority state transition
- evaluate the execution-time decision after the transition
- compare `full` and `none` revalidation behavior
- isolate mutable state between tests
- preserve deterministic expected outcomes
- retain existing API validation behavior
- retain existing decision-record retrieval behavior
- run successfully through the documented project setup
- run successfully through the repository CI workflow

## Current Implementation

The implementation introduces a narrow process-local mutation function:

```python
set_current_runtime_state(authority_valid=...)
```

The function changes the server-controlled `RuntimeState` used by the existing runtime-state dependency.

It is used by the experimental test harness to create an explicit authority transition before calling `POST /decide`.

It is not exposed through the decision request or as an HTTP endpoint.

Two controlled scenarios are tested.

### Full revalidation scenario

```text
authority = true
       |
       | controlled mutation
       v
authority = false
       |
       v
POST /decide
revalidation_mode = full
       |
       v
current = false
result = MISMATCH
outcome = HOLD
```

### No-revalidation scenario

```text
authority = true
       |
       | controlled mutation
       v
authority = false
       |
       v
POST /decide
revalidation_mode = none
       |
       v
current = null
result = NOT_EVALUATED
outcome = PROCEED
```

The autouse test fixture resets the process-local authority state before and after each test so the mutable experimental state does not intentionally carry across test cases.

## Interpretation Boundary

If the expected tests pass, the supported engineering observation is narrow:

> In this process-local implementation, when the controlled authority state changes from `true` to `false` before execution-time evaluation, full revalidation observes the changed state and produces `MISMATCH` and `HOLD`, while the no-revalidation baseline leaves the authority obligation `NOT_EVALUATED` and returns `PROCEED`.

This would demonstrate the implemented behavior under the controlled scenario.

It would not establish:

- that every authority change is governance-material
- that the prior decision was originally justified
- that Boolean authority adequately represents real authorization
- that the authority source is trustworthy
- that `HOLD` is universally appropriate
- that the resulting evidence is sufficient for independent governance assurance
- that an external action would actually be prevented
- that the mechanism generalizes to policy, evidence, target, tool, or execution-state changes
- that the mechanism remains correct when composed with other Governed Execution tracks

## Verification

Verification requires:

```bash
git diff --check
python -m pytest -v
```

The expected suite size after this increment is:

```text
13 tests
```

The final observed result should be recorded here only after the reviewed implementation and documentation changes have been rerun successfully.

## Next Step

After final verification:

1. Mark the acceptance criteria according to observed behavior.
2. Record the final test result.
3. Complete this increment document.
4. Review the branch diff against `main`.
5. Open the Increment 009 pull request.

A subsequent research increment can address what evidence is required to represent and reconstruct governance-material state transitions themselves, rather than relying on the experimental procedure to establish that the transition occurred.
