# Draw.io house style

These are the defaults the user approved. Ask before you change them.

## Layout

- Put the legend in one row under the title: color swatches, then a "call" line sample and an "identity / secrets flow" line sample. List only the roles that the page uses.
- Place callers and people on the left, our system in the middle, and external systems in a column on the right.
- Group external systems in dashed frames, one per provider: a cloud platform, an API gateway, a SaaS vendor, or a set of peer services. Give each frame a small vendor icon (about 30 px) at the right end of its tab. Get icon styles with `drawio-skill/scripts/shapesearch.py`.
- Put notes at the bottom left and footnotes under the notes.

## Palette

| Role | Fill | Stroke | Shape |
|---|---|---|---|
| Service frame | `#d6b656` | `#b09500` | `shape=umlFrame;container=1;pointerEvents=0` |
| Component inside a service | `#f5f5f5` | `#666666` | rounded box |
| External system or frame | `#dae8fc` | `#6c8ebf` | `dashed=1` |
| Infra / orchestration (runtime platform frame, platform services) | `#e1d5e7` | `#9673a6` | box or `umlFrame` |
| Actor | `#fff2cc` | `#d6b656` | `shape=umlActor`, label on the right |

## Arrows and labels

- Calls: `edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;fontSize=10;labelBackgroundColor=#ffffff;endArrow=block;endFill=1;`
- Identity and secrets flows: the call style plus `dashed=1;strokeColor=#b85450;fontColor=#b85450;`
- Edge labels read "purpose · protocol", or purpose only when the user prefers that.
- Box labels: a bold title, then 10 px sublabels for the class name, the technology, or the endpoint.
