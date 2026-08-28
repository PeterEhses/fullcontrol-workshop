# Day 3 · Noodles

**Files:** `a-cross-section.py`, `b-past-the-die.py`, then `e1-die.py`, `e2-place-it.py`, `e3-noodle.py`
**Roughly:** 2 h · 2 h · rest of the day
**You need:** a laptop. A printer is worth more today than on any other day.

## Context

Pasta is extruded: dough is pushed through a metal die and comes out as a continuous
shape, which is then cut. The die is a cross-section, and the noodle is that
cross-section dragged along a line.

Yesterday's vessel was the same operation — a circle dragged upward. So a die is a
useful thing to think with, and more useful still for what it *can't* do: one fixed
cross-section for the whole length, and no control over the material once it has left
the opening. Part A works inside that constraint. Part B removes it.

This is the day the workshop is built around. Settings get driven out of spec on
purpose, and the question is not whether the result is correct but whether it is
something you would keep.

## Python this adds

Conditions that depend on position — `if` on where you are along the path rather than on
which preset was chosen. And objects in the `steps` list that are not points:
`fc.ExtrusionGeometry`, `fc.Printer`, `fc.Extruder` change how the machine behaves from
that position onward.

## Part A — The die

Open `a-cross-section.py`. Eight named shapes in the dropdown, all produced by the same
loop. The table below is the whole difference between them.

| Shape | Length × radius | Ridges | Rings | Twist | Slant | Bend | Coil |
|---|---|---|---|---|---|---|---|
| Ziti | 60 × 9 | — | — | — | — | — | — |
| Rigatoni | 45 × 10 | 14 @ 0.16 | — | — | — | — | — |
| Penne | 55 × 8 | 12 @ 0.14 | — | — | 7 mm | — | — |
| Fusilli | 70 × 8 | 3 @ 0.45 | — | 3 turns | — | — | — |
| Maccheroni | 55 × 7 | — | — | — | — | 14 mm | — |
| Cavatappi | 80 × 6 | 10 @ 0.14 | — | 1 turn | — | — | 9 mm, 2.5 turns |
| Radiatori | 40 × 9 | 8 @ 0.5 | 9 @ 0.3 | — | — | — | — |
| Bucatini | 120 × 3.5 | — | — | — | — | — | — |

Work through these:

1. Rigatoni. Raise ridge depth until the readout warns that the valleys are cutting
   deeper than the wall is thick, and look at what the preview does there.
2. From rigatoni, add twist. Nothing structural changed and it is now fusilli.
3. Bend, then coil. The cross-section code is untouched; only the position of its centre
   moves.
4. Push bend and coil until the noodle stops standing up.
5. Segments per lap to `5`, on any shape.

### Parameters

| Control | Useful range | What it changes | Where it breaks |
|---|---|---|---|
| Ridges | 0–30 | Wave repeats around the tube | Above ~20 at this radius the ridges are finer than the bead |
| Ridge depth | 0–0.5 | How deep the wave cuts | Past `1 − 1.45/radius` the valleys collide with themselves |
| Rings | 0–30 | The same wave running along the length | Above ~15 the rings are closer together than the bead is tall |
| Twist | −6 to 6 turns | Rotation of the cross-section as it climbs | Past ~4 turns the ridges shear into a smear |
| Slant | 0–20 mm | Diagonal cut at the top | Above ~half the length it cuts into the body |
| Bend | −40 to 40 mm | Sideways lean of the axis | Past ~20 mm on a 55 mm tube the walls overhang badly |
| Coil | 0–30 mm | Helical path for the axis | Combined with few coil turns, the drift per lap goes past the bead width |

### What to observe

**On screen:** the readout gives the overhang per lap as a percentage of extrusion width.
Past about 50%, the outer edge of the bead has nothing under it.

**On the bed:** that percentage is a prediction, not a fact. Find where it actually
starts drooping and compare. Bend and coil are the two that get there fastest.

Every shape in that dropdown exists because a factory can extrude it, cut it, dry it
without cracking, box it without breaking, and cook it evenly. Those are real constraints
on a real product, and none of them apply to you.

## Part B — Past the die

Open `b-past-the-die.py`. Four things a die has no access to: how much plastic comes out,
where the nozzle sits within a lap, how far past its support it reaches, and whether it
extrudes at all.

Each one takes a **region** — a band of height and a slice of the circle — so it applies
somewhere specific rather than everywhere.

| Quirk | What it changes mechanically | In the preview | On the print |
|---|---|---|---|
| Bulge | Extrusion width multiplied up to 3.5× in the region | Visibly fatter tube | Extra material piles up; the surface goes glossy and lumpy |
| Ripple | z moved up and down within each lap | Wavy laps | Ridged surface; laps partly bond to their neighbours |
| Flare | Radius pushed out up to 12 mm past its support | Wall leans out sharply | Overhang sags and strings on the way down |
| Threads | Extruder off for some segments while still moving | Thin travel lines | Fine strings across the gap, cooling as they cross |

Work through these:

1. Each quirk on its own, full height band, full sector, strength around `0.6`.
2. Narrow the sector to `0–90`. The same quirk now applies to one side only.
3. Turn fade off. A hard edge at the band boundary is a different object from a ramp, and
   both are choices.
4. Place two quirks at stated positions on one object and write down the values you used.

### What to observe

Being able to say "it bulges from 35% to 60% of the height, on this side, at this
strength" is the whole difference between a result and an accident. A defect you can
reproduce, place and scale is a technique. Nothing about the machine changed — only
whether you chose the values.

## Practice

**`e1-die.py`** — repetition. Cut a die: fill in `section_at` to make rigatoni's 14
ridges, fusilli's 3 blades, an oval, and a square-ridged tube using `if` instead of
`sin`.

**`e2-place-it.py`** — repetition. Fill in `amount_at` so the bulge lands where you say:
everywhere, the top third, one side, both at once, then faded in rather than switched on.
A readout counts how many times the flow changes along the path.

**`e3-noodle.py`** — transfer. Die, quirk and loop, all three editable. `section_at`
gets the position along the tube as well as around it, so it can do what a real die
can't. Make something the dropdown couldn't, with one quirk placed on purpose.

## With a printer

Today's prints need supervising. Print small — 40–60 mm — and stay at the machine.

- **Threads first.** Stringing is the defect slicers work hardest to eliminate and the
  one that looks least like a defect once it's deliberate. It is also the lowest-risk
  thing here: the extruder is off, so nothing accumulates.
- **Bulge needs watching.** At high strength the extra material can build up on the
  nozzle and collide with the part on the next lap. If the head starts dragging the part
  around or knocking it, stop the print.
- **Flare will sag, which is the point.** But a sagging wall can wrap onto the nozzle.
  Watch the flared section through at least one lap before leaving it.
- Anything that has come loose from the bed, stop. Nothing printed at that point is
  recoverable and the nozzle can end up buried.
- Keep the failures. A print that stopped halfway is a legitimate result, and you'll want
  it in front of you tomorrow.
