#!/bin/bash
# Links the files in this repo into $HOME.
# Default: show the plan and change nothing. --apply: make the changes.
set -euo pipefail

REPO="$(cd "$(dirname "$0")" && pwd)"
BACKUP_ROOT="$HOME/.dotfiles-backup"
# APM writes here. A snapshot of these paths makes the APM step reversible.
APM_PATHS=".apm .config/opencode/skills .config/opencode/commands"

say() { printf '%s\n' "$*"; }
die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

# links.txt lines: <path in repo> <path under $HOME>.
# Each folder in agents/skills/ also gets a link, without a line in links.txt.
entries() {
  grep -vE '^[[:space:]]*(#|$)' "$REPO/links.txt"
  local d
  for d in "$REPO"/agents/skills/*/; do
    d="${d%/}"
    echo "agents/skills/${d##*/} .agents/skills/${d##*/}"
  done
}

# Prints: ok | missing | file | other-link
state() {
  if [ -L "$2" ]; then
    if [ "$(readlink "$2")" = "$1" ]; then echo ok; else echo other-link; fi
  elif [ -e "$2" ]; then
    echo file
  else
    echo missing
  fi
}

preflight() {
  case "$(uname)" in
    Darwin | Linux) ;;
    *) die "macOS or Linux (including WSL) only" ;;
  esac
  [ "$(id -u)" != 0 ] || die "do not run as root"
  command -v brew >/dev/null || die "install Homebrew first (https://brew.sh) and put brew on PATH"
  local src dst
  while read -r src dst; do
    [ -e "$REPO/$src" ] || die "links.txt: $src does not exist in the repo"
    case "$dst" in /* | *..*) die "links.txt: $dst must be a plain path under \$HOME" ;; esac
  done < <(entries)
}

plan() {
  say "Homebrew packages:"
  HOMEBREW_NO_AUTO_UPDATE=1 brew bundle check --file="$REPO/Brewfile" --no-upgrade --verbose || true
  say ""
  say "Links:"
  local src dst
  while read -r src dst; do
    case "$(state "$REPO/$src" "$HOME/$dst")" in
      ok) say "  ok       ~/$dst" ;;
      missing) say "  create   ~/$dst" ;;
      *)
        if diff -rq "$REPO/$src" "$HOME/$dst" >/dev/null 2>&1; then
          say "  replace  ~/$dst  (same content)"
        else
          say "  replace  ~/$dst  (DIFFERS, see: diff -ru ~/$dst $REPO/$src)"
        fi
        ;;
    esac
  done < <(entries)
  say ""
  say "Then: apm install -g (shows a dry run first and asks)."
  say "Nothing changed. Run '$0 --apply' to make these changes."
}

apply() {
  brew bundle install --file="$REPO/Brewfile" --no-upgrade

  local stamp bak src dst s d answer
  stamp="$(date +%Y%m%d-%H%M%S)"
  bak="$BACKUP_ROOT/$stamp"
  mkdir -p "$bak"

  while read -r src dst; do
    s="$REPO/$src"
    d="$HOME/$dst"
    case "$(state "$s" "$d")" in
      ok) continue ;;
      file | other-link)
        mkdir -p "$(dirname "$bak/$dst")"
        mv "$d" "$bak/$dst"
        echo "backup $dst" >>"$bak/manifest"
        ;;
    esac
    mkdir -p "$(dirname "$d")"
    ln -s "$s" "$d"
    echo "link $dst" >>"$bak/manifest"
    say "  linked ~/$dst"
  done < <(entries)

  local p
  for p in $APM_PATHS; do
    if [ -e "$HOME/$p" ]; then
      mkdir -p "$(dirname "$bak/apm-before/$p")"
      cp -Rp "$HOME/$p" "$bak/apm-before/$p"
    fi
  done
  echo "apm-snapshot" >>"$bak/manifest"
  say "Undo with: $0 --restore $stamp"

  apm install -g --dry-run
  printf 'Run apm install -g now? [y/N] '
  read -r answer || answer=""
  if [ "$answer" = y ]; then apm install -g; else say "Skipped. Run 'apm install -g' later."; fi
}

check() {
  local bad=0 src dst st
  while read -r src dst; do
    st="$(state "$REPO/$src" "$HOME/$dst")"
    [ "$st" = ok ] && continue
    bad=1
    say "  $st  ~/$dst"
    if [ "$st" = file ]; then
      say "      A tool replaced the link. Compare first: diff -ru $REPO/$src ~/$dst"
    fi
  done < <(entries)

  # Skills in ~/.agents/skills that this repo does not manage, or links to removed skills.
  local e
  for e in "$HOME"/.agents/skills/*; do
    [ -e "$e" ] || [ -L "$e" ] || continue
    case "$(readlink "$e" 2>/dev/null || true)" in
      "$REPO"/*)
        if [ ! -e "$e" ]; then
          bad=1
          say "  dangling  ~/.agents/skills/${e##*/} (the skill is gone from the repo: rm the link)"
        fi
        ;;
      *) say "  info: not in the repo  ~/.agents/skills/${e##*/}" ;;
    esac
  done

  if [ "$bad" = 0 ]; then say "All links OK."; else exit 1; fi
}

restore() {
  [ -n "${1:-}" ] || die "usage: $0 --restore <timestamp> (see: ls $BACKUP_ROOT)"
  local bak="$BACKUP_ROOT/$1" dst d
  [ -f "$bak/manifest" ] || die "no backup record in $bak"

  # Put the APM folders back as they were. The current ones move to apm-after/.
  local p
  if grep -qx apm-snapshot "$bak/manifest"; then
    for p in $APM_PATHS; do
      if [ -e "$HOME/$p" ]; then
        mkdir -p "$(dirname "$bak/apm-after/$p")"
        mv "$HOME/$p" "$bak/apm-after/$p"
      fi
      if [ -e "$bak/apm-before/$p" ]; then
        mv "$bak/apm-before/$p" "$HOME/$p"
      fi
    done
    say "  restored APM folders (the replaced ones are in $bak/apm-after)"
  fi

  # Remove only links that still point into this repo.
  while read -r dst; do
    d="$HOME/$dst"
    case "$(readlink "$d" 2>/dev/null || true)" in
      "$REPO"/*) rm "$d" && say "  removed link ~/$dst" ;;
    esac
  done < <(sed -n 's/^link //p' "$bak/manifest")

  # Put the old files back, but never over something new.
  while read -r dst; do
    d="$HOME/$dst"
    if [ -e "$d" ] || [ -L "$d" ]; then
      say "  skipped ~/$dst: the path is in use"
      continue
    fi
    mv "$bak/$dst" "$d" && say "  restored ~/$dst"
  done < <(sed -n 's/^backup //p' "$bak/manifest")
}

case "${1:-}" in
  "")
    preflight
    plan
    ;;
  --apply)
    preflight
    apply
    ;;
  --check) check ;;
  --restore) restore "${2:-}" ;;
  *) die "usage: $0 [--apply | --check | --restore <timestamp>]" ;;
esac
