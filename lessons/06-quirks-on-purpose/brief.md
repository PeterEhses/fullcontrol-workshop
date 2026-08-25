# 06 · Past the die

**Day 3 · ~2 h**

## The move

A die makes one fixed cross-section for the whole length. That's the constraint every
shape in lesson 05 was built under.

You don't have that constraint. You can change the shape anywhere along the noodle, and
you can change things a die has no access to at all — how much plastic comes out, how
fast the nozzle moves, whether it extrudes at all.

Four of those are on sliders here, each with a **region**: a band of height, a slice of
the circle, faded or hard-edged. Everything outside the region prints clean.

## Do

Bulge, ripple, flare, threads. One at a time first.

Then place two of them somewhere specific on the same object. Not "it blobbed" — "it
blobs *here*, this much, because I put it there."

Hand it to someone without saying anything and watch whether they read it as damage or
as a decision. If they can't tell, that's information about the object.

**With a printer:** the threads setting is the one to print. Stringing is the defect
slicers work hardest to eliminate, and it's the one that looks least like a defect once
it's deliberate.

**Without:** the preview is at real extrusion width, so bulge and flare show up as
volume. For the threads, look for the thin travel lines and picture what trails behind
a hot nozzle crossing that gap.

## Leave on

`amount_at` returns a number for a position. Right now it's a band and a sector. It
could be a spiral, a pattern, a rule that depends on what the path did last.

**What would you want it to be?**
