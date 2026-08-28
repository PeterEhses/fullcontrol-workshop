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
    # Day 1 - Exercise 2: the same tile, from a loop

    `offset_at` is called once per point, with `i` counting from 0, and returns where that
    point goes in millimetres from the middle of the bed. Right now it draws a circle of
    60 points.

    1. Make the circle bigger, then smaller.
    2. Make a hexagon / triangle shape.
    3. Make the shape spiral outwards.
    4. Make every second point closer to the middle than the others. (`i % 2` = `0` on
       even numbers and = `1` on odd ones.)
    """)
    return


@app.cell
def _():
    count = 60

    def offset_at(i):
        angle = i / count * math.tau
        radius = 30

        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        return x, y
    return count, offset_at


@app.cell(hide_code=True)
def _(count, offset_at):
    _centre = PRINTER.centre()

    steps = [fc.Extruder(on=True)]
    for _i in range(count + 1):
        _x, _y = offset_at(_i)
        steps.append(fc.Point(x=_centre.x + _x, y=_centre.y + _y, z=_centre.z))
    return (steps,)


@app.cell(hide_code=True)
def _(steps):
    plot_steps(steps)
    return


@app.cell(hide_code=True)
def _():
    name = mo.ui.text(value="loop-tile", label="Name")
    save = mo.ui.run_button(label="Save G-code")
    mo.hstack([name, save], justify="start", gap=1)
    return name, save


@app.cell(hide_code=True)
def _(name, save, steps):
    mo.md(f"Saved to `output/{save_gcode(steps, name.value).name}`") if save.value else None
    return


if __name__ == "__main__":
    app.run()
