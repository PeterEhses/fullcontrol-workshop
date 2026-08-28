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
    # Day 1 · Exercise 3 — repeat it

    Your tile, repeated across a grid. `cell_shape` gives one cell; the loop below places
    it `columns` × `rows` times.

    The nozzle keeps extruding between cells, so the connecting lines are part of the
    object. `fc.Extruder(on=False)` before a move and `on=True` after it would leave the
    gaps empty instead.

    Design a panel, a lattice, or a grille.
    """)
    return


@app.cell
def _():
    def cell_shape(size):
        """One cell, as (x, y) offsets from that cell's centre."""
        half = size / 2

        return [
            (-half, -half),
            (half, -half),
            (half, half),
            (-half, half),
            (-half, -half),
        ]
    return (cell_shape,)


@app.cell
def _(cell_shape):
    columns = 4
    rows = 4
    spacing = 30

    centre = PRINTER.centre()
    left = centre.x - (columns - 1) * spacing / 2
    front = centre.y - (rows - 1) * spacing / 2

    steps = [fc.Extruder(on=True)]

    for row in range(rows):
        for column in range(columns):
            cell_x = left + column * spacing
            cell_y = front + row * spacing

            for x, y in cell_shape(spacing):
                steps.append(fc.Point(x=cell_x + x, y=cell_y + y, z=centre.z))
    return (steps,)


@app.cell(hide_code=True)
def _(steps):
    plot_steps(steps)
    return


@app.cell(hide_code=True)
def _(steps):
    _xs = [p.x for p in steps if isinstance(p, fc.Point)]
    _ys = [p.y for p in steps if isinstance(p, fc.Point)]

    mo.md(
        "### ⚠️ This runs off the bed."
        if min(_xs) < 0 or max(_xs) > PRINTER.bed_width or min(_ys) < 0 or max(_ys) > PRINTER.bed_depth
        else f"{max(_xs) - min(_xs):.0f} × {max(_ys) - min(_ys):.0f} mm"
    )
    return


@app.cell(hide_code=True)
def _():
    name = mo.ui.text(value="pattern", label="Name")
    save = mo.ui.run_button(label="Save G-code")
    mo.hstack([name, save], justify="start", gap=1)
    return name, save


@app.cell(hide_code=True)
def _(name, save, steps):
    mo.md(f"Saved to `output/{save_gcode(steps, name.value).name}`") if save.value else None
    return


if __name__ == "__main__":
    app.run()
