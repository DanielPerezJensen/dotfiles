---
name: review-pr
description: Use when asked to review a GitHub pull request for correctness, security, or unnecessary complexity, including /review-pr.
---

# Review a PR

Read [GitHub context](references/github-context.md) and
[Report format](references/report-format.md) first.

1. **Gather.** Resolve the PR. Collect the pinned metadata, diff, requirements, CI
   status, stack context, relevant source and all discussion pages, as the shared
   context describes. If the PR is closed or merged, stop and ask whether to
   continue. Review a draft PR when the user asked for it, and say it is a draft.
2. **Review through two lenses.**
   - **Correctness/security:** behaviour, failure handling, authorization,
     affected callers, meaningful regression coverage, and the repository's
     requirements.
   - **Simplification:** dead code, speculative flexibility, redundant
     dependencies, and abstractions whose complexity has no demonstrated purpose.

   Apply the shared context's **Contract and standards** checks across both lenses.
   Judge repository compliance separately from acceptance-criteria completeness.
   Include documentation drift and weakened quality gates when the change supports
   it. Do not add stack-specific rules. Do not execute the PR's code.
3. **Try to disprove each candidate finding** before it enters the report. Open the
   cited code at the pinned SHA. Check the callers, guards and tests that reach it,
   and check the skip list in the report format. Drop the finding if they rule it
   out. Merge duplicates of the same underlying issue.
4. **Match existing comments** by substantive concern, not merely by file. If a
   comment search is incomplete, say so. Do not write "not raised".
5. **Classify** each remaining finding with Impact, Confidence and Introduced, as the
   report format defines them. Mark uncertain claims.
6. **Write and save the report** in the report format, then save it as below.

## Saving

Save the same report at the path the shared context's **Report location** gives.
If a report exists at that path:

1. Copy it to `pr-<n>.<UTC time as yyyymmddThhmmssZ>.md` in the same folder.
2. Keep the ID of each finding that matches a prior finding.
3. Give new findings IDs after the prior maximum.

Only the local report is written. Source edits, GitHub comments and publication
need a separate request. `review-check` assesses received feedback.
`review-followup` checks this saved report later.
