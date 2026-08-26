# Increment 009: Authority Change Revalidation

Status: In Progress

## Objective

Test whether a change in server-controlled authority state can invalidate the authority assumption attached to a prior decision before consequential execution.

The uncertainty being tested is:

> When authority is represented as valid for a prior decision but becomes invalid before execution, does full revalidation detect the change and prevent the prior decision from proceeding unchanged?

This increment introduces an explicit runtime-change scenario rather than only testing independently supplied matching and mismatching values.

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

The comparison between `full` and `none` is important.

The `none` case represents a baseline in which the prior authority assumption is not re-evaluated at execution time.

The `full` case represents the current change-aware revalidation mechanism.

## Research Hypothesis

For this implementation:

> If server-controlled authority changes from valid to invalid after the state represented by a prior decision, full revalidation will detect the mismatch, while the no-revalidation baseline will not evaluate the changed authority state.

This is a research hypothesis for this bounded implementation, not a conclusion about runtime governance generally.

## Independent Variable

Revalidation mode:

- `full`
- `none`

The authority-change scenario remains otherwise equivalent.

## Dependent Variables

Observed outputs include:

- decision outcome
- obligation evaluation result
- current authority value recorded in evidence
- whether the changed authority state was evaluated

## Controlled Runtime Change

The process-local authority source will support controlled state mutation for tests.

The test sequence will explicitly establish:

```text
authority_valid = true
```

followed by:

```text
authority_valid = false
```

before the execution-time decision is evaluated.

The action request itself will not control this mutation.

## Expected Behavior

### Full revalidation

After the authority change:

```text
expected = true
current = false
result = MISMATCH
outcome = HOLD
```

### No revalidation baseline

Under the same changed authority condition:

```text
current = null
result = NOT_EVALUATED
outcome = PROCEED
```

`PROCEED` in the no-revalidation case does not mean the action is justified.

It means this implementation did not re-evaluate the changed authority condition.

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

## Failure Criteria

The increment fails its intended behavioral test if:

- full revalidation proceeds despite the changed authority state
- full revalidation does not record the mismatch
- no-revalidation accidentally evaluates the changed state
- the decision request can directly control the authority state
- test results depend on execution order or leaked mutable state

## Evidence Requirements

A successful experimental run must make it possible to reconstruct:

- the prior expected authority condition
- whether revalidation occurred
- the current authority value when evaluated
- whether the obligation matched or mismatched
- the resulting `PROCEED` or `HOLD` disposition

The current evidence does not prove that the authority state itself is correct or authoritative.

## Scope and Non-Goals

This increment does not:

- implement an admission-time authorization service
- prove that the prior decision was correctly issued
- authenticate authority mutations
- integrate with an external IAM or delegation system
- model multiple identities, resources, or actions
- establish authority provenance
- provide durable authority-state history
- provide distributed state consistency
- enforce an external consequential action
- claim that every authority change should produce `HOLD`

## Threats to Validity

The prior decision remains a controlled test fixture rather than an artifact issued by an independently implemented admission-time authorization mechanism.

The authority source remains process-local.

The current authority model is a single Boolean and does not capture subject, resource, scope, delegation chain, conditions, or provenance.

The experiment therefore tests the mechanics of detecting a bounded authority-state change, not the adequacy of the authority representation itself.

## Reproducibility Requirements

The test suite must:

- start from a known authority state
- explicitly perform the state transition
- isolate mutable state between tests
- preserve deterministic expected outcomes
- run successfully through the documented project setup and CI workflow

## Next Step

Implement a controlled process-local authority-state transition and compare full revalidation against the no-revalidation baseline.
