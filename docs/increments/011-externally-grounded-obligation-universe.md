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
- Authors: Rui Tang, Qiangqiang Liu, Yichi Zhang, Youwei Yang, Xi Chen, Chen Dong (corrected from "Youwei Wang," recorded in error in an earlier pass of this file, against a direct re-fetch of the arXiv listing during this checkpoint)
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
| 1 | Policy-state currency | MasuGate (Peng & Wu 2026) | retain as candidate, overlap with `authority_valid` unresolved (design decision pending, see analysis below) |
| 2 | Witness/authorization freshness | CommitGuard (Santos-Grueiro 2026) | retain as candidate; source-verified this checkpoint; recommended to absorb Candidate 6's staleness sub-case |
| 3 | Causal/ordering priority | CommitGuard (Santos-Grueiro 2026) | defer to a later Track A experiment (resolved this checkpoint) |
| 4 | Effect/action binding | CommitGuard (Santos-Grueiro 2026) | retain as candidate; source-verified this checkpoint |
| 5 | Target/commit eligibility | CommitGuard (Santos-Grueiro 2026) | retain as candidate; source-verified this checkpoint (source's own framing is "authorizing-path eligibility," slightly narrower than the label) |
| 6 | Evidence/witness coverage sufficiency | SAGE-Fin (Tang et al. 2026) | retain as candidate, narrowed to the absence/type-binding sub-cases; staleness sub-case recommended to fold into Candidate 2 |
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
- **Source mechanism:** one of four named heterogeneous conditions ("Freshness") checked at every protected commit in a durable-effect commit-time authorization. Re-read against the primary source (arXiv HTML) during this checkpoint, Section 3 ("Boundary Checks") and Table 3.
- **Source terminology:** "Freshness," "witness," "commit boundary." Source's own boundary question: "is the witness that still licenses the effect current at commit?"
- **Condition that must hold:** the witness (source examples: "live page, token, approval, or version") that licenses the effect is still current at commit time.
- **Depends on:** a single named witness object (page, token, approval, or version), per Table 3.
- **Invalidating event, per source:** "expiry, DOM mutation, version advance, revocation" (Table 3).
- **Independently checkable, per source:** yes; the four conditions are checked as a set of independent boundary questions, not folded into one another, though the source does not give a symbolic-logic equation. Section 3 states plainly: "An externally consequential action is authorized only when all four checks hold at the boundary."
- **Source-associated mitigation on failure:** "refresh the witness"; Section 6 also describes "pre-execution revalidation" that refreshes relevant state immediately before action execution.
- **Provisional Track A normalized label:** witness/authorization freshness. The label is faithful to the source's own use of "Freshness."
- **Candidate runtime witness:** a timestamp or age value attached to the authorization witness.
- **Candidate invalidating intervention:** let time elapse past the freshness threshold, or administratively expire the witness (mirroring the source's own "expiry" invalidator), without changing the underlying authorization decision itself or removing the witness outright.
- **Evaluation observability:** compare witness age at original decision time against witness age at revalidation time relative to a fixed threshold.
- **Overlap / possible duplicate:** partially resolved this checkpoint against Candidate 6 (SAGE-Fin's coverage debt). See "Freshness vs. coverage debt: source comparison" below for the detailed analysis. Summary: CommitGuard's Freshness corresponds closely to coverage debt's own "stale-witness" sub-case (a single witness aging past a recompute interval), but not to coverage debt's broader absence and type/binding sub-cases. The staleness sub-case of Candidate 6 should likely fold into this candidate; the remainder of Candidate 6 should not.
- **Track A relevance:** CommitGuard is the strongest available full-commit-boundary baseline exemplar: a real, heterogeneous, named multi-condition commit-time decision, exactly the shape Track A's full-reevaluation comparison arm needs. The source confirms, in its own words, that all four conditions are checked every time ("single-condition checks are insufficient because different hazards break different boundary conditions," Section 6.2), with no mechanism shown for selectively skipping or trusting any of the four. Using Freshness as a Track A candidate for selective revalidation would therefore not be replicating an existing selective mechanism; it would be a new application of a condition CommitGuard itself always fully rechecks.
- **Current disposition:** retain as candidate.
- **Unresolved interpretation:** the source gives named invalidators and a mitigation but not a formal threshold-computation rule (e.g., how the freshness interval itself is chosen); that operational detail is not recorded in the source material fetched for this checkpoint and would need a further, narrower read of the source before implementation.

### Candidate 3: Causal/ordering priority

- **Source:** CommitGuard (Santos-Grueiro 2026, arXiv:2607.10487).
- **Source mechanism:** one of the same four named conditions ("Causal priority"), checked at every protected commit. Re-read against the primary source during this checkpoint, Section 3 ("Boundary Checks" and "Why endpoint correctness can diverge") and Table 3.
- **Source terminology:** "Causal priority," "commit boundary." Source's own boundary question: "did all required predecessors complete before the effect, with no unresolved dependency still pending?"
- **Condition that must hold:** all required predecessor steps completed before the effect, with no unresolved dependency still pending.
- **Depends on:** "predecessor completion or barrier token" (Table 3), an inherently multi-step, relational witness, not a single value.
- **Invalidating event, per source:** "callback reorder, missing await, late worker result" (Table 3): all multi-event phenomena describing a violation of expected step ordering, not a single value change.
- **Independently checkable, per source:** yes, as one of the four independent boundary checks; but its own witness (a barrier token or predecessor-completion signal) is intrinsically about the relationship between two or more events, unlike the single-value witnesses the other three conditions use.
- **Source-associated mitigation on failure:** "wait for the predecessor," or replanning to reestablish proper dependency ordering (Section 3).
- **Provisional Track A normalized label:** causal/ordering priority. The label is faithful to the source's "Causal priority" term.
- **Candidate runtime witness:** an event sequence or ordering marker (a barrier token, per the source) associated with the authorization and with candidate intervening events.
- **Candidate invalidating intervention:** insert an intervening event that violates the required ordering between the original decision and the commit (mirroring the source's own "callback reorder" or "late worker result" invalidators).
- **Evaluation observability:** compare recorded ordering markers; requires an explicit barrier-token or sequence mechanism that Runtime Validity's current bounded implementation does not have.
- **Overlap / possible duplicate:** none identified against the other candidates; ordering is a distinct dimension from state-value comparison.
- **Track A relevance:** grounded in the same strong full-commit-boundary baseline as Candidate 2. See "Causal/ordering priority: first-experiment disposition" below for the resolved disposition.
- **Current disposition:** defer to a later Track A experiment (resolved this checkpoint; see below).
- **Unresolved interpretation:** the source's own witness for this condition, a "predecessor completion or barrier token," presupposes some minimal notion of ordered steps or a barrier mechanism. Whether a single-decision, single-intervention experiment can represent that witness without building at least a minimal sequencing mechanism is the open question resolved (as: no, not without added infrastructure) in the disposition analysis below.

### Candidate 4: Effect/action binding

- **Source:** CommitGuard (Santos-Grueiro 2026, arXiv:2607.10487).
- **Source mechanism:** one of the same four named conditions ("Effect binding"), checked at every protected commit. Re-read against the primary source during this checkpoint, Section 3 ("Boundary Checks") and Table 3.
- **Source terminology:** "Effect binding," "binding," "commit boundary." Source's own boundary question: "does the witness still name the same concrete target, version, ticket, page instance, or branch that the effect makes durable?"
- **Condition that must hold:** the witness still names the same concrete target (version, ticket, page instance, or branch) that the effect is about to make durable; the authorization must not be reusable for a substituted target.
- **Depends on:** "target identifier bound to witness" (Table 3), a single identifier-match witness.
- **Invalidating event, per source:** "retarget, repaint, rebinding, branch retarget" (Table 3).
- **Independently checkable, per source:** yes, as one of the four independent boundary checks; a clean identifier-equality question.
- **Source-associated mitigation on failure:** "rebind the target," or "version binding or reservation ties the effect to a concrete version" (Sections 3 and 6).
- **Provisional Track A normalized label:** effect/action binding. Faithful to the source's "Effect binding" term.
- **Candidate runtime witness:** an effect or target identifier recorded at decision time.
- **Candidate invalidating intervention:** substitute a different effect or target identifier at commit time while presenting the same prior decision (mirroring the source's own "retarget" invalidator).
- **Evaluation observability:** compare the effect/target identifier recorded at decision time against the one presented at commit/revalidation time. A clean equality check; no additional infrastructure beyond an identifier field appears to be required.
- **Overlap / possible duplicate:** none identified against the other candidates, contingent on experimental design keeping the substituted target's own eligibility state constant (see the experimental-distinctness table below).
- **Track A relevance:** same full-commit-boundary baseline as Candidates 2 and 3; CommitGuard always rechecks this condition, so a Track A experiment selectively revalidating it (or trusting it while rechecking others) would not replicate an existing selective mechanism.
- **Current disposition:** retain as candidate.
- **Unresolved interpretation:** none material; the source's own definition is specific enough (identifier match against "target, version, ticket, page instance, or branch") to operationalize as recorded here.

### Candidate 5: Target/commit eligibility

- **Source:** CommitGuard (Santos-Grueiro 2026, arXiv:2607.10487).
- **Source mechanism:** one of the same four named conditions ("Commit eligibility"), checked at every protected commit. Re-read against the primary source during this checkpoint, Section 3 ("Boundary Checks") and Table 3.
- **Source terminology:** "Commit eligibility," "commit boundary." Source's own boundary question: "is the authorizing path still live, with no cancellation, revocation, losing branch, or supersession?"
- **Condition that must hold:** the authorizing path is still live at commit time, with no cancellation, revocation, losing branch, or supersession.
- **Depends on:** "live branch, approval epoch, or authorization marker" (Table 3).
- **Invalidating event, per source:** "branch cancellation, losing speculative path, approval loss" (Table 3).
- **Independently checkable, per source:** yes, as one of the four independent boundary checks.
- **Source-associated mitigation on failure:** "refuse the ineligible path," or gating through eligibility recomputation at commit (Sections 3 and 6).
- **Provisional Track A normalized label:** target/commit eligibility. On re-reading, the source's own condition is about the *authorizing path's* liveness (branch/approval-epoch state), not narrowly about a physical target or environment's eligibility; "target/commit eligibility" is retained as a workable label but is a slightly broader gloss than the source's own framing, which is closer to "authorizing-path eligibility." This gap is noted rather than silently normalized away.
- **Candidate runtime witness:** a liveness/eligibility flag for the authorizing path (branch, approval epoch, or authorization marker).
- **Candidate invalidating intervention:** cancel, supersede, or revoke the authorizing path between the prior decision and commit time (mirroring the source's own "branch cancellation" or "approval loss" invalidators), while leaving the target identifier itself unchanged.
- **Evaluation observability:** compare the authorizing-path liveness flag at decision time against its value at revalidation time.
- **Overlap / possible duplicate:** none identified against the other candidates, contingent on experimental design keeping the target identifier constant while only the path's liveness state changes (see the experimental-distinctness table below). Still corresponds loosely to the "Target/environment" entry in Increment 011's own candidate change classes (Source Discipline section), though the source's own framing (authorizing-path liveness) is more about the state of the authorization itself than about a physical target/environment.
- **Track A relevance:** same full-commit-boundary baseline as Candidates 2 through 4.
- **Current disposition:** retain as candidate.
- **Unresolved interpretation:** the "target/environment" gloss noted above under Provisional Track A normalized label; the source's condition is somewhat narrower (path liveness) than a general target/environment-state concept would suggest.

### Candidate 6: Evidence/witness coverage sufficiency

- **Source:** SAGE-Fin (Tang et al. 2026, arXiv:2608.09025).
- **Source mechanism:** "coverage debt," re-read against the primary source (arXiv HTML) during this checkpoint. Section 6.1, Definition 3, gives the formal statement: for active witnesses W_t and validators V_t, the debt set D_t(c_t*) "contains each predicate in W_t^req ∪ V_t^req whose corresponding witness or validator is absent, stale, unpromoted, provenance-invalid, or scope-incompatible." Coverage debt is therefore a **set-level** aggregate over all required predicates for one candidate action, not a single witness's condition.
- **Source terminology:** "coverage debt," "institutional obligation" (source's own term for the required witness/validator predicates; verified in this file's Terminology Decision Point to denote a state condition, not a UCON oBligation-B duty), "adapter-bound candidate," "exact-artifact receipt" (a separate mechanism, defined in Section 6.3/Definition 8, that binds a candidate to an exact-artifact hash to prevent cross-artifact reuse; distinct from coverage debt itself, not a synonym for it).
- **Condition that must hold:** every witness/validator required for the candidate action is present, current, correctly typed, and provenance-valid for the consuming adapter; the debt set is empty.
- **Named sub-components, per the source (Section 5.3 examples):** (a) **absence**: "a live-trade candidate that has a fresh price witness but no slippage-assumption witness has *partial* coverage debt"; (b) **staleness**: a witness "whose user-tier witness is older than the tier-recompute interval has *stale-witness* coverage debt"; (c) **type/binding failure**: "unpromoted, provenance-invalid, or scope-incompatible" witnesses. These are explicitly three distinct failure modes within one umbrella concept, not three names for the same thing.
- **Provisional Track A normalized label:** evidence/witness coverage sufficiency. On re-reading, this label is faithful to the source's broad concept but risks obscuring that the source itself distinguishes three sub-components with different experimental shapes; see the comparison below.
- **Candidate runtime witness:** a per-required-witness presence/validity/type-match flag, for the required-witness set of one candidate action.
- **Candidate invalidating intervention:** remove a required witness entirely (absence), or invalidate its type/provenance/scope match (type/binding), after the prior decision, leaving other witnesses' presence and freshness untouched. (Aging a witness past a threshold without removing it is the staleness sub-case; see "Freshness vs. coverage debt: source comparison" below for why that sub-case is treated separately.)
- **Evaluation observability:** compare the coverage state (which required witnesses are present and correctly typed) at decision time against revalidation time, scoped to the absence and type/binding sub-cases.
- **Overlap / possible duplicate:** resolved this checkpoint, in part. See "Freshness vs. coverage debt: source comparison" immediately below. Summary: coverage debt's staleness sub-case is the same underlying dependency as Candidate 2 (CommitGuard Freshness) and should fold into it; coverage debt's absence and type/binding sub-cases are not covered by Freshness and remain a distinct, narrower version of this candidate.
- **Track A relevance:** a per-candidate, typed staleness/coverage-tracking concept in one domain (financial market agents); does not itself describe a controlled-intervention-to-affected-dependency mapping or a full-versus-selective reevaluation comparison. An adjacent single-domain instantiation, not a mechanism to measure Track A against.
- **Current disposition:** retain as candidate, narrowed to the absence and type/binding sub-cases; the staleness sub-case is recommended to fold into Candidate 2 rather than remain here (see comparison below). This narrowing is a research-triage recommendation from this checkpoint, not a final selection.
- **Unresolved interpretation:** whether "absence" and "type/binding failure" should themselves remain one candidate or split into two is not resolved by this checkpoint; the source treats both as coverage-debt sub-components without further internal distinction beyond the examples quoted above.

### Freshness vs. coverage debt: source comparison

This subsection resolves research task 2 (Freshness vs. coverage debt) using the primary-source text quoted above for both CommitGuard and SAGE-Fin. This is a research-triage conclusion about experimental design, not a Track A experimental result.

| | CommitGuard Freshness | SAGE-Fin coverage debt |
|---|---|---|
| Object being checked | one named witness (page, token, approval, or version) | a set of required predicates (W_t^req ∪ V_t^req) for one candidate action |
| Cardinality | single witness | set (potentially many witnesses/validators) |
| Temporal component | yes: witness age vs. a freshness threshold, invalidated by "expiry... version advance" | yes, but only in one of three named sub-components ("stale-witness coverage debt," a witness "older than the tier-recompute interval") |
| Missing-evidence component | not named as such; the closest source invalidator is "revocation," which removes a witness's validity rather than its presence | yes, named explicitly as "absence" / "partial coverage debt" (a required witness never obtained) |
| Typing/binding component | not part of Freshness; CommitGuard checks this separately as its own condition ("Effect binding") | yes, named explicitly ("unpromoted, provenance-invalid, or scope-incompatible") |
| Invalidation event | expiry, DOM mutation, version advance, revocation (source, Table 3) | witness never produced (absence); age past recompute interval (staleness); provenance/scope mismatch (binding) |
| Potential runtime witness | one witness's age/timestamp | membership and per-member status (present/valid/typed) across a required-witness set |
| Experimentally distinguishable from each other? | staleness sub-case: **no**, same experimental shape as Freshness (age one witness past a threshold, holding presence and typing fixed) | absence and type/binding sub-cases: **yes**, distinguishable from Freshness (remove a witness entirely, or break its type/provenance match, while holding age fixed) |

**Provisional disposition: hierarchical relationship, not a clean merge and not a clean separation.** CommitGuard's Freshness corresponds to exactly one of coverage debt's three named sub-components (staleness); the other two sub-components (absence, type/binding) are not covered by Freshness and are not evidenced as equivalent to any other single candidate in this matrix. The practical recommendation for a later selection step: fold the staleness sub-case of Candidate 6 into Candidate 2 (they are the same dependency under two source vocabularies), and retain a narrower Candidate 6 covering only the absence and type/binding sub-cases, distinct from Candidate 2. This is not forced by the shared word "stale": it follows from the source definitions themselves, which name staleness as one sub-case among three, and from the fact that an intervention aging one witness (holding presence and typing fixed) is not experimentally distinguishable between the two papers' framings, while an intervention removing or mistyping a witness (holding age fixed) is.

### Causal/ordering priority: first-experiment disposition

This subsection resolves research task 4, using the primary-source detail on Candidate 3 established above.

Applying the stated criteria:

- **Can one deterministic controlled intervention invalidate it?** Weakly. The source's own invalidators ("callback reorder, missing await, late worker result") are all relational, describing the order of two or more events, not a single value change. A controlled intervention would need to construct at least two steps and violate their required order, which is a qualitatively different intervention shape than flipping a Boolean or changing one identifier.
- **Can the intervention be represented without building a concurrency system?** Only partially. A minimal, artificial two-step ordering could be simulated in a test harness without a full concurrency system, but the source's own witness, a "predecessor completion or barrier token," presupposes some sequencing or barrier mechanism, which Runtime Validity's current bounded implementation does not have.
- **Can its witness be observed without distributed ordering infrastructure?** Not with the current implementation; a barrier-token or sequence witness would need to be added first.
- **Does it test the central stale-justification question?** Only indirectly. The central Track A question is whether a justification that was valid earlier remains valid at the point of execution given a runtime intervention. Causal priority instead asks whether execution steps occurred in the required order, an execution-integrity property, adjacent to but not the same question.
- **Does it primarily introduce event-ordering/concurrency semantics that are a separate research problem?** Yes. Its verified invalidators (reordering, missing await, late results) place it structurally closer to the already-classified later-track concerns (Janicke et al. 2008's inter-process dependency graph, Katt et al. 2008's any-attribute-change reevaluation) than to the other five candidates' single-value witnesses.

**Provisional disposition: defer to a later Track A experiment.** Retaining Candidate 3 in the first experiment would require building sequencing/barrier infrastructure the current implementation lacks, and would risk absorbing a concurrency/ordering question under the Track A name rather than testing the primary stale-justification question directly. It is not excluded from Track A altogether (it is a real, source-grounded, heterogeneous condition, unlike the sources classified as vocabulary-only or later-track-only below), but it is not retained as viable for the *first* experiment. This is a research-triage judgment, not a claim that ordering is unimportant to governed execution generally.

### Policy-state currency vs. `authority_valid`: conceptual-distinctness analysis

This subsection resolves research task 3. No code changes were made or considered; this is a design-level analysis only.

Two controlled interventions are useful to distinguish:

- **Intervention A:** a subject's underlying authority fact changes (for example, a credential or delegation is revoked) while the policy content that interprets that fact is unchanged.
- **Intervention B:** the policy content/version that determines what counts as valid authority changes, while the subject's underlying authority facts are unchanged.

**Conceptually distinct in source-grounded models:** yes. MasuGate treats policy state as an independently versioned, mutable object with its own read/write scopes, separate from the entities the policy governs. Ray 2004 separately models "policy objects" (subject-set, target-set, rights-set) as distinct from the runtime data transactions execute against. Park, Zhang, Sandhu 2004's UCON taxonomy treats subject/object attribute mutability as a distinct concern from the policy rules that interpret those attributes. Across these source-grounded models, "the policy changed" and "the subject's authority fact changed" are different kinds of event.

**Currently distinguishable in Runtime Validity: no.** The current bounded implementation represents authority as a single opaque Boolean, `authority_valid`, with no field recording which policy rule or which subject-level fact produced that value. Intervention A and Intervention B are both observable, today, only as the same signal: `authority_valid` flips (or does not). There is no way, with the current schema, to determine after the fact whether a flip was caused by a policy-content change or a subject-fact change.

**Minimum future witness that would separate them:** a policy-fragment identifier, version, or hash, recorded alongside `authority_valid` at decision time and compared again at revalidation time, mirroring MasuGate's policy-read-scope concept. With such a field, Intervention B would change the recorded policy-fragment version while Intervention A would leave it unchanged (even if `authority_valid` itself also changed under Intervention A, depending on how the subject-level determination is wired). This field does not exist today and is not added by this checkpoint.

**What this checkpoint does not conclude:** that policy-state currency and `authority_valid` are necessarily one dependency, merely because the current Boolean cannot separate them. The inseparability observed today is an implementation limitation of the bounded reference implementation, not evidence about the underlying conceptual structure. Whether to add the witness needed to separate them, and whether doing so is worth the added scope, is left open for the final-selection step.

**Provisional disposition: unresolved, pending a design decision on witness investment.** Policy-state currency remains a retained candidate (see Candidate 1 above), with its overlap against `authority_valid` explicitly flagged rather than assumed resolved in either direction.

### Experimental-distinctness table

This table addresses whether an intervention can be defined for each of Candidates 1, 2, 4, 5, and 6 that changes that candidate while holding the others constant. It is a design-feasibility check, not an executed experiment.

| Candidate | Controlled intervention | Other candidates held fixed | Observable witness | Potential confound | Experimentally distinguishable? |
|---|---|---|---|---|---|
| 1. Policy-state currency | Version-bump the specific policy fragment read by the decision | `authority_valid` subject-level fact; witness freshness; effect binding; target/path eligibility | Policy-fragment version/hash (does not exist today) | Without a real policy-version witness, a "policy-only" intervention can currently only be simulated by also flipping `authority_valid`, confounding it with a direct authority-state change | Unresolved: no with current implementation; yes if a policy-version witness is added |
| 2. Witness/authorization freshness | Age one witness past its freshness threshold (or trigger source-style "expiry") | Witness presence (not removed); effect binding; target/path eligibility; causal order; policy content | Witness age/timestamp vs. threshold | If "expiry" is implemented as outright removal rather than marking-stale-while-present, it collapses into Candidate 6's absence sub-case | Yes, if the intervention ages the witness without removing it |
| 4. Effect/action binding | Substitute a different target/effect identifier at commit time, keeping the original witness | Witness freshness; causal order; policy content; the substituted target's own eligibility | Effect/target identifier match | If the substitute target is itself ineligible, this collapses into Candidate 5 | Yes, if the substitute target is chosen to remain independently eligible |
| 5. Target/commit eligibility | Cancel, supersede, or revoke the authorizing path, keeping the same target identifier | Effect binding (same identifier); witness freshness; causal order; policy content | Authorizing-path liveness flag | If revoking the path also changes the target identifier itself, this collapses into Candidate 4 | Yes, if the target identifier is held constant while only path liveness changes |
| 6. Evidence/witness coverage sufficiency (narrowed to absence/type-binding) | Remove a required witness entirely, or break its type/provenance/scope match | Presence and age of the remaining, untouched required witnesses; effect binding; target/path eligibility; causal order | Presence/type-match flags across the required-witness set | If the intervention ages rather than removes or mistypes a witness, it collapses into Candidate 2 (see the Freshness-vs-coverage-debt comparison above) | Yes, if scoped to removal or type/provenance mismatch rather than aging |

### Baseline-only and excluded sources (not retained as obligation candidates)

- **Whole-transaction policy compatibility (Ray 2004, DKE).** Verified mechanism: a statically precomputed commute set determines whether a data transaction may continue under its original authorization when a concurrent policy-update transaction of a known type is in progress; otherwise the transaction is aborted. This is a proven instance of reuse-instead-of-recompute under a known class of change, at whole-transaction granularity. It is treated as a strong baseline for the general claim that formal compatibility reasoning permits reuse under classified change, not as a source of a specific heterogeneous per-obligation candidate, because the source does not decompose one transaction's authorization into multiple independently reevaluable conditions. Reason against inclusion as a candidate: operates at a different granularity than Track A's proposed intra-decision, per-obligation mechanism; the source mechanism already fully resolves reuse-versus-abort at commit time for its own granularity, leaving no distinct sub-condition for Track A to add.
- **Any-attribute-change ongoing reevaluation (Katt et al. 2008).** Verified mechanism: any subject, object, or environment attribute change triggers a full `ongoingCheck` reevaluation of the applicable rule combination for the session. This is treated as a UCON-lineage baseline for "full reevaluation triggered by any change," directly relevant to Track A's full-commit-boundary comparison arm, but it supplies no mapping from a specific attribute change to a specific invalidated predicate, and no reuse of prior partial results. Reason against inclusion as a candidate: the source's own mechanism recomputes everything on any change; it does not identify a distinct dependency Track A could selectively revalidate. Its trusted/non-trusted obligation distinction is noted as useful adjacent vocabulary, not adopted as a candidate here.
- **Inter-process concurrency dependency (Janicke et al. 2008).** Verified mechanism: a static dependency graph over shared mutable policy-rule state determines which usage processes must be mutually excluded versus may run concurrently. Reason against inclusion as a candidate: this is an inter-process synchronization relation, not an intra-decision relation over one decision's own heterogeneous conditions. It belongs primarily to a later concurrency/ordering track, per this increment's own Exclusion Criteria and Scope.
- **Attribute mutability taxonomy (Park, Zhang, Sandhu 2004).** Verified mechanism: a formal taxonomy of why and how UCON attributes change (mutability, liveness, five variation types), with no enforcement mechanism, no dependency concept, and no selective-reevaluation mechanism. Reason against inclusion as a candidate: source is vocabulary-only; it classifies reasons attributes change rather than supplying a condition Track A could revalidate. Retained as background vocabulary for describing intervention types, not as an obligation source.
- **Selective recomputation technique family (Doyle 1979; Forgy 1982; Gupta, Mumick, Subrahmanian 1993; Binder; SecPAL; Margrave).** These establish that dependency-tracked selective recomputation is a decades-old, mechanically mature computational pattern, with an established (if not explicitly combined) substrate inside the authorization domain. Reason against inclusion as candidates: none of these are authorization-decision-revalidation mechanisms in their own right; they are general-purpose technique precedent for how a Track A implementation might eventually be built, not sources of governance conditions to revalidate.
- **Whole-transaction policy compatibility, DBSec variant (Ray/Xin DBSec 2004).** Bibliographically identified (title, authors, year, DOI), mechanism not independently verified for this matrix. Its full text has not been read in this review. It is not used as the sole or partial basis for any candidate above, and its relevance is assumed, cautiously, to track the verified Ray 2004 DKE paper only insofar as that assumption is explicitly flagged here as unconfirmed.

## Matrix Review Before Final Selection

This is a checkpoint review, not a selection. No final 3-4 obligation set is chosen in this increment.

**Distinct candidate dependencies remaining after obvious merges.** Six candidates are retained (Candidates 1 through 6 above). This checkpoint resolved the CommitGuard-side definitions and the Freshness/coverage-debt overlap (Candidate 6's staleness sub-case is recommended to fold into Candidate 2), leaving the Candidate 1/`authority_valid` overlap as the one still fully unresolved. If Candidate 1 resolves toward merging with `authority_valid` and Candidate 6 is narrowed as recommended, five operationally distinct candidates remain (2/6-staleness merged as Candidate 2, Candidate 6 narrowed to absence/type-binding, 3, 4, 5). If Candidate 1 is kept as a separate policy-content dimension, six remain, with Candidate 3 already provisionally deferred rather than counted toward a first experiment.

**Strongest candidates for experimental manipulation.** Candidates 4 (effect/action binding) and 5 (target/commit eligibility) remain strongest for a first controlled experiment, now with source-verified definitions: each has a clean, single-value witness, a clearly stated invalidating intervention that does not depend on inventing new infrastructure, and (per the experimental-distinctness table above) a known, avoidable confound with the other. Candidate 2 (witness/authorization freshness) is also strong, now with its overlap against Candidate 6 resolved in the narrow sense that its own staleness-based experimental design is distinct from Candidate 6's narrowed absence/type-binding design.

**Ambiguous candidates.** Candidate 1 (policy-state currency) remains ambiguous: conceptually distinct from `authority_valid` in source-grounded models, but not currently distinguishable in Runtime Validity's implementation without new witness infrastructure (see the conceptual-distinctness analysis above). This is now a design-investment question (add the witness, or do not), not an unexamined gap.

**Baseline-only.** Ray 2004 (DKE), Katt et al. 2008, and the classical mechanism ancestry group remain baseline-only: they constrain what Track A can credibly claim as novel and supply the strong-baseline shape (especially CommitGuard, now source-verified as the leading full-commit-boundary baseline exemplar and as the source of Candidates 2 through 5), but are not themselves candidate obligations.

**Deferred / excluded.** Janicke et al. 2008 (inter-process concurrency, later-track concern) and Park, Zhang, Sandhu 2004 (vocabulary only) remain excluded from candidacy for the reasons stated in their entries above. Candidate 3 (causal/ordering priority) is now provisionally deferred to a later Track A experiment rather than merely flagged as weaker (see the first-experiment disposition analysis above); it remains a real, source-grounded candidate for a future experiment, not excluded from Track A altogether.

### Source-resolution checkpoint

This subsection answers the questions posed for this checkpoint directly.

- **Which candidate definitions are now source-verified.** All four of CommitGuard's named conditions (Candidates 2, 3, 4, 5) were re-read against the primary source (arXiv:2607.10487, Section 3 and Table 3) during this checkpoint, including their dependencies, invalidating events, and source-associated mitigations, quoted above in each candidate's entry. SAGE-Fin's "coverage debt" (Candidate 6) was re-read against the primary source (arXiv:2608.09025, Section 6.1 Definition 3 and Section 5.3), including its three named sub-components. A bibliographic error was also found and corrected during this re-verification: SAGE-Fin's fourth author is Youwei Yang, not "Youwei Wang" as an earlier pass of this file recorded.
- **Which overlaps were resolved.** The Candidate 2/Candidate 6 overlap is resolved to a hierarchical relationship: coverage debt's staleness sub-component is the same dependency as Freshness; its absence and type/binding sub-components are not, and remain a narrower, distinct version of Candidate 6. The Candidate 3 first-experiment question is resolved: defer, for the reasons in the disposition analysis above.
- **Which remain unresolved.** The Candidate 1/`authority_valid` overlap remains unresolved; it depends on a design decision (whether to add a policy-version witness) rather than further source reading, and that decision is explicitly not made by this checkpoint. Whether "absence" and "type/binding failure" (Candidate 6's two remaining sub-components) should themselves stay merged or split further is also unresolved. The master-term question ("governance obligation" versus "decision dependency" or another term) remains open, per the existing Terminology Decision Point; this checkpoint's findings, if anything, strengthen the case that none of the retained candidates are UCON oBligations (B), but no rename is made here.
- **Which candidates are experimentally distinguishable.** Per the experimental-distinctness table above: Candidates 2, 4, and 5 are distinguishable from each other and from Candidate 6 (narrowed) with careful intervention design that avoids the identified confounds. Candidate 1 is distinguishable from `authority_valid` only if new witness infrastructure is added; today it is not. Candidate 3 is not cleanly distinguishable without sequencing/barrier infrastructure the current implementation lacks.
- **Which should likely be deferred.** Candidate 3 (causal/ordering priority), for the reasons above. Whether Candidate 1 should be deferred pending witness infrastructure, or included with the infrastructure added as part of the same future step, is left to the final-selection step rather than decided here.
- **Whether enough evidence now exists for a separate final-selection decision.** Closer than before this checkpoint, but not yet complete. The four candidates with no remaining source-definition gap and a clear experimental design (2, 4, 5, and the narrowed 6) could plausibly support a final-selection decision on their own. The remaining open item is Candidate 1, where the blocker is a design choice (add a policy-version witness or not) rather than a source-reading gap; that decision, not further literature review, is what a final-selection step would need to make.

**Source or conceptual gaps that must still be resolved before selecting the initial 3-4 set:**

1. Decide whether to add a policy-fragment version/hash witness to distinguish Candidate 1 (policy-state currency) from `authority_valid`, or to treat Candidate 1 as out of scope for the first experiment absent that witness.
2. Decide whether Candidate 6's two remaining sub-components (absence, type/binding) should stay combined or split into two candidates.
3. Confirm or replace, as a separate and explicit decision (not made here), whether "governance obligation" remains the master term given that none of the six retained candidates are UCON oBligations (B) in the technical sense; this file's existing Terminology Decision Point already flags this as open.
4. Independently verify Ray/Xin DBSec 2004 if it is to be used for anything beyond an unconfirmed cross-reference to the verified Ray 2004 DKE paper.
5. If Candidate 3 is ever revisited for inclusion, define a minimal sequencing/barrier witness first; this checkpoint does not attempt that design.

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

**Research work completed in this checkpoint (first pass, matrix construction):** the obligation-source matrix described in "Planned Artifact" was produced, applying the prior-mechanism-coverage check from "Planned Evaluation" to every source already recorded in "Verified Prior-Art Sources." Six candidates were retained pending selection, two flagged with unresolved overlaps, one flagged weaker than the others.

**Research analysis result (this checkpoint, source-resolution pass):** re-read CommitGuard (arXiv:2607.10487) and SAGE-Fin (arXiv:2608.09025) directly against their primary-source text (not summaries) to resolve four specific open questions:

1. CommitGuard's four named conditions (Freshness, Causal priority, Effect binding, Commit eligibility) now have source-verified dependencies, invalidating events, and mitigations, recorded in each candidate's entry above. A bibliographic error (SAGE-Fin's fourth author name) was found and corrected during this re-verification.
2. Freshness (CommitGuard) and coverage debt (SAGE-Fin) are resolved to a hierarchical relationship, not a clean merge or a clean separation: coverage debt's staleness sub-component is the same dependency as Freshness; its absence and type/binding sub-components are not.
3. Policy-state currency and `authority_valid` are conceptually distinct in source-grounded models but not currently distinguishable in Runtime Validity's implementation without new witness infrastructure that does not exist today; this remains a design-investment decision, not resolved by source reading alone.
4. Causal/ordering priority is provisionally judged to defer to a later Track A experiment, given its reliance on relational, multi-event witnesses (a "predecessor completion or barrier token") that the current bounded implementation has no infrastructure to represent.

See "Matrix Review Before Final Selection" and its "Source-resolution checkpoint" subsection above for the full reasoning and the experimental-distinctness table.

**Observed experimental result: Not yet evaluated.** There is still no Track A experimental result. This checkpoint produces research-triage and source-verification findings, not an invalidation-mapping finding, a disposition-preservation finding, or any other Track A conclusion. No obligation kind was added to `/decide`, no runtime code changed, and no final obligation set was selected.

## Next Step

The remaining gaps before selecting the initial 3-4 obligation set are now design decisions rather than source-reading gaps: (1) whether to add a policy-fragment version witness to make Candidate 1 distinguishable from `authority_valid`, and (2) whether Candidate 6's absence and type/binding sub-components should stay combined or split. A separate final-selection step can be taken once those two decisions are made; it does not require further literature review of the sources already reviewed. Independent verification of Ray/Xin DBSec 2004 remains outstanding if that source is ever used for more than an unconfirmed cross-reference. If Candidate 3 is revisited later, a minimal sequencing/barrier witness would need to be designed first.
