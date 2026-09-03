# Increment 012: Track A Research Alignment

Status: Complete

## Objective

Make the repository's public research framing (`README.md`) accurately state the controlling Track A research question, the priority ordering among its parts, and which parts of that question the current implementation (Increments 001-010) and the in-progress prior-art work (Increment 011) do and do not evaluate.

The uncertainty being reduced is:

> Does the current README allow a reader to correctly distinguish the Track A research question from the bounded engineering mechanisms that exist so far, or does it risk being read as though those mechanisms already answer that question?

This increment introduces no new experimental result and no new runtime capability.

## Starting State

Read in full before making any change: `README.md`, Increments 002, 004, 008, 009, 010, 011, `src/runtime_validity/api.py`, `tests/test_api.py`, `pyproject.toml`, `.github/workflows/test.yml`.

Findings from that reading:

- The implementation boundaries documented in README are already strong and carefully hedged (explicit MATCH/MISMATCH/NOT_EVALUATED semantics, explicit non-claims for transition evidence, an explicit "Current Limitations" section).
- README's opening research framing is generic: "runtime validity and revalidation of prior governance decisions before consequential action." This is not the actual controlling Track A research question and could be read as though the existing authority-change mechanism already constitutes that question.
- README's "Next Research Question" section (decision-to-state binding) is presented as "the next candidate experiment" without being explicitly subordinated to a stated primary Track A question, risking the appearance that binding is the central open question rather than an enabling one.
- README does not mention Increment 011 at all. Increment 011 exists (committed at `444b2df`) as an in-progress, uncompleted prior-art literature review with `Observed Result: Not yet evaluated`.
- README's test count ("20 passed") is stale: the actual current suite is 23 tests (verified by running `python -m pytest -v` before this increment's edits; the additional 3 tests cover a guarded experimental authority-control HTTP endpoint added after the "20 passed" text was last written, in commit `f1a9d5e`).
- README presents `revalidation_mode="none"` primarily as a baseline contrast, which is appropriate for what Increments 001-010 actually tested, but does not yet distinguish that from the stronger baseline (full commit-boundary reevaluation) that the eventual Track A obligation-scoped-revalidation study will need to compare against.

## Scope

Documentation and research-framing alignment only, in `README.md`, plus this increment record. No implementation, test, or dependency-lock file changes.

Specifically:

- State the controlling Track A research question substantially as specified, with an explicit primary/secondary/tertiary priority ordering.
- Add a section relating the current implementation (001-010) and in-progress Increment 011 to that research question, including an explicit list of what has not yet been evaluated.
- Correct the baseline framing so `none` is not presented as the strong Track A comparison baseline.
- Mention Increment 011 accurately: in progress, no final obligation set selected, no evaluated result.
- Re-subordinate the decision-to-state-binding "Next Research Question" to the primary invalidation-mapping question rather than letting it read as a replacement.
- Correct the stale test count and coverage list.
- Preserve existing setup, API usage, record/transition retrieval, CI, project-structure, and limitations documentation.

## Non-Goals

This increment does not:

- add a new obligation kind or change `/decide`;
- implement obligation-scoped or selective revalidation;
- implement intervention-to-obligation mapping;
- run or fabricate a new experiment or evaluation result;
- modify, complete, renumber, or reinterpret Increment 011;
- modify `src/runtime_validity/api.py` or `tests/test_api.py`;
- modify or stage `uv.lock`;
- claim external literature novelty or completeness (that is Increment 011's concern, not this one's);
- perform a new implementation audit of the experimental authority-control endpoint beyond correcting the test count and coverage list that already describe it.

## Assumptions

- The repository's own increment-numbering discipline (one file per number under `docs/increments/`) should be preserved; Increment 011 is not renumbered or touched.
- "Observed" results in this record must reflect commands actually run in this session, not commands merely planned.
- The Track A research question, priority ordering, and terminology given in the task instructions are the authoritative statement to record; this increment does not originate new research content, it aligns documentation to an already-decided framing.

## Controlling Research Question

> Given a prior decision justification composed of heterogeneous governance obligations, which controlled runtime interventions invalidate which obligations, and under what conditions does obligation-scoped revalidation preserve the same policy-expected disposition as full commit-boundary reevaluation with lower revalidation work?

Priority ordering:

1. Primary: intervention-to-obligation invalidation mapping.
2. Secondary: disposition preservation relative to full commit-boundary reevaluation.
3. Tertiary, conditional on (2): revalidation work and latency.

## Research Baselines

- Current implemented comparison (Increments 001-010): `revalidation_mode="none"` (NOT_EVALUATED/PROCEED) vs `revalidation_mode="full"` (MATCH/PROCEED or MISMATCH/HOLD) for the single `authority_valid` obligation. Useful for demonstrating non-evaluation versus reevaluation; not the strong Track A baseline.
- Planned Track A baseline: full commit-boundary reevaluation of all obligations in a prior decision, compared against obligation-scoped revalidation, with policy-expected disposition as the equivalence criterion, and revalidation work/latency compared only after disposition equivalence is established. Obligation-scoped revalidation does not exist in this repository yet.

## Planned Documentation Changes

- `README.md`: opening description and "Relationship to Governed Execution" (future-scope the "candidate component" language); new "Track A Research Question" section with priority ordering; new "Relationship of the Current Implementation to the Track A Research Question" section with a per-increment mapping table (001-011) and an explicit not-yet-evaluated list; corrected baseline language; corrected test count and coverage list in "Run Tests"; "Current Increment Progression" updated to list Increment 011 as in progress; "Next Research Question" re-subordinated to the primary question; light cross-references from "Research Position" and "Current Limitations" to avoid duplicating the same limitations in more than two places.
- This file, updated with observed results after the edits and checks are complete.

## Planned Checks

- `python -m pytest -v` before editing (starting state) and after editing (regression check) — expected unchanged, since no test or implementation file is modified.
- `git diff --check` after staging.
- Manual review of the final `README.md` for the failure criteria listed below and for the specific terms: Track A, research question, heterogeneous, obligation-scoped, selective revalidation, full commit-boundary, none, invalidation, disposition, latency, work, transition, binding, Governed Execution Runtime, complete, validated, proof, proven.
- Confirmation that Increment 011's file is byte-for-byte unchanged and that `uv.lock` remains untracked.

These are planned checks. They are recorded as observed only in the Observed Result section below, after they are actually run.

## Failure Criteria

This increment is unsuccessful if the final `README.md`:

- implies Increments 001-011 evaluate the full Track A question;
- implies Increment 011 is complete;
- implies a heterogeneous obligation universe has been selected;
- claims scoped or selective revalidation is implemented;
- uses `none` as the strong Track A baseline;
- makes latency or revalidation work the primary Track A question;
- presents transition evidence as independent evidence;
- makes decision-to-state binding the replacement Track A question;
- promotes candidate change classes or candidate substrate dimensions to a validated taxonomy;
- treats the pytest suite result as independent validation or a research conclusion;
- implies a composed Governed Execution Runtime currently exists;
- broadens Runtime Validity into a claim of general runtime-governance validation.

It is also unsuccessful if Increment 011 is modified, renumbered, or reinterpreted, or if `uv.lock` is staged, deleted, or modified.

## Observed Result

`python -m pytest -v` before any edit in this increment: **23 passed** (not the 20 the README previously stated; the difference is 3 tests for the guarded experimental authority-control endpoint added in commit `f1a9d5e`, after README's test-count text was last written).

`README.md` was then edited per the Planned Documentation Changes above. After editing:

- `python -m pytest -v`: **23 passed in 0.21s**, unchanged from the starting count. No implementation or test file was modified in this increment.
- `git diff --check`: clean (no output, exit 0).
- `git diff HEAD -- docs/increments/011-externally-grounded-obligation-universe.md`: empty diff, confirming Increment 011's file is byte-for-byte unchanged.
- `git status --short uv.lock`: still reported as `??` (untracked); not staged, not modified, not deleted.
- Manual grep review of the final `README.md` for: Track A, research question, heterogeneous, obligation-scoped, selective revalidation, full commit-boundary, none, invalidation, disposition, latency, work, transition, binding, Governed Execution Runtime, complete, validated, proof, proven. Every occurrence reviewed; none violates the failure criteria above (no claim that a heterogeneous obligation universe, obligation-scoped revalidation, or a composed Governed Execution Runtime exists; `none` is not presented as the strong baseline; latency/work/transition evidence/binding are each explicitly subordinated to the primary and secondary research questions; Increment 011 is described only as in-progress with no evaluated result).
- Markdown link anchors added (`#track-a-research-question`, `#relationship-of-the-current-implementation-to-the-track-a-research-question`) were checked against the actual heading list in the file and resolve correctly.

## Claim Classification

- The Track A research question itself: **Definition**, restated from the controlling framing, not derived from this increment's own analysis.
- "Increments 001-010 implement bounded prerequisites and one authority-change experimental case, and do not evaluate the full Track A question": **Engineering observation**, supported by direct reading of the increment records and the current source.
- The corrected test count (23 passed): **Internal test result** for this commit, not independent validation.
- "Increment 011 is in-progress prior-art research with no evaluated result": **Engineering observation** about the current repository state, not a claim about Increment 011's eventual conclusions.
- The priority ordering (primary/secondary/tertiary) and the strong-baseline distinction: **Design/research-planning statements**, carried into this repository from the controlling research framing, not new findings produced by this increment.
- Nothing in this increment is a **Research conclusion** about Track A itself: no invalidation mapping, no disposition-preservation result, and no obligation universe exists yet to draw a conclusion from.

## Threats to Validity

- This increment is a documentation change; its main risk is prose imprecision (accidentally overstating or understating what is implemented) rather than an experimental confound.
- The corrected test count is accurate only as of this commit; future increments can change it again, and README should continue to be re-verified against `python -m pytest -v` rather than trusted from memory.
- Restating the controlling Track A research question here does not itself validate that the question is well-posed or answerable; that remains open research work.

## Reproducibility Notes

- Test count and pass/fail state can be reproduced with `python -m pytest -v` from a clean checkout of the commit this increment lands on, using the project's declared dependencies (`python -m pip install -e ".[dev]"`).
- `git diff --check` reproduces the whitespace/line-ending check performed before commit.
- No new fixtures, environment variables, or external services are introduced by this increment.

## Artifacts

- `README.md` (modified).
- This file, `docs/increments/012-track-a-research-alignment.md`.
- No code, test, or dependency-lock artifacts.

## Final Commit

Recorded after commit: see the repository's `main` branch history for the commit introducing this increment.
