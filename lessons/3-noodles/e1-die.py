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
    # Day 3 · Exercise 1 — cut a die

    `section_at` is the die. It is called once per point with `round_the_tube`, which runs
    0 to 1 once per lap, and returns a radius in millimetres.

    A plain circle right now. Make it produce:

    1. Rigatoni: 14 shallow ridges. (`math.sin(round_the_tube * math.tau * 14)` runs
       through 14 full waves per lap.)
    2. Fusilli's section: 3 deep blades instead.
    3. An oval: one wave per lap.
    4. A tube whose ridges are square rather than rounded, using `if` instead of `sin`.

    The tube is 50 mm long with a 10 mm radius.
    """)
    return


@app.cell
def _():
    def section_at(round_the_tube):
        return 10.0
    return (section_at,)


@app.cell(hide_code=True)
def _(section_at):
    _length = 50
    _segments = 72

    _origin = PRINTER.centre()
    _laps = max(1, int(_length / PRINTER.extrusion_height))
    _total = _laps * _segments

    steps = [fc.Extruder(on=True)]
    for _i in range(_total + 1):
        _round_the_tube = (_i / _segments) % 1.0
        _angle = _round_the_tube * math.tau
        _r = section_at(_round_the_tube)

        steps.append(
            fc.Point(
                x=_origin.x + _r * math.cos(_angle),
                y=_origin.y + _r * math.sin(_angle),
                z=_origin.z + (_i / _total) * _length,
            )
        )
    return (steps,)


@app.cell(hide_code=True)
def _(steps):
    plot_steps(steps)
    return


@app.cell(hide_code=True)
def _():
    name = mo.ui.text(value="die", label="Name")
    save = mo.ui.run_button(label="Save G-code")
    mo.hstack([name, save], justify="start", gap=1)
    return name, save


@app.cell(hide_code=True)
def _(name, save, steps):
    mo.md(f"Saved to `output/{save_gcode(steps, name.value).name}`") if save.value else None
    return


if __name__ == "__main__":
    app.run()
