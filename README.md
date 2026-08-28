# Machine control as a design material

A four-day workshop on designing 3D printer toolpaths directly, in Python. No CAD, no
slicer — you write where the nozzle goes, and that list of positions *is* the design.

Built on [FullControl](https://github.com/FullControlXYZ/fullcontrol) and
[marimo](https://marimo.io). No prior Python needed. A printer helps but isn't required —
every lesson previews at real extrusion size and exports G-code either way.

## Start

**Windows** — double-click `setup_windows.bat`, then `run.bat`.

**macOS / Linux** — `./setup_mac.sh`, then `./run.sh`.

Either one opens the first notebook as an app: move the sliders, watch the shape change.
That is the only notebook that runs that way. From the second one onward the code is on
screen, because from there on the code is the thing you're working in.

For everything else:

```
./run.sh 1 b        # day 1, part b  ("./run.sh 1b" works too)
./run.sh 3 e1       # day 3, the first exercise
./run.sh browse     # marimo's editor: file sidebar, all lessons
```

Day and notebook are matched by prefix, so as little as is unique will do. `./run.sh 2`
lists what's in day 2. On Windows it's `run.bat` with the same arguments.

`browse` prints a URL with an access token in the terminal — open that one, not plain
`localhost`.

Saved G-code lands in `output/`.

## The four days

Each day has taught notebooks (`a-`, `b-`) with the controls and the explanations, and
then exercises (`e1-`, `e2-`, ...) which are stripped to one editable thing each. The
`brief.md` in each folder is the day's plan: steps, a parameter table, what to look at,
and what to watch for at the machine.

| | | |
|---|---|---|
| **Day 1** | [Tiles](lessons/1-tiles) | Points in order, then a loop that writes them. One flat layer: a tile, a lattice, a panel. |
| **Day 2** | [Vessels](lessons/2-vessels) | Extrusion width, layer height and the bed. z climbs continuously, so one bead runs from the bed to the rim. |
| **Day 3** | [Noodles](lessons/3-noodles) | A die is one fixed cross-section. A printer isn't — so flow, position and extrusion can change anywhere along the path. Settings go out of spec on purpose. |
| **Day 4** | [Studio](lessons/4-studio) | Code that reacts to where it is: an attractor point, a spout, a flat face. Then an empty template and the rest of the day. |

Day 3 is what the workshop is for. Days 1 and 2 make it possible; day 4 is where you find
out whether it was worth doing.

[`reference/bauble.py`](reference/bauble.py) is a finished piece using everything above.
It should read as ordinary by the end of day 3.

## Layout

```
lessons/     four days: taught notebooks, exercises, and a brief
reference/   a worked example
workshop/    the printer profile and the marimo-compatible plot, shared by every lesson
output/      your G-code
```

Changing printer: edit `workshop/printer.py` once. Values there are for a Prusa MK4S.
