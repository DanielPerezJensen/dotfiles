---
name: system-diagram-workflow
description: Source-grounded architecture diagrams in draw.io. Use when drawing or revising C4 context, container, or component views of a system or codebase.
---

Each page goes from **evidence** to an Archify check, then a sketch, then a draw.io build taken to **green**.

- **Evidence**: a fact backed by a pinned commit and a `file:line` range, or a fact the user stated.
- **Green**: a page where every check in step 6 passes.

## Steps

1. **Gather evidence.** For each repository, run `git fetch --prune origin` and record `HEAD`, the origin URL, and dirty files. Read the entry points, configuration, deployment files, and call sites behind every element and arrow you plan to draw.
   Done when every planned element and arrow has evidence, and every gap is written down as a question.

2. **Interview.** Load the `grilling` skill. Ask the decision frontier in rounds, with a recommended answer for each question. Look facts up yourself; put decisions to the user.
   Done when the frontier is empty and the user has confirmed the summary.

3. **Archify check.** Load the `archify` skill. Draw every level (L1, L2, L3) as a native diagram, with sources and the pinned commit. Run `finalize` for each.
   Done when every level's `finalize` receipt passes and the user has confirmed the structure of each level.

4. **Sketch.** For each draw.io page, write a text sketch: elements by position, frames, arrows with their labels, legend, and notes.
   Done when the user has approved the sketch for that page.

5. **Build.** Load the `drawio-skill` skill and read its `references/xml-authoring.md`. Hand-place the approved sketch on a planned grid, styled per [DRAWIO-STYLE.md](DRAWIO-STYLE.md). Use automatic layout only above about 15 nodes. When the user already has a file, back it up, edit only the pages in scope, and keep the user's text.
   Done when the page is green (step 6).

6. **QA to green.** For each page:
   - `python3 ~/.agents/skills/drawio-skill/scripts/validate.py FILE --score`: 0 errors. Score 0, or each remaining crossing is approved by the user and drawn with `jumpStyle=arc`.
   - `python3 ~/.agents/skills/system-diagram-workflow/scripts/layout_qa.py FILE --page N`: 0 errors, or each finding is checked in the PNG and dismissed with a reason.
   - Export the page with `drawio -x -f png --page-index N --width 2000 -b 10`, read the PNG, and pass every item in [VISUAL-QA.md](VISUAL-QA.md).

   Fix findings with [LAYOUT-FIXES.md](LAYOUT-FIXES.md), then run all three checks again.
   Done when the page is green.

7. **Text.** Load the `no-ai-slop` skill and apply it to every title, label, and note. Write without em dashes. Run step 6 again for every page you changed.
   Done when every page is green after the edits.

8. **Handoff.** Export each page with `-e -s 2`, then run `drawio-skill/scripts/repair_png.py` on each PNG. Commit only to a branch the user has named.
   Done when the user has the file paths, the QA result per page, and the backup path.
