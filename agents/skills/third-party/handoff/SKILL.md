---
name: handoff
description: Use when asked to hand off a session, prepare a fresh agent to continue, or save continuation context before ending a conversation.
metadata:
  argument-hint: "What will the next session be used for?"
---

# Handoff

Write a concise continuation document to a file. Treat supplied arguments as the
next session's focus. Capture enough state to resume without rediscovery; reference
existing specs, plans, issues, commits and diffs by path or URL instead of restating
them. Redact secrets and personally identifiable information.

## Destination

- Default to `<active-project-root>/plans/handoffs/<YYYYMMDD-HHMMSS>-<topic>.md`.
  Resolve the active project explicitly; do not use the skill installation directory.
  If multiple projects are plausible or no project is active, ask for a destination.
- Honor an explicit user-supplied output path. Inspect the parent before creating
  directories. Preserve existing handoffs; choose a unique sibling on collision
  unless the user explicitly asks to replace a particular file.
- For the default location in a Git repository, verify `plans/handoffs/` is ignored.
  If not, ask for an alternative or permission to add an ignore rule; do not silently
  change repository settings. In a non-Git project, state that ignore checking is
  inapplicable and write the file. Do not stage or commit handoffs.

## Contents

1. **Goal and next-session focus.** Include the user's latest constraints.
2. **Current state.** Completed work, in-progress changes, relevant paths and branch
   or commit when known. Distinguish observed facts from assumptions.
3. **Decisions and open questions.** Record unresolved choices and blockers.
4. **Verification.** Actual commands and outcomes; label failed, environment-blocked
   and unrun checks honestly. An attempted test is not a passing test.
5. **Next actions.** Prioritized, concrete starting steps and needed context.
6. **Suggested skills.** Name the relevant skills for the next agent to load.

Read back the saved file and return its absolute path with a brief continuation
prompt. If writing is blocked, say so and provide the handoff inline to avoid losing
context; do not claim it was saved.
