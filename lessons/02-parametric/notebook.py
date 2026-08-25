import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")

with app.setup:
    import math

    import marimo as mo
    import fullcontrol as fc

    from workshop import PRINTER, plot_steps


@app.cell(hide_code=True)
def _():
    mo.md("""
    # 02 · Let the loop type it

    The same four-corner idea, except the corners are calculated. Now a hundred
    points costs the same as four.
    """)
    return


@app.cell(hide_code=True)
def _():
    turns = mo.ui.slider(1, 60, value=20, label="Turns")
    start_radius = mo.ui.slider(1, 50, value=10, label="Starting radius (mm)")
    radius_growth = mo.ui.slider(-2.0, 2.0, value=0.5, step=0.1, label="Radius growth per turn (mm)")
    rise = mo.ui.slider(0.0, 2.0, value=0.2, step=0.05, label="Rise per turn (mm)")
    resolution = mo.ui.slider(3, 120, value=24, label="Points per turn")

    mo.vstack([turns, start_radius, radius_growth, rise, resolution])
    return radius_growth, resolution, rise, start_radius, turns


@app.cell(hide_code=True)
def _():
    show_code = mo.ui.checkbox(label="Show code")
    show_code
    return (show_code,)


@app.cell
def _(radius_growth, resolution, rise, show_code, start_radius, turns):
    centre = PRINTER.centre()
    points_per_turn = resolution.value

    steps = []
    for i in range(turns.value * points_per_turn + 1):
        # how far round we've gone, counted in whole turns — 2.5 means two and a half laps
        turn = i / points_per_turn

        angle = turn * math.tau
        radius = start_radius.value + turn * radius_growth.value

        # polar to cartesian: the printer only understands x and y
        x = centre.x + radius * math.cos(angle)
        y = centre.y + radius * math.sin(angle)
        z = centre.z + turn * rise.value

        steps.append(fc.Point(x=x, y=y, z=z))

    mo.show_code() if show_code.value else None
    return (steps,)


@app.cell(hide_code=True)
def _(steps):
    plot_steps(steps)
    return


@app.cell(hide_code=True)
def _(steps):
    mo.md(f"""
    **{len(steps)} points.** You typed none of them.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md("""
    ## Things to try

    - Rise per turn at `0` — a flat spiral, one layer, no height at all.
    - Radius growth negative — it winds inward instead. What happens when the
      radius passes zero?
    - Points per turn at `3`, `4`, `6` — the circle stops being a circle.
    - Two loops instead of one, the second offset by half a turn.

    ---

    Turn the rise down to `0.05` and the turns up to `60`. The plot still looks
    fine.

    **The layers are now 0.05 mm apart and the nozzle is 0.4 mm across. What would
    the printer do with that?**
    """)
    return


if __name__ == "__main__":
    app.run()
