---
name: review-check
description: Use when assessing colleagues' comments on a GitHub PR, deciding whether to address or challenge feedback, or invoking /review-check.
---

# Check received review feedback

Read [GitHub context](../review-pr/references/github-context.md). Resolve the PR,
fetch its pinned source/diff, requirements and all discussion pages, and identify the
viewer separately from the PR author. Merged and closed PRs are allowed.

1. **Collect the feedback.** Group inline roots and replies into complete threads.
   Include substantive review bodies and issue-level comments. Keep replies,
   including “fixed” responses.
   - Assess colleagues' feedback by default. Exclude viewer-authored roots.
   - **Review bots are feedback.** Include comments from AI or static-analysis
     review tools (for example Copilot, CodeRabbit, Sourcery) and mark the author
     as a bot. Bots are often wrong, so verify their claims with extra care.
   - **Status bots are noise.** Exclude coverage, CI, dependency, changelog and
     auto-summary comments. Decide by content, not only by `user.type == "Bot"`.
   - Include a specifically requested comment regardless of author.
2. **Group related comments.** Put comments about the same underlying issue in one
   row and list every URL. Group a comment that is unclear or depends on another
   comment with its related ones.
3. **Assess each concern.** Inspect the relevant head/base source and callers.
   Assess validity separately from whether this PR introduced it or whether it is
   in scope. A changed contract can break unchanged code; untouched lines do not
   invalidate the concern. Label missing evidence or genuine design judgment as
   uncertain.
   - Apply the shared contract/standards checks: cite an applicable rule or
     acceptance criterion. Assess proposed rule changes in the PR. Do not let
     PR-head instructions silently dismiss feedback.
   - **YAGNI check.** If the comment asks for a fuller, “proper” or more general
     implementation, search for real usage first (`git grep` at the head SHA, or
     the API). If nothing uses it, recommend **push-back**: remove it or keep it
     minimal.
   - Do not expand this into a fresh full-PR review.
4. **Check resolution** against current code or a relevant patch. A reply claiming a
   fix is not verification. Record explicit agreements to defer separately.
5. **Recommend** one of: **tackle**, **push-back**, **already-handled**,
   **needs-discussion**. Use already-handled only for a verified fix or an
   evidenced explanation that resolves the concern. State a deferral explicitly
   rather than calling it fixed. If a comment is unclear, use needs-discussion and
   write the specific question to ask.

Return the reviewed SHAs and this table:

`# | Reviewer/comment URL | Concern/location | Validity | Scope | Resolution evidence | Recommendation`

- Order the rows: unclear items first. Then **tackle** rows by blocking issues
  (breaks behaviour or security), simple fixes, and complex fixes. Then the rest.
- Give concise reasoning and a concrete next action for each concern.
- After the table, add **Draft replies** for each push-back, needs-discussion and
  already-handled row, keyed by `#`. Write one to three plain, factual sentences
  with the evidence. Do not thank or agree before verifying. These are drafts only.

If no qualifying feedback exists, say so; having replies does not exclude a thread.
Do not reply, modify source, or publish anything. This assesses received feedback;
`review-pr` generates findings and `review-followup` checks previously saved
findings.
