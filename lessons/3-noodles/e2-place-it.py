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
    # Day 3 - Exercise 2: put it somewhere

    `amount_at` decides how strongly the bulge applies. `along` runs 0 at the bed to 1 at
    the top; `degrees` runs 0 to 360 around the tube. Return 0 for none and 1 for full.

    Right now it returns 0 everywhere, so the tube prints clean. Make the bulge happen:

    1. Everywhere. (Return `1.0`.)
    2. Only in the top third.
    3. Only on one side — between 0 and 90 degrees.
    4. Only in the top third and only on that side.
    5. Fading in from nothing at half height to full at the top, instead of switching on.

    Each one is a different object. Save the ones worth keeping.
    """)
    return


@app.cell
def _():
    def amount_at(along, degrees):
        return 0.0
    return (amount_at,)


@app.cell(hide_code=True)
def _(amount_at):
    _height = 50
    _radius = 15
    _segments = 64

    _centre = PRINTER.centre()
    _laps = max(1, int(_height / PRINTER.extrusion_height))
    _total = _laps * _segments

    steps = [fc.ExtrusionGeometry(width=PRINTER.extrusion_width, height=PRINTER.extrusion_height)]
    _flow = 1.0

    for _i in range(_total + 1):
        _along = _i / _total
        _angle = (_i / _segments) * math.tau
        _degrees = math.degrees(_angle) % 360

        _wanted = 1.0 + amount_at(_along, _degrees) * 2.5
        if abs(_wanted - _flow) > 0.01:
            steps.append(
                fc.ExtrusionGeometry(width=PRINTER.extrusion_width * _wanted, height=PRINTER.extrusion_height)
            )
            _flow = _wanted

        steps.append(
            fc.Point(
                x=_centre.x + _radius * math.cos(_angle),
                y=_centre.y + _radius * math.sin(_angle),
                z=_centre.z + _along * _height,
            )
        )
    return (steps,)


@app.cell(hide_code=True)
def _(steps):
    plot_steps(steps)
    return


@app.cell(hide_code=True)
def _(steps):
    _changes = sum(1 for s in steps if isinstance(s, fc.ExtrusionGeometry)) - 1
    mo.md(f"The flow changes **{_changes}** times along the path.")
    return


@app.cell(hide_code=True)
def _():
    name = mo.ui.text(value="placed", label="Name")
    save = mo.ui.run_button(label="Save G-code")
    mo.hstack([name, save], justify="start", gap=1)
    return name, save


@app.cell(hide_code=True)
def _(name, save, steps):
    mo.md(f"Saved to `output/{save_gcode(steps, name.value).name}`") if save.value else None
    return


if __name__ == "__main__":
    app.run()
