# Day 1 · Tiles

**Files:** `a-points.py`, `b-loop.py`, then `e1-tile.py`, `e2-loop.py`, `e3-pattern.py`
**Roughly:** 30 min · 90 min · rest of the day
**You need:** a laptop with the environment set up. A printer is useful at the end but
not required.

## Context

A 3D print is a list of positions with the extruder switched on or off, and the printer
visits them in the order you give. There is no model and no slicer in this workshop —
you write the list, and that list is the design.

Today's output is flat: a tile, a lattice, a panel. One layer, a few minutes on the bed,
something you can hold by the end of the day.

## Python this adds

A list, a `for` loop, a counter, and `math.sin` / `math.cos`. The tile exercise also uses
one loop inside another to walk a grid.

## Part A — Five points

Open `a-points.py`. This is the only notebook in the workshop that runs as an app with
the code hidden; from part B onward the code is on screen.

1. Move **Size**. The square scales.
2. Set **Lift per corner** above 0. The four corners are now at four different heights.
   Nothing was re-modelled or re-sliced — the numbers in the list changed.
3. Untick **Return to the start**. The path stops at the fourth corner.
4. Tick **Show code**. Five points, all visible at once.
5. Read the G-code block against them. Five points, five `G1` lines. `X` and `Y` are the
   position, `Z` the height, `E` how much plastic to push out on the way there.

### What to observe

The relationship between one point in the code and one line of G-code is exactly
one-to-one. Everything for the rest of the week is a way of producing that list without
typing it.

## Part B — The loop

Open `b-loop.py`. The code is visible from here on; read it once before touching the
sliders.

1. Move each slider and watch the plot. Get a feel for what each one does first.
2. Rise per turn to `0`. A flat spiral, one layer — this is a tile.
3. Radius growth negative. The spiral winds inward, passes through zero radius, and
   comes out the other side unwinding, offset by half a turn.
4. Points per turn to `3`, then `4`, then `6`. A circle drawn with six points is a
   hexagon. The loop didn't change; only how often it stops.
5. In the code, add a second `steps.append(...)` inside the loop using `angle + math.pi`.
   Two spirals half a turn apart, still one path.

### Parameters

| Control | Useful range | What it changes | Where it breaks |
|---|---|---|---|
| Turns | 1–60 | How many laps the path makes | Above ~40 at low rise, laps overlap into each other |
| Starting radius | 1–50 mm | Radius at the first point | Below ~2 mm the points are closer than the bead is wide |
| Radius growth | −2 to 2 mm/turn | Spacing between laps | Below 1.45 mm/turn (one extrusion width) laps touch or merge |
| Rise per turn | 0–2 mm | Height gained each lap | `0` is a flat tile; below 0.48 mm laps overlap vertically |
| Points per turn | 3–120 | How round the circle is | Below ~12 it is visibly a polygon; above ~60 nothing changes |

### What to observe

Set rise to `0.05` and turns to `60`. The preview draws it happily. Those laps are
0.05 mm apart and this printer lays a bead 0.48 mm tall, so each lap would be buried in
the nine below it. The preview has no model of the plastic — it draws whatever list you
give it. That distinction is day 2.

## Practice

Three small notebooks. Each has one thing in it that you edit and nothing else.

**`e1-tile.py`** — repetition. A list of coordinates. Change them, add more, design a
tile. This is the whole of part A with the plumbing out of sight.

**`e2-loop.py`** — repetition. The same tile from a loop. `offset_at` is called once per
point and returns where it goes; it draws a 60-point circle. Five stated changes, each
with a right answer you can see: bigger, fewer points, a spiral, every second point
pulled in.

**`e3-pattern.py`** — transfer. Your cell shape, repeated across a grid by two loops.
Design a panel, a lattice or a grille. This is the one to print.

## With a printer

A flat tile prints in a few minutes and is the safest thing you will print this week.

- Watch the first layer go down. If the bead is not sticking to the bed, or is being
  dragged around rather than laid down, stop the print rather than letting it run.
- Adjacent lines should touch. If there are gaps between them, your point spacing is
  wider than the 1.45 mm bead; if the nozzle is pushing up ridges, it is narrower.
- Let it cool before removing it. A one-layer part will distort if you lever it off warm.
