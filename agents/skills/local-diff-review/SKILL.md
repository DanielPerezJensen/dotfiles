---
name: local-diff-review
description: Use at a review milestone, when a slice of implementation is done or the user should see the changes under discussion, when the user asks to review or see the diff, or before acting on review notes the user left in Hunk.
---

# Local diff review

The user reviews local changes in Hunk, in a review tab inside Rex. This
skill is the user's standing request for that tab: open it once, then reuse it
for every review iteration. The user closes it. This replaces the Hunk skill's
step "If no session exists, ask the user to launch Hunk".

Use the `rex` skill for Rex commands and JSON fields. In Rex, a tab is a
window. Read the Hunk skill at
`$(hunk skill path)` for `hunk session` commands.

## Pick the diff

Show the changes under discussion, not the whole branch. Check the state with
`git status --short` and `git log --oneline`.

The steps stage all changes, and a plain `hunk diff` hides staged changes, so
the uncommitted case uses `diff HEAD`.

| Changes under discussion | Hunk command |
|---|---|
| Only uncommitted | `diff HEAD` |
| Committed during this work, with or without uncommitted changes on top | `diff <base>`, where `<base>` is the commit before the first commit of this work |
| Exactly one commit, nothing uncommitted on top | `show <sha>` |

If the first commit of this work is not clear, ask the user.

## Steps

`<worktree>` is the output of `git rev-parse --show-toplevel`. `<label>` is
`review: <branch>`.

1. Run `test -n "${REX_SESSION:-}"`. If it fails, give the user the commands
   to run in their terminal (for example `git add . && hunk diff HEAD`), and
   stop.
2. Run `git add .` in `<worktree>`. Hunk shows untracked files differently;
   staged, they show as normal new-file diffs.
3. Run `hunk session list --json`. Look for a session whose `repoRoot` is
   `<worktree>`. If more than one matches, use its `sessionId` instead of
   `--repo <worktree>` in the commands below.
4. If the session exists:
   - Run `hunk session reload --repo <worktree> -- <hunk command>`.
   - Find the window labeled `<label>` with
     `rex window ls -s "$REX_SESSION" --json | jq -r --arg l "<label>" '.windows[] | select(.label == $l) | .window_id'`,
     and run `rex focus -s "$REX_SESSION" <window_id>`.
5. If no session exists:
   - Run `rex window new -s "$REX_SESSION" "<label>" -c <worktree> --json -- hunk <hunk command>`.
     Hunk is an interactive TUI: start it only in the review window, never in
     your own shell. Do not use `--wait`.
   - Repeat `hunk session list --json` until the session for `<worktree>` shows.
6. Add notes where the diff does not explain itself: intent, a risk, a
   trade-off, or an open question. Send all notes in one
   `hunk session comment apply --repo <worktree> --stdin --focus` batch. A diff
   that explains itself needs no notes.
7. Tell the user the tab label and which diff it shows. Stop and wait for the
   review.

Done when the session for `<worktree>` shows in `hunk session list`, it shows
the diff from the table, the notes (if any) are applied, and the user has the
tab label.

## Next iteration

1. Read the user's notes before you change code:
   `hunk session comment list --repo <worktree> --type user --json`.
2. After the change, go to step 2 above. The existing session gets reloaded.
