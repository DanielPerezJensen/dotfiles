---
name: pr-title-desc
description: Use when drafting or revising a pull request title and description.
---

# Draft a PR title and description

1. Resolve the PR and its actual target branch from GitHub using `gh`, and read
   its current title and full body, or use the supplied PR text, diff, and base.
   If an existing PR's text is unavailable, ask for it before proposing a revision.
   For a new PR, establish the intended base before comparing.
   Describe only this PR's committed changes, including when stacked; exclude
   uncommitted work. Ask when the target or intent cannot be established.
2. Read the repository's PR template and conventions. Preserve any existing
   tool-managed stack block verbatim at the top. For a new or empty description,
   use the repository template if present, or the fallback below. For an existing
   description, follow the revision rules below while satisfying required template
   fields and conventions.
3. Write in the author's voice, with concrete changes and rationale. Preserve
   technical meaning, and remove filler. Drafting does not authorize publishing
   or editing a PR.

## Revising an existing PR

Use the current title and body as the starting point. Propose the smallest useful
update rather than regenerating the description from the diff.

- Keep an accurate title and useful wording, headings, section order, and extra
  author-provided context, such as rollout notes, rationale, links, and reviewer
  guidance. Templates guide required content; they do not erase extra sections.
- Correct or remove claims contradicted by the committed changes or other reliable
  evidence, including stale scope. Edit the
  affected claim, preserving useful surrounding content.
- Information absent from the diff is not necessarily incorrect. Keep supplemental
  context that is not contradicted; flag uncertainty or ask a focused question when
  needed instead of silently deleting it or presenting it as independently verified.
- Add missing information supported by the evidence. Leave accurate content alone
  unless a required convention or the user's request calls for a change.

Example: if a rollout section has a false retry claim plus a support handover link,
remove or correct the retry claim and retain the section and handover link.

## Fallback format

Title: Conventional Commits style, e.g. `feat: add profile lookup`.

```markdown
# Description
Purpose and outcome in at most five sentences.

# Changes
- Specific changes, at most two sentences each.
```

Start PR description headings at h1 (`#`). Use `##` to `####` for nested
subsections when needed, and do not go deeper than h4. This applies to the fallback format, to repository
templates, and to headings you add or change when you revise an existing
description.

Include screenshots only for UI changes when available; otherwise suggest what
to capture. Return the proposed title and full body. For an existing PR, briefly
summarize the proposed changes and reasons, including corrections or removals;
if no changes are needed, say so. No additional editing skill required.
