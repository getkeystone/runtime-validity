# Increment 014: Implement Pure Witness Mapping Mechanism

Status: Complete

## Objective

Implement the minimum pure in-memory representations and deterministic
derivation rules needed to interpret observed witness state for the four frozen
Increment 013 dependencies, without executing the scenario matrix or changing
Runtime Validity's API or policy behavior.

This increment is mechanism implementation only:

```text
mechanism implementation
    !=
experiment execution
    !=
internal Track A experimental result
    !=
research conclusion
```

Passing unit tests in this increment would be engineering verification, not
experimental validation.

## Starting State

Observed before this prospective record was created:

- branch: `main`;
- HEAD: `face7038270b7d05318d0cb47aefef44b61c8ab4`;
- Increment 013: Complete;
- tracked working tree: clean;
- initially untracked working-tree entry: `uv.lock`;
- repository-local interpreter:
  `/data/repos/getkeystone/runtime-validity/.venv/bin/python`;
- Python: 3.12.3;
- test command:
  `/data/repos/getkeystone/runtime-validity/.venv/bin/python -m pytest`;
- observed test result: 23 tests passed, 0 failed;
- current implementation: the `/decide` path remains limited to the bounded
  `authority_valid` obligation and supports full or no revalidation;
- no heterogeneous four-dependency mechanism exists;
- no Track A invalidation-mapping experiment has run;
- `uv.lock` was pre-existing and untracked at this starting point; its later
  independent transition into repository history is recorded below.

The test result above is a starting-state engineering observation about the
existing implementation. It is not an Increment 014 implementation result or a
Track A experimental result.

## Repository Provenance Note

Increment 014 implementation began from commit
`face7038270b7d05318d0cb47aefef44b61c8ab4`.

Commit `9040bf44b8bed71c21552c4a0f9c12ead1db5fff`, titled `Increment 014
(WIP): observation, binding, freshness, eligibility mechanisms`, first committed
the accumulated Increment 014 work for the observation foundation, freshness,
effect/action binding, authorizing-path eligibility, their focused tests, and
the accumulated Increment 014 record. These mechanisms had been developed and
reviewed as bounded slices, but Git provenance does not preserve those slices as
separate commits: they first appear together in this single WIP commit. This
weakens the commit-level granularity of the engineering history and prevents a
later reviewer from reconstructing each slice boundary solely from Git commits.
The intermediate review chronology preserved in this record is not a substitute
for nonexistent slice-level commits. No history rewrite is being attempted to
fabricate finer-grained provenance.

The bundled commit does not convert focused engineering tests into experimental
results. It does not establish an internal Track A experimental result or a
research conclusion.

Commit `5253559d1e4cdc3122e4470943adc06831a3a05c`, titled `Track uv.lock for
reproducible test environment`, subsequently tracked `uv.lock` in a separate
lockfile-only commit. `pyproject.toml`, dependency declarations, Increment 014
mechanism code, and this record were unchanged in that commit. `uv.lock` was
therefore initially untracked during early Increment 014 work and later tracked
independently for the repository-environment purpose stated by the commit
subject. That transition was not part of the Increment 014 mechanism
implementation.

After HEAD `5253559d1e4cdc3122e4470943adc06831a3a05c`, required-witness coverage
was implemented as a working-tree delta in:

```text
src/runtime_validity/_experiment_mapping.py
tests/test_experiment_coverage.py
```

That delta then underwent the skeptical review recorded under Intermediate
Observed Coverage Engineering Result below and is committed as its own slice
together with this record update, separately from the earlier bundled WIP
commit.

This coarser-than-actual commit history is a research-engineering provenance and
reproducibility limitation. It is not by itself a scientific validity result.

## Frozen Inputs from Increment 013

Increment 013 supplies the prospective experiment-local definitions used by
this increment. Increment 014 does not reopen the four selected dependency
semantics:

1. witness/authorization freshness;
2. effect/action binding;
3. authorizing-path eligibility;
4. required-witness coverage, limited to the absence sub-case.

It also inherits the distinctions among:

- `observation_attempted`;
- `AVAILABLE` and `UNAVAILABLE` observation outcomes;
- `PRESERVED`, `INVALIDATED`, and `NON_EVALUABLE` experiment-local mapping
  outcomes;
- deliberate non-observation producing `NOT_EVALUATED`.

Increment 013's expected scenario mappings remain research hypotheses. Making
the derivation mechanism executable does not make those hypotheses observed or
confirmed.

## Scope

### In scope

Prospectively authorized implementation is limited to:

1. Pure experiment-local representations for the four frozen dependencies.

   **Freshness**

   - stable witness identifier;
   - fixture-controlled scalar age/currentness value;
   - fixed maximum-age threshold.

   **Effect/action binding**

   - prior `effect_id`;
   - current `effect_id`;
   - opaque, fixture-local identity semantics.

   **Authorizing-path eligibility**

   - stable `authorizing_path_id`;
   - Boolean liveness.

   **Required-witness coverage**

   - fixed required-ID set;
   - observed present-ID set.

2. The observation semantics frozen by Increment 013:

   - whether observation was attempted;
   - `AVAILABLE` and `UNAVAILABLE`;
   - bounded observation failure reasons;
   - a substantive observed value only when observation is `AVAILABLE`.

3. Pure deterministic derivation behavior:

   - an available value satisfying its dependency rule derives `PRESERVED`;
   - an available value violating its dependency rule derives `INVALIDATED`;
   - an attempted observation that is unavailable or unassessable derives
     `NON_EVALUABLE`;
   - deliberately unattempted observation derives `NOT_EVALUATED`.

4. Validation of structurally impossible or internally inconsistent observation
   combinations.
5. Focused unit tests constructed directly from synthetic witness values.
6. Regression execution of all existing repository tests.
7. An internal experiment-specific module boundary isolated from the current
   `/decide` API execution path.

The internal module boundary is a local engineering choice for this bounded
mechanism. It is not a Governed Execution architectural requirement.

## Explicitly Out of Scope

This increment does not authorize:

- canonical baseline fixture implementation;
- scenario IDs as mechanism inputs;
- expected mapping labels as mechanism inputs;
- implementation of the 13-row scenario matrix;
- a scenario runner;
- an experiment harness;
- experiment execution;
- run IDs;
- retained experimental run records;
- a serialization format;
- persistence;
- artifact storage;
- experimental evidence packages;
- an internal Track A experimental result;
- a research conclusion;
- changes to `/decide`;
- public API or schema changes;
- runtime witness acquisition;
- external witness integration;
- authentic external revocation;
- production authentication or authorization;
- policy disposition;
- `PROCEED`, `HOLD`, `DENY`, or `ESCALATE` behavior for these mappings;
- full commit-boundary reevaluation implementation;
- obligation-scoped reevaluation implementation;
- full-versus-scoped disposition comparison;
- work, latency, or cost evaluation;
- Governed Execution Lab integration;
- policy-state currency;
- causal/ordering priority;
- the required-witness type/binding sub-case;
- authority-intent lifecycle;
- target re-admission lifecycle;
- distributed revocation reachability;
- retry or delegation propagation;
- cross-system witness independence;
- human-oversight evaluation;
- a generalized epistemic ontology;
- third-party dependencies unless separately justified prospectively before
  implementation.

## Assumptions

- Increment 013's definitions are frozen inputs to this increment.
- The four selected dependency semantics are not being reopened.
- Dependency observations can be represented deterministically in memory for
  this bounded engineering increment.
- Direct unit-test witness values are synthetic engineering fixtures, not
  authentic external witnesses.
- Existing API behavior must remain unchanged.
- No mechanism may consume a scenario ID or prospectively expected outcome.
- Freshness requires no wall-clock behavior; it uses fixture-controlled scalar
  values.
- No persistence or distributed behavior is required.
- The pure mechanism can be tested independently of FastAPI request and response
  objects.

## Planned Implementation

The later bounded implementation should provide:

- pure in-memory value and observation representations;
- deterministic dependency-specific derivation functions;
- validation of structurally impossible observation combinations;
- no scenario or matrix lookup;
- no API integration;
- no persistence.

This record freezes behavior, not speculative software architecture. It does not
choose class names, file names, inheritance hierarchies, framework abstractions,
database schemas, or public APIs. The smallest clear implementation structure
should be selected during implementation and recorded as an engineering design
choice.

## Threat Model and Engineering Failure Modes

This increment does not establish a production security boundary. Relevant
bounded engineering threats are:

- expected-result or scenario metadata leaking into mapping logic;
- freshness becoming dependent on wall-clock passage or execution timing;
- unavailable observation being interpreted as known substantive invalidity;
- `NOT_EVALUATED` being conflated with `NON_EVALUABLE`;
- unavailable coverage inventory being represented as an empty present set;
- effect identity and authorizing-path eligibility becoming accidentally
  coupled;
- mutation or shared state making identical inputs nondeterministic;
- the new mechanism being imported by, or changing, the existing API execution
  path;
- representations expanding into deferred dependency semantics;
- tests encoding expected matrix answers through metadata rather than exercising
  derivation from witness values.

## Planned Engineering Tests

This section distinguishes observed checks for the implemented slices from the
checks that remain planned. None of these engineering tests
constitutes Track A experimental validation.

### Observation invariants — observed

- deliberate non-observation is valid only without observation status, failure
  reason, or observed value;
- attempted observation requires an observation status;
- `AVAILABLE` requires an observed value and forbids a failure reason;
- `UNAVAILABLE` requires a bounded failure reason and forbids an observed value;
- non-Boolean `observation_attempted` values are rejected;
- raw, non-enum observation-status values are rejected;
- raw, unbounded failure-reason values are rejected.

These checks verify the observation prerequisites. Mapping-result derivation is
now implemented for freshness, binding, eligibility, and required-witness
coverage, as recorded below.

### Freshness — observed

- same witness with age less than or equal to threshold derives `PRESERVED`;
- same witness with age greater than threshold derives `INVALIDATED`;
- deliberate non-observation derives `NOT_EVALUATED`;
- attempted unavailable observation derives `NON_EVALUABLE` independently of
  its bounded failure reason;
- changed witness identity is rejected rather than classified as freshness
  invalidation;
- derivation has no wall-clock dependency;
- identical inputs produce identical output;
- available observations with the wrong payload type are rejected;
- Boolean and floating-point age or threshold values are rejected.

### Binding — observed

- equal prior and current `effect_id` values derive `PRESERVED`;
- different `effect_id` values derive `INVALIDATED`;
- changed identity is classified rather than rejected;
- deliberate non-observation derives `NOT_EVALUATED`;
- attempted unavailable observation derives `NON_EVALUABLE` independently of
  its bounded failure reason;
- effect comparison embeds no authorizing-path eligibility decision;
- available observations with the wrong payload type are rejected;
- non-string current or expected effect identifiers are rejected.

### Eligibility — observed

- deliberate non-observation derives `NOT_EVALUATED`;
- attempted unavailable observation derives `NON_EVALUABLE` independently of
  its bounded failure reason;
- same path ID with liveness `true` derives `PRESERVED`;
- same path ID with liveness `false` derives `INVALIDATED`;
- changed path identity is rejected rather than classified as ordinary
  eligibility invalidation;
- available observations with the wrong payload type are rejected;
- integer and string stand-ins for Boolean liveness are rejected;
- identical inputs produce identical results;
- the derivation interface accepts no scenario or expected-result input;
- the representation requires no unrelated authority, policy, target, or
  effect state;
- non-string observed or expected path identifiers are rejected.

### Coverage — observed

- deliberate non-observation derives `NOT_EVALUATED`;
- attempted unavailable inventory observation derives `NON_EVALUABLE`
  independently of its bounded failure reason;
- required set being a subset of the present set derives `PRESERVED`;
- known absence of either required member derives `INVALIDATED`;
- an available empty present set is known absence and derives `INVALIDATED`;
- unavailable inventory is not converted to an empty present set and remains
  distinct from an available empty inventory;
- present witnesses outside the required set do not invalidate coverage;
- an empty required set uses subset semantics and derives `PRESERVED` when the
  inventory is available (see the bounded design choice recorded below);
- available observations with the wrong payload type are rejected;
- mutable sets and non-string identifiers are rejected for both the required
  and present inventories;
- identical inputs produce identical results;
- the derivation interface accepts only the required-ID set and the
  observation;
- the representation contains only the present-ID set.

### Isolation — observed and planned

Observed for all four implemented dependency slices:

- the private observation and mapping modules are not imported by the current
  API execution path;
- the observation and mapping modules have no FastAPI or persistence
  dependency;
- the implemented derivation interfaces, including `derive_coverage`, do not
  accept scenario IDs, expected mapping labels, policy dispositions, or current
  Runtime Validity API request objects.

### Regression — intermediate observed result

- the repository test suite passed with 38 tests and 0 failures after the first
  implementation slice;
- the existing `/decide` tests continued to pass without the API importing the
  private observation module;
- the repository test suite passed with 79 tests and 0 failures after the
  eligibility implementation and skeptical review;
- the repository test suite passed with 97 tests and 0 failures after the
  coverage implementation and skeptical review;
- final cross-mechanism regression and scope verification remain required after
  the remaining Increment 014 work.

## Intermediate Observed Engineering Result

The first implementation slice created:

```text
src/runtime_validity/_experiment_observation.py
tests/test_experiment_observation.py
```

The implementation is a private experiment-specific module containing a generic
in-memory `Observation` representation implemented as a frozen, slotted
dataclass. `ObservationStatus` contains only `AVAILABLE` and `UNAVAILABLE`.
`ObservationFailureReason` contains the bounded vocabulary inherited from
Increment 013. Constructor-time `ValueError` validation rejects structurally
inconsistent combinations. The module has no FastAPI or persistence dependency
and is not imported by the current `/decide` path.

The implemented observation behavior is:

```text
observation_attempted = false
    -> no observation_status
    -> no observation_failure_reason
    -> no observed_value

observation_attempted = true + AVAILABLE
    -> observed_value required
    -> observation_failure_reason forbidden

observation_attempted = true + UNAVAILABLE
    -> bounded observation_failure_reason required
    -> observed_value forbidden
```

Attempted observation without a status, non-Boolean
`observation_attempted`, raw non-enum status values, and raw unbounded failure
reasons are also rejected.

Observation semantics implemented are distinct from mapping-result derivation.
The observation foundation established the prerequisites without deriving a
dependency result. The later freshness slice recorded below now derives mapping
results for freshness only.

Fifteen focused tests construct synthetic observation values directly. Together
with the existing tests, the repository-local test command completed with 38
tests passed and 0 failed. This is an engineering observation about the bounded
mechanism, not execution of the frozen 13-row scenario matrix or an internal
Track A experimental result.

The bounded intermediate engineering observation is:

> The frozen observation states can be represented in memory and the specified
> impossible observation combinations are mechanically rejected under the
> focused engineering tests.

### Structural-absence limitation

Observed-value absence is currently represented by `None`. In an abstract
generic representation this would be ambiguous if `None` were intended as a
substantive payload. None of the four frozen Increment 014 dependency payloads
uses `None` as a substantive value, so a private sentinel is not required for
this bounded mechanism. This choice must be revisited if a future dependency
legitimately needs `None` as an observed value. This is a bounded engineering and
design limitation, not an observed failure.

### Mutation limitation

Frozen dataclass fields cannot be reassigned after construction. The generic
observation envelope does not guarantee deep immutability of a contained payload.
When required-witness coverage is implemented, its set payload should use or be
normalized to an immutable representation if mutation would otherwise undermine
deterministic mapping. No coverage representation is implemented in this slice.

### Development history

The first skeptical review found two missing direct tests: rejection of a
non-Boolean `observation_attempted` value and rejection of a raw non-enum
`observation_status`. These were test-coverage gaps, not implementation defects.
Two focused tests corrected the gaps, and no source implementation change was
required.

### Remaining Increment 014 work

Increment 014 remains incomplete. Planned work still includes:

- required-witness coverage representation and derivation;
- its focused engineering tests;
- final cross-mechanism regression and scope review;
- the Increment 014 completion review.

Nothing performed so far constitutes scenario-matrix execution, experiment
execution, an internal Track A experimental result, a research conclusion, API
integration, runtime witness acquisition, persistence, policy disposition, or
full/scoped reevaluation.

## Intermediate Observed Freshness Engineering Result

The freshness slice created:

```text
src/runtime_validity/_experiment_mapping.py
tests/test_experiment_freshness.py
```

The private experiment-local `MappingResult` enum contains exactly
`PRESERVED`, `INVALIDATED`, `NON_EVALUABLE`, and `NOT_EVALUATED`. These are
experiment mechanism results, not policy dispositions.

The private frozen, slotted `FreshnessValue` representation contains the stable
`witness_id` and fixture-controlled integer/logical `age`. The deterministic
`derive_freshness` function consumes an expected witness identity, a fixed
maximum-age threshold, and the existing `Observation` envelope. It implements:

```text
deliberate non-observation
    -> NOT_EVALUATED

attempted + UNAVAILABLE
    -> NON_EVALUABLE

AVAILABLE + matching witness identity + age <= maximum_age
    -> PRESERVED

AVAILABLE + matching witness identity + age > maximum_age
    -> INVALIDATED
```

Witness identity mismatch is rejected with `ValueError` and is not classified
as freshness `INVALIDATED`. Unavailable evidence is not interpreted as stale
evidence, and its bounded failure reason does not change the `NON_EVALUABLE`
result. Deliberate non-observation and unavailable paths do not inspect a
freshness payload. An available observation must carry a `FreshnessValue`; a
wrong payload type is rejected deterministically with `ValueError`.

Freshness age and `maximum_age` use exact Python integer values for this bounded
experiment mechanism. Boolean values are rejected even though `bool` subclasses
`int`, and floating-point ages and thresholds are rejected. Negative integer
values remain accepted because Increment 013 and Increment 014 do not prohibit
them. Witness identity uses direct equality. These are bounded experiment
representation choices, not universal freshness semantics.

The derivation uses only its explicit inputs. It has no wall-clock progression,
timestamp, expiry lifecycle, global mutable state, scenario lookup, or API-state
dependency. Its interface accepts no scenario ID, scenario name, expected
mapping, matrix row, policy disposition, or API request object. The current
`/decide` path does not import the experiment mapping module.

Sixteen focused freshness engineering tests cover the exact mapping-result
member set, deliberate non-observation, unavailable observation, below-threshold
preservation, threshold-equality preservation, above-threshold invalidation,
witness-identity mismatch, repeated-input determinism, failure-reason
independence, interface isolation, absence of wall-clock imports, wrong-payload
rejection, and Boolean and floating-point rejection for both age and threshold.
Together with the existing tests, the repository-local test command completed
with 54 tests passed and 0 failed.

The bounded intermediate engineering observation is:

> The frozen freshness rule can be represented and deterministically derived
> from synthetic observation values under focused engineering tests while
> preserving witness-identity control, threshold equality, and the distinction
> between unavailable evidence and substantive invalidation.

This is an engineering observation only. It is not a Track A experimental
result, evidence that the prospective freshness intervention is empirically
correct, evidence of authentic witness freshness, evidence of production
authorization correctness, or a research conclusion.

### Freshness development history

The initial freshness implementation passed its first engineering verification.
Skeptical review then found missing direct tests for an available observation
with a non-`FreshnessValue` payload, Boolean and floating-point age rejection,
and Boolean and floating-point `maximum_age` rejection. These were test-coverage
gaps, not implementation defects. Five focused tests corrected the gaps, and no
source implementation change was required.

## Intermediate Observed Binding Engineering Result

The effect/action binding slice added:

```text
tests/test_experiment_binding.py
```

to the existing private experiment mapping module. The private frozen, slotted
`BindingValue` representation contains only one fixture-local `effect_id` and
reuses the existing private `MappingResult` enum. The pure `derive_binding`
function consumes an expected effect identity and the existing `Observation`
envelope. It implements:

```text
deliberate non-observation
    -> NOT_EVALUATED

attempted + UNAVAILABLE
    -> NON_EVALUABLE

AVAILABLE + current effect_id == expected effect_id
    -> PRESERVED

AVAILABLE + current effect_id != expected effect_id
    -> INVALIDATED
```

Changed effect identity is the selected binding invalidation and is not rejected
merely because identity changed. Unavailable identity evidence is not interpreted
as binding invalidation, and its bounded failure reason does not alter the
`NON_EVALUABLE` result. An available observation must carry a `BindingValue`; a
wrong payload type is rejected deterministically with `ValueError`.

Increment 013 freezes opaque fixture-local string-valued effect identifiers.
Using exact built-in Python `str` validation is a bounded implementation design
choice. Non-string values and string subclasses are rejected. Empty strings and
whitespace-only strings are accepted. No non-empty, UUID, URI, normalization,
global-uniqueness, target-lifecycle, or external-identity semantics are imposed.
This representation is not a universal consequence-identity model.

`expected_effect_id` is validated before observation availability is interpreted.
A malformed expected configuration therefore raises `ValueError` even when the
observation is deliberately unattempted or unavailable. Increment 013 and
Increment 014 do not specify invalid-configuration precedence, so this
deterministic ordering is a bounded implementation choice for valid mechanism
configuration, not a program-wide rule or research conclusion.

The derivation depends only on explicit inputs and accepts no scenario ID,
scenario name, matrix row, expected mapping, expected-result label, policy
disposition, or API request object. It does not independently evaluate target
lifecycle, target or substitute eligibility, authorizing-path liveness, witness
freshness, policy state, authority validity, artifact identity, or external
resource state. The bounded mechanism answers only whether the observed
fixture-local consequential effect is the same effect previously bound. The
current `/decide` path does not import the experiment mapping module.

Eleven focused binding engineering tests cover deliberate non-observation,
unavailable observation, same-ID preservation, different-ID invalidation without
rejection, wrong-payload rejection, repeated-input determinism, failure-reason
independence, interface isolation, absence of target/path/policy requirements,
and rejection of non-string current and expected effect identifiers. Together
with the existing tests, the repository-local test command completed with 65
tests passed and 0 failed.

The bounded intermediate engineering observation is:

> The frozen effect/action binding rule can be represented and deterministically
> derived from synthetic observation values under focused engineering tests,
> with changed fixture-local effect identity classified as binding invalidation
> and unavailable identity evidence kept distinct from substantive invalidation.

This is an engineering observation only. It is not a Track A experimental
result, evidence that `effect_id` correctly captures real-world consequence
identity, evidence of authentic target binding, evidence of substitute
eligibility, evidence of authorization correctness, or a research conclusion.

### Binding review history

The binding slice underwent a skeptical read-only review. Frozen-design
conformance, binding representation, observation and configuration behavior,
derivation, oracle and API isolation, and test coverage were all assessed as
clean. No bounded correction to source or tests was required. This differs from
the earlier observation and freshness slices, whose reviews found test-coverage
gaps that were corrected.

## Intermediate Observed Eligibility Engineering Result

The eligibility slice added:

```text
EligibilityValue
derive_eligibility
tests/test_experiment_eligibility.py
```

The private frozen, slotted `EligibilityValue` representation contains only a
fixture-local `authorizing_path_id` and `authorizing_path_live`. Increment 013
freezes stable fixture-local path identity but does not freeze a concrete Python
identifier type. Exact built-in Python `str` is therefore a bounded design
choice. Liveness requires exact Python `bool`; integer stand-ins such as `0` and
`1`, string truthiness stand-ins, and other non-Boolean values are rejected.
Empty and whitespace-only strings remain accepted because the frozen design
places no content constraints on path identifiers. String subclasses are
rejected by the exact-type validation. These choices are experiment-local and
are not universal authorizing-path identity semantics.

The deterministic `derive_eligibility` function consumes only the expected
authorizing path identity and the existing observation envelope. It reuses the
existing private `MappingResult` enum and implements:

```text
deliberate non-observation
    -> NOT_EVALUATED

attempted + UNAVAILABLE
    -> NON_EVALUABLE

AVAILABLE + matching path identity + authorizing_path_live = true
    -> PRESERVED

AVAILABLE + matching path identity + authorizing_path_live = false
    -> INVALIDATED

AVAILABLE + different path identity
    -> ValueError
```

Path identity remains a fixed control and liveness is the manipulated dependency
value. Changed path identity is rejected as outside the frozen liveness
intervention rather than classified as ordinary eligibility `INVALIDATED`.
Unavailable evidence is not interpreted as `authorizing_path_live = false`, and
its bounded failure reason does not alter the `NON_EVALUABLE` result. Available
observations with the wrong payload type and invalid identifier or liveness
types are rejected deterministically with `ValueError`.

The expected `authorizing_path_id` is validated before observation-state
handling. A malformed expected path identity therefore raises `ValueError` even
for deliberate non-observation or an `UNAVAILABLE` observation. Increment 013
and this record do not specify invalid-configuration precedence, so this
deterministic ordering is a bounded design choice rather than a research
conclusion.

The derivation depends only on explicit inputs. It accepts no scenario ID,
scenario name, matrix row, expected mapping, expected-result label, policy
disposition, or API request object. It does not independently evaluate authority
validity, revocation semantics, policy validity, target state, effect identity,
freshness, substitute-path eligibility, alternate-path discovery, path topology,
delegation reconstruction, external reachability, or revocation cause. The
bounded mechanism answers only: "Is this same frozen authorizing path currently
live?" The current `/decide` path does not import the experiment mapping module.

Fourteen focused eligibility engineering tests cover deliberate
non-observation, unavailable observation, same-path preservation and
invalidation, changed-path rejection, wrong-payload rejection, integer and
string liveness rejection, repeated-input determinism, failure-reason
independence, interface isolation, representation isolation, and rejection of
non-string observed and expected path identifiers. Together with the existing
tests, the repository-local test command completed with 79 tests passed and 0
failed.

The bounded intermediate engineering observation is:

> The frozen authorizing-path eligibility rule can be represented and
> deterministically derived from synthetic observation values under focused
> engineering tests, with Boolean liveness changing the mapping while path
> identity remains a fixed control and unavailable evidence remains distinct
> from substantive invalidation.

This is an engineering observation only. It is not a Track A experimental
result, evidence of authentic external revocation, evidence that a production
authorization path is actually live or revoked, evidence that alternate paths
do or do not exist, evidence of policy correctness, or a research conclusion.

### Eligibility review history

The eligibility slice underwent a skeptical read-only review. Frozen-design
conformance, eligibility representation, observation and configuration
behavior, derivation, oracle and API isolation, and test coverage were all
assessed as clean. No bounded correction to source or tests was required.

### Remaining work after eligibility

At the eligibility checkpoint, required-witness coverage, its focused tests,
final cross-mechanism regression and scope review, and the Increment 014
completion review remained outstanding. Coverage is recorded below.

Nothing completed so far constitutes canonical baseline execution, 13-row
matrix execution, experiment execution, an internal Track A experimental
result, a research conclusion, API integration, runtime witness acquisition,
persistence, policy disposition, or full/scoped reevaluation.

## Intermediate Observed Coverage Engineering Result

The coverage slice added:

```text
CoverageValue
derive_coverage
tests/test_experiment_coverage.py
```

The private frozen, slotted `CoverageValue` representation contains only the
observed `present_witness_ids`, an exact built-in `frozenset` of exact built-in
`str` identifiers. The fixed required-ID set is a keyword-only configuration
input to the pure `derive_coverage` function, not part of the observed value,
matching Increment 013's separation of the fixed required-set definition from
the observed present-ID set. Mutable sets, `frozenset` subclasses, and
non-string identifiers are rejected with `ValueError`. The required-ID set is
validated before observation state is interpreted, consistent with the
configuration-first ordering chosen for binding and eligibility.

Derivation follows the frozen Increment 013 absence sub-case:

```text
not attempted                                -> NOT_EVALUATED
attempted, UNAVAILABLE (any bounded reason)  -> NON_EVALUABLE
AVAILABLE, required is a subset of present   -> PRESERVED
AVAILABLE, some required ID absent           -> INVALIDATED
```

With a non-empty required set, an available empty present set is a
successful, complete observation that establishes known absence of every
required member and therefore derives `INVALIDATED`. An unavailable inventory carries no present-ID set and derives
`NON_EVALUABLE`; it is never represented as, or converted to, an empty present
set. This preserves Increment 013's rule that inability to read the inventory
must never be used to infer absence. Present IDs outside the required set do not
affect the result, because the frozen dependency concerns required-member
absence only.

### Empty required-set semantics: bounded design choice

Increment 013 freezes the fixture-local required-ID set as `{W1, W2}` and does
not specify behavior for an empty required set. Increment 014's planned coverage
rule states only that a required set that is a subset of the present set derives
`PRESERVED`. Applied literally, an empty required set is a subset of every
available present set, so `derive_coverage` returns `PRESERVED` for it, and
`test_empty_required_inventory_uses_subset_semantics` pins that behavior.

This is retained as a bounded implementation design choice, not a frozen
specification:

- it follows the literal Increment 014 subset rule and introduces no new result
  category or rejection rule absent from the frozen design;
- it is unreachable in the frozen 13-row intervention matrix, whose required
  set is always `{W1, W2}`;
- it is consistent with the precedent recorded for binding and eligibility,
  where properties the frozen design leaves unconstrained (for example empty
  identifier strings) are accepted and documented rather than newly restricted.

The choice has a known risk: an empty required set is vacuously covered, so a
misconfigured or accidentally empty required set would derive `PRESERVED`
rather than surface as a configuration defect. Any later use of this mechanism
outside the frozen fixtures, or any experiment that varies the required set,
must decide prospectively whether an empty required set is valid configuration,
a configuration error, or `NON_EVALUABLE`. This record does not make that
decision.

Increment 013 also names an unobtainable required-set definition as a
`NON_EVALUABLE` condition. In this pure mechanism the required set is a fixed
configuration input supplied by the fixture, so there is no runtime acquisition
of the required-set definition to fail; a malformed definition is rejected with
`ValueError` as a configuration error. Representing an unobtainable required-set
definition as an observation is outside this mechanism slice.

Eighteen focused coverage engineering tests cover deliberate non-observation,
unavailable observation, preservation with both required witnesses present,
invalidation with either required witness absent, invalidation by an available
empty inventory, non-invalidation by extra present witnesses, the distinction
between unavailable and available-empty inventories, wrong-payload rejection,
repeated-input determinism, failure-reason independence, interface isolation,
representation isolation, mutable-inventory and non-string-identifier
rejection for both inventories, and empty-required-set subset semantics.
Together with the existing tests, the repository-local test command completed
with 97 tests passed and 0 failed.

The bounded intermediate engineering observation is:

> The frozen required-witness coverage absence rule can be represented and
> deterministically derived from synthetic observation values under focused
> engineering tests, with known absence of a required member invalidating
> coverage and unavailable inventory evidence remaining distinct from both
> absence and an available empty inventory.

This is an engineering observation only. It is not a Track A experimental
result, evidence that any real witness inventory is complete or authentic,
evidence about witness type or binding sufficiency, which remain deferred, or a
research conclusion.

### Coverage review history

The coverage slice underwent a skeptical read-only review against Increments 013
and 014. Frozen-design conformance, coverage representation, observation and
configuration behavior, derivation, the unavailable versus available-empty
distinction, oracle and API isolation, and test coverage were assessed as
consistent with the frozen design. No source or test correction was required.
The review identified two items recorded rather than changed: the
empty-required-set semantics documented above, and that configuration-first
validation ordering with an unattempted or unavailable observation is exercised
by code but, as in the binding and eligibility slices, not pinned by a focused
test. The latter is carried into the final cross-mechanism review.

### Remaining work after coverage

Increment 014 remains incomplete. The final cross-mechanism regression and
scope review and the Increment 014 completion review remain outstanding.

Nothing completed so far constitutes canonical baseline execution, 13-row
matrix execution, experiment execution, an internal Track A experimental
result, a research conclusion, API integration, runtime witness acquisition,
persistence, policy disposition, or full/scoped reevaluation.

## Failure Criteria

Increment 014 fails or requires correction if:

- implementation requires scenario IDs or expected-result labels to derive
  mappings;
- mapping logic uses prospective matrix answers as lookup data;
- identical valid inputs produce nondeterministic results;
- freshness requires real wall-clock progression;
- unavailable evidence can be mistaken for substantive invalidity;
- `NOT_EVALUATED` and `NON_EVALUABLE` cannot be mechanically distinguished;
- coverage absence and inventory unavailability cannot be mechanically
  distinguished;
- effect binding and path eligibility cannot be represented independently;
- implementation changes the existing `/decide` API, schema, or behavior;
- implementation requires persistence, external witness infrastructure, or a
  deferred dependency to express the frozen semantics;
- existing regression tests fail because of the new mechanism;
- a third-party dependency becomes necessary without prospective justification;
- scenario execution, experimental artifacts, or an experimental result are
  introduced as part of the mechanism implementation.

These criteria distinguish engineering failure from a scientifically
interesting future negative result. Inability to implement the four semantics
independently without hidden coupling is an engineering observation that must be
preserved and may force redesign. It must not be patched over merely to make
prospectively expected tests pass.

## Claim Classification

- Inherited Increment 013 observation, freshness, effect/action binding, and
  authorizing-path eligibility semantics used by the implemented slices:
  **Definitions**.
- The private experiment-specific observation module, generic frozen/slotted
  `Observation` representation, bounded enums, constructor-time `ValueError`
  validation, and use of `None` as structural absence for the current bounded
  payload universe: **Design choices**.
- The private `MappingResult` enum, private frozen/slotted `FreshnessValue`,
  exact-integer age and threshold representation, deterministic pure freshness
  derivation, and `ValueError` treatment of freshness-specific invalid inputs:
  **Design choices**.
- The private frozen/slotted `BindingValue`, exact built-in Python string
  validation, direct equality comparison, deterministic `ValueError` treatment
  of invalid binding payload or configuration types, and validation of expected
  identity before observation availability: **Design choices**.
- The private frozen/slotted `EligibilityValue`, exact built-in Python string
  representation for path identity, exact Boolean liveness representation,
  keyword-only pure derivation, deterministic `ValueError` treatment, and
  validation of expected path identity before observation-state handling:
  **Design choices**.
- The observation representation exists, the specified impossible states are
  mechanically rejected under focused tests, the current API path remains
  isolated, two direct test-coverage gaps were identified and corrected without
  source changes: **Engineering observations**.
- The freshness mechanism exists, witness-identity drift is rejected, threshold
  equality is preserved, unavailable observation derives `NON_EVALUABLE` rather
  than `INVALIDATED`, five direct validation test gaps were identified and
  corrected without source changes: **Engineering observations**.
- The binding mechanism exists, same identity preserves, changed identity
  invalidates rather than being rejected, unavailable identity evidence remains
  `NON_EVALUABLE`, fixed-control isolation is preserved, skeptical review
  required no source or test correction: **Engineering observations**.
- The eligibility mechanism exists, stable path identity plus true liveness
  preserves, stable path identity plus false liveness invalidates, changed path
  identity is rejected, unavailable evidence remains `NON_EVALUABLE`,
  fixed-control isolation is preserved, skeptical review required no source or
  test correction, and the repository suite passed with 79 tests and 0 failures:
  **Engineering observations**.
- The private frozen/slotted `CoverageValue` containing only the present-ID
  set, exact `frozenset` and exact `str` validation, the required-ID set as a
  keyword-only configuration input validated before observation-state
  handling, subset-based derivation, and subset semantics for an empty required
  set outside the frozen matrix: **Design choices**.
- The coverage mechanism exists, full presence preserves, known absence of
  either required member invalidates, an available empty inventory invalidates,
  unavailable inventory remains `NON_EVALUABLE` and distinct from an available
  empty inventory, extra present witnesses do not invalidate, skeptical review
  required no source or test correction, and the repository suite passed with
  97 tests and 0 failures: **Engineering observations**.
- Git history shows that the previously reviewed observation, freshness,
  binding, and eligibility slices first entered repository history together in
  WIP commit `9040bf4`, followed by independent tracking of `uv.lock` in commit
  `5253559`: **Engineering observations**.
- Commit-level provenance is coarser than the actual slice-by-slice engineering
  and review process, and the individual slice boundaries cannot be reconstructed
  solely from Git commits: **Research-engineering provenance and reproducibility
  limitation**.
- The four frozen Increment 013 dependency semantics can be represented as
  isolated deterministic in-memory mechanisms over synthetic observation
  values, with deliberate non-evaluation, observation failure, preservation,
  and substantive invalidation mechanically distinguished under focused
  engineering tests: **Engineering observation**.
- Internal evaluation result: **None**.
- Increment 013's expected mappings: **Research hypotheses**, unchanged by this
  prospective record.
- Research conclusion: **None**.
- External evidence: **None added by Increment 014**.

The verified branch, commit, interpreter, test result, and working-tree state in
Starting State are engineering observations about the repository before
Increment 014 implementation. They are not observations of the new mechanism.

## Reproducibility Requirements

Later implementation evidence should preserve at minimum:

- repository commit;
- Python interpreter and version;
- dependency environment;
- exact test command;
- complete test result;
- implementation files changed;
- test files changed;
- confirmation that no scenario label or expected-result oracle is an input to
  the mechanism;
- confirmation that the current API execution path remains unchanged;
- failures and corrections encountered during implementation.

The intermediate evidence is local engineering verification. No independent
reproduction claim may be made without independent reproduction.

## Completion Criteria

Increment 014 may be marked Complete only when:

- the bounded mechanism has been implemented;
- focused engineering tests exist and pass;
- all existing regression tests pass;
- `git diff --check` passes;
- existing API behavior remains unchanged;
- no scenario harness or experiment execution was introduced;
- no unexpected dependency or scope expansion occurred;
- observed engineering results and failures are recorded honestly;
- claim classifications are updated from planned to observed where applicable.

## Observed Result

Five intermediate Increment 014 engineering results have been observed. First,
the frozen observation states can be represented in memory and the specified
impossible observation combinations are mechanically rejected. Second, the
frozen freshness rule can be deterministically derived while preserving witness
identity, threshold equality, and the distinction between unavailable evidence
and substantive invalidation. Third, the frozen effect/action binding rule can
be deterministically derived with changed fixture-local effect identity
classified as binding invalidation and unavailable identity evidence kept
distinct from substantive invalidation. Fourth, the frozen authorizing-path
eligibility rule can be deterministically derived while path identity remains a
fixed control, Boolean liveness supplies the dependency value, and unavailable
evidence remains distinct from substantive invalidation. Fifth, the frozen
required-witness coverage absence rule can be deterministically derived with
known absence of a required member classified as invalidation and unavailable
inventory evidence kept distinct from both absence and an available empty
inventory. The repository test suite passed with 97 tests and 0 failures, and the
current `/decide` path remains isolated from the private experiment modules.

All four frozen dependency mechanisms now exist as private pure derivations.
The final cross-mechanism regression, scope, and completion-readiness reviews
found the bounded engineering completion criteria satisfied after the README
claim-classification correction recorded below. Increment 014 is complete. No
canonical baseline or scenario matrix has been executed, no Track A experiment
has run, no internal evaluation result exists, and no research conclusion is
claimed. Nothing implemented performs API integration, runtime witness
acquisition, persistence, policy disposition, or full/scoped reevaluation.

## Completion Review and Closure

Increment 014 completed the bounded mechanism objective with the following
private experiment-local implementation:

1. The observation foundation distinguishes deliberate non-observation,
   `AVAILABLE`, and `UNAVAILABLE`; admits only bounded observation failure
   reasons; and rejects structurally impossible observation states.
2. The shared mapping result contains exactly `PRESERVED`, `INVALIDATED`,
   `NON_EVALUABLE`, and `NOT_EVALUATED`.
3. Freshness retains a stable witness identity, uses deterministic
   integer/logical age and a fixed maximum-age threshold, preserves when age is
   less than or equal to the threshold, invalidates when age exceeds the
   threshold, and rejects witness-identity drift as outside the frozen
   intervention.
4. Effect/action binding uses fixture-local effect identity, preserving equal
   identity and invalidating changed identity.
5. Authorizing-path eligibility retains stable path identity and exact Boolean
   liveness, preserving when liveness is true, invalidating when it is false,
   and rejecting path-identity drift as outside the frozen intervention.
6. Required-witness coverage implements only the frozen absence sub-case. It
   uses a fixed required-ID inventory and an immutable present-ID inventory,
   preserves when the required IDs are a subset of the present IDs, invalidates
   known required-member absence, and derives `NON_EVALUABLE` for unavailable
   inventory evidence without converting it into an available empty inventory.

### Completion evidence

- the repository-local suite passed with 97 tests and 0 failures;
- the focused mechanism tests remain engineering tests over synthetic
  observations and do not implement the Increment 013 scenario matrix;
- the existing API regression tests remain passing;
- `git diff --check` passed;
- the current `/decide` path remains unchanged and does not import the private
  experiment modules;
- Increment 014 mechanism work introduced no new third-party dependency;
- no 13-row scenario matrix, scenario runner, or experiment execution was
  introduced.

The final closure-readiness review identified one documentation and
claim-discipline issue, not an implementation defect. README had classified the
aggregate result as: "The 97-test result is an internal evaluation result for
this commit." It was corrected to: "The 97-test result is a repository-local
engineering verification result for this commit."

### Claim boundaries at completion

- **Definition:** the bounded mechanism uses the inherited Increment 013
  observation, freshness, effect/action binding, authorizing-path eligibility,
  and required-witness coverage semantics.
- **Design choices:** the private experiment-local Python representations and
  derivations, exact primitive-type validation choices, immutable coverage
  inventories, deterministic `ValueError` handling, and the recorded
  configuration-validation ordering.
- **Engineering observation:** the four frozen Increment 013 dependency
  semantics can be represented as isolated deterministic in-memory mechanisms
  over synthetic observation values, with deliberate non-evaluation,
  observation failure, preservation, and substantive invalidation mechanically
  distinguished under focused engineering tests.
- **Internal evaluation result:** None.
- **Research hypothesis:** Increment 013's expected scenario mappings remain
  hypotheses.
- **Research conclusion:** None.

Completion does not establish that the 13-row mapping experiment passed, that
the prospective mappings are empirically correct, that obligation-scoped
revalidation preserves full-reevaluation disposition, that authentic external
witness acquisition or revocation occurred, that production authentication or
authorization is implemented, that policy behavior is correct, that external
consequences are enforced, that the mechanism is portable beyond this bounded
implementation, or that Track A has a research conclusion.

## Artifacts

Prospective increment record:

```text
docs/increments/014-implement-pure-witness-mapping-mechanism.md
```

Intermediate implementation and test artifacts:

```text
src/runtime_validity/_experiment_observation.py
src/runtime_validity/_experiment_mapping.py
tests/test_experiment_observation.py
tests/test_experiment_freshness.py
tests/test_experiment_binding.py
tests/test_experiment_eligibility.py
tests/test_experiment_coverage.py
```

## Commit

The accumulated observation, freshness, binding, and eligibility work first
entered repository history together in WIP commit `9040bf4`. The later
lockfile-only commit is `5253559`. The required-witness coverage slice, its
focused tests, the provenance note, and this record update are committed
together as a separate coverage-slice commit following `5253559`.

## Next Step

Increment 014 leaves the frozen mechanism ready for a separately authorized
future increment that may instantiate and execute the Increment 013 scenario
matrix. That future work remains separate from Increment 014 and is not
authorized by this record.
