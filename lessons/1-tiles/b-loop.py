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
    # Day 1b · The loop writes the points

    The same idea as the four corners, except each position is calculated instead of
    typed. A hundred points now costs the same as four, so the thing you are designing
    is the rule that produces them.

    The code is below the plot. Read it once before you move the sliders.
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


@app.cell
def _(radius_growth, resolution, rise, start_radius, turns):
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
    return (steps,)


@app.cell(hide_code=True)
def _(steps):
    plot_steps(steps)
    return


@app.cell(hide_code=True)
def _(steps):
    mo.md(f"""
    **{len(steps)} points**, from five slider values and one loop.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md("""
    ## Work through these

    1. Rise per turn to `0` — a flat spiral, one layer. This is a tile.
    2. Radius growth negative — the spiral winds inward. Keep going: past zero radius
       it comes out the other side and unwinds, offset by half a turn.
    3. Points per turn to `3`, then `4`, then `6`. A circle drawn with six points is a
       hexagon; the loop has not changed, only how often it stops.
    4. In the code, add a second `steps.append(...)` inside the loop with `angle + math.pi`
       — two spirals, half a turn apart, in one path.

    ---

    Set rise per turn to `0.05` and turns to `60`. The preview draws it without
    complaint. Those laps are 0.05 mm apart, and this printer lays a bead 0.48 mm tall,
    so each lap would be buried in the nine below it and the nozzle would drag through
    all of them.

    The preview does not know that. `2-vessels/a-extrusion.py` is where the bead gets a
    width and a height.
    """)
    return


if __name__ == "__main__":
    app.run()
