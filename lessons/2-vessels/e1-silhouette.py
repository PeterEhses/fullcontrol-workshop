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
    # Day 2 - Exercise 1: fill in the silhouette

    `radius_at` is called once per point. `fraction` is 0 at the bed and 1 at the rim, and
    what comes back multiplies the radius. It returns `1.0` at every height, which is a
    cylinder. Make it produce each of these in turn:

    1. A cone: full width at the bed, nothing at the top.
    2. The other cone: nothing at the bed, full width at the top.
    3. A barrel: widest at half height, narrower at both ends.
    4. A step: 60% of the radius below half height, full radius above it.
    5. A stack of four steps, without writing four `if`s. (hint: `int(fraction * 4)`)

    The vessel is 70 mm tall with a 25 mm radius.

    Numbers 2 and 3 start at zero radius, so they stand on a point and won't print. That
    is the same problem as the sphere in `b-continuous.py`, and the same two-line fix.
    """)
    return


@app.function
def radius_at(fraction):
    return 1.0


@app.cell(hide_code=True)
def _():
    _height = 70
    _radius = 25
    _segments = 64

    _centre = PRINTER.centre()
    _laps = max(1, int(_height / PRINTER.extrusion_height))
    _total = _laps * _segments

    steps = []
    for _i in range(_total + 1):
        _fraction = _i / _total
        _angle = (_i / _segments) * math.tau
        _r = _radius * radius_at(_fraction)

        steps.append(
            fc.Point(
                x=_centre.x + _r * math.cos(_angle),
                y=_centre.y + _r * math.sin(_angle),
                z=_centre.z + _fraction * _height,
            )
        )
    return (steps,)


@app.cell(hide_code=True)
def _(steps):
    plot_steps(steps)
    return


@app.cell(hide_code=True)
def _():
    name = mo.ui.text(value="silhouette", label="Name")
    save = mo.ui.run_button(label="Save G-code")
    mo.hstack([name, save], justify="start", gap=1)
    return name, save


@app.cell(hide_code=True)
def _(name, save, steps):
    mo.md(f"Saved to `output/{save_gcode(steps, name.value).name}`") if save.value else None
    return


if __name__ == "__main__":
    app.run()
