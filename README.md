# dotfiles

My personal OpenCode and APM setup: agent instructions, skills, agents, the
skill packages I install with [APM](https://microsoft.github.io/apm/), my zsh
config, and the Homebrew packages they need.

The repo is the source of truth. `install.sh` links each path in `links.txt`,
and each folder in `agents/skills/`, into `$HOME`. An edit in either place is a
git diff here.

## Add a skill

1. Create `agents/skills/<name>/SKILL.md`.
2. Run `./install.sh --apply`. It links the folder to `~/.agents/skills/<name>`.

Skills from other people go in [`apm/apm.yml`](apm/apm.yml), not here.

## Install

```sh
git clone <this repo> ~/projects/dotfiles
cd ~/projects/dotfiles
./install.sh            # preview: shows what would change, changes nothing
./install.sh --apply    # back up, link, install packages
```

Needs macOS and [Homebrew](https://brew.sh). The zsh config expects
[Oh My Zsh](https://ohmyz.sh) in `~/.oh-my-zsh`, and works without it.

## What `--apply` does

1. `brew bundle` for the `Brewfile`, without `--cleanup` and without upgrades.
2. For each line in `links.txt` and each skill folder: move an existing file to
   `~/.dotfiles-backup/<timestamp>/`, then create the symlink.
3. Snapshot `~/.apm`, `~/.config/opencode/skills` and
   `~/.config/opencode/commands`.
4. Show `apm install -g --dry-run` and ask before `apm install -g`.

## Other commands

| Command | Effect |
|---|---|
| `./install.sh --check` | Reports links that are missing, wrong, dangling, or replaced by a normal file, and lists skills in `~/.agents/skills` that the repo does not manage |
| `./install.sh --restore <timestamp>` | Undoes one `--apply`, including the APM step. Restore the newest first. |

## Notes

- `apm install -g` removes skills that are no longer in `apm/apm.yml`.
- Add MCP servers to `opencode/opencode.json`, not through APM: APM does not
  write through symlinks.
- Secrets stay out of the repo. Use `{env:NAME}` in `opencode.json`.
- Put machine-specific or private shell settings (extra `PATH` entries, tokens
  read from the keychain) in `~/.zshrc.local`. `zsh/zshrc` sources it, and it
  never goes in the repo.
- Run `pre-commit install` once. The hook scans commits with gitleaks.
