# Editor Patterns

How to build each element by hand in the Confluence editor. Menu names can differ by editor version. If a name does not match, type `/` and search for a similar word.

## Page skeleton

1. Info panel: summary
2. Table of contents (long pages only)
3. Headings (h2, h3) with the body content
4. Tables for comparisons, status lozenges for state
5. Expand sections for long detail
6. Final section: open questions or next steps

## Panels

| Goal | Steps |
|---|---|
| Info, note, warning, tip, success, error panel | Type `/`, then the panel name (for example `/info`). Type the text inside the panel. |
| Move existing text into a panel | Cut the text. Insert the panel. Paste inside it. |
| Change panel type | Click the panel. Use the icon in the panel toolbar. |

Use: info for summaries, note for caveats, warning for risk, tip for advice, success for confirmed results, error for failures.

## Status lozenge

1. Type `/status`.
2. Type the label in capitals, for example `IN PROGRESS`.
3. Choose a colour: grey (not started), blue (in progress), yellow (at risk), green (done), red (blocked).

Use one meaning per colour on the whole page.

## Table of contents

1. Place the cursor under the summary panel.
2. Type `/table of contents`.
3. In the macro options, set the heading levels to include (for example 2 to 3).

## Expand section

1. Type `/expand`.
2. Type the title. Type or paste the hidden content inside.

## Tables

1. Type `/table`, or use the table button.
2. Make the first row a header row (table options).
3. Use a status lozenge inside a cell for state columns.
4. Keep cells short. Move long text to an expand section or a paragraph under the table.

## Code

1. Type `/code`.
2. Choose the language. Paste the code.

## Layout: columns

1. Type `/layout`, or use the layout option in the toolbar.
2. Choose two or three columns.
3. Put content in each column.

Do not nest panels or expand sections inside narrow columns if they hold wide tables.

## Links and mentions

- Link to another page: type `[[` or `@` and the page name, or use Ctrl/Cmd+K.
- Mention a person: type `@` and the name.
- Jira issue: paste the issue URL or type the key. Confluence may offer a smart link.

## Images

1. Drag the image into the page, or type `/image`.
2. Add alt text. Set the width if it is too wide.
3. Add a caption as a normal paragraph under the image.

## Headings and text shortcuts

| Type | Result |
|---|---|
| `#` then space | Heading 1 (use `##` for 2, `###` for 3) |
| `-` then space | Bullet list |
| `1.` then space | Numbered list |
| `---` | Divider |
| ``` | Code block |
| `**text**` | Bold |

Use these shortcuts for fast entry. They apply while typing in the editor, not to pasted Markdown.

## Pasting content

Pasted Markdown often does not convert in the editor. Paste plain text first. Then apply the elements above.
