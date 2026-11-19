#!/usr/bin/env python3
"""Estimate text fit and label collisions in a draw.io file.

Complements drawio-skill's validate.py, which checks geometry but not text.
Text widths use approximate Helvetica metrics with a 5 % safety margin, so
results are estimates. Calibrate against a PNG export before you trust them.

  python3 layout_qa.py diagram.drawio [--page N]

Findings (exit status 1 when any error is found):
  text-overflow        label wider or taller than its box
  label-over-box       edge label overlaps a box
  label-straddles-frame edge label crosses the border of a container
  label-over-label     two edge labels overlap
  label-over-edge      edge label sits on another edge (warning)

Labels placed outside their shape (labelPosition, verticalLabelPosition=bottom)
are not checked for fit.

Edge label positions are estimated at the midpoint of the route. Edges with no
waypoints are auto-routed by draw.io, so their label boxes are marked "approx".
"""
import argparse
import html
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path.home() / ".agents/skills/drawio-skill/scripts"))
from validate import abs_rect, edge_route, endpoint, rect, style_num  # noqa: E402

INSET = 6
INSET_V = 2
LINE = 1.2
SAFETY = 1.05
BOLD = 1.08
TITLE_PAD = 12


def char_w(c):
    if c in "il.,:;'!|ft ":
        return 0.28
    if c in "jr":
        return 0.36
    if c in "mwMW@%":
        return 0.86
    if c.isupper():
        return 0.68
    if c.isdigit():
        return 0.56
    return 0.55


def text_width(text, size, bold):
    return sum(char_w(c) for c in text) * size * (BOLD if bold else 1.0) * SAFETY


SEP = re.compile(r"<br\s*/?>|</?div[^>]*>|</?p[^>]*>|</?li[^>]*>|</?ul[^>]*>", re.I)


def html_segments(value, base_size, bold_default):
    """Return [(text, size, bold)] for each visual line of a draw.io label."""
    out = []
    for seg in SEP.split((value or "").replace("&nbsp;", " ")):
        text = html.unescape(re.sub(r"<[^>]+>", "", seg)).strip()
        if not text:
            continue
        sizes = re.findall(r"font-size:\s*(\d+(?:\.\d+)?)px", seg)
        size = float(sizes[-1]) if sizes else base_size
        out.append((text, size, bold_default or "<b>" in seg))
    return out


def wrapped_lines(text, size, bold, avail):
    lines, current = 1, ""
    for word in text.split(" "):
        trial = (current + " " + word).strip()
        if not current or text_width(trial, size, bold) <= avail:
            current = trial
        else:
            lines += 1
            current = word
    return lines


def fit_findings(cell, box, style):
    value = cell.get("value") or ""
    _, _, w, h = box
    base = style_num(style, "fontSize") or 12
    bold = "fontStyle=1" in style
    segs = html_segments(value, base, bold)
    if not segs:
        return []
    if "labelPosition=" in style or "verticalLabelPosition=bottom" in style:
        return []
    avail_w = w - 2 * INSET
    findings = []
    if "container=1" in style or "umlFrame" in style or "swimlane" in style:
        for text, size, b in segs:
            if text_width(text, size, b) > w - TITLE_PAD:
                findings.append(f"text-overflow: title '{text}' wider than frame ({w:g}px)")
        return findings
    wrap = "whiteSpace=wrap" in style
    need_h = 0.0
    for text, size, b in segs:
        if wrap:
            longest = max(text_width(word, size, b) for word in text.split(" "))
            if longest > avail_w:
                findings.append(f"text-overflow: word in '{text[:40]}' wider than box")
            n = wrapped_lines(text, size, b, avail_w)
        else:
            n = 1
            if text_width(text, size, b) > avail_w:
                findings.append(f"text-overflow: line '{text[:40]}' wider than box")
        need_h += n * size * LINE
    if need_h + 2 * INSET_V > h:
        findings.append(f"text-overflow: needs ~{need_h + 2 * INSET_V:.0f}px height, box has {h:g}px")
    return findings


def seg_hits_box(p, q, box, eps=0.0):
    """Liang-Barsky test: does segment p-q pass through the box interior?"""
    x, y, w, h = box
    xmin, xmax, ymin, ymax = x + eps, x + w - eps, y + eps, y + h - eps
    dx, dy = q[0] - p[0], q[1] - p[1]
    t0, t1 = 0.0, 1.0
    for pk, qk in ((-dx, p[0] - xmin), (dx, xmax - p[0]), (-dy, p[1] - ymin), (dy, ymax - p[1])):
        if pk == 0:
            if qk < 0:
                return False
            continue
        r = qk / pk
        if pk < 0:
            if r > t1:
                return False
            t0 = max(t0, r)
        else:
            if r < t0:
                return False
            t1 = min(t1, r)
    return t0 <= t1


def polyline_midpoint(points):
    total = sum(((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5 for a, b in zip(points, points[1:]))
    if total == 0:
        return points[0]
    target, walked = total / 2, 0.0
    for a, b in zip(points, points[1:]):
        seg = ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5
        if walked + seg >= target and seg:
            f = (target - walked) / seg
            return (a[0] + f * (b[0] - a[0]), a[1] + f * (b[1] - a[1]))
        walked += seg
    return points[-1]


def edge_offset(edge):
    g = edge.find("mxGeometry")
    if g is None:
        return (0.0, 0.0)
    for pt in g.findall("mxPoint"):
        if pt.get("as") == "offset":
            return (float(pt.get("x", 0)), float(pt.get("y", 0)))
    return (0.0, 0.0)


def label_box(edge, by_id):
    value = edge.get("value") or ""
    segs = html_segments(value, style_num(edge.get("style") or "", "fontSize") or 11, False)
    if not segs:
        return None, None
    base = style_num(edge.get("style") or "", "fontSize") or 11
    lw = max(text_width(t, s, b) for t, s, b in segs) + 4
    lh = sum(s * LINE for _, s, _ in segs) + 2
    route = edge_route(edge, by_id)
    approx = route is None
    if route is None:
        s, t = endpoint(edge, "source", by_id), endpoint(edge, "target", by_id)
        if s is None or t is None:
            return None, None
        route = [s, t]
    cx, cy = polyline_midpoint(route)
    ox, oy = edge_offset(edge)
    cx, cy = cx + ox, cy + oy
    return (cx - lw / 2, cy - lh / 2, lw, lh), approx


def known_route(edge, by_id):
    """Explicit route, or a straight segment when source and target are aligned."""
    route = edge_route(edge, by_id)
    if route is not None:
        return route
    s, t = endpoint(edge, "source", by_id), endpoint(edge, "target", by_id)
    if s and t and (abs(s[0] - t[0]) < 1 or abs(s[1] - t[1]) < 1):
        return [s, t]
    return None


def check_page(index, diagram):
    name = diagram.get("name", f"page {index}")
    root = diagram.find("mxGraphModel/root")
    if root is None:
        return [f"page {index} '{name}': no mxGraphModel"]
    cells = [c for c in root.iter("mxCell") if c.get("id") not in (None, "0", "1")]
    by_id = {c.get("id"): c for c in cells}
    parents_of = {}
    for c in cells:
        parents_of.setdefault(c.get("parent"), []).append(c)
    containers = {cid for cid, kids in parents_of.items() if cid in by_id and any(k.get("vertex") == "1" for k in kids)}
    findings = []
    boxes, labels = {}, []
    for c in cells:
        cid = c.get("id")
        style = c.get("style") or ""
        if c.get("edge") == "1":
            box, approx = label_box(c, by_id) if (c.get("value") or "").strip() else (None, None)
            if box:
                labels.append((cid, box, approx))
            continue
        if c.get("vertex") != "1" or "edgeLabel" in style:
            continue
        box = abs_rect(c, by_id)
        if box is None:
            continue
        boxes[cid] = (box, cid in containers or "container=1" in style or "umlFrame" in style or "swimlane" in style)
        for msg in fit_findings(c, box, style):
            findings.append(f"page {index} '{name}': {msg} [{cid}]")
    routes = {c.get("id"): known_route(c, by_id) for c in cells if c.get("edge") == "1"}
    for cid, box, approx in labels:
        tag = " (approx)" if approx else ""
        edge_id = cid
        for bid, (b, is_frame) in boxes.items():
            if is_frame:
                inter = not (box[0] + box[2] <= b[0] or b[0] + b[2] <= box[0] or box[1] + box[3] <= b[1] or b[1] + b[3] <= box[1])
                inside = b[0] <= box[0] and box[0] + box[2] <= b[0] + b[2] and b[1] <= box[1] and box[1] + box[3] <= b[1] + b[3]
                if inter and not inside:
                    findings.append(f"page {index} '{name}': label-straddles-frame{tag}: label of {edge_id} crosses frame {bid}")
            elif not (box[0] + box[2] <= b[0] or b[0] + b[2] <= box[0] or box[1] + box[3] <= b[1] or b[1] + b[3] <= box[1]):
                findings.append(f"page {index} '{name}': label-over-box{tag}: label of {edge_id} overlaps {bid}")
        for oid, obox, _ in labels:
            if oid <= edge_id:
                continue
            if not (box[0] + box[2] <= obox[0] or obox[0] + obox[2] <= box[0] or box[1] + box[3] <= obox[1] or obox[1] + obox[3] <= box[1]):
                findings.append(f"page {index} '{name}': label-over-label{tag}: {edge_id} and {oid}")
        for rid, route in routes.items():
            if rid == edge_id or not route:
                continue
            if any(seg_hits_box(p, q, box) for p, q in zip(route, route[1:])):
                findings.append(f"page {index} '{name}': label-over-edge{tag}: label of {edge_id} sits on {rid}")
    return findings


def main():
    ap = argparse.ArgumentParser(description="Estimate text fit and label collisions.")
    ap.add_argument("file")
    ap.add_argument("--page", type=int, help="1-based page number; default all pages")
    args = ap.parse_args()
    tree = ET.parse(args.file)
    pages = tree.getroot().findall("diagram") or [tree.getroot()]
    findings = []
    for i, page in enumerate(pages, start=1):
        if args.page and i != args.page:
            continue
        findings += check_page(i, page)
    for f in findings:
        print(f)
    errors = [f for f in findings if "label-over-edge" not in f]
    print(f"{len(errors)} error(s), {len(findings) - len(errors)} warning(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
