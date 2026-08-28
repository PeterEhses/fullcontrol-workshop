# Day 4 - Studio

Files: `a-conditions.py`, `e1-attractor.py`, `studio.py`
You need: a laptop. A printer, if there is one, for whatever people want to run.

## Context

Days 1 to 3 each gave you a product type and a worked example: a tile, a vessel, a noodle.
Today gives you neither. That is a change in how the day works, not a reveal that the
earlier days were scaffolding.

One short notebook first, and it is not a summary of the week. You have been stacking
modulations since day 3 — fusilli is ridges plus twist, cavatappi is ridges plus twist
plus a coiled axis — so that idea is already yours.

What hasn't appeared in four days is code that asks a question about a point before
deciding what to do with it. Everything so far has been a smooth function of position:
same height and angle, same answer, anywhere on the object. That is one way to write this
and not the only one.

## Python this adds

`if` on a measured quantity rather than on a setting — the distance between two points,
whether an angle falls in a range, whether a coordinate went past a limit. `math.dist`,
and the modulo trick for comparing angles. Plus order of operations, which matters once
conditions are involved.

## Part A — Conditions

`a-conditions.py`. Four demos on a plain cylinder, each independently switchable, each
asking a different kind of question before it places a point.

| Demo | The question | What it does |
|---|---|---|
| Attractor | How far is this point from a point in space? | Wall moves out (or in) by an amount that fades to nothing at the edge of the reach |
| Spout | Is this point in the region I care about? | Wall pushes out and the rim lifts, both ramping toward the top |
| Flat face | Did this point end up past a plane? | Pulls it back onto the plane, so the section goes from a circle to a D |
| Overhang limiter | What did the path already do a lap ago? | Refuses to let the wall step out further per lap than the bead can bridge |

The attractor is the Grasshopper one, and it is four lines: work out the distance, fade it
over the reach, multiply by a strength, add it to the radius. Negative strength is the
same question with the opposite answer.

The flat face is the odd one out and worth the time. The first two decide before placing
the point; it checks after. That is why it works regardless of what the others did, and
why moving it earlier in the loop stops it working at all. The limiter goes further and
looks backwards, at a point the loop already placed.

1. Attractor alone, moved around the vessel. Then reach `25`, `12`, `6` in turn and watch
   the steepest-outward number climb from about `0.19` to `0.58` mm per lap — the same
   bulge delivered in fewer laps.
2. Reach down to `3`. Nothing happens: the attractor sits 4 mm off the wall and the reach
   no longer spans the gap. The condition still runs and never fires.
3. Attractor strength negative: a dent instead of a bulge.
4. Reach `6`, strength `15`. The readout says about `0.87` mm per lap, past the `0.72` a
   bead this wide can bridge. Switch the limiter on: the bulge is still there, the readout
   drops to exactly `0.72`, and the wall reaches the same place over more laps.
5. Spout alone. Narrow to `20°`, then widen to `160°`. Somewhere in between it stops being
   a spout and becomes an oval vessel.
6. Flat face on, spout on, spout angle at `90` so it points at the plane. The spout gets
   sliced off — the flat face runs last and doesn't care what put the point there.
7. Move the flat-face block above the attractor block and re-run. The face is no longer
   flat.

### What to observe

A condition with a narrow reach produces a steep wall, and the readout will tell you when
that passes what the bead can bridge. This is the day-2 overhang number arriving from a
different direction: you didn't choose a steep wall, you chose a tight radius of
influence, and the steep wall came with it. The limiter is that constraint written as a
rule the code enforces rather than a number you have to remember.

Three of the four demos ask about the point in front of them. The limiter asks about a
point the loop already placed, which is why it needs `radii`, a list of what happened.
Once code can look at its own output it can react to anything it has done.

`reference/bauble.py` is four smooth modulations on a sphere — the same species as day 3's
noodles, on a different silhouette. Worth reading as a finished piece, but it is not the
payoff for this day. `studio.py` is.

## Practice

`e1-attractor.py` — repetition. One function, `push_at`, called with where each point was
about to go. Five steps from "always true" to a two-target falloff, each one line. The
readout shows the overhang climbing as the falloff tightens.

## Studio

`studio.py`. Printer profile, preview, build-volume check and export are wired up; the
generation cell is empty.

One constraint: use at least one quirk from day 3 deliberately — placed where you want it,
at a value you can state.

The closing cell lists everything available to you, including the mid-path objects
(`fc.ExtrusionGeometry`, `fc.Printer`, `fc.Extruder`) if you want flow, speed or extrusion
to change partway through.

Export the G-code. Print it if there's a machine and time.

---

## For whoever is running the closing session

This is not a review. Nobody is being marked and nothing is finished.

Describe before interpreting: the first round is only what people can see, no "it looks
like a..." yet and no "it works / it doesn't". Keep quality talk out of the first pass —
once the word "good" is in the room the conversation narrows and doesn't widen again. Talk
about the path, not the person: "this section leans out and catches", not "you were
ambitious here". Equal airtime, including for the ones who'd rather not.

Include the failed prints. A print that stopped halfway is a result, and sessions that
only look at what came off the bed intact teach a narrower lesson than the week did.

End on the next experiment, not a summary — everyone leaves with one thing they want to
try rather than a verdict on what they made. That is the easiest point to drop when the
session runs late and the one worth protecting. The objects are unfinished on purpose.
