# Day 1 - Tiles

Files: `a-points.py`, `b-loop.py`, then `e1-tile.py`, `e2-loop.py`, `e3-pattern.py`
You need: a laptop with the environment set up. A printer is useful at the end, not required.

## Context

A 3D print is a list of positions with the extruder on or off, visited in the order you
give. No model and no slicer in between — you write the list, and the list is the design.
Today's output is flat: a tile, a lattice, a panel. One layer.

## Python this adds

A list, a `for` loop, a counter, `math.sin` / `math.cos`. `e3-pattern.py` also puts one
loop inside another to walk a grid.

## Part A — Five points

`a-points.py`, the only notebook that runs as an app with the code hidden.

1. Move Size. The square scales.
2. Lift per corner above 0. The four corners sit at four different heights. Nothing was
   re-modelled or re-sliced; the numbers in the list changed.
3. Untick Return to the start. The path stops at the fourth corner.
4. Tick Show code. Five points, all visible at once.
5. Read the G-code block against them. Five points, five `G1` lines. `X` and `Y` are
   position, `Z` height, `E` how much plastic to push out on the way there.

### What to observe

One point in the code is one line of G-code. The rest of the week is ways of producing
that list without typing it.

## Part B — The loop

`b-loop.py`. Code is visible from here on. Read it once before touching the sliders.

1. Move each slider and watch the plot.
2. Rise per turn to `0`. A flat spiral, one layer — a tile.
3. Radius growth negative. The spiral winds inward, passes through zero radius and comes
   out unwinding, offset by half a turn.
4. Points per turn to `3`, then `4`, then `6`. A circle drawn with six points is a
   hexagon. The loop didn't change, only how often it stops.
5. Add a second `steps.append(...)` inside the loop using `angle + math.pi`. Two spirals
   half a turn apart, still one path.

### Parameters

| Control | Useful range | What it changes | Where it breaks |
|---|---|---|---|
| Turns | 1-60 | How many laps the path makes | Above ~40 at low rise, laps overlap into each other |
| Starting radius | 1-50 mm | Radius at the first point | Below ~2 mm the points are closer than the bead is wide |
| Radius growth | -2 to 2 mm/turn | Spacing between laps | Below 1.45 mm/turn (one extrusion width) laps touch or merge |
| Rise per turn | 0-2 mm | Height gained each lap | `0` is a flat tile; below 0.48 mm laps overlap vertically |
| Points per turn | 3-120 | How round the circle is | Below ~12 it is visibly a polygon; above ~60 nothing changes |

### What to observe

Set rise to `0.05` and turns to `60`. The preview draws it happily. Those laps are
0.05 mm apart and the printer lays a bead 0.48 mm tall, so each would be buried in the
nine below it. The preview has no model of the plastic — it draws whatever list you give
it. That distinction is day 2.

## Practice

Three notebooks, one editable thing in each.

`e1-tile.py` — repetition. A list of coordinates. Change them, add more, design a tile.
Part A with the plumbing out of sight.

`e2-loop.py` — repetition. The same tile from a loop. `offset_at` is called once per point
and returns where it goes; it draws a 60-point circle. Five stated changes, each with a
right answer you can see: bigger, fewer points, a spiral, every second point pulled in.

`e3-pattern.py` — transfer. Your cell shape, repeated across a grid by two loops. A panel,
a lattice or a grille. This is the one to print.

## With a printer

A flat tile is the safest thing you will print this week.

Watch the first layer go down. If the bead is not sticking, or is being dragged around
rather than laid down, stop the print. Adjacent lines should touch: gaps mean your point
spacing is wider than the 1.45 mm bead, ridges mean it is narrower. Let it cool before
removing it — a one-layer part distorts if you lever it off warm.
