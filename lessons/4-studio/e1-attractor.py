import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")

with app.setup:
    import math

    import marimo as mo
    import fullcontrol as fc

    from workshop import PRINTER, plot_steps, save_gcode


@app.cell(hide_code=True)
def _():
    mo.md("""
    # Day 4 · Exercise 1 — write the condition

    `push_at` is called for every point, with where that point was about to go. It returns
    how many millimetres to move the wall outward there — negative moves it inward.

    It returns 0, so the vessel is a plain cylinder 60 mm tall with a 20 mm radius. The
    attractor point sits at `target`, 4 mm off the wall at half height.

    1. Push the wall out by 8 mm everywhere. (Return `8.0` — a condition that is always
       true is still a condition.)
    2. Push it out by 8 mm only where the point is within 10 mm of `target`.
       `math.dist((x, y, z), target)` gives you the distance.
    3. Fade it: full 8 mm on top of the target, nothing at 10 mm away, proportional in
       between.
    4. Turn it into a dent by making it negative.
    5. Add a second target on the opposite side and react to whichever is nearer.

    The readout says how far the wall steps outward per lap. With an 8 mm push it goes
    from about `0.19` at a 20 mm falloff to `0.46` at 6 mm — the same bulge delivered in
    fewer laps. Push 15 mm over a 6 mm falloff and it crosses what the bead can bridge,
    and the readout says so.
    """)
    return


@app.cell
def _(target):
    def push_at(x, y, z):
        """How far to move the wall outward at this point, in mm."""
        return 0.0
    return (push_at,)


@app.cell(hide_code=True)
def _():
    _centre = PRINTER.centre()

    # 4 mm outside a 20 mm wall, half way up a 60 mm vessel
    target = (_centre.x, _centre.y + 24, _centre.z + 30)
    return (target,)


@app.cell(hide_code=True)
def _(push_at):
    _height = 60
    _radius = 20
    _segments = 96

    _centre = PRINTER.centre()
    _laps = max(1, int(_height / PRINTER.extrusion_height))
    _total = _laps * _segments

    steps = []
    radii = []

    for _i in range(_total + 1):
        _fraction = _i / _total
        _angle = (_i / _segments) * math.tau
        _z = _centre.z + _fraction * _height

        # where the point would have gone, before the condition looks at it
        _x = _centre.x + _radius * math.cos(_angle)
        _y = _centre.y + _radius * math.sin(_angle)

        _r = _radius + push_at(_x, _y, _z)
        radii.append(_r)

        steps.append(
            fc.Point(x=_centre.x + _r * math.cos(_angle), y=_centre.y + _r * math.sin(_angle), z=_z)
        )
    return radii, steps


@app.cell(hide_code=True)
def _(steps):
    plot_steps(steps)
    return


@app.cell(hide_code=True)
def _(radii):
    _per_lap = 96
    _steepest = max((radii[i + _per_lap] - radii[i] for i in range(len(radii) - _per_lap)), default=0.0)
    _allowed = PRINTER.extrusion_width / 2

    mo.md(
        f"Steepest outward step: **{_steepest:.2f} mm per lap**"
        + (f" — past the {_allowed:.2f} mm this bead can bridge." if _steepest > _allowed else ".")
    )
    return


@app.cell(hide_code=True)
def _():
    name = mo.ui.text(value="attractor", label="Name")
    save = mo.ui.run_button(label="Save G-code")
    mo.hstack([name, save], justify="start", gap=1)
    return name, save


@app.cell(hide_code=True)
def _(name, save, steps):
    mo.md(f"Saved to `output/{save_gcode(steps, name.value).name}`") if save.value else None
    return


if __name__ == "__main__":
    app.run()
