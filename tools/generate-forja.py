#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""Regenerates forja/*.dxf with forja-cli: every drawing is built from engine commands, so
the files are Nodalia's own work. Usage: generate-forja.py [FORJA_CLI] [OUT_DIR]
(defaults: `forja-cli` on PATH, ../forja). Needs forja-cli 0.3 or newer."""
import json, os, subprocess, sys

B = sys.argv[1] if len(sys.argv) > 1 else "forja-cli"
OUT = os.path.abspath(sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(__file__), "..", "forja"))
os.makedirs(OUT, exist_ok=True)
env = dict(os.environ, FORJA_CONFIG_DIR="")


def run(name, cmds, ext="dxf"):
    args = [B, "run", "--metric"]
    for c, p in cmds:
        args += ["--cmd", f"{c} {json.dumps(p)}"]
    args += ["--save", os.path.join(OUT, f"{name}.{ext}")]
    r = subprocess.run(args, capture_output=True, text=True, env=env)
    bad = [l for l in (r.stdout + r.stderr).splitlines() if "rror" in l or "nvalid" in l or "nknown" in l]
    if r.returncode or bad:
        sys.exit(f"{name}: {'; '.join(bad) or r.returncode}")
    print("wrote", name + "." + ext)


run("basic-shapes", [
 ("rectang", {"p1": [0, 0], "p2": [100, 60]}),
 ("circle", {"center": [50, 30], "radius": 20}),
 ("arc", {"center": [50, 30], "radius": 28, "start": 20, "end": 160}),
 ("line", {"points": [[0, 0], [100, 60]]}),
 ("line", {"points": [[0, 60], [100, 0]]}),
 ("ellipse", {"center": [50, 30], "major": [45, 0], "ratio": 0.4}),
 ("donut", {"center": [15, 15], "inside": 3, "outside": 6}),
])
run("plate-with-text", [
 ("pline", {"vertices": [[0, 0], [80, 0], [80, 40], [40, 60], [0, 40]], "closed": True}),
 ("circle", {"center": [20, 20], "radius": 5}),
 ("circle", {"center": [60, 20], "radius": 5}),
 ("text", {"at": [5, -8], "text": "Plate A-100", "height": 4}),
 ("text", {"at": [40, 30], "text": "Centred", "height": 3, "justify": "MC"}),
 ("mtext", {"at": [90, 55], "text": "Material: mild steel\\PThickness: 6 mm", "height": 2.5, "width": 60}),
])
run("layers-and-linetypes", [
 ("layer.new", {"name": "WALLS", "color": 1, "lineweight": 0.5}),
 ("layer.new", {"name": "DOORS", "color": 3}),
 ("layer.new", {"name": "HIDDEN", "color": 5}),
 ("layer.set", {"name": "WALLS", "current": True}) ,
 ("rectang", {"p1": [0, 0], "p2": [500, 300]}),
 ("rectang", {"p1": [200, 0], "p2": [500, 300]}),
 ("layer.set", {"name": "DOORS", "current": True}),
 ("arc", {"center": [200, 0], "radius": 80, "start": 0, "end": 90}),
 ("line", {"points": [[200, 0], [280, 0]]}),
 ("layer.set", {"name": "HIDDEN", "frozen": False, "current": True}),
 ("line", {"points": [[0, 150], [500, 150]]}),
])
run("curves", [
 ("spline", {"fit": [[0, 0], [20, 30], [50, 10], [80, 40], [110, 0]]}),
 ("spline.cv", {"control": [[0, -30], [25, -60], [55, -10], [90, -50]], "degree": 3}),
 ("ellipse", {"center": [60, 80], "major": [40, 10], "ratio": 0.5, "start": 0, "end": 270}),
 ("pline", {"vertices": [[0, 100], {"p": [30, 100], "bulge": 0.5}, [60, 130], {"p": [90, 100], "bulge": -0.3}, [120, 100]]}),
])
run("hatch-and-dimensions", [
 ("rectang", {"p1": [0, 0], "p2": [120, 70]}),
 ("circle", {"center": [60, 35], "radius": 18}),
 ("hatch", {"points": [[5, 5]], "pattern": "ANSI31", "scale": 2}),
 ("dimlinear", {"p1": [0, 0], "p2": [120, 0], "at": [60, -15]}),
 ("dimlinear", {"p1": [120, 0], "p2": [120, 70], "at": [140, 35]}),
])
run("hole", [
 ("circle", {"center": [0, 0], "radius": 4}),
 ("line", {"points": [[-6, 0], [6, 0]]}),
 ("line", {"points": [[0, -6], [0, 6]]}),
])
run("blocks-and-inserts", [
 ("rectang", {"p1": [0, 0], "p2": [100, 60]}),
 ("insert", {"name": "HOLE", "file": os.path.join(OUT, "hole.dxf"), "at": [10, 10]}),
 ("insert", {"name": "HOLE", "at": [90, 10], "scale": 1.5, "rotation": 45}),
 ("minsert", {"name": "HOLE", "at": [30, 30], "rows": 2, "columns": 4, "rowSpacing": 15, "columnSpacing": 15}),
])
