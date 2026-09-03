# Increment 011: Externally Grounded Obligation Universe

Status: In Progress

## Objective

Define the initial Track A obligation universe from published runtime enforcement, authorization, delegation, usage-control, and commit-time authorization mechanisms rather than deriving the obligation set from Runtime Validity implementation details or from Governed Execution candidate dimensions.

The uncertainty being reduced is:

> Which heterogeneous governance obligations should Track A include in its first controlled invalidation-mapping experiment, based on conditions already required by relevant published mechanisms?

This increment is preparatory research work for the Track A invalidation experiment.

It does not yet add new runtime obligation kinds or change `/decide`.

## Starting State

The current Runtime Validity implementation supports one deliberately narrow obligation kind:

```text
authority_valid
```

Increment 002 explicitly states that this is not intended to define a complete obligation ontology.

The current implementation demonstrates a bounded authority-change case:

```text
prior expected authority = true

runtime authority:
true -> false

full revalidation:
current = false
result = MISMATCH
outcome = HOLD
```

Increment 010 additionally retains a process-local artifact representing the implementation-recorded authority transition.

These mechanisms establish an engineering baseline.

They do not establish which obligation classes are appropriate for the broader Track A experiment.

## Track A Research Role

Track A is mapping-first.

The primary empirical object is:

```text
controlled runtime intervention
        x
governance obligation
        |
        v
invalidation result
```

The intended research priority is:

1. intervention-to-obligation invalidation mapping
2. disposition preservation relative to full commit-boundary reevaluation
3. revalidation work, latency, or cost

Increment 011 addresses the obligation side of that matrix.

## Research Question

> Which distinct governance obligations are explicitly or operationally required by strong published runtime enforcement, authorization, delegation, usage-control, and commit-time authorization mechanisms, and which of those obligations are suitable for controlled Track A invalidation experiments?

## Scope

This increment will:

- identify a bounded set of strong published mechanisms relevant to Track A;
- extract the conditions those mechanisms require to hold;
- preserve source terminology separately from Track A normalization;
- record why each candidate obligation is included;
- identify overlaps and apparent duplicates;
- identify conditions that belong primarily to later Governed Execution tracks;
- select a minimal initial obligation universe for controlled experimentation;
- preserve unresolved interpretations rather than forcing premature normalization.

Each candidate obligation should retain at least:

```text
source
source mechanism
source terminology
Track A normalized label
condition that must hold
candidate runtime witness
candidate invalidating intervention
scope notes
unresolved interpretation
```

## Source Discipline

The obligation universe must be grounded in published mechanisms.

Governed Execution candidate substrate dimensions such as:

- Identity
- Task state
- Tempo
- Cost
- Currency
- Fidelity

must not be used as the source of the obligation ontology.

Likewise, candidate change classes such as:

- Authority
- Governance/policy
- Evidence
- Target/environment
- Interface/tool
- Execution state

may later help organize interventions, but they must not be treated as evidence that corresponding obligations exist.

Runtime Validity implementation fields must not become research obligations merely because the code already contains them.

## Terminology Decision Point

UCON's Authorization (A), oBligation (B), and Condition (C) are precise, distinct technical terms (Park, Zhang, Sandhu 2004; Katt et al. 2008). None of Track A's current or candidate conditions are oBligations in UCON's technical sense — they are state predicates, structurally closer to UCON's Authorization or Condition. Track A's use of "obligation" must not be silently read as UCON's (B).

SAGE-Fin's "coverage debt" (see "Verified Prior-Art Sources" below) was earlier described here as duty-like, on the strength of an unverified secondary characterization. Checked directly against the primary source, coverage debt denotes required witness/validator predicates that are missing, stale, unpromoted, or invalid — a state condition that must hold, not a duty an actor must actively discharge. It is therefore closer to UCON's Authorization/Condition than to oBligation (B), the same direction as Track A's own conditions rather than a counter-example to it. This correction is recorded here so the earlier, unverified characterization is not repeated.

"Governance obligation" remains the current master term used across Track A documentation. This increment records, as an open decision point rather than a resolved one, whether "decision dependency" or another neutral term would be a less ambiguous normalized experimental representation, given the collisions above. No rename is made by this increment. Any future rename is a separate, explicit design decision to be recorded when made, not a silent substitution.

## Baselines

Strong commit-time and stateful authorization mechanisms are serious baselines.

The prior-art review must distinguish:

```text
mechanism already evaluates a condition at commit time
```

from:

```text
Track A selectively revalidates obligations from a prior decision
```

If an existing mechanism already subsumes a proposed Track A mechanism or experimental condition, that should narrow the Track A claim rather than be presented as novelty.

No source is treated as prior art for Track A merely because it was previously named in this repository. Each source below was independently verified (full text obtained and read, except where noted) before being recorded. The review remains open to additional relevant sources and does not claim completeness.

See "Verified Prior-Art Sources" below for the sources this review currently relies on, and "Current Claim Position" for what those sources do and do not establish about Track A.

## Verified Prior-Art Sources

Each entry carries: exact title, authors, year, the verified mechanism, the source's own terminology, its relevance to Track A, and an explicit distinction from Track A's proposed mechanism. A stable identifier (DOI, arXiv version, or other canonical publication identifier) is included where it was independently verified in this session. Verified bibliographic identity (title, authors, year, venue) is a separate requirement from stable-identifier availability: the former is required for every entry; the latter is recorded when verified and marked explicitly unresolved, not silently omitted or invented, when it was not. Where full text was not obtained, that limitation is stated rather than papered over.

### MasuGate

- Title: Stateful Governance for Concurrent Agentic Systems
- Authors: Yuxiang Peng, Xiaodi Wu
- Year: 2026 (v1 submitted August 3, 2026; v2 August 10, 2026)
- Identifier: arXiv:2608.02764v2
- Verified mechanism: defines policy-state serializability (PSS) — a correctness condition requiring that concurrent governed operations be explainable as a serial history in which each decision matches the policy state immediately before its position and its effect applies exactly there. Computes, per operation, a policy read scope, an effect read scope, and an effect write scope, via a policy compiler (certifies at compile time the finite set of policy-state view calls a policy may evaluate) and provider-declared effect footprint resolvers (map an action to the policy-state scopes it reads or writes). Detects an inter-operation conflict when one operation's effect write scope overlaps another's policy read scope, and serializes only conflicting operations via local keyed locks plus provider-level scoped locks (e.g. PostgreSQL), leaving non-conflicting operations to proceed concurrently. Handles delayed human approval via split-phase operations (reservation mode: escrow-style capacity reservation; transaction mode: fresh revalidation at resolution). Benchmarked in a PostgreSQL-backed procurement-workflow prototype against a "Global" (single coarse-lock, full-serialization) baseline and a "Manual tx" baseline; scoped modes match Global's correctness (zero stale allows, full PSS) while running faster. Provider-declared scope resolvers are trusted, not verified — an incomplete resolver silently voids the correctness guarantee (the paper's Theorem 2, Policy-State Serializability by Scoped Enforcement).
- Source terminology: "policy-state serializability," "policy read scope," "effect read/write scope," "scoped enforcement," "reservation." Scoping here is a synchronization/locking-granularity concept, not a selective-evaluation concept.
- Relevance to Track A: strong overlapping baseline for stale authorization under mutable policy state, policy-state serializability, policy read scopes, effect read/write scopes, provider-declared scope soundness, scoped inter-operation coordination, commit-time policy/effect coupling, and delayed-approval revalidation/reservation.
- Distinction from Track A: MasuGate's scoping is inter-operation coordination — it determines which concurrent operations must wait for each other over shared policy state. MasuGate describes fresh policy evaluation within the protected scoped enforcement context. The reviewed paper does not describe selective reuse of unaffected predicate/dependency results from an earlier decision. Track A's candidate scope is different: affected dependencies within one prior decision, not concurrent operations contending over shared state. MasuGate does not subsume this, and Track A is not thereby made novel relative to MasuGate — the two occupy adjacent, overlapping problem space with different mechanisms, and it remains unresolved which one, if either, Track A's specific question actually needs.

### Janicke, Cau, Siewe, Zedan 2008

- Title: Concurrent Enforcement of Usage Control Policies
- Authors: Helge Janicke, Antonio Cau, Francois Siewe, Hussein Zedan
- Year: 2008
- Identifier: IEEE POLICY 2008, DOI 10.1109/POLICY.2008.44
- Verified mechanism: stateful UCON policies with mutable shared attributes are analyzed statically to compare which usage processes/controllers read and write overlapping policy-rule state. This comparison constructs a dependency graph between usage processes. Processes connected in that graph are constrained to mutual exclusion; processes in independent (disconnected) subgraphs may execute concurrently without synchronization between them. The purpose is selective concurrency enforcement — avoiding one global interleaving over all usage processes — not selective re-evaluation of any single process's own policy predicates.
- Source terminology: "dependencies between policy rules," "static analysis," "concurrent enforcement." The dependency here is an inter-process relation over shared mutable attributes, not an intra-decision relation over one decision's own heterogeneous conditions.
- Relevance to Track A: strong adjacent prior art for the general idea that concurrent authorization work need not be globally serialized — dependency structure over shared state can determine which units of work may safely proceed independently. Structurally the closest sibling to MasuGate's own inter-operation conflict detection, predating it by roughly eighteen years within the same UCON lineage.
- Distinction from Track A: Janicke's dependency relation is inter-usage-process to synchronization constraint (should process A and process B be mutually excluded, given what state each touches). Track A's candidate mechanism is runtime intervention to affected dependencies within one prior decision to selective reevaluation/reuse (should this one decision recheck condition X while trusting condition Y, given what specifically changed). These are not the same relation, and this paper does not perform the second. Classified as strong adjacent prior art, not an exact match.

### Ray lineage (recorded as two distinct sources)

- Title: Real-time update of access control policies
- Author: Indrakshi Ray
- Year: 2004
- Identifier: Data & Knowledge Engineering 49(3), 287–309, DOI 10.1016/j.datak.2003.09.003
- Verified mechanism (full text read): a database/transaction model in which policy objects (subject-set, target-set, rights-set) can be updated by policy-update transactions concurrently with ordinary data transactions executing under those policies. Defines "policy-secure": every read or write a transaction performs must be authorized by policy for the entire duration of the operation. Proves, with theorems, that well-formed, two-phase-locked transactions are conflict-serializable and policy-secure under naive strict locking. Introduces a semantics-based improvement: for each type of policy-update transaction, a commute set is derived once, via formal proof (Z-notation specifications plus a commutativity definition), identifying which other transaction types may execute concurrently with it without being invalidated. At runtime, when a lock request conflicts with an in-progress policy deployment, the system checks type membership in the precomputed commute set: if the conflicting transaction's type commutes, it is not aborted and continues under its original, unmodified authorization; if not, it is aborted. Proves that this semantics-based locking strictly dominates naive locking in achievable concurrency while preserving serializability and policy-security.
- Source terminology: "policy-secure," "commute set," "policy relaxation/restriction," conflict-serializability (following Bernstein et al.).

- Title: Implementing Real-Time Update of Access Control Policies
- Authors: Indrakshi Ray, Tai Xin
- Year: 2004
- Identifier: DBSec 2004, DOI 10.1007/1-4020-8128-6_5
- Status: a real, distinct citation with its own author list and DOI. Its full text has not been independently verified in this review. It is not assumed to be identical in content to the DKE paper above, and must not be cited as though the two were interchangeable.

- Relevance to Track A (applies to the verified DKE paper; treat with corresponding caution for the unverified DBSec paper): strong prior-art pressure for the claim that formal compatibility/commutativity reasoning permits some already-authorized transactions to continue without recomputation, while incompatible cases are prevented or aborted — a proven instance of reuse-instead-of-recompute under a known class of change (policy update), with a proven baseline comparison (naive locking vs. semantics-based locking).
- Distinction from Track A: the reuse/abort decision operates at whole-transaction granularity, driven by a statically precomputed transaction-type compatibility table, not by decomposing one transaction's own authorization into multiple heterogeneous dependencies and selectively rechecking a subset while reusing the rest. It remains whole-transaction/policy-update compatibility rather than heterogeneous per-dependency selective reevaluation within one prior decision.

### Park, Zhang, Sandhu 2004

- Title: Attribute Mutability in Usage Control
- Authors: Jaehong Park, Xinwen Zhang, Ravi Sandhu
- Year: 2004
- Identifier: DBSec 2004, DOI 10.1007/1-4020-8128-6_2
- Verified mechanism: a formal taxonomy, not an enforcement mechanism. Classifies attribute management (admin-controlled/immutable vs. system-controlled/mutable) and attribute liveness (temporary vs. persistent), and identifies five mutability variations (exclusive/inclusive, consumable/creditable, immediate revocation, obligation, dynamic confinement), each formalized with worked UCON_ABC examples. Explicitly excludes Conditions from mutability treatment, since conditions are subject/object-independent. Contains no dependency concept, no selective-reevaluation mechanism, and no empirical or architectural component.
- Source terminology: UCON_ABC's own Authorization (A), oBligation (B), Condition (C); "mutability"; "temporary/persistent attribute." These are precise, distinct technical terms and are preserved as such, not normalized into Track A's "obligation."
- Relevance to Track A: foundational vocabulary and a source-grounded catalogue of concrete reasons an attribute might change.
- Distinction from Track A: addresses a different problem — a classification of when and why mutability matters — rather than any revalidation-efficiency or selective-reevaluation mechanism. A vocabulary and example source, not a baseline candidate.

### Katt, Zhang, Breu, Hafner, Seifert 2008

- Title: A General Obligation Model and Continuity-Enhanced Policy Enforcement Engine for Usage Control
- Authors: Basel Katt, Xinwen Zhang, Ruth Breu, Michael Hafner, Jean-Pierre Seifert
- Year: 2008
- Identifier: SACMAT 2008, DOI 10.1145/1377836.1377856
- Verified mechanism: extends UCON's state transition with an explicit `ongoingCheck` state entered whenever any subject, object, or environment attribute changes; in that state the applicable ongoing decision (onA/onB/onC, "or any combination of them") is re-evaluated. Organizes enforcement rules by session state (RequestCheckRules, OngoingCheckRules, DeniedRules, EndRules, RevokedRules) via an XACML-based architecture with an Attribute Decision Function and an Obligation Decision Function. Classifies obligations by who performs them (system vs. subject), what they act on (controllable vs. non-controllable object), and when they are checked, distinguishing "trusted" obligations (no fulfillment check needed) from "non-trusted" ones. Demonstrated only via a proof-of-concept eHealth prototype for feasibility; the paper's own conclusion explicitly defers performance evaluation to future work. No dependency graph, no selective-reevaluation mechanism, no correctness theorem, no baseline comparison.
- Source terminology: UCON_ABC's Authorization/oBligation/Condition; "trusted/non-trusted obligation"; "controllable/non-controllable object"; "ongoing check."
- Relevance to Track A: direct UCON-continuity lineage for what triggers reevaluation during an ongoing session, and a genuinely useful trusted/non-trusted obligation filter concept.
- Distinction from Track A: reevaluation is triggered by any attribute change and recomputes the full applicable ongoing rule combination for the session state; there is no mechanism mapping which specific attribute change affects which specific one of several predicates, and no reuse of prior partial results.

### CommitGuard

- Title: Temporary Authority, Permanent Effects: Commit-Time Authorization for LLM Agents
- Author: Igor Santos-Grueiro
- Year: 2026 (submitted July 11, 2026)
- Identifier: arXiv:2607.10487
- Verified mechanism: decomposes a single durable-effect commit-time authorization into four named, heterogeneous conditions — Freshness, Causal priority, Effect binding, Commit eligibility — each checked at every protected commit. All four conditions are evaluated every time; the paper's pseudocode gates abort/repair independently per condition, but no mechanism or experiment in the paper shows that a known intervention type allows some of the four to be skipped or trusted while only rechecking the others. No baseline comparison between full and selective reevaluation is present.
- Source terminology: "witness," "eligibility," "binding," "causal priority," "commit boundary."
- Relevance to Track A: a particularly important full commit-boundary baseline — a real, heterogeneous, named multi-condition commit-time decision, exactly the shape Track A needs for its full-reevaluation comparison arm.
- Distinction from Track A: this is a full-reevaluation exemplar, not a selective-reuse mechanism. No verified selective reuse mechanism was located in the reviewed paper. It must not be described as already performing obligation-scoped revalidation.

### SAGE-Fin

- Title: Context Is Not Authority: Structured Runtime Governance for Financial Market Agents
- Authors: Rui Tang, Qiangqiang Liu, Yichi Zhang, Youwei Wang, Xi Chen, Chen Dong
- Year: 2026 (v1 August 10, 2026; v2 August 17, 2026)
- Identifier: arXiv:2608.09025 (primary category cs.AI; secondary cs.CR, stat.ML)
- Verified mechanism: defines "coverage debt" as the set of required witnesses or validators that are missing, stale, unpromoted, or invalid for a candidate action — described in the paper as runtime state, not a footnote, that can downgrade commitment level, block execution authorization, or require clarification, repair, escalation, or human approval. Compiles proposals into typed, adapter-bound candidates and requires an exact-artifact receipt whose nominal type matches the consuming response, execution, or policy adapter before an effect is permitted.
- Source terminology: "coverage debt," "institutional obligation" (used for the required witness/validator predicates a candidate must satisfy), "adapter-bound candidate," "exact-artifact receipt." Directly verified against the primary source: both terms denote authorization-like state predicates that must hold at consumption time, not duties requiring active fulfillment — see the correction recorded in "Terminology Decision Point" above.
- Relevance to Track A: a per-candidate, typed staleness/coverage-tracking concept in one domain (financial market agents), conceptually adjacent to a per-obligation staleness signal.
- Distinction from Track A: domain-specific to financial adapters and typed effects; does not describe a controlled-intervention-to-affected-dependency mapping, and does not compare full versus selective reevaluation. An adjacent single-domain instantiation, not a general mechanism to measure Track A against.

### Classical mechanism ancestry (general-purpose, not authorization-specific)

Bibliographic identity (title, authors, year, venue) is verified for every entry below. A stable identifier is recorded where it was independently verified in this session; where one was searched for and not confirmed, that is stated explicitly rather than left silently absent or filled with a guessed value.

- Doyle, J. (1979). A Truth Maintenance System. Artificial Intelligence 12(3), 231–272. Identifier: DOI 10.1016/0004-3702(79)90008-0 (independently verified). Justification-based dependency tracking: retracting an assumption retracts only the beliefs whose justification chain depends on it; everything else stands unchanged.
- Forgy, C. (1982). Rete: A Fast Algorithm for the Many Pattern/Many Object Pattern Match Problem. Artificial Intelligence 19(1), 17–37. Identifier: DOI 10.1016/0004-3702(82)90020-0 (independently verified). When one fact changes, only the reachable parts of a compiled matching network are re-evaluated; unaffected partial matches are retained.
- Gupta, A., Mumick, I.S., Subrahmanian, V.S. (1993). Maintaining Views Incrementally. Proceedings of ACM SIGMOD 1993, pp. 157–166. Identifier: DOI 10.1145/170035.170066 (independently verified). (The DRed algorithm.) Incremental Datalog/view maintenance: over-delete the consequences of a deleted fact, then re-derive whatever remains provable via alternative derivations, instead of full recomputation.
- Binder: DeTreville, J. (2002). Binder, a Logic-Based Security Language. IEEE Symposium on Security and Privacy 2002, pp. 105–113. Identifier: DOI 10.1109/SECPRI.2002.1004365 (independently verified); also circulated as Microsoft Research Technical Report MSR-TR-2002-21. Authorization expressed as a Datalog program.
- SecPAL: Becker, M.Y., Fournet, C., Gordon, A.D. (2010). SecPAL: Design and Semantics of a Decentralized Authorization Language. Journal of Computer Security 18(4), 619–665. Identifier: DOI 10.3233/JCS-2009-0364 (independently verified). Authorization expressed as Datalog with constraints. Neither Binder nor SecPAL was found, in this review, explicitly coupled to an incremental/seminaive Datalog evaluator for revalidation purposes, despite that substrate being a natural fit.
- Margrave: Fisler, K., Krishnamurthi, S., Meyerovich, L.A., Tschantz, M.C. (2005). Verification and Change-Impact Analysis of Access-Control Policies. ICSE 2005, pp. 196–205. Identifier: DOI 10.1145/1062455.1062502 (independently verified). Computes, for two versions of an access-control policy, the exact set of requests whose decision changes between them, via multi-terminal binary decision diagrams — change-impact analysis of policy-text edits, not of runtime state changes affecting one already-issued decision.
- Relevance to Track A: establishes that dependency-tracked selective recomputation — the general computational shape of what Track A proposes — is not a novel Track A primitive. It is decades old and mechanically mature outside the authorization domain (Doyle, Forgy, Gupta/Mumick/Subrahmanian), and has an established substrate inside the authorization domain (Binder, SecPAL as Datalog-based authorization; Margrave as policy change-impact analysis), without those two lines having been shown, in this review, to be explicitly combined for the purpose Track A is studying.
- Distinction from Track A: none of these are authorization-decision-revalidation mechanisms in their own right; they are the general-purpose technique family and adjacent policy-analysis tooling any Track A implementation would be built on or measured against for mechanism precedent, not competing experimental claims.

## Planned Artifact

The primary artifact for this increment will be an obligation-source matrix.

Conceptually:

```text
| Source | Mechanism | Source condition | Normalized obligation | Runtime witness | Candidate invalidating intervention | Notes |
```

Normalized obligation names are experimental labels only.

They do not establish a universal Governed Execution obligation ontology.

## Planned Evaluation

For each candidate obligation/dependency:

1. locate the published mechanism it comes from;
2. identify the exact condition, invariant, or state dependency relevant to consequential action;
3. preserve the source terminology;
4. determine whether it is operationally distinct from already selected candidates;
5. identify the runtime witness that establishes it;
6. identify what kind of controlled runtime change can make prior reliance on it unusable;
7. determine whether it can be manipulated independently in a controlled experiment;
8. identify at least one candidate intervention expected to invalidate it;
9. identify what full commit-boundary reevaluation would naturally inspect for it;
10. classify whether it belongs in Track A or primarily in another track;
11. prior-mechanism-coverage check: determine whether a verified prior-art source (see "Verified Prior-Art Sources") already fully exercises this exact candidate under a known class of change. If so, record it explicitly as a replication/baseline candidate rather than an implicitly novel case, and record which source subsumes it and to what degree.

## Inclusion Criteria

A candidate obligation should enter the initial Track A experiment only if:

- it is grounded in a published mechanism;
- its meaning can be stated operationally;
- a runtime witness can be defined;
- at least one controlled intervention can plausibly change whether it holds;
- its inclusion adds a distinct experimental condition rather than merely renaming another obligation.

The initial experimental set is capped at no more than 3-4 candidates. This cap bounds the final selection; it is not a target to fill. Selection occurs only after the obligation-source matrix is complete enough to justify a choice, not before. This increment does not select the final experimental set.

## Exclusion Criteria

A candidate should not enter the initial Track A obligation universe merely because:

- it appears in the Governed Execution master;
- it exists in Keystone code;
- it is intuitively governance-related;
- it may matter in a future production system;
- it belongs primarily to evidence reconstruction;
- it belongs primarily to distributed governability;
- it belongs primarily to cross-system portability;
- it belongs primarily to meaningful human review.

## Non-Goals

This increment does not:

- claim a complete governance ontology;
- claim that selected obligations generalize across domains;
- add new obligation implementations to the API;
- implement intervention detection;
- implement obligation-scoped revalidation;
- compare scoped versus full reevaluation;
- measure latency or computational work;
- establish action-boundary enforcement;
- establish production authentication or authorization;
- establish independent evidence validity;
- validate Governed Execution as a whole;
- select the final experimental obligation/dependency set;
- claim or deny Track A novelty relative to reviewed prior art.

## Failure Criteria

This increment should be considered unsuccessful or incomplete if:

- candidate obligations are primarily derived from Keystone or Governed Execution terminology rather than published mechanisms;
- source terminology cannot be traced to the originating work;
- multiple candidate obligations are retained despite being operationally indistinguishable;
- selected obligations cannot be manipulated or observed in a controlled experiment;
- Track A absorbs questions that properly belong to later tracks without explicit justification;
- the resulting obligation set is presented as complete or universal;
- a candidate fully covered by a verified prior-art source is retained without being flagged as a replication/baseline case;
- a source is cited as prior art without a verified title, author list, and year, or with a stable identifier presented as verified when it was not independently confirmed.

## Claim Classification

At the start of this increment:

- the obligation universe is a **Research hypothesis / experimental design artifact**;
- normalized obligation labels are **Design choices**;
- source-mechanism descriptions are **External evidence** when accurately supported by published sources;
- selection of obligations for the experiment is a **Research design choice**;
- no Track A research conclusion exists yet.

## Current Claim Position

This records the accurate current state, not a Track A research conclusion:

- incremental/selective recomputation under dependency tracking is established prior art (Doyle 1979; Forgy 1982; Gupta, Mumick, Subrahmanian 1993), predating this research program by decades;
- continuous/stateful authorization is established prior art (the UCON_ABC lineage: Park, Zhang, Sandhu 2004; Katt et al. 2008);
- scoped concurrent enforcement over shared mutable policy state is established prior art (Janicke et al. 2008; MasuGate, Peng and Wu 2026);
- selective reuse of an already-issued authorization under a known, formally characterized class of change is established prior art (Ray 2004);
- no exact match has yet been located in the sources reviewed so far for the specific Track A experimental combination: heterogeneous intra-decision dependencies, plus a controlled runtime intervention, plus affected-subset reevaluation and reuse of the rest, plus a disposition comparison against full commit-boundary reevaluation of the same decision.

That final item is classified as an unresolved research gap, not a research conclusion. It does not establish that Track A's proposed combination is achievable, valuable, or free of confounds once attempted; it establishes only that this review did not find it already done. Absence of an exact match in a broad but non-exhaustive review is not proof that no such match exists.

## Threats to Validity

Expected threats include:

- incomplete prior-art coverage;
- misinterpreting source mechanisms;
- normalizing distinct mechanisms too aggressively;
- retaining duplicate obligations under different names;
- selecting obligations because they are easy to implement;
- overfitting the obligation set to the existing authority demo;
- confusing permission governance with broader decision justification;
- assuming that an obligation useful in one domain is portable to others;
- treating a paired conference/journal citation (e.g. the Ray 2004 lineage) as a single identical source without independently verifying each;
- treating a search-engine-synthesized characterization of a source as equivalent to verified full-text content.

## Reproducibility Requirements

The completed increment should retain:

- sources reviewed;
- source versions, identifiers, or publication dates where available;
- source terminology and extracted conditions;
- normalization decisions;
- rejected candidate obligations and reasons;
- unresolved interpretations;
- prior-mechanism-coverage determinations for each candidate;
- final selected obligation set;
- later corrections discovered during implementation.

## Planned Tests

No runtime tests are added by this increment unless implementation changes become necessary.

The primary verification is research-artifact verification:

- every selected obligation is traceable to a source mechanism;
- source wording and Track A normalization remain distinguishable;
- rejected candidates and duplicate mappings are preserved;
- selected obligations satisfy the inclusion criteria;
- every first-class source carries a verified exact title, author list, and year before being used to justify or reject a candidate, plus a stable identifier (DOI/arXiv version) where one has been independently verified in this session — where no identifier could be independently verified, the source carries an explicit "identifier not independently verified" note rather than an omitted or invented field;
- no runtime code changes are introduced merely to fit the proposed ontology.

## Observed Result

Not yet evaluated.

## Next Step

Continue the obligation-source matrix using the sources in "Verified Prior-Art Sources" above, applying the prior-mechanism-coverage check in "Planned Evaluation" to each candidate, before changing runtime code. Do not select the final experimental set until the matrix is complete enough to justify a bounded (3-4 candidate) selection.
