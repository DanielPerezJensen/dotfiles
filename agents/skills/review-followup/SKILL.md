---
name: review-followup
description: Use when checking whether findings from a saved PR review were raised, explained, and resolved, including /review-followup.
---

# Follow up a saved review

Read [GitHub context](../review-pr/references/github-context.md). Resolve the PR
and load the saved report. Use the path the context's **Report location** gives
(main checkout, not the current worktree), or the report path the user supplied.
Verify the report's repository/PR identity. If it is absent, ask for the report or
explain that `review-pr` creates it. Do not reconstruct findings or launch a fresh
review. Merged and closed PRs are allowed.

1. Keep the saved finding IDs. Read the report's base/head SHAs and review
   timestamp, then fetch current pinned source and complete discussions. If the
   report has no SHAs or timestamp, say the historical baseline is unknown. Do not
   infer a “since review” cutoff from commit titles.
2. For each finding, match substantive comments and replies. Record **who raised
   it** and the URL separately from whether the authenticated viewer raised it.
   Assess comment quality as **good** (problem and impact), **thin**, or **missing**.
3. Inspect relevant patches and current head code against the original failure
   mechanism and cited contract or repository invariant. A weaker rule or a test
   asserting a mock interaction alone does not fix missing production behavior.
   If an explicit accepted scope/contract change supersedes the finding, report
   that decision separately with evidence rather than calling the original behavior
   fixed. Preserve a distinction between these resolution states:

   | State | Evidence required |
   | --- | --- |
   | Verified fixed | Current code/patch addresses the original problem; name the evidence and any unrun checks. |
   | Claimed fixed | A reply claims success, but supporting code evidence is unavailable. |
   | Deferred | Explicit agreement to defer; link the decision. |
   | Unresolved | Current code still demonstrates the original problem. |
   | Unknown | Insufficient evidence to establish current status. |

   A finding can be fixed without ever being posted as a comment. If current code
   contradicts a “fixed” reply, mark unresolved. Commit metadata, filenames,
   thread closure and green checks alone do not establish a fix.

Return the current reviewed SHAs, baseline limitations and:

`ID | Finding | Raised by / URL | Comment quality | Resolution | Evidence / next action`

Report inline. Preserve the original saved review, and do not edit source or reply
on GitHub. This is a focused follow-up, not a new full review or automatic chain.
