# Day 4 · Studio

**Files:** `a-conditions.py`, `e1-attractor.py`, `studio.py`
**Roughly:** 75 min · 45 min · rest of the day, then the closing session
**You need:** a laptop. A printer, if there is one, for whatever people want to run.

## Context

Days 1 to 3 each gave you a product type and a worked example: a tile, a vessel, a
noodle. Today gives you neither. That is a change in how the day works, not a reveal that
the earlier days were scaffolding — you learned the tool and the material by making three
real things, and this is the point where the examples stop.

One short notebook first, and it is not a summary of the week. You have been stacking
modulations since day 3 — fusilli is ridges plus twist, cavatappi is ridges plus twist
plus a coiled axis — so that idea is already yours and doesn't need re-teaching.

What hasn't appeared in four days is code that asks a question about a point before
deciding what to do with it. Everything so far has been a smooth function of position:
same height and angle, same answer, everywhere on the object. That is one way to write
this, and not the only one.

## Python this adds

`if` used on a measured quantity rather than on a setting — the distance between two
points, whether an angle falls within a range, whether a coordinate went past a limit.
`math.dist`, and the modulo trick for comparing angles. Plus order of operations, which
turns out to matter once conditions are involved.

## Part A — Conditions

Open `a-conditions.py`. Three demos on a plain cylinder, each independently switchable,
each asking a different kind of question before it places a point.

| Demo | The question | What it does |
|---|---|---|
| Attractor | How far is this point from a point in space? | Wall moves out (or in) by an amount that fades to nothing at the edge of the reach |
| Spout | Is this point in the region I care about? | Wall pushes out and the rim lifts, both ramping toward the top |
| Flat face | Did this point end up past a plane? | Pulls it back onto the plane, so the section goes from a circle to a D |

The attractor is the Grasshopper one, and it is four lines: work out the distance, fade
it over the reach, multiply by a strength, add it to the radius. Negative strength is the
same question with the opposite answer.

The flat face is the odd one out and worth the time: the other two decide *before*
placing the point, it checks *after*. That is why it works regardless of what the others
did, and why moving it earlier in the loop stops it working at all.

Work through these:

1. Attractor alone, moved around the vessel. Then reach down to `6` — the readout's
   steepest-movement number climbs, because the wall now has to travel the same distance
   in fewer laps.
2. Attractor strength negative: a dent instead of a bulge.
3. Spout alone. Narrow to `20°`, then widen to `160°`. Somewhere in between it stops
   being a spout and becomes an oval vessel.
4. Flat face on, spout on, spout angle set to `90` so it points at the plane. The spout
   gets sliced off.
5. Move the flat-face block above the attractor block and re-run. The face is no longer
   flat.

### What to observe

A condition with a narrow reach produces a steep wall, and the readout will tell you when
that goes past what the bead can bridge. This is the day-2 overhang number arriving again
from a completely different direction — you didn't choose a steep wall, you chose a
tight radius of influence, and the steep wall came with it.

`reference/bauble.py` is four smooth modulations on a sphere — the same species as
day 3's noodles, on a different silhouette. Worth reading as a finished piece, but it is
not the payoff for this day. `studio.py` is.

## Practice

**`e1-attractor.py`** — repetition. One function, `push_at`, called with where each
point was about to go. Five steps from "always true" to a two-target falloff, each one
line. The readout shows the overhang climbing as the falloff tightens.

Then `studio.py` is the transfer, and it is the rest of the day.

## Studio

`studio.py`. Printer profile, preview, build-volume check and export are wired up; the
generation cell is empty.

One constraint: use at least one quirk from day 3 deliberately — placed where you want
it, at a value you can state.

The closing cell in the notebook lists everything available to you, including the
mid-path objects (`fc.ExtrusionGeometry`, `fc.Printer`, `fc.Extruder`) if you want flow,
speed or extrusion to change partway through.

Export the G-code. Print it if there's a machine and time.

---

## For whoever is running the closing session

This is not a review. Nobody is being marked and nothing is finished.

- **Describe before interpreting.** The first round is only what people can see. No "it
  looks like a…" yet, and no "it works / it doesn't".
- **No quality talk in the first pass.** Once the word "good" is in the room the
  conversation narrows and doesn't widen again.
- **Talk about the path, not the person.** "This section leans out and catches" — not
  "you were ambitious here".
- **Equal airtime**, including for the ones who'd rather not.
- **Include the failed prints.** A print that stopped halfway is a result. Sessions that
  only look at what came off the bed intact teach a narrower lesson than the week did.
- **End on the next experiment, not a summary.** Everyone leaves with one thing they want
  to try, rather than a verdict on what they made.

The last point is the easiest to drop when the session runs late, and the one worth
protecting. The objects are unfinished on purpose.
