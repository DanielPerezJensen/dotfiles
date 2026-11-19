# Report format

Used by `review-pr`. `review-followup` reads reports in this format.

## Header

- Repository and PR URL, PR state (note if draft)
- UTC review time
- Base branch and SHA; head SHA
- Stack: parent and child PRs with state, or "none"
- Requirements used: PR body, linked issues, ticket key, or "unavailable"
- CI: failing and pending checks by name, or "all green"
- Checked scope and limitations (omitted areas, unavailable evidence, comment
  search status)

## Findings summary

One table, sorted: introduced before pre-existing, then High to Low.

`| ID | Impact | Confidence | Introduced | Finding | Already raised |`

Use stable IDs (`F1`, `F2`, …). Then one block per finding (see the example).
If there are no findings, say so and name what was checked.

Put Low-confidence concerns in a short **Questions to verify** list after the
table. They get no ID and no impact rating.

## Impact

| Level | Meaning |
| --- | --- |
| High | Breaks requested behavior, a security boundary or data integrity on a reachable path. Fix before merge. |
| Medium | Real defect or maintenance cost with limited reach or a workaround. Fix in this PR or track it. |
| Low | Worth fixing, safe to defer: small simplification, weak test, documentation drift. |

Do not report nits.

## Confidence

| Level | Meaning |
| --- | --- |
| High | Verified in code at the pinned SHA. The mechanism and the reachable path are shown. |
| Medium | The mechanism is clear. One caller, input or setting could not be verified. Say which. |
| Low | A hypothesis. Goes in **Questions to verify**, not in the findings table. |

## Introduced

- **yes**: the diff creates the problem, or changes a contract that unchanged
  code relies on.
- **pre-existing**: the problem exists on the base. Report it only when the PR
  touches or relies on the affected code and it changes the review outcome.
- **unclear**: base behavior could not be established.

## Skip list

Do not report these, even if they look real:

- Style, formatting, naming or import order. Anything a configured linter,
  formatter or type checker already catches (do not run them to check).
- Pedantic points a senior engineer would not raise.
- Code that looks wrong but is correct: a caller, guard, type or test rules it out.
- A missing check that a caller, middleware or earlier guard already makes.
- Problems the code deliberately silences (lint ignore, documented exception),
  unless the silencing itself is unjustified.
- Pre-existing problems the PR neither touches nor relies on.

## Fix size

`~LOC` is the approximate number of changed lines to fix. Use a negative number for
net removals. Use "unknown" when the scope is not established.

## Example

Header and summary (shortened):

```markdown
# PR review: acme/shop#412

- URL: https://github.com/acme/shop/pull/412 (open)
- Reviewed: 2026-11-12T09:30:00Z
- Base: `main` @ `a1b2c3d`. Head: `e4f5a6b`
- Stack: none
- Requirements: PR body, issue #398
- CI: all green
- Scope: all 9 changed files. Limitation: no local clone, caller search via API only.

| ID | Impact | Confidence | Introduced | Finding | Already raised |
| --- | --- | --- | --- | --- | --- |
| F1 | High | High | yes | `refund()` skips the owner check | No |
| F2 | Low | High | yes | `RetryPolicy` has one caller; inline it | No |

**Questions to verify**
- Does the nightly job call `refund()` with a system user? (not found in the diff)
```

Finding block:

```markdown
### F1: Refund endpoint skips the owner check

- **Impact / Confidence / Introduced:** High / High / yes
- **Lens:** Correctness/security
- **Location:** [`src/api/refunds.py` L42-L58](https://github.com/acme/shop/blob/e4f5a6b…/src/api/refunds.py#L42-L58)
- **Evidence:** `refund()` loads the order by ID and never compares
  `order.user_id` with the caller. The old handler (base, L40) did. Any
  authenticated user can refund any order by guessing its numeric ID.
  Requirement #398 says "only the buyer can request a refund".
- **Fix:** Compare `order.user_id` to `current_user.id` and return 403.
  Add a test where user B refunds user A's order.
- **~LOC:** +4
- **Already raised:** No (all three comment streams searched)
```

Use source links pinned to the reviewed commit and comment URLs for matches. Links
need the full 40-character SHA (the example shortens it) and a line range
(`#L42-L58`).
