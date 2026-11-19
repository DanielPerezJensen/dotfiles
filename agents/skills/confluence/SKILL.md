---
name: confluence
description: Plan and style Confluence pages with native elements (panels, status lozenges, expand, layouts, TOC) instead of raw Markdown. Reads page content the user provides and returns an edit plan with editor steps. Use when asked to "improve a Confluence page", "make this Confluence page look nice", "restructure a Confluence page", or "draft a Confluence page".
---

# Confluence Skill

This skill does not connect to Confluence. It has no scripts, no API calls, and no credentials. The user copies content in and applies the changes by hand in the Confluence editor.

## Rules

1. Never read, ask for, or handle credentials or API tokens.
2. Never call the Confluence or Atlassian API, MCP tools, or CLIs for this skill.
3. Work only from content the user provides: pasted text, a Markdown file, an HTML export, or storage XML.
4. Do not invent content. Keep the meaning of the page. Change structure and styling, not facts. Mark any gap as a question to the user.
5. Do not output raw Markdown as the final page. Output an edit plan that uses native Confluence elements.

## Workflow

1. Ask the user for the page content, if not given. Ask for the goal: new page, restructure, or restyle.
2. Choose a structure with the [page skeleton](references/editor_patterns.md#page-skeleton).
3. Map each part of the content to a native element. Use [editor_patterns.md](references/editor_patterns.md).
4. Give the result in the output format below.

## Output format

Return two parts.

**1. Edit plan.** A numbered list in page order. Each step has:

- Where: the heading or text the step applies to.
- Action: what to add, change, or move.
- How: the editor steps (for example, type `/info`, choose "Info panel", paste the text).
- Text: the exact final wording, in a code block the user can copy.

**2. Final text.** The full page text in reading order, with markers such as `[INFO PANEL: Summary]` and `[STATUS: DONE (green)]` where an element goes. The user can read it as a check against the plan.

Keep steps short. Group steps that need the same element. Put the highest-impact changes first.

## Style guide

- Start with an info panel that has a one or two sentence summary.
- Add a table of contents for pages with more than four headings.
- Use status lozenges for state. Use note, warning, and tip panels for callouts.
- Use tables for comparisons and lists of items with attributes.
- Use expand sections for long detail the reader may skip.
- Use two-column layouts only for side-by-side content.
- Use headings in order (h1 once, then h2, h3). Do not repeat the page title as the first heading.
- Keep one idea per paragraph. Use plain words.

## If the user pastes storage XML or HTML

Read it to find the current structure and macros. Keep macros the user did not ask to change. Describe changes as editor steps, not as XML. Give XML only if the user asks for it.
