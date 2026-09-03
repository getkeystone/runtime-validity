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

## Obligation-Source Matrix

This section applies the methodology in "Planned Evaluation" to the sources in "Verified Prior-Art Sources" above. It is a checkpoint artifact that supports a later selection decision. It is not the final obligation-universe selection, and no candidate below is asserted to be validated, canonical, or complete.

Each candidate below is built only from what is already recorded and verified in this file's "Verified Prior-Art Sources" section, re-read in full immediately before writing this matrix. No new external verification was performed for this checkpoint. Where a source names a condition without this file already recording its detailed formal definition (this applies to three of CommitGuard's four named conditions), that gap is stated explicitly rather than filled by inference or invention.

### Summary index

| # | Candidate (provisional label) | Primary source | Current disposition |
|---|---|---|---|
| 1 | Policy-state currency | MasuGate (Peng & Wu 2026) | retain as candidate, overlap unresolved |
| 2 | Witness/authorization freshness | CommitGuard (Santos-Grueiro 2026) | retain as candidate |
| 3 | Causal/ordering priority | CommitGuard (Santos-Grueiro 2026) | retain as candidate, weaker for a first experiment |
| 4 | Effect/action binding | CommitGuard (Santos-Grueiro 2026) | retain as candidate |
| 5 | Target/commit eligibility | CommitGuard (Santos-Grueiro 2026) | retain as candidate |
| 6 | Evidence/witness coverage sufficiency | SAGE-Fin (Tang et al. 2026) | retain as candidate, overlap with #2 unresolved |
| - | Whole-transaction policy compatibility | Ray 2004 (DKE) | baseline only |
| - | Any-attribute-change ongoing reevaluation | Katt et al. 2008 | baseline only |
| - | Inter-process concurrency dependency | Janicke et al. 2008 | later-track concern |
| - | Attribute mutability taxonomy | Park, Zhang, Sandhu 2004 | vocabulary/background only |
| - | Selective recomputation technique family | Doyle 1979; Forgy 1982; Gupta, Mumick, Subrahmanian 1993; Binder; SecPAL; Margrave | baseline only (general technique precedent) |
| - | Whole-transaction policy compatibility (DBSec variant) | Ray/Xin DBSec 2004 | pending source verification |

Six candidates are retained pending final selection. That is intentionally more than the eventual 3-4 cap: this checkpoint is meant to overshoot the cap so a later, separate step can select rather than merely accept whatever this review happened to produce first.

### Candidate 1: Policy-state currency

- **Source:** MasuGate (Peng & Wu 2026, arXiv:2608.02764v2).
- **Source mechanism:** policy-state serializability via a compile-time policy read scope: the finite set of policy-state view calls a policy may evaluate, computed per operation.
- **Source terminology:** "policy read scope," "policy-state serializability." MasuGate uses "scope" as a synchronization/locking-granularity concept, not a selective-evaluation concept; this candidate borrows only the idea that a decision reads an identifiable, bounded slice of policy state, not MasuGate's locking mechanism itself.
- **Condition that must hold:** the specific policy-state slice a decision's justification read has not changed since it was read.
- **Provisional Track A normalized label:** policy-state currency. Structurally closer to UCON's Condition than to oBligation (B); not asserted to be the master "governance obligation" term.
- **Candidate runtime witness:** a version or hash identifier for the specific policy fragment(s) read by the original decision.
- **Candidate invalidating intervention:** mutate or version-bump the specific policy fragment that was read (leaving unrelated policy fragments unchanged).
- **Evaluation observability:** compare the policy-fragment version/hash recorded at decision time against the current version/hash for that same fragment at revalidation time. Concerns relation (2) only: whether this specific dependency is invalidated, not whether final disposition changes.
- **Overlap / possible duplicate:** unresolved against Runtime Validity's current `authority_valid` predicate. In the current bounded implementation, "authority" and "the policy content that determines authority" are conflated into a single Boolean; there is no witness distinguishing an intervention on the policy content from an intervention on a subject's authorization state. Whether these are experimentally distinguishable depends on adding a policy-version witness that does not exist today. Not resolved by this checkpoint.
- **Track A relevance:** MasuGate is a strong overlapping baseline for stale-authorization-under-mutable-policy-state, but its own mechanism performs fresh evaluation within a protected scope, not selective reuse of an earlier decision's unaffected dependencies. MasuGate does not subsume this candidate; the candidate is inspired by MasuGate's scope concept, not evidenced by MasuGate performing the candidate's proposed reuse.
- **Current disposition:** retain as candidate, overlap unresolved.
- **Unresolved interpretation:** whether "policy content" and "authority state" are one dependency or two in Runtime Validity's bounded model is an open design question, not answered by the source review. See "Matrix Review Before Final Selection."

### Candidate 2: Witness/authorization freshness

- **Source:** CommitGuard (Santos-Grueiro 2026, arXiv:2607.10487).
- **Source mechanism:** one of four named heterogeneous conditions ("Freshness") checked at every protected commit in a durable-effect commit-time authorization.
- **Source terminology:** "Freshness," "witness," "commit boundary."
- **Condition that must hold:** the authorization witness relied upon is not older than the mechanism's freshness threshold at commit time.
- **Provisional Track A normalized label:** witness/authorization freshness.
- **Candidate runtime witness:** a timestamp or age value attached to the authorization witness.
- **Candidate invalidating intervention:** let time elapse past the freshness threshold, or administratively expire the witness, without changing the underlying authorization decision itself.
- **Evaluation observability:** compare witness age at original decision time against witness age at revalidation time relative to a fixed threshold.
- **Overlap / possible duplicate:** possible overlap with Candidate 6 (SAGE-Fin's coverage debt), which also treats "stale" witnesses as an invalidating condition. Not resolved whether these are the same dependency under two names or genuinely distinct (see Candidate 6 and "Matrix Review Before Final Selection").
- **Track A relevance:** CommitGuard is the strongest available full-commit-boundary baseline exemplar: a real, heterogeneous, named multi-condition commit-time decision, exactly the shape Track A's full-reevaluation comparison arm needs. CommitGuard checks all four of its conditions every time; no mechanism in the reviewed material shows any of the four being selectively skipped or trusted. Using Freshness as a Track A candidate for selective revalidation would therefore not be replicating an existing selective mechanism; it would be a new application of a condition CommitGuard itself always fully rechecks.
- **Current disposition:** retain as candidate.
- **Unresolved interpretation:** this file records only the name "Freshness" and the general commit-time-authorization framing from CommitGuard; it does not record CommitGuard's own formal definition of the freshness threshold or how it is computed. That detail requires re-reading the primary source before this candidate can be operationalized, and is not assumed here.

### Candidate 3: Causal/ordering priority

- **Source:** CommitGuard (Santos-Grueiro 2026, arXiv:2607.10487).
- **Source mechanism:** one of the same four named conditions ("Causal priority"), checked at every protected commit.
- **Source terminology:** "Causal priority," "commit boundary."
- **Condition that must hold:** the authorization event maintains the required ordering relationship relative to other relevant events before the commit is permitted (for example, that no intervening event should have preceded and altered it).
- **Provisional Track A normalized label:** causal/ordering priority.
- **Candidate runtime witness:** an event sequence or ordering marker associated with the authorization and with candidate intervening events.
- **Candidate invalidating intervention:** insert an intervening event that violates the required ordering between the original decision and the commit.
- **Evaluation observability:** compare recorded ordering markers; requires an explicit event log or sequence mechanism that Runtime Validity's current bounded implementation does not have.
- **Overlap / possible duplicate:** none identified against the other candidates; ordering is a distinct dimension from state-value comparison.
- **Track A relevance:** grounded in the same strong full-commit-boundary baseline as Candidate 2, but weaker for a first controlled experiment: ordering conditions are inherently about relationships between multiple events, which is structurally closer to Janicke et al. 2008's and Katt et al. 2008's concerns (concurrency and session-state ordering) than to a single-decision, single-intervention Boolean-style predicate. Retaining it risks Track A absorbing a later-track ordering/concurrency question under its own name.
- **Current disposition:** retain as candidate, weaker for a first experiment.
- **Unresolved interpretation:** as with Candidate 2, only the name and general framing are recorded here; CommitGuard's exact formal definition of causal priority requires re-reading the primary source. Additionally unresolved: whether a single-decision experiment can operationalize an ordering condition at all without first building a minimal event-sequencing mechanism, which is itself out of this increment's scope.

### Candidate 4: Effect/action binding

- **Source:** CommitGuard (Santos-Grueiro 2026, arXiv:2607.10487).
- **Source mechanism:** one of the same four named conditions ("Effect binding"), checked at every protected commit.
- **Source terminology:** "Effect binding," "binding," "commit boundary."
- **Condition that must hold:** the specific effect or action being committed matches the effect or action that was actually authorized; the authorization must not be reusable for a substituted effect.
- **Provisional Track A normalized label:** effect/action binding.
- **Candidate runtime witness:** an effect or action identifier recorded at decision time.
- **Candidate invalidating intervention:** substitute a different effect or action at commit time while presenting the same prior decision.
- **Evaluation observability:** compare the effect/action identifier recorded at decision time against the one presented at commit/revalidation time. A clean equality check; no additional infrastructure beyond an identifier field appears to be required.
- **Overlap / possible duplicate:** none identified against the other candidates.
- **Track A relevance:** same full-commit-boundary baseline as Candidates 2 and 3; CommitGuard always rechecks this condition, so a Track A experiment selectively revalidating it (or trusting it while rechecking others) would not replicate an existing selective mechanism.
- **Current disposition:** retain as candidate.
- **Unresolved interpretation:** only the name and general framing are recorded here; CommitGuard's exact formal definition of effect binding requires re-reading the primary source before final operationalization.

### Candidate 5: Target/commit eligibility

- **Source:** CommitGuard (Santos-Grueiro 2026, arXiv:2607.10487).
- **Source mechanism:** one of the same four named conditions ("Commit eligibility"), checked at every protected commit.
- **Source terminology:** "Commit eligibility," "commit boundary."
- **Condition that must hold:** the target or environment the effect would act upon remains in a state eligible to receive that effect at commit time.
- **Provisional Track A normalized label:** target/commit eligibility.
- **Candidate runtime witness:** an eligibility flag or state value for the target/environment.
- **Candidate invalidating intervention:** change the target/environment's state to ineligible between the prior decision and commit time (for example, the target no longer exists or has moved to a disqualifying state).
- **Evaluation observability:** compare the target/environment eligibility flag at decision time against its value at revalidation time.
- **Overlap / possible duplicate:** none identified against the other candidates. Corresponds to the "Target/environment" entry in Increment 011's own candidate change classes (Source Discipline section); this is the one candidate in this matrix with a direct, source-grounded connection to one of those hypothesis classes, rather than only a Runtime Validity or Governed Execution origin.
- **Track A relevance:** same full-commit-boundary baseline as Candidates 2 through 4.
- **Current disposition:** retain as candidate.
- **Unresolved interpretation:** only the name and general framing are recorded here; CommitGuard's exact formal definition of commit eligibility requires re-reading the primary source before final operationalization.

### Candidate 6: Evidence/witness coverage sufficiency

- **Source:** SAGE-Fin (Tang et al. 2026, arXiv:2608.09025).
- **Source mechanism:** "coverage debt," defined as the set of required witnesses or validators that are missing, stale, unpromoted, or invalid for a candidate action; typed, adapter-bound candidates require an exact-artifact receipt matching the consuming adapter before an effect is permitted.
- **Source terminology:** "coverage debt," "institutional obligation" (source's own term for the required witness/validator predicates; verified in this file's Terminology Decision Point to denote a state condition, not a UCON oBligation-B duty), "adapter-bound candidate," "exact-artifact receipt."
- **Condition that must hold:** all witnesses/validators required for the candidate action are present, current, and correctly typed for the consuming adapter; no coverage debt exists.
- **Provisional Track A normalized label:** evidence/witness coverage sufficiency.
- **Candidate runtime witness:** a per-required-witness presence/validity/type-match flag.
- **Candidate invalidating intervention:** remove, invalidate, or type-mismatch one required witness after the prior decision, leaving other witnesses untouched.
- **Evaluation observability:** compare the coverage state (which required witnesses are present and valid) at decision time against revalidation time.
- **Overlap / possible duplicate:** likely overlaps with Candidate 2 (CommitGuard's Freshness): both describe a witness becoming stale or otherwise invalid as the invalidating condition. Whether "coverage debt" and "witness freshness" are the same dependency described in two domains (financial adapters vs. generic commit-time authorization) or two operationally distinct conditions (coverage is about presence/type-match across possibly multiple required witnesses; freshness is specifically about age) is not resolved by this checkpoint.
- **Track A relevance:** a per-candidate, typed staleness/coverage-tracking concept in one domain (financial market agents); does not itself describe a controlled-intervention-to-affected-dependency mapping or a full-versus-selective reevaluation comparison. An adjacent single-domain instantiation, not a mechanism to measure Track A against.
- **Current disposition:** retain as candidate, overlap with Candidate 2 unresolved.
- **Unresolved interpretation:** whether coverage sufficiency should merge with witness freshness into one candidate, or remain distinct on the grounds that coverage concerns presence/type-matching across potentially several witnesses while freshness concerns the age of one, is an open question for the next step, not resolved here.

### Baseline-only and excluded sources (not retained as obligation candidates)

- **Whole-transaction policy compatibility (Ray 2004, DKE).** Verified mechanism: a statically precomputed commute set determines whether a data transaction may continue under its original authorization when a concurrent policy-update transaction of a known type is in progress; otherwise the transaction is aborted. This is a proven instance of reuse-instead-of-recompute under a known class of change, at whole-transaction granularity. It is treated as a strong baseline for the general claim that formal compatibility reasoning permits reuse under classified change, not as a source of a specific heterogeneous per-obligation candidate, because the source does not decompose one transaction's authorization into multiple independently reevaluable conditions. Reason against inclusion as a candidate: operates at a different granularity than Track A's proposed intra-decision, per-obligation mechanism; the source mechanism already fully resolves reuse-versus-abort at commit time for its own granularity, leaving no distinct sub-condition for Track A to add.
- **Any-attribute-change ongoing reevaluation (Katt et al. 2008).** Verified mechanism: any subject, object, or environment attribute change triggers a full `ongoingCheck` reevaluation of the applicable rule combination for the session. This is treated as a UCON-lineage baseline for "full reevaluation triggered by any change," directly relevant to Track A's full-commit-boundary comparison arm, but it supplies no mapping from a specific attribute change to a specific invalidated predicate, and no reuse of prior partial results. Reason against inclusion as a candidate: the source's own mechanism recomputes everything on any change; it does not identify a distinct dependency Track A could selectively revalidate. Its trusted/non-trusted obligation distinction is noted as useful adjacent vocabulary, not adopted as a candidate here.
- **Inter-process concurrency dependency (Janicke et al. 2008).** Verified mechanism: a static dependency graph over shared mutable policy-rule state determines which usage processes must be mutually excluded versus may run concurrently. Reason against inclusion as a candidate: this is an inter-process synchronization relation, not an intra-decision relation over one decision's own heterogeneous conditions. It belongs primarily to a later concurrency/ordering track, per this increment's own Exclusion Criteria and Scope.
- **Attribute mutability taxonomy (Park, Zhang, Sandhu 2004).** Verified mechanism: a formal taxonomy of why and how UCON attributes change (mutability, liveness, five variation types), with no enforcement mechanism, no dependency concept, and no selective-reevaluation mechanism. Reason against inclusion as a candidate: source is vocabulary-only; it classifies reasons attributes change rather than supplying a condition Track A could revalidate. Retained as background vocabulary for describing intervention types, not as an obligation source.
- **Selective recomputation technique family (Doyle 1979; Forgy 1982; Gupta, Mumick, Subrahmanian 1993; Binder; SecPAL; Margrave).** These establish that dependency-tracked selective recomputation is a decades-old, mechanically mature computational pattern, with an established (if not explicitly combined) substrate inside the authorization domain. Reason against inclusion as candidates: none of these are authorization-decision-revalidation mechanisms in their own right; they are general-purpose technique precedent for how a Track A implementation might eventually be built, not sources of governance conditions to revalidate.
- **Whole-transaction policy compatibility, DBSec variant (Ray/Xin DBSec 2004).** Bibliographically identified (title, authors, year, DOI), mechanism not independently verified for this matrix. Its full text has not been read in this review. It is not used as the sole or partial basis for any candidate above, and its relevance is assumed, cautiously, to track the verified Ray 2004 DKE paper only insofar as that assumption is explicitly flagged here as unconfirmed.

## Matrix Review Before Final Selection

This is a checkpoint review, not a selection. No final 3-4 obligation set is chosen in this increment.

**Distinct candidate dependencies remaining after obvious merges.** Six candidates are retained (Candidates 1 through 6 above). Of those, Candidate 6 has a flagged, unresolved overlap with Candidate 2, and Candidate 1 has a flagged, unresolved overlap with Runtime Validity's existing `authority_valid` predicate. If both overlaps resolve toward merging, as few as four operationally distinct candidates could remain (Candidates 2/6 merged, 3, 4, 5, and Candidate 1 either merged into `authority_valid` or kept as a separate policy-content dimension). If both overlaps resolve toward keeping the candidates distinct, six remain.

**Strongest candidates for experimental manipulation.** Candidates 4 (effect/action binding) and 5 (target/commit eligibility) currently look strongest for a first controlled experiment: each has a clean, single-value witness, a clearly stated invalidating intervention that does not depend on inventing new infrastructure (an identifier comparison and a state-flag comparison, respectively), and no unresolved overlap with another candidate. Candidate 2 (witness/authorization freshness) is also comparatively strong, contingent on resolving its overlap with Candidate 6.

**Ambiguous candidates.** Candidate 1 (policy-state currency) is ambiguous because Runtime Validity's current implementation cannot distinguish a policy-content change from an authority-state change without new witness infrastructure; whether that infrastructure is worth adding before or after obligation selection is unresolved. Candidate 6 (evidence/witness coverage sufficiency) is ambiguous for the reason stated in its own entry (possible duplicate of Candidate 2).

**Baseline-only.** Ray 2004 (DKE), Katt et al. 2008, and the classical mechanism ancestry group are baseline-only: they constrain what Track A can credibly claim as novel and supply the strong-baseline shape (especially CommitGuard, treated both as the leading full-commit-boundary baseline exemplar and as the source of Candidates 2 through 5), but are not themselves candidate obligations.

**Deferred / excluded.** Janicke et al. 2008 (inter-process concurrency, later-track concern) and Park, Zhang, Sandhu 2004 (vocabulary only) are excluded from candidacy for the reasons stated in their entries above. Candidate 3 (causal/ordering priority) is retained but flagged as the weakest of the six for a first experiment, for the same later-track-adjacency reason.

**Source or conceptual gaps that must be resolved before selecting the initial 3-4 set:**

1. Resolve whether Candidate 1 (policy-state currency) is operationally distinguishable from `authority_valid` in Runtime Validity's current implementation, or requires new witness infrastructure to become distinguishable.
2. Resolve whether Candidate 6 (evidence/witness coverage sufficiency) is the same dependency as Candidate 2 (witness/authorization freshness) under two source vocabularies, or a genuinely distinct one.
3. Re-read CommitGuard's primary source (arXiv:2607.10487) directly for the formal definitions of Freshness, Causal priority, Effect binding, and Commit eligibility; this file currently records only their names and a general commit-time-authorization framing, not their exact conditions.
4. Decide whether Candidate 3 (causal/ordering priority) belongs in the initial Track A experiment at all, given its structural adjacency to later-track ordering/concurrency concerns, or should be deferred alongside Janicke et al. 2008.
5. Confirm or replace, as a separate and explicit decision (not made here), whether "governance obligation" remains the master term given that none of the six retained candidates are UCON oBligations (B) in the technical sense; this file's existing Terminology Decision Point already flags this as open.
6. Independently verify Ray/Xin DBSec 2004 if it is to be used for anything beyond an unconfirmed cross-reference to the verified Ray 2004 DKE paper.

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

**Research work completed in this checkpoint:** the obligation-source matrix described in "Planned Artifact" was produced (see "Obligation-Source Matrix" and "Matrix Review Before Final Selection" above), applying the prior-mechanism-coverage check from "Planned Evaluation" to every source already recorded in "Verified Prior-Art Sources." Six candidates are retained pending selection, two of them with explicitly unresolved overlaps, one flagged weaker than the others, and six sources or source groups are classified as baseline-only, vocabulary-only, later-track, or pending verification, each with a stated reason.

**Observed experimental result: Not yet evaluated.** There is still no Track A experimental result. This checkpoint produces a research-triage artifact, not an invalidation-mapping finding, a disposition-preservation finding, or any other Track A conclusion. No obligation kind was added to `/decide`, no runtime code changed, and no final obligation set was selected.

## Next Step

Resolve the specific gaps recorded in "Matrix Review Before Final Selection" before selecting the initial 3-4 obligation set: in particular, re-read CommitGuard's primary source for the formal definitions of its four named conditions (this file currently records only their names), and resolve the two flagged overlaps (Candidate 1 against `authority_valid`, and Candidate 6 against Candidate 2). Do not select the final experimental set until those gaps are addressed or explicitly carried forward as accepted open questions.
