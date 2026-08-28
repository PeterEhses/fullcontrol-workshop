# Day 2 - Vessels

Files: `a-extrusion.py`, `b-continuous.py`, then `e1-silhouette.py`, `e2-vessel.py`
You need: a laptop. A printer for the afternoon if there is one. A G-code viewer —
PrusaSlicer, or [gcode.ws](https://gcode.ws) in a browser.

## Context

Yesterday's path was a line, and a line has no thickness. What the printer lays down is a
bead about 1.45 mm wide and 0.48 mm tall, pressed flat into whatever is underneath. From
today the preview draws at the real bead size and checks the result against the build
volume.

That bead size is not one number for the whole print. It can be set per segment, which
makes flow a thing you draw with rather than a setting you get right once. Part A does
that on a stack of layers. Part B removes the layers.

Today's output is a vessel: one continuous bead from the bed to the rim.

## Python this adds

Writing your own function, with `if` and `return`. `radius_at` takes a number and returns
a number, and that one function is the whole silhouette of the object.

Part A adds no new Python. It uses `math.floor` and the `math.sin` from day 1, and puts a
second kind of object in the `steps` list — `fc.ExtrusionGeometry`, which sets the bead
size from that point onward. The list is not only points.

## Part A — Width, height, and the bed

`a-extrusion.py`. Yesterday's spiral, now with volume and with layers.

1. Compare the preview to yesterday's. Two things changed. The path is drawn as tubes at
   the real extrusion size instead of hairlines, and z now holds flat for a whole lap and
   steps up between laps. Yesterday's was a helix; this is a stack.
2. Open The machine and move extrusion width. The path is unchanged; the amount of
   plastic on it is not.
3. Push the shape off the bed — starting radius up, or radius growth up. The readout
   turns into a warning naming the limit you crossed.
4. Layer height to `0.1`, leaving extrusion width at `1.45`.
5. Open Flow. Variation to `0.5`, bulges per lap to `6`. The bead now swells and thins as
   it goes round — a knurled wall from one line of `math.sin`.
6. Bulges per lap to `4`, then `4.5`, then `4`. At `4` every lap bulges in the same four
   places and they stack into vertical ribs. At `4.5` each lap lands opposite the one
   below and the ribs spiral. Nothing changed but half a unit.
7. Drift to `-0.8`, variation back to `0`. The wall starves as it rises and goes lacy at
   the top.
8. Variation to `2.0`. Read the warning, then look at the preview, which draws it anyway.
9. Save a G-code file, open it in a viewer, check it against the plot.

### Parameters

| Control | Useful range | What it changes | Where it breaks |
|---|---|---|---|
| Extrusion width | 0.9-2.0 mm | Bead width; how much plastic per mm of path | Below ~0.9 mm the bead is taller than it is wide and falls over |
| Layer height | 0.3-0.6 mm | Bead height, and the rise between laps | Below ~0.25 mm the 1.45 mm bead has nowhere to spread |
| Turns | 1-80 | Height of the stack | Past ~450 turns it exceeds the 220 mm gantry limit |
| Starting radius | 1-100 mm | Where the first lap sits | Off the bed past ~120 mm with growth |
| Radius growth | -2 to 4 mm/turn | Wall lean | Past ~0.7 mm/turn the wall overhangs its own support |
| Variation | 0-0.5 | How far the bead swells and thins | Past ~0.32 the fattest bead exceeds 4× the layer height; by 1.0 it is 2 mm and piling up |
| Bulges per lap | 0-24 | Where the swelling lands | Above ~20 the bulges are finer than the bead is wide, so they blur into a smooth wall |
| Drift | -0.3 to 0.3 | Flow ramp from bed to top | Below ~-0.34 the top drops under 2× the layer height and goes porous; above ~0.33 it over-extrudes |

### What to observe

On screen: bulges per lap is one number that produces three different objects. A whole
number stacks into a rib, a half lands opposite each lap, anything else drifts round and
spirals. The pulse is counted in whole turns, not in position around the lap, and that is
the entire reason.

At 0.1 mm layer height with 1.45 mm width the bead is fourteen times wider than it is
tall. The readout catches that, because a ratio is a number about the bead. What it cannot
catch is what the plastic does afterwards.

On the bed: at variation `0.5` the bulges are a surface. Past about `1.0` they are a
problem — material builds where the flow spikes, and the nozzle meets it again on the next
lap. Under-extruded sections do the opposite and simply leave gaps.

The preview tells you where the path goes, not what the material does when it gets there.
Day 3 works in the gap between the two.

## Part B — One continuous path

`b-continuous.py`.

Part A did a lap, stopped, stepped up, did the next lap — that step is a seam and a
retraction, once per layer, all the way up. Here z climbs by a fraction of a layer at
every segment instead, so the path never stops. Slicers offer this as vase mode.

1. Each profile in turn. Note the height at which the wall leans furthest outward.
2. Segments per lap down to `5`. Still one continuous path, now a pentagonal vessel.
3. In `radius_at`, add `+ 0.05 * math.sin(fraction * math.pi * 8)` to the vase line.
   Eight ribs up the height.
4. Add `+ fraction * math.tau` to `angle` in the loop. The vessel twists once from bed to
   rim.
5. Choose sphere and look at the bottom. `math.sin(0)` is 0, so the first lap has no
   radius and the vessel stands on a point. Clamp `fraction` to a minimum of `0.15` at the
   top of `radius_at` and it stands on a disc. That is the first code in the workshop that
   checks where it is before deciding what to do.

### What to observe

On screen: the readout gives laps, points, and confirms one unbroken path — no travel
moves, no retractions, no layer changes.

On the bed: each lap is held up by the one below, so what matters is how far it sits
outside that one. Past roughly half an extrusion width per lap — about 0.7 mm here — the
outer edge of the bead has nothing under it and sags on the way down. The cone and sphere
profiles show exactly where that starts.

## Practice

`e1-silhouette.py` — repetition. One function to fill in, five shapes to make with it: two
cones, a barrel, a step, a stack of four steps. Each takes one line and has a right
answer. Two of them stand on a point and won't print, which is the sphere's problem and
the sphere's fix.

`e2-vessel.py` — transfer. Your own silhouette and the loop that uses it, both editable.
The readout gives the steepest outward step per lap and says when it passes what the bead
can bridge. Print this one.

## With a printer

Print at most one vessel per person, at 60-80 mm.

If you print a flow-modulated wall from Part A, keep variation at or below `0.5` and print
it short — 20 mm. Above that the fat sections put down more plastic than the layer has
room for, it builds on the outside of the nozzle, and the nozzle collides with it on the
next lap. If the head starts dragging or knocking the part, stop the print. The starved
version is the safe direction: a wall with gaps in it is a weak part, not a damaged
machine.

Stay for the first three laps. A continuous path has no seam and no retraction, so if the
first lap doesn't stick there is nothing to recover and the print will drag a ball of
plastic around the bed. Watch where the wall leans out and compare it against the number
the readout gave you — they will not match exactly, and the difference is useful. If you
deliberately went past the overhang threshold, stay at the machine for that section.
