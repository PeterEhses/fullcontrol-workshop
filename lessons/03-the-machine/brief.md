# 03 · The machine has properties

**Day 2 · ~90 min**

## The move

Lines have no thickness. What a printer lays down does — a squashed bead with a width, a
height, a temperature and a bed it has to fit on. Same geometry, now with a body.

## Do

Note that the preview changed: it draws tubes at the real extrusion size instead of
hairlines. That is the same path you had yesterday.

Pull the sliders past what the machine can do — layer height at `0.1` with extrusion
width at `1.45`. The preview draws it happily.

Save a G-code file. Open it in a G-code viewer (PrusaSlicer, or gcode.ws) and check it
against the plot.

**With a printer:** print it. It's a spiral vase, it takes minutes.

## Leave on

**The preview will show you things the machine cannot do.** It has no idea what plastic
is. That gap is where the next two days live.
