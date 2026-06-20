<!--
Sync Impact Report
==================
Version change: TEMPLATE (unversioned) → 1.0.0
Bump rationale: Initial ratification of a concrete constitution from the template.

Principles defined:
  - I. Ship Fast, Iterate Later
  - II. Prototype Mindset (YAGNI)
  - III. Testing Is Optional
  - IV. Working Software Over Process
  - V. Minimal Dependencies & Simplicity

Added sections:
  - Prototype Constraints
  - Development Workflow
  - Governance

Removed sections: none (all template placeholders resolved)

Templates requiring updates:
  - ✅ .specify/templates/plan-template.md (Constitution Check is generic; aligns — no edit needed)
  - ✅ .specify/templates/spec-template.md (testing references are manual/acceptance-based — compatible)
  - ✅ .specify/templates/tasks-template.md (tests already marked OPTIONAL — fully aligned)
  - ✅ .specify/templates/checklist-template.md (no principle-specific content — no edit needed)

Follow-up TODOs: none
-->

# Pagination Constitution
<!-- A rapid-prototyping project. Speed of iteration is the primary value. -->

## Core Principles

### I. Ship Fast, Iterate Later

Speed of delivery is the highest priority. Code MUST be written to get a
working result in front of someone as quickly as possible. Perfect structure,
exhaustive edge-case handling, and premature abstractions are explicitly
deprioritized. When a choice exists between "correct but slow to build" and
"good enough and fast to build", the fast option MUST be chosen unless it
creates an irreversible problem.

**Rationale**: This is a prototype. Learning from a running artifact is worth
more than polishing code that may be discarded.

### II. Prototype Mindset (YAGNI)

Build only what is needed for the current goal. Features, configuration knobs,
and generalizations MUST NOT be added speculatively ("You Aren't Gonna Need
It"). Hardcoding values, inlining logic, and taking shortcuts are acceptable
when they accelerate progress. Code MAY be deleted or rewritten freely.

**Rationale**: Every line written for an imagined future need is time taken
from validating the present idea.

### III. Testing Is Optional

Unit tests are NOT required. Automated test suites, coverage targets, and
test-first (TDD) workflows are explicitly OPTIONAL and SHOULD be skipped unless
a specific bug or behavior is hard to verify by hand. Manual/visual
verification that the feature works is sufficient to consider a task done.

**Rationale**: For a prototype, the cost of writing and maintaining tests
generally exceeds their value; behavior changes too rapidly for tests to pay
off.

### IV. Working Software Over Process

A running, demonstrable result is the definition of done. There is no mandatory
review gate, sign-off ceremony, or documentation requirement before code is
considered complete. The question "Does it work when I run it?" MUST be
answerable with "yes" before a task is closed.

**Rationale**: Process exists to protect long-lived systems; a prototype
optimizes for the shortest path to a working demo.

### V. Minimal Dependencies & Simplicity

Prefer the simplest approach that works. New third-party dependencies SHOULD be
added only when they clearly save more time than they cost to integrate. Avoid
heavy frameworks, build pipelines, or infrastructure that slow down the
edit-run loop.

**Rationale**: Every dependency and layer of indirection is friction against
fast iteration.

## Prototype Constraints

- This codebase is a PROTOTYPE and MUST be treated as disposable, not as a
  production system.
- Code that is "good enough to demonstrate the idea" satisfies the quality bar.
- Refactoring is done on demand, not pre-emptively.
- Security, scalability, and performance hardening are OUT OF SCOPE unless the
  prototype's goal is specifically to test one of them.

## Development Workflow

- Implement the smallest change that achieves the goal, then run it.
- Verify by running the code or inspecting output by hand.
- Tests are added only when explicitly requested or when a defect is
  genuinely faster to pin down with a test.
- Commit and move on; do not block progress on polish.

## Governance

This constitution defines how work is prioritized for this prototype. Its
principles supersede default best-practice habits (such as mandatory testing or
heavy review) for the duration of the prototype phase.

- Amendments are made by editing this file and bumping the version below.
- Versioning follows semantic versioning: MAJOR for principle removals or
  incompatible redefinitions, MINOR for new principles or materially expanded
  guidance, PATCH for clarifications and wording fixes.
- If the project graduates from "prototype" to "product", this constitution
  MUST be revisited — especially Principles III and IV.

**Version**: 1.0.0 | **Ratified**: 2026-06-20 | **Last Amended**: 2026-06-20
