# Third-party skills and adapted guidance

Canonical global home: `~/.agents/skills/`. Vendored skills are kept here for
offline, reviewable use. Preserve applicable license notices when copying them.

Imported on 2026-09-15 from a previously vendored local snapshot. Upstream
revisions below were recorded in its provenance manifest; no new upstream revision
was fetched during this import.

| Skill | Upstream and original path | Pinned revision | License | Global adaptations |
| --- | --- | --- | --- | --- |
| `handoff` | [mattpocock/skills](https://github.com/mattpocock/skills), `skills/productivity/handoff` | `3cca18b368ae95cdbdebbff572ccafa662551015` | [MIT](licenses/mattpocock-skills-LICENSE) | Retained OpenCode-compatible frontmatter; writes unique project `plans/handoffs/` files, checks destination/ignore status, records state, blockers, verification and next actions; global thin launcher. |
| `diagnosing-bugs` | [mattpocock/skills](https://github.com/mattpocock/skills), `skills/engineering/diagnosing-bugs` | `3cca18b368ae95cdbdebbff572ccafa662551015` | [MIT](licenses/mattpocock-skills-LICENSE) | None; includes the human-in-the-loop script template. |
| `verification-before-completion` | [obra/superpowers](https://github.com/obra/superpowers), `skills/verification-before-completion` | `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` | [MIT](licenses/obra-superpowers-LICENSE) | None. |
| `writing-skills` | [obra/superpowers](https://github.com/obra/superpowers), `skills/writing-skills` | `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` | [MIT](licenses/obra-superpowers-LICENSE) | Canonical global paths; self-contained RED/GREEN/REFACTOR instead of an installed TDD dependency; removed references to renderer/examples absent from the vendored snapshot; unavailable behavioral testing is reported honestly; publication requires explicit request. Support references retained. |

## Other adapted guidance

The following include material by Mahesh Bishnoi, covered by
[the retained MIT license](licenses/mahesh-bishnoi-LICENSE) (Copyright 2026):

- `../doc-upkeep/SKILL.md`: stack-neutral, automatic discovery with approval before edits, user/developer/agent
  docs and architecture/flows, standalone audits, no global ADR workflow.
- `../review-pr/`, `../review-check/`, `../review-followup/`: existing personal
  workflows augmented with contract-versus-standards review and evidence guidance;
  preserved origin-only review and
  each workflow's scope. Shared guidance lives in
  `../review-pr/references/github-context.md`.
- `~/.config/opencode/commands/handoff.md`: adapted thin launcher;
  the workflow lives in the shared skill.

The source snapshot had no Git metadata, so its own revision is not asserted.
To update, review the upstream changes and reapply these documented adaptations;
do not overwrite personal workflow changes with a fresh wholesale copy.
