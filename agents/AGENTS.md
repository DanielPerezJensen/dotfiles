# Personal agent instructions

## General

1. Ask when intent, architecture, or requirements are unclear, and state your
   assumptions. When useful, run a small, local, low-risk experiment. When you
   work unattended, proceed with the most reasonable interpretation and record
   the assumption.
2. Build the simplest solution that solves the problem. Add flexibility only
   for a current need.
3. Keep changes inside the task scope. Report other code or design problems
   separately, with a better approach when it has lasting value.

## Response style (ASD-STE100)

Write final answers to me about 75% of the way towards ASD-STE100 Simplified
Technical English, as used in airline maintenance manuals. This applies to the
wording of the final answer only. Do not let it change your reasoning, depth,
accuracy, or the amount of checking you do.

- Use short sentences: about 20 words for instructions, 25 for descriptions.
- One idea per sentence. One topic per paragraph.
- Use active voice and the simple present tense. Avoid the passive.
- Use commands for steps ("Run the tests", not "The tests should be run").
  Number the steps and keep them in order.
- Use simple, common words. Prefer "use" to "utilize", "start" to "initiate".
  Use one word for one meaning and do not swap synonyms for variety.
- Do not use idioms, figures of speech, or filler.
- Keep articles ("the", "a"). Do not drop them to save words.
- Put warnings and cautions before the step they apply to.
- Use lists and tables for steps, options, and specifications.
- Do not stretch the rules (the 75%): keep exact technical terms, code,
  commands, file paths, and library names as they are. Allow a longer or
  slightly less plain sentence when strict rules would make it unclear or
  wrong. Do not use the full STE dictionary or its approved-word list.
- Code, commit messages, PR text, and file contents follow their own project
  conventions, not this section.

## Skills, tools, and plans

- Write personal skills in the dotfiles repo, in
  `~/projects/dotfiles/agents/skills/<name>/`, then run
  `~/projects/dotfiles/install.sh --apply` to link them into `~/.agents/skills/`.
  A skill created directly in `~/.agents/skills/` is not tracked.
  `~/.claude/skills/` is not a source of truth: keep skills out of it.
- OpenCode commands in `~/.config/opencode/commands/` are thin launchers; put
  workflow instructions in the skills.
- To install, update, or remove skills or MCP servers, load the `apm-packages`
  skill. Run `apm` with `-g`: in `~`, `apm` without `-g` deploys into many tool
  folders.
- Install other CLI tools and applications with Homebrew. Use another package
  manager only when Homebrew has no suitable package, and say so.
- Save plan documents in `<repo-root>/.opencode/plans/*.md`, the only path the
  OpenCode plan agent can write. Plans, and the contents of a gitignored
  `plans/` directory, are non-shipped work: no linting and no unit tests.

## Git workflow

- For non-trivial work, use a git worktree on its own branch: several agents in
  one checkout overwrite each other's changes. Small, quick edits can stay in
  place.
- In a Next.js or front-end monorepo, work in the current checkout on a normal
  branch. Create a worktree there only when I ask for it.
- Ask me for the branch name before you create a worktree. Put the worktree in
  `.worktrees/<branch>`, with each `/` replaced by `-`. Example: branch
  `feature/add-logging` in `.worktrees/feature-add-logging`.
- Move the session into a new worktree (`session_move`) before you edit files
  there.
- For feature work, use the `gh-stack` skill. Default to one commit per branch;
  use more when useful. Review a stack top-down and merge it bottom-up: merge a
  lower PR only when the PR that depends on it is ready to merge.
- Run `git fetch --prune origin` before you compare with the remote, edit an
  existing branch, or work on a PR or stack.
- Use the fetched `@{upstream}` as the baseline. Without an upstream, use
  `origin/<default-branch>`. Compare local `HEAD` with the baseline:
  - Equal: continue.
  - Behind only: `git merge --ff-only @{upstream}`.
  - Ahead only: keep the local commits.
  - Diverged: stop and ask whether to rebase or discard local commits. Resolve
    divergence destructively only with my explicit approval.

## Local diff review

At each review milestone (a finished slice of work, or before you ask me to
review), load the `local-diff-review` skill. I review diffs in Hunk inside
Rex.

## Code

- Suggest tests when useful. Add or change tests for small changes only when I
  ask. In plan mode, include test writing as an explicit step.
- Python: name private fields without a leading underscore (a deliberate
  exception to PEP 8). Write docstrings only for non-obvious constraints,
  invariants, or side effects.
