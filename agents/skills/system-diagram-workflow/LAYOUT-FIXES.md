# Layout fixes

A **corridor** is an empty band between rows or columns of boxes, kept free for arrows and labels. Plan corridors in the sketch, and route long arrows through them.

| Finding | Fix |
|---|---|
| Label crosses a frame border or tab | Move the label into a corridor with `<mxPoint x="DX" y="DY" as="offset"/>`. Split it over two lines with `<br>`. Widen the gap between the frames. |
| Label overlaps a box or another label | Widen the gap to about `6.5 px × characters + 21 px`. Move the label to the longest straight segment of its route. |
| Text overflows its box | Widen or heighten the box. Shorten the sublabel. Keep `whiteSpace=wrap`. |
| Arrow passes through a box | Pin `exitX/exitY` and `entryX/entryY`. Add waypoints in `<Array as="points">` along a corridor. Move the box out of the path. |
| Arrows stack on one side of a box | Spread the ends over even slots, for example `exitY` 0.2, 0.4, 0.7, 0.9. `drawio-skill/scripts/edgeports.py` does this for a whole file. |
| Unplanned crossing | Place each target on the side of its source. Nest L-shaped routes so that the outer source turns at the outer corridor. An unavoidable crossing gets `jumpStyle=arc;jumpSize=10`. |
| Vertical arrow hits a frame tab | Route it outside the x range of the tab, or narrow the tab with the `width=` value in the frame style. |
| Nested frame sticks out of its parent | Raise the parent's padding, or shorten the inner frame's title. |
| Large empty area | Move the whole group by the same offset: shift every vertex and every waypoint. |

After each fix, run all of step 6 again. A fix often moves a defect to another place.
