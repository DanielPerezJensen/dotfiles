---
name: apm-packages
description: Use when installing, updating, or removing agent skills or MCP servers, or when ~/.apm/apm.yml, ~/.apm/apm.lock.yaml, or the skills in ~/.config/opencode/skills/ look wrong.
---

# APM packages

APM (Agent Package Manager) installs every skill and MCP server when an
APM-installable source exists: a GitHub repo, a repo subpath, or a skill
collection. Use another method only when APM cannot install it, and say so.

The only personal manifest is the global one: `~/.apm/apm.yml` (target:
`opencode`). It is a symlink to `apm/apm.yml` in the dotfiles repo, so edits
show up there as a git diff. Pin every dependency (`#tag` or `#sha`). The lock
file `~/.apm/apm.lock.yaml` is per machine and stays out of the repo. APM
deploys skills into `~/.config/opencode/skills/`, and `apm install -g` removes
deployed skills that are no longer in `apm.yml`.

## Rules

- Pass `-g` to `apm install`, `apm uninstall`, and `apm update`. In `~`, these
  commands without `-g` treat the home folder as a project and deploy into many
  tool folders (`.claude`, `.kiro`, `.grok`, `.agents`). Keep `~/apm.yml`
  absent.
- `apm prune` has no `-g`: run it from `~/.apm`.
- Add skill files only through APM, not by copying them. To change an
  APM-installed skill, change its source package or a fork: the next install
  overwrites local edits.
- Before you install, check that no skill with the same name exists in
  `~/.agents/skills/` or `~/.config/opencode/skills/`. Duplicate skill names
  conflict.

## Commands

| Task | Command |
|---|---|
| Install a skill | `apm install -g <owner>/<repo>[/<path>]` (run with `--dry-run` first) |
| Install one skill from a collection | add `--skill <name>` |
| Install from a plugin-bundle repo | use the skill subpath, for example `petergyang/no-ai-slop/skills/no-ai-slop`; a full-repo install fails |
| Install an MCP server | Not through APM: `opencode.json` is a symlink into the dotfiles repo, and APM refuses to write MCP config through symlinks. An MCP entry in `apm.yml` makes every `apm install -g` fail. Add the server to `opencode/opencode.json` in the dotfiles repo. |
| Update | `apm update -g` |
| Remove | `apm uninstall -g <package>`, then do the bug check below |

## Known bug: uninstall re-deploys collections

`apm uninstall -g` re-deploys every skill of collection packages and ignores
the `skills:` subset. After any uninstall:

1. Run `apm install -g`.
2. List `~/.config/opencode/skills/`.
3. Delete the skills that are not in `~/.apm/apm.lock.yaml`.
