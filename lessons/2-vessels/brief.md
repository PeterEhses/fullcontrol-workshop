# Day 2 · Vessels

**Files:** `a-extrusion.py`, `b-continuous.py`, then `e1-silhouette.py`, `e2-vessel.py`
**Roughly:** 60 min · 90 min · rest of the day
**You need:** a laptop. A printer for the afternoon if there is one. A G-code viewer —
PrusaSlicer, or [gcode.ws](https://gcode.ws) in a browser.

## Context

Yesterday's path was a line, and a line has no thickness. What the printer lays down is
a bead about 1.45 mm wide and 0.48 mm tall, pressed flat into whatever is underneath it.
Yesterday's preview would have drawn 0.05 mm layer spacing without complaint; today the
preview draws at the real bead size and checks the result against the build volume.

Today's output is a vessel: one continuous bead from the bed to the rim.

## Python this adds

Writing your own function, with `if` and `return`. `radius_at` takes a number and returns
a number, and that one function is the entire silhouette of the object.

## Part A — Width, height, and the bed

Open `a-extrusion.py`. Same spiral as yesterday, now with volume.

1. Compare the preview to yesterday's. Same geometry, drawn as tubes at the real
   extrusion size instead of hairlines.
2. Open **The machine** and move extrusion width. The path is unchanged; the amount of
   plastic on it is not.
3. Push the shape off the bed — starting radius up, or radius growth up. The readout
   turns into a warning and tells you which limit you crossed.
4. Set layer height to `0.1`, leaving extrusion width at `1.45`.
5. Save a G-code file. Open it in a G-code viewer and check it against the plot.

### Parameters

| Control | Useful range | What it changes | Where it breaks |
|---|---|---|---|
| Extrusion width | 0.9–2.0 mm | Bead width; how much plastic per mm of path | Below ~0.9 mm the bead is taller than it is wide and falls over |
| Layer height | 0.3–0.6 mm | Bead height, and the rise per turn | Below ~0.25 mm the 1.45 mm bead has nowhere to spread |
| Turns | 1–80 | Height of the spiral | Past ~450 turns it exceeds the 220 mm gantry limit |
| Starting radius | 1–100 mm | Where the first lap sits | Off the bed past ~120 mm with growth |
| Radius growth | −2 to 4 mm/turn | Wall lean | Past ~0.7 mm/turn the wall overhangs its own support |

### What to observe

At 0.1 mm layer height with 1.45 mm width, the bead is fourteen times wider than it is
tall. The preview reports no problem, because it checks the build volume and nothing
else — it has no model of the plastic. On a machine, that much material has nowhere to
go: it spreads sideways into the previous lap and the nozzle ploughs through what it
just laid.

Keep that distinction. The preview tells you where the path goes, not whether the path
is printable. Day 3 works in the gap between the two.

## Part B — One continuous path

Open `b-continuous.py`.

A normal print does a lap, stops, steps up, does the next lap; every step is a seam and
a retraction. Here z climbs by a fraction of a layer at every segment, so the path never
stops. Slicers offer this as vase mode.

1. Each profile in turn. Note the height at which the wall leans furthest outward.
2. Segments per lap down to `5`. Still one continuous path, now a pentagonal vessel.
3. In `radius_at`, add `+ 0.05 * math.sin(fraction * math.pi * 8)` to the vase line.
   Eight ribs up the height.
4. Add `+ fraction * math.tau` to `angle` in the loop. The vessel twists once from the
   bed to the rim.
5. Choose **sphere** and look at the bottom. `math.sin(0)` is 0, so the first lap has no
   radius at all and the vessel stands on a point. Clamp `fraction` to a minimum of
   `0.15` at the top of `radius_at` and it stands on a disc instead. That is the first
   code in the workshop that checks where it is before deciding what to do.

### What to observe

**On screen:** the readout gives laps, points and confirms one unbroken path — no travel
moves, no retractions, no layer changes.

**On the bed:** each lap is held up by the one below, so what matters is how far it sits
outside that one. Past roughly half an extrusion width per lap — about 0.7 mm here — the
outer edge of the bead has nothing under it and sags on the way down. On the cone and
sphere profiles you can see exactly where that starts.

## Practice

**`e1-silhouette.py`** — repetition. One function to fill in, five shapes to make with
it: two cones, a barrel, a step, a stack of four steps. Each has a right answer and takes
one line. Two of them stand on a point and won't print, which is the same problem as the
sphere and the same fix.

**`e2-vessel.py`** — transfer. Your own silhouette and the loop that uses it, both
editable. The readout gives the steepest outward step per lap and says when it passes
what the bead can bridge. Print this one.

## With a printer

A vessel at 60–80 mm takes 20–40 minutes. Print at most one per person.

- Stay for the first three laps. A continuous path has no seam and no retraction, so if
  the first lap doesn't stick there is nothing to recover and the whole print will drag
  a ball of plastic around the bed.
- Watch where the wall leans out. Compare where it actually starts sagging against the
  number the readout gave you — they will not match exactly, and the difference is
  useful.
- If you deliberately went past the overhang threshold, stay at the machine for that
  section.
