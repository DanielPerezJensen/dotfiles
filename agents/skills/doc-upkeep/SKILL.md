---
name: doc-upkeep
description: Use automatically when changes affect documented behavior, setup, configuration, APIs, architecture, flows, or developer and agent workflows; also use for explicit documentation updates or drift audits across projects.
---

# Documentation upkeep

Automatically identify documentation impact, then **ask before editing**. Follow
the active project's conventions and sources of truth; this skill imposes no
directory layout, framework, diagram format or build tool.

## Discover and propose

1. Read applicable project instructions and inspect the relevant change or requested
   audit scope. Locate the existing documentation index, README, feature/API pages,
   architecture/flow sources, and contributor or agent guidance as relevant.
2. Compare documentation with code, configuration, build scripts and tests. Separate
   verified drift from uncertain intent; ask about contradictions instead of
   silently rewriting a contract to match an implementation bug.
3. Present a short proposal: affected paths, what needs updating, and validation to
   run. Ask for approval before edits or generation commands that write files.
   If the user already explicitly approved those documentation changes, proceed
   within that scope without asking again. Ask again if scope materially expands.

| Change | Documentation to inspect |
| --- | --- |
| Behavior, API, default or configuration | User-facing feature/API docs, examples and README |
| Setup, deployment or dependencies | Quickstart, environment examples and operational instructions |
| Component, dependency boundary or flow | Existing architecture descriptions, models and flow diagrams |
| Build, tests, quality gates or agent workflow | Contributor guidance, command references and AGENTS.md |

Use existing document owners; link instead of duplicating conventions. If a needed
document is missing, propose its purpose and location. Ask before adding a new
documentation category, template, generator or dependency. ADR creation and
maintenance are outside this skill; follow any separate project requirements.

## Update and validate

- Make approved, focused updates alongside the related code change. Describe the
  actual supported behavior, including limitations that affect the documented use.
- For generated docs and diagrams, edit the authoritative source and use the
  project's existing generator. Never hand-edit generated output. If regeneration
  is unavailable, report the source/output discrepancy explicitly.
- Use the project's existing link, documentation and diagram checks for the affected
  files. Verify examples and command names against their implementation; do not run
  destructive, production or credential-dependent examples just to check docs.
- Inspect the resulting diff for consistency, valid relative links and accidental
  unrelated changes. Report checks run and their results, and identify unrun checks.
  Do not claim rendered output is current without verifying it.

## Standalone audits

Agree the scope if unclear, then report drift ranked by user impact with `path:line`,
evidence and a concrete correction. Cover broken links, stale defaults/commands,
contradictory guidance and generated-source drift where applicable. An audit request
authorizes inspection, not edits; propose fixes and ask before applying them. If no
issues are found, state the inspected scope and limitations.
