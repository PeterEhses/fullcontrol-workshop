# fullcontrol-workshop

Four days of [marimo](https://marimo.io) notebooks for writing 3D printer toolpaths in
Python with [FullControl](https://github.com/FullControlXYZ/fullcontrol). No CAD and no
slicer — you build a list of positions and export it as G-code. Assumes no prior Python.
A printer is optional; the lessons preview at real extrusion size and export G-code
without one.

## Install

Windows: `setup_windows.bat`, then `run.bat`. macOS/Linux: `./setup_mac.sh`, then
`./run.sh`. Both install `uv` if it is missing and run `uv sync`. Run setup first, `run`
will not do it for you.

## Usage

```
./run.sh              lessons/1-tiles/a-points.py, as an app
./run.sh 1 b          day 1, part b   (./run.sh 1b works too)
./run.sh 3 e1         day 3, exercise 1
./run.sh 2            list day 2
./run.sh browse       marimo editor, all lessons
```

`run.bat` takes the same arguments. Day and notebook are prefix-matched, and an ambiguous
prefix errors and lists the candidates. `a-points.py` opens with `marimo run` and its code
hidden; everything else opens in the editor. `browse` prints a URL with an access token —
open that one, plain `localhost` will not authenticate. G-code is written to `output/`.

## Lessons

Each day has taught notebooks (`a-`, `b-`) carrying the sliders and the explanation,
exercises (`e1-`, `e2-`, ...) with one editable thing each, and a `brief.md` with the
schedule, a parameter table giving working ranges and failure points, and printer notes.

1. [tiles](lessons/1-tiles) — points in order, then a loop that writes them. One flat layer.
2. [vessels](lessons/2-vessels) — extrusion width, layer height, the bed. z climbs continuously, so one bead runs from bed to rim.
3. [noodles](lessons/3-noodles) — flow, position and extrusion change along the path. Settings go out of spec on purpose.
4. [studio](lessons/4-studio) — code that reacts to where it is (attractor point, spout, flat face), then an empty template.

`reference/bauble.py` is a finished piece using everything in days 1-3.
`reference/coral.py` prints the current state of a growth simulation as each layer instead
of evaluating a formula per layer.

## Layout

```
lessons/     notebooks, exercises, brief, one folder per day
reference/   worked examples, not taught
workshop/    printer profile and a marimo-compatible plot(), imported by every lesson
output/      generated G-code
```

Printer settings are in `workshop/printer.py`, currently a Prusa MK4S. Change them there
and every lesson follows.
