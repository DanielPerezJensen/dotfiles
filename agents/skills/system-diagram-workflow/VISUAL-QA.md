# Visual QA checklist

Read every page PNG against every item. When an item is unclear at full size, crop and zoom:
`sips -c HEIGHT WIDTH --cropOffset Y X page.png --out crop.png`

1. All text sits inside its box, with no clipped words.
2. Every edge label is clear of boxes, frame borders and frame tabs, other labels, and other arrows.
3. Every arrow passes between boxes, never through one.
4. Every crossing was planned and is drawn with an arc.
5. Every frame contains all its members with padding, and every non-member sits outside it.
6. Every arrowhead ends a straight segment of at least 20 px.
7. Each icon renders as an image.
8. The title, legend, and notes are clear of the diagram, and the page has no large empty area.

## What the scripts cannot see

- `validate.py` checks routes only for arrows with explicit waypoints. Draw.io routes the others at render time, so only the PNG shows their path.
- `layout_qa.py` estimates text widths and label positions. Its `(approx)` findings come from auto-routed arrows.
- A clean script run does not make a page green. The PNG review decides.
