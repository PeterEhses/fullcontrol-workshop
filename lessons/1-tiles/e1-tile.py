import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")

with app.setup:
    import marimo as mo
    import fullcontrol as fc

    from workshop import PRINTER, plot_steps, save_gcode


@app.cell(hide_code=True)
def _():
    mo.md("""
    # Day 1 · Exercise 1 — a tile

    Below is a list of coordinates, in millimetres from the middle of the bed. The nozzle
    visits them in the order they are written.

    Change them. Add more. Design a tile.
    """)
    return


@app.cell
def _():
    shape = [
        (-20, -20),
        (20, -20),
        (20, 20),
        (-20, 20),
        (-20, -20),
    ]
    return (shape,)


@app.cell(hide_code=True)
def _(shape):
    _centre = PRINTER.centre()

    steps = [fc.Extruder(on=True)]
    for _x, _y in shape:
        steps.append(fc.Point(x=_centre.x + _x, y=_centre.y + _y, z=_centre.z))
    return (steps,)


@app.cell(hide_code=True)
def _(steps):
    plot_steps(steps)
    return


@app.cell(hide_code=True)
def _():
    name = mo.ui.text(value="tile", label="Name")
    save = mo.ui.run_button(label="Save G-code")
    mo.hstack([name, save], justify="start", gap=1)
    return name, save


@app.cell(hide_code=True)
def _(name, save, steps):
    mo.md(f"Saved to `output/{save_gcode(steps, name.value).name}`") if save.value else None
    return


if __name__ == "__main__":
    app.run()
