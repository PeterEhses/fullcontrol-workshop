# Machine control as a design material

A four-day workshop on designing 3D printer toolpaths directly, in Python. No CAD, no
slicer — you write where the nozzle goes, and that list of positions *is* the design.

Built on [FullControl](https://github.com/FullControlXYZ/fullcontrol) and
[marimo](https://marimo.io). No prior Python needed. A printer helps but isn't required —
every lesson previews at real extrusion size and exports G-code either way.

## Start

**Windows** — double-click `setup_windows.bat`, then `run_windows.bat`.

**macOS / Linux** — `./setup_mac.sh`, then `./run_mac.sh`.

Either one opens lesson 01 in your browser as an app: move the sliders, watch the shape
change. Tick **Show code** when you want to see what's underneath.

To open a different lesson, or to edit the code rather than drive it:

```
./run_mac.sh 05-the-noodle          # or run_windows.bat 05-the-noodle
./run_mac.sh 05-the-noodle edit     # code visible and editable
./run_mac.sh browse                 # marimo's own editor: file browser, sidebar, all lessons
```

`browse` prints a URL with an access token in the terminal — open that one, not plain
`localhost`.

Saved G-code lands in `output/`.

## The four days

**Day 1 — the path is the object.** There is no model and no slicer.

| | |
|---|---|
| [01-the-path](lessons/01-the-path) | Points, in order. Read the G-code they turn into. |
| [02-parametric](lessons/02-parametric) | A loop writes the points, so a hundred cost the same as four. |

**Day 2 — the machine has properties.** Width, height, speed, a bed with edges.

| | |
|---|---|
| [03-the-machine](lessons/03-the-machine) | Extrusion width and layer height. The path gets a body. |
| [04-one-continuous-path](lessons/04-one-continuous-path) | z climbs while the path goes round. One unbroken bead. |

**Day 3 — break it on purpose.** The hinge of the workshop.

| | |
|---|---|
| [05-the-noodle](lessons/05-the-noodle) | Code actual pasta. Eight named shapes, one loop, different numbers. |
| [06-quirks-on-purpose](lessons/06-quirks-on-purpose) | Past the die: bulge, ripple, flare, threads — placed on purpose. |

**Day 4 — compose.**

| | |
|---|---|
| [07-modulation](lessons/07-modulation) | Silhouette × cross-section × twist × bumps. They stack. |
| [08-studio](lessons/08-studio) | Empty template, wired up. Build something. |

Each folder has a `brief.md` — the move being made, what to do, and the question to leave
on. [08-studio](lessons/08-studio/brief.md) also has notes for whoever runs the closing
session.

[`reference/bauble.py`](reference/bauble.py) is a finished piece using everything above,
worth reading once lesson 07 makes it legible.

## Layout

```
lessons/     eight lessons, one notebook + one brief each
reference/   a worked example
workshop/    the printer profile and the marimo-compatible plot, shared by every lesson
output/      your G-code
```

Changing printer: edit `workshop/printer.py` once. Values there are for a Prusa MK4S.
