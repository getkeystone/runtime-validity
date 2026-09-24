# Increment 013: Design Executable Witness Model and Intervention Matrix

Status: Complete

## Objective

Design, before implementation, the executable witness representation and
controlled intervention matrix for the four dependencies selected in Increment
011.

The design must establish exactly:

- what was bound at T0;
- what current witness must be observed at T1;
- how the intervention is applied;
- what other variables must remain fixed;
- how `INVALIDATED` versus `PRESERVED` is determined;
- what happens when the required current witness cannot be successfully obtained
  or assessed;
- what evidence must be retained so the mapping result is reconstructable.

The uncertainty being reduced is:

> Can the four selected dependencies be represented and intervened on
> independently, with prospective mapping semantics that distinguish known
> dependency failure from failure to obtain or assess the required current
> witness?

This increment defines a prospective experimental design. It does not implement
or execute that design.

## Track A Research Role

The controlling Track A research question is:

> Given a prior decision justification composed of heterogeneous governance
> obligations, which controlled runtime interventions invalidate which
> obligations, and under what conditions does obligation-scoped revalidation
> preserve the same policy-expected disposition as full commit-boundary
> reevaluation with lower revalidation work?

The priority ordering remains:

1. intervention-to-dependency invalidation mapping;
2. disposition preservation against full commit-boundary reevaluation;
3. revalidation work or latency only after disposition equivalence.

Increment 013 prepares the first item. It also records the minimum state that a
later implementation would need to prepare for the second item. It does not
evaluate either item.

## Scope

Design only:

- a minimal experiment-local witness observation representation;
- T0 and T1 witness requirements for the four selected dependencies;
- one canonical preserved, invalidated, and non-evaluable family per dependency;
- a deliberate-no-revalidation control distinct from failed witness observation;
- controls required to isolate one dependency per intervention;
- minimum diagnostic evidence required to reconstruct a later mapping result;
- prerequisites for later full and scoped reevaluation arms.

This increment introduces:

- no runtime implementation;
- no API change;
- no scoped-revalidation engine;
- no experiment execution;
- no disposition-performance result;
- no claim that the selected four dependencies form a complete ontology.

## Non-Goals

This increment does not:

- adopt UTDA as a Track A dependency model;
- add `COLLAPSED` or any UTDA-specific state;
- implement probabilistic confidence;
- implement general provenance or lineage;
- implement delegation lifecycle;
- implement distributed revocation reachability;
- introduce external witnesses;
- design or execute Track B-F experiments;
- add causal/ordering priority;
- add policy-state currency;
- add required-witness coverage's type/binding sub-case;
- assign a universal policy disposition to unavailable evidence;
- define production fail-open or fail-closed behavior;
- implement durable evidence, cryptographic integrity, or external consequence
  enforcement.

## Starting State

Increment 011 selected four dependencies for the first bounded experiment:

1. witness/authorization freshness;
2. effect/action binding;
3. authorizing-path eligibility;
4. required-witness coverage, limited to the absence sub-case.

Increment 011 explicitly deferred policy-state currency, causal/ordering
priority, and the required-witness type/binding sub-case.

No executable heterogeneous witness model exists. `/decide` still implements
only the bounded `authority_valid` obligation. Its current runtime state is a
strict Boolean, and its evaluated results are `MATCH` or `MISMATCH`. When
`revalidation_mode="none"`, it records `NOT_EVALUATED` instead of attempting
revalidation.

No Track A invalidation-mapping experiment has been run. No obligation-scoped
revalidation exists. Full commit-boundary reevaluation remains the strong future
comparison arm. The existing authority demo and internal tests establish bounded
engineering behavior only; they are not a Track A invalidation result.

The current committed test record reports 23 passing tests. This is an internal
test result for the existing implementation, not an experimental result for this
increment.

## Experimental Semantics

The design keeps four concepts separate:

```text
witness acquisition / assessability
        !=
dependency-specific observed value
        !=
derived invalidation mapping
        !=
policy disposition
```

### Candidate observation representation

The minimum prospective representation is:

```text
observation_attempted:
    false
    true

observation_status:
    AVAILABLE
    UNAVAILABLE
    present only when observation_attempted = true

observation_failure_reason:
    null when observation_status = AVAILABLE
    otherwise exactly one of:
        OBSERVATION_SOURCE_MISSING
        INACCESSIBLE
        MALFORMED
        INCOMPLETE
        OTHER_DECLARED_FAILURE

dependency_value:
    dependency-specific value
    meaningful only when observation_status = AVAILABLE

mapping_result:
    PRESERVED
    INVALIDATED
    NON_EVALUABLE

deliberate control result when observation_attempted = false:
    NOT_EVALUATED
```

These names are design candidates for a later experiment-local model, not new
public Runtime Validity API states.

### Invariants

1. `observation_attempted = false` means current witness observation was
   deliberately not attempted. It has no `observation_status`, no current
   dependency value, and the deliberate control result is `NOT_EVALUATED`.
2. `observation_attempted = true` requires `observation_status` to be either
   `AVAILABLE` or `UNAVAILABLE`.
3. `AVAILABLE` requires a successfully obtained and assessed
   dependency-specific value and a null failure reason.
4. `UNAVAILABLE` requires a declared failure reason and no interpreted
   dependency value.
5. `PRESERVED` or `INVALIDATED` may be assigned only when the required current
   witness is `AVAILABLE` and assessable.
6. `observation_attempted = true` plus `UNAVAILABLE` always derives
   `NON_EVALUABLE` for the dependency mapping.
7. `NON_EVALUABLE` is retained as a separately reported experimental condition
   and excluded from invalidation-mapping accuracy and disposition-equivalence
   calculations. It is not silently discarded as though no run occurred.
8. The experiment records the observation attempt and failure reason even when
   no mapping classification can be made.
9. `OBSERVATION_SOURCE_MISSING` means the source needed to perform the current
   observation could not be obtained. It does not mean that a successfully
   observed required-witness inventory explicitly lacked a member.

`NON_EVALUABLE` is not:

- a public Runtime Validity outcome;
- `HOLD`;
- `DENY`;
- `ESCALATE`;
- `NOT_EVALUATED`;
- `UNKNOWN` or `UNAVAILABLE` as a universal ontology term;
- UTDA `COLLAPSED` or UTDA invalidity.

### Deliberate non-evaluation

The existing:

```text
revalidation_mode = "none"
```

means revalidation was intentionally not attempted. It produces the current
implementation's `NOT_EVALUATED` result.

That is distinct from:

```text
revalidation attempted
    +
required current witness could not be obtained or assessed
    ->
NON_EVALUABLE
```

The first bounded experiment must record those paths separately.

```text
observation_attempted = false
    !=
observation_attempted = true + observation_status = UNAVAILABLE

NOT_EVALUATED
    !=
NON_EVALUABLE
```

## Dependency 1: Witness / Authorization Freshness

### Source grounding

Increment 011 derives this dependency from CommitGuard's `Freshness` condition
and folds in only SAGE-Fin coverage debt's staleness sub-case. Increment 011 is
the canonical source record; this increment does not repeat or extend its
literature claim.

### Prospective design

1. **T0 witness:** stable witness identifier, deterministic scalar age in
   fixture-controlled integer/logical units, fixed maximum allowed age, and a T0
   assessment that `age <= maximum_age`.
2. **T1 witness:** the same witness identifier and a successfully observed
   deterministic scalar age in the same fixture-controlled units.
3. **Witness identity:** the witness record must remain present and retain the
   same identity from T0 to T1.
4. **Invalidating intervention:** set the same present witness's scalar age to a
   value greater than the fixed maximum allowed age.
5. **Fixed controls:** witness presence, fixture-local `effect_id`,
   authorizing-path liveness, required-witness membership, threshold, and frozen
   policy composition.
6. **`PRESERVED`:** the T1 witness is available and
   `age <= maximum_age`.
7. **`INVALIDATED`:** the T1 witness is available and assessable, remains
   present, and is stale under the fixed threshold.
8. **`NON_EVALUABLE`:** the witness or the value needed to assess its age cannot
   be obtained or assessed.
9. **Required evidence:** witness ID, T0 and T1 scalar ages, maximum allowed age,
   observation status, failure reason if any, derived mapping, intervention ID,
   and fixed-control snapshot.
10. **Nearest confound:** required-witness coverage.
11. **Confound control:** change only the scalar age in place; never delete the
    witness or remove it from the required set.
12. **Implementation requirement:** stable witness identity plus a scalar age in
    fixture-controlled integer/logical units and a fixed-threshold comparison.
13. **Frozen first-experiment representation:** fixture-controlled scalar age
    and fixed maximum allowed age. Wall-clock timestamps, distributed-clock
    behavior, validity intervals, and expiry lifecycle machinery are outside this
    design.

A stale witness successfully observed is a known invalidation. A witness that
cannot be observed or assessed is non-evaluable, not stale.

## Dependency 2: Effect / Action Binding

### Source grounding

Increment 011 derives this dependency from CommitGuard's `Effect binding`
condition.

### Prospective design

1. **T0 witness:** the fixture-local `effect_id` bound to the prior decision.
2. **T1 witness:** the fixture-local `effect_id` for the exact proposed
   consequential effect.
3. **Witness identity:** `effect_id` is an opaque fixture-local identifier for
   the exact proposed consequential effect represented by the fixture. The
   canonical values are `effect-A` and `effect-B`.
4. **Invalidating intervention:** substitute `effect-B` at T1 while retaining a
   prior decision bound to `effect-A`.
5. **Fixed controls:** witness freshness, authorizing-path liveness,
   required-witness completeness, frozen policy, and the substituted target's
   independent eligibility.
6. **`PRESERVED`:** both identifiers are available and both equal `effect-A`.
7. **`INVALIDATED`:** both identifiers are available and the prior bound
   `effect-A` differs from current proposed `effect-B`.
8. **`NON_EVALUABLE`:** either required identifier cannot be successfully
   established or cannot be compared in the declared namespace.
9. **Required evidence:** T0 `effect_id`, T1 `effect_id` when available,
   observation status for each required observation, failure reason, equality
   result, mapping result, intervention ID, and fixed controls.
10. **Nearest confound:** authorizing-path eligibility.
11. **Confound control:** select a substitute effect whose authorizing path remains
    independently eligible; change only the fixture-local `effect_id`.
12. **Implementation requirement:** a T0 fixture-local `effect_id`, a T1 proposed
    fixture-local `effect_id`, and an equality comparison.
13. **Frozen first-experiment representation:** opaque fixture-local strings.
    URIs, global uniqueness, hashes, target/action decomposition, and artifact
    identity architecture are not required. This is an experiment-local
    operationalization of Increment 011's effect/action-binding dependency, not
    a universal identity model.

Identifier unavailability is not a binding mismatch.

## Dependency 3: Authorizing-Path Eligibility

### Source grounding

Increment 011 derives this dependency from CommitGuard's `Commit eligibility`
condition and uses the normalized label `authorizing-path eligibility` because
the source condition concerns the authorizing path's liveness.

### Prospective design

1. **T0 witness:** stable `authorizing_path_id` and
   `authorizing_path_live = true`.
2. **T1 witness:** the Boolean `authorizing_path_live` value for that same
   `authorizing_path_id`.
3. **Witness identity:** the path, approval epoch, or authorization marker must
   retain the same identity from T0 to T1.
4. **Invalidating intervention:** apply one declared controlled revocation (or
   equivalent declared intervention) that changes `authorizing_path_live` from
   `true` to `false`. The intervention cause is not part of the dependency value.
5. **Fixed controls:** fixture-local `effect_id`, witness freshness,
   required-witness completeness, path identity, and frozen policy.
6. **`PRESERVED`:** current liveness is available and remains `true`.
7. **`INVALIDATED`:** current liveness is available and is `false`.
8. **`NON_EVALUABLE`:** current liveness cannot be obtained or assessed.
9. **Required evidence:** path identifier, T0 and T1 liveness values when
   available, observation status, failure reason, intervention ID, mapping
   result, and fixed-control snapshot.
10. **Nearest confound:** effect/action binding.
11. **Confound control:** mutate only the dedicated liveness value; do not clear
    or replace the fixture-local `effect_id` or path identifier.
12. **Implementation requirement:** a dedicated `authorizing_path_id` and a
    separate Boolean `authorizing_path_live` value.
13. **Frozen first-experiment representation:** stable path ID plus Boolean live
    state. Lifecycle enums, retry/delegation state, distributed revocation
    reachability, and propagation semantics are outside this design.

An explicit, successfully observed not-live value is a known negative. Failure
to establish current liveness is non-evaluable, not revoked and not invalidated.

## Dependency 4: Required-Witness Coverage

### Source grounding

Increment 011 derives this dependency from SAGE-Fin coverage debt and limits the
first experiment to the absence sub-case. Type/binding insufficiency remains
deferred.

### Prospective design

1. **T0 witness:** the fixed fixture-local required-ID set `{W1, W2}` and the
   successfully observed present-ID set `{W1, W2}`.
2. **T1 witness:** a successfully and completely observed present-ID set for the
   same fixed required-ID set.
3. **Witness identity:** the required IDs `W1` and `W2` remain stable from T0 to
   T1.
4. **Invalidating intervention:** remove exactly `W2`, producing the successfully
   observed present-ID set `{W1}`, while `W1` stays present and unaged.
5. **Fixed controls:** required-set definition, age of remaining witnesses,
   fixture-local `effect_id`, authorizing-path liveness, and frozen policy.
6. **`PRESERVED`:** inventory observation succeeds and present IDs are
   `{W1, W2}`.
7. **`INVALIDATED`:** inventory observation succeeds and present IDs are `{W1}`,
   establishing known absence of required member `W2`.
8. **`NON_EVALUABLE`:** the required-set definition or current inventory cannot
   be obtained or assessed completely. Failed inventory observation must not be
   interpreted as witness absence.
9. **Required evidence:** required member IDs, T0 and T1
   membership when available, removed witness ID for the intervention,
   observation status, failure reason, mapping result, and fixed controls.
10. **Nearest confound:** witness/authorization freshness.
11. **Confound control:** remove the witness rather than aging it; keep all other
    witnesses present and current.
12. **Implementation requirement:** fixed required-ID set `{W1, W2}`, observed
    present-ID set, and complete inventory/membership assessment.
13. **Frozen first-experiment representation:** normalized fixture-local sets of
    required and present IDs. Witness type, binding, provenance, and general
    coverage-debt semantics remain outside this design.

Known absence may invalidate coverage. Inability to read the inventory is
non-evaluable and must never be used to infer absence.

An empty or missing inventory is not used to represent either condition. An
available inventory contains the observed present-ID set. An inventory that
cannot be obtained or assessed is `UNAVAILABLE` and has no interpreted present-ID
set.

## Canonical Valid Baseline Fixture

All scenarios use one shared fixture-local baseline unless a scenario declares
one delta:

```text
freshness:
    witness_id = witness-A
    age = 1
    maximum_age = 2

binding:
    prior_bound_effect_id = effect-A
    current_proposed_effect_id = effect-A

eligibility:
    authorizing_path_id = path-A
    authorizing_path_live = true

coverage:
    required_ids = {W1, W2}
    present_ids = {W1, W2}
```

Every dependency-mapping invalidation scenario changes exactly one selected
dependency value from this baseline. Every observation-failure control leaves
the baseline's substantive value unchanged and changes only whether the current
observation can be successfully obtained or assessed.

## Prospective Scenario Matrix

The matrix contains three distinct scenario classes. The eight dependency-mapping
scenarios are the primary intervention-to-dependency experiment. Four
observation-failure controls test observation/mapping separation and are not
dependency-invalidating interventions. One deliberate-no-revalidation control
tests the distinction between `NOT_EVALUATED` and `NON_EVALUABLE`.

Each row is a delta from the canonical valid baseline above. `mapping
interpretation` is diagnostic only and does not assign a policy disposition.

| scenario class | scenario_id | dependency | scenario delta | observation_attempted | observation_status | observation_failure_reason | T1 observed value | expected mapping result | mapping interpretation | confound control |
|---|---|---|---|---|---|---|---|---|---|---|
| dependency mapping | fresh-preserved | freshness | none | true | AVAILABLE | null | age = 1; maximum_age = 2 | PRESERVED | currentness unchanged | same witness remains present |
| dependency mapping | fresh-invalidated | freshness | set age = 3 | true | AVAILABLE | null | age = 3; maximum_age = 2 | INVALIDATED | known stale witness | change age only; do not delete witness |
| dependency mapping | binding-preserved | binding | none | true | AVAILABLE | null | prior/current = effect-A | PRESERVED | exact effect unchanged | substitute not introduced |
| dependency mapping | binding-invalidated | binding | set current effect_id = effect-B | true | AVAILABLE | null | effect-A differs from effect-B | INVALIDATED | known exact-effect mismatch | effect-B remains independently eligible |
| dependency mapping | eligibility-preserved | eligibility | none | true | AVAILABLE | null | path-A live = true | PRESERVED | path remains live | effect_id unchanged |
| dependency mapping | eligibility-invalidated | eligibility | set path-A live = false | true | AVAILABLE | null | path-A live = false | INVALIDATED | known path ineligibility | path/effect IDs unchanged |
| dependency mapping | coverage-preserved | coverage | none | true | AVAILABLE | null | present = {W1, W2} | PRESERVED | required set complete | complete inventory observed |
| dependency mapping | coverage-invalidated | coverage | remove W2 | true | AVAILABLE | null | present = {W1} | INVALIDATED | known absence of W2 | W1 remains present/current; inventory complete |
| observation failure | fresh-non-evaluable | freshness | make age observation unavailable; substantive age remains 1 | true | UNAVAILABLE | OBSERVATION_SOURCE_MISSING | none | NON_EVALUABLE | no freshness mapping | do not infer stale |
| observation failure | binding-non-evaluable | binding | make current effect_id observation unavailable; substantive ID remains effect-A | true | UNAVAILABLE | OBSERVATION_SOURCE_MISSING | none | NON_EVALUABLE | no binding mapping | do not infer mismatch |
| observation failure | eligibility-non-evaluable | eligibility | make liveness observation unavailable; substantive value remains true | true | UNAVAILABLE | OBSERVATION_SOURCE_MISSING | none | NON_EVALUABLE | no eligibility mapping | do not infer revoked |
| observation failure | coverage-non-evaluable | coverage | make complete inventory observation unavailable; substantive set remains {W1, W2} | true | UNAVAILABLE | OBSERVATION_SOURCE_MISSING | none | NON_EVALUABLE | no coverage mapping | do not infer empty set or absence |
| deliberate no revalidation | deliberate-no-revalidation | control | deliberately select no-revalidation arm | false | none | none | none | NOT_EVALUATED control, not a mapping result | no observation attempted | all baseline values unchanged |

This is a bounded canonical matrix of 13 rows, not combinatorial coverage. Later negative
tests may vary malformed, inaccessible, or incomplete observations without
promoting each failure reason to a new dependency or public state.

## Relationship to Policy Disposition

```text
mapping result
    !=
policy disposition
```

`PRESERVED`, `INVALIDATED`, and `NON_EVALUABLE` are experiment-local dependency
mapping semantics.

`PROCEED`, `HOLD`, `DENY`, and `ESCALATE` are policy dispositions. Increment 013
does not assign a universal disposition to `NON_EVALUABLE` and does not infer one
from production fail-closed intuitions.

Two treatments were considered:

1. invalidate and discard a non-evaluable cell/run from the experiment;
2. retain it as a separately reported experimental condition while excluding it
   from mapping and disposition-equivalence calculations.

This design selects option 2. Preserving the attempted observation and declared
failure reason protects failure lineage and allows the experiment to report how
often its own witness interface could not support a mapping. Exclusion from the
mapping denominator prevents those cases from being counted as either correct
invalidation or preservation. A later policy increment may study dispositions
for unavailable evidence; this increment does not.

## Preparation for Full Versus Scoped Reevaluation

A later experiment is expected to prepare for at least:

```text
Arm B: full reevaluation
    reevaluate every applicable selected dependency
    -> recompute the frozen policy

Arm C: scoped reevaluation
    predict invalidated subset
    -> reevaluate only predicted-invalidated dependencies
    -> reuse dependencies predicted preserved
    -> recompute the same frozen policy
```

Neither arm is implemented here.

The later comparison requires T0 state containing:

- experiment definition revision;
- dependency ID and kind;
- stable witness identity coordinates;
- dependency-specific T0 value;
- T0 observation status;
- frozen policy-composition ID and canonical fixture ID when more than one is
  available within the same experiment definition;
- the exact policy input derived from each dependency;
- scenario ID.

It requires T1 witness interfaces that return, separately:

- whether acquisition and assessment succeeded;
- a bounded failure reason when they did not;
- the dependency-specific current value when they did;
- the identity/version of the witness observed;
- enough fixed-control values to detect unintended multi-dependency mutation.

The later scoped arm must never reuse a dependency merely because its current
witness was unavailable. Reuse eligibility and witness availability are separate
questions to be specified by the later implementation increment.

## Evidence Requirements

The minimum diagnostic evidence for each later scenario/run is:

```text
run_id
scenario_id
experiment_definition_revision
canonical_fixture_id (only if the revision defines more than one fixture)
frozen_policy_composition_id (only if the revision defines more than one)
later_implementation_commit (once implementation exists)
dependency_under_test

T0:
    dependency_id
    dependency_kind
    witness_identity
    dependency_value
    observation_status

intervention:
    intervention_id
    intervention_kind
    declared target dependency
    deterministic parameters

T1 observation:
    observation_attempted
    observation_status when attempted
    observation_failure_reason
    witness_identity when available
    dependency_value when available

mapping:
    prospectively expected mapping_result
    later observed mapping_result

controls:
    fixed values for all non-target dependencies
    control verification result
```

`experiment_definition_revision` transitively identifies the frozen dependency
definitions, canonical baseline, scenario matrix, interventions, mapping
derivation rules, observation semantics, witness interpretation, and
evidence-field semantics. For the first experiment, it replaces independent
semantic versions for the dependency registry, matrix, witness schema, and
required-witness inventory. A repository commit is sufficient when it
unambiguously identifies that complete definition.

This is diagnostic Track A evidence. It is not a complete reviewer-evidence,
provenance, or Track B architecture. Field formats, serialization, storage, and
integrity mechanisms are deferred until a later implementation or Lab increment
requires them.

## Assumptions

- Controlled interventions are deterministic and declared before execution.
- Experiment witnesses are fixture-controlled.
- Witness identity is stable within a scenario unless binding is the controlled
  intervention.
- Source authenticity is not independently established in the first experiment.
- Observation-status semantics are local to this experiment design.
- Scenario IDs and expected mappings are experiment-definition metadata and must
  not be supplied to the mechanism under test as inputs that determine its
  result.
- Full commit-boundary reevaluation remains the correctness comparison arm.
- The same frozen policy composition is used for full and later scoped arms.
- Fixed controls can be observed well enough to detect unintended mutation.
- No external consequence occurs.

## Threat Model

This increment does not establish a security boundary. Relevant experimental
threats are:

- conflating known witness absence with observation failure;
- conflating intentional non-evaluation with failed evaluation;
- confounding freshness with witness removal;
- confounding target substitution with target ineligibility;
- confounding path ineligibility with target mismatch;
- hidden mutation of more than one dependency;
- post-hoc assignment of expected mapping results;
- implementation behavior influencing the prospective matrix;
- treating fixture evidence as authentic external evidence;
- reusing a dependency when its current witness was not assessable;
- silently dropping failed or non-evaluable runs.
- using wall-clock passage or test ordering to determine freshness;
- sharing mutable fixture state across scenarios without deterministic reset;
- allowing scenario labels or expected mappings to determine observed results.

## Failure Criteria

These criteria identify experimental-design or experimental-validity failures
that require correction or rejection. An unexpected mapping result obtained
without violating them is a preservable negative result, not a design failure.

Increment 013 is incomplete or unsuccessful if:

- the selected dependencies cannot be represented distinctly;
- one canonical intervention necessarily changes more than one selected
  dependency;
- witness availability cannot be separated from dependency value;
- expected invalidation mapping cannot be specified prospectively;
- a failed observation can be classified `PRESERVED` or `INVALIDATED`;
- required evidence cannot reconstruct whether observation was attempted and
  whether it succeeded;
- deliberate non-evaluation becomes indistinguishable from attempted-but-failed
  evaluation;
- `observation_attempted = false` is represented as an observation status;
- substantive coverage absence and observation-source absence use the same
  representation;
- freshness invalidation requires witness deletion;
- binding invalidation also makes the substituted target ineligible;
- eligibility invalidation changes the fixture-local `effect_id`;
- coverage invalidation is inferred from failed inventory observation;
- fixed controls cannot be verified for a retained scenario;
- freshness outcome depends on wall-clock passage, execution timing, or test
  order rather than the frozen fixture-controlled scalar;
- scenarios share mutable fixture state such that one run can affect another;
- observed results depend on scenario execution order;
- scenario IDs, expected-result labels, expected mappings, or equivalent oracle
  metadata influence the mapping logic under evaluation;
- full and obligation-scoped comparison arms evaluate different frozen policy
  compositions when disposition equivalence is measured;
- the design requires deferred Track A infrastructure;
- the design silently changes the four-dependency set;
- the design assigns a universal policy disposition to `NON_EVALUABLE`;
- the design imports UTDA terminology or treats collaboration input as
  validation;
- an experiment or test result is claimed before execution.

## Planned Tests

These are planned design-verification checks, not observed results:

- every dependency has a defined T0 and T1 witness;
- every canonical invalidating intervention has explicit fixed controls;
- every selected dependency has preserved, invalidated, and non-evaluable
  semantics;
- no unavailable witness is classified `PRESERVED` or `INVALIDATED`;
- deliberate no-revalidation remains distinguishable from
  attempted-but-unavailable;
- each selected dependency remains traceable to Increment 011 source grounding;
- no deferred dependency is introduced through the design;
- each invalidating matrix row changes exactly one selected dependency;
- every matrix row declares enough evidence to reconstruct the intended mapping;
- every non-evaluable row declares an observation attempt and bounded failure
  reason;
- the deliberate-no-revalidation control records
  `observation_attempted = false` and no observation status;
- one experiment definition revision identifies the mapping derivation rules and
  evidence semantics used by every row;
- the matrix and expected results can be frozen before implementation.

## Claim Classification

- The experiment-local observation representation, canonical fixture
  representation, scenario construction, matrix structure, derivation procedure,
  and evidence contract: **Design choices**.
- The `NON_EVALUABLE` representation and its separately reported treatment:
  **Design choice**.
- Published mechanism definitions already verified and recorded in Increment
  011: **External evidence**.
- The normalized dependency labels and controlled interventions: **Research
  design choices**, inherited from and refined within the boundary set by
  Increment 011.
- The prospectively predicted `PRESERVED` or `INVALIDATED` result for each
  controlled dependency-mapping scenario, and the prediction that the
  observation-failure controls yield `NON_EVALUABLE` under the frozen semantics:
  **Research hypotheses**.
- The current implementation lacks a heterogeneous witness representation:
  **Engineering observation**.
- Internal evaluation result for Increment 013: **None yet**.
- Research conclusion for Increment 013: **None yet**.

## Threats to Validity

- Fixture-controlled witness acquisition may not represent real distributed
  observability.
- Binary `AVAILABLE`/`UNAVAILABLE` may later prove too coarse.
- Failure-reason categories may not generalize beyond the bounded fixtures.
- Simple scalar and identifier witnesses may make invalidation artificially easy
  to isolate.
- The source-grounded dependencies remain an initial bounded set, not an
  ontology.
- The prospective matrix may encode researcher expectations into both the
  intervention and expected result.
- Later implementation may reveal hidden coupling that this design misses.
- Preserving non-evaluable runs does not make their failure reasons authentic or
  independently verified.
- A successful controlled mapping would not establish production enforcement or
  external validity.

## Reproducibility Requirements

A later engineer needs the following to reproduce the design and eventual
experiment:

- exact experiment definition revision, identified by repository commit or an
  equivalent immutable content identifier;
- exact controlled intervention definitions and parameters;
- canonical fixture ID if the experiment definition contains more than one;
- frozen policy-composition ID if the experiment definition contains more than
  one;
- stable scenario identifiers;
- recorded observation-status and failure-reason semantics;
- later implementation commit/hash;
- preserved successful, failed, and non-evaluable runs;
- explicit fixed-control snapshots for every scenario;
- the exact rule used to exclude `NON_EVALUABLE` cases from mapping and
  equivalence calculations.

These are requirements for later implementation and experiment artifacts. This
design increment does not yet create schemas, version hierarchies, hashes, run records, or retained
experimental artifacts.

## Observed Result

**Observed experimental result: Not yet evaluated.**

Increment 013 establishes a prospective experimental design only. No
runtime code or API behavior has changed, no heterogeneous witness has been
implemented, and no invalidation-mapping or disposition-preservation experiment
has been run.

## Completion / Closure

Increment 013 freezes the prospective first-experiment witness model, canonical
baseline, intervention/scenario matrix, mapping semantics, evidence requirements,
experimental-validity failure criteria, and reproducibility requirements.

This is a prospective experimental-design result only. No heterogeneous
four-dependency experiment has been executed, and no Runtime Validity
implementation for these four dependencies has been created. Increment 013
produces no internal evaluation result and no research conclusion. Its expected
scenario mappings remain prospective research hypotheses.

Runtime Validity remains bounded to its existing implementation. Completing this
design increment neither authorizes implementation by itself nor demonstrates
implementation correctness. Implementation may occur only through a subsequent
prospective increment.

## Artifacts

Prospective artifact:

```text
docs/increments/013-design-executable-witness-model-and-intervention-matrix.md
```

README reconciliation is limited to correcting stale Increment 011 status and
next-step statements.

## Commit

Not yet committed.

## Next Step

Any implementation must be proposed and justified by a subsequent increment.
Increment 013 authorizes no implementation work and makes no implementation or
experimental claim.
