import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")

with app.setup:
    import marimo as mo
    import fullcontrol as fc

    from workshop import PRINTER, plot_steps, to_gcode


@app.cell(hide_code=True)
def _():
    mo.md(
        """
        # 01 · The path is the object

        No model. No slicer. A list of places the nozzle goes, in order.
        """
    )
    return


@app.cell(hide_code=True)
def _():
    size = mo.ui.slider(10, 80, value=40, label="Size (mm)")
    corner_lift = mo.ui.slider(0.0, 4.0, value=0.0, step=0.1, label="Lift per corner (mm)")
    close_loop = mo.ui.checkbox(value=True, label="Return to the start")

    mo.vstack([size, corner_lift, close_loop])
    return close_loop, corner_lift, size


@app.cell(hide_code=True)
def _():
    show_code = mo.ui.checkbox(label="Show code")
    show_code
    return (show_code,)


@app.cell
def _(close_loop, corner_lift, size, show_code):
    centre = PRINTER.centre()
    half = size.value / 2
    lift = corner_lift.value

    corners = [
        (-half, -half),
        (+half, -half),
        (+half, +half),
        (-half, +half),
    ]

    steps = []
    for i, (dx, dy) in enumerate(corners):
        steps.append(fc.Point(x=centre.x + dx, y=centre.y + dy, z=centre.z + i * lift))

    if close_loop.value:
        steps.append(fc.Point(x=centre.x - half, y=centre.y - half, z=centre.z + 4 * lift))

    mo.show_code() if show_code.value else None
    return (steps,)


@app.cell(hide_code=True)
def _(steps):
    plot_steps(steps)
    return


@app.cell(hide_code=True)
def _(steps):
    _moves = [line for line in to_gcode(steps, primer="no_primer").splitlines() if line.startswith("G1")]

    mo.md(
        "## What the printer actually receives\n\n"
        + "```\n"
        + "\n".join(_moves)
        + "\n```\n\n"
        + "One line per point. `X` and `Y` are where to go, `Z` is how high, `E` is how much "
        + "plastic to push out on the way there. That is the entire format."
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(
        """
        ---

        Four corners took four lines to type. A circle needs a hundred points.

        **Are you going to type them?**
        """
    )
    return


if __name__ == "__main__":
    app.run()
