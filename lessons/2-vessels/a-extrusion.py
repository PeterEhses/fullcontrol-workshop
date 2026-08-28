import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")

with app.setup:
    import math

    import marimo as mo
    import fullcontrol as fc

    from workshop import PRINTER, plot_controls, plot_steps, save_gcode


@app.cell(hide_code=True)
def _():
    mo.md(
        f"""
        # Day 2a · Width, height, and the bed

        Yesterday's path was a line, and a line has no thickness. What the printer lays
        down is a bead roughly **{PRINTER.extrusion_width} mm** wide and
        **{PRINTER.extrusion_height} mm** tall, pressed flat against whatever is under it.

        Same spiral as yesterday. The preview now draws it at that real size, and the
        readout below checks it against the build volume.
        """
    )
    return


@app.cell(hide_code=True)
def _():
    extrusion_width = mo.ui.slider(0.3, 2.0, value=PRINTER.extrusion_width, step=0.05, label="Extrusion width (mm)")
    extrusion_height = mo.ui.slider(0.1, 0.8, value=PRINTER.extrusion_height, step=0.02, label="Layer height (mm)")

    turns = mo.ui.slider(1, 80, value=30, label="Turns")
    start_radius = mo.ui.slider(1, 100, value=15, label="Starting radius (mm)")
    radius_growth = mo.ui.slider(-2.0, 4.0, value=0.4, step=0.1, label="Radius growth per turn (mm)")

    controls = mo.accordion(
        {
            "Shape": mo.vstack([turns, start_radius, radius_growth]),
            "The machine": mo.vstack(
                [
                    extrusion_width,
                    extrusion_height,
                    mo.md(
                        """
                        **Extrusion width** is wider than the nozzle bore, because the
                        plastic is pressed sideways as it goes down. A workable bead is
                        roughly 2 to 4 times as wide as it is tall; this profile is
                        1.45 by 0.48, about 3 to 1.

                        **Layer height** doubles as the rise per turn here — there is no
                        separate setting. Each lap sits directly on the one below it.
                        """
                    ),
                ]
            ),
        },
        lazy=False,
    )
    controls
    return extrusion_height, extrusion_width, radius_growth, start_radius, turns


@app.cell
def _(extrusion_height, extrusion_width, radius_growth, start_radius, turns):
    printer = PRINTER.but(
        extrusion_width=extrusion_width.value,
        extrusion_height=extrusion_height.value,
    )

    centre = printer.centre()
    points_per_turn = 48

    steps = []
    for i in range(turns.value * points_per_turn + 1):
        turn = i / points_per_turn
        angle = turn * math.tau
        radius = start_radius.value + turn * radius_growth.value

        steps.append(
            fc.Point(
                x=centre.x + radius * math.cos(angle),
                y=centre.y + radius * math.sin(angle),
                # the rise per turn IS the layer height. anything else and the layers
                # either float apart or plough into each other.
                z=centre.z + turn * printer.extrusion_height,
            )
        )
    return printer, steps


@app.cell(hide_code=True)
def _(printer, steps):
    plot_steps(steps, plot_controls(printer))
    return


@app.cell(hide_code=True)
def _(printer, steps):
    _xs = [p.x for p in steps]
    _ys = [p.y for p in steps]
    _z = max(p.z for p in steps)

    _problems = []
    if min(_xs) < 0 or max(_xs) > printer.bed_width or min(_ys) < 0 or max(_ys) > printer.bed_depth:
        _problems.append(f"It runs off the bed ({printer.bed_width} × {printer.bed_depth} mm).")
    if _z > printer.max_height:
        _problems.append(f"It's {_z:.0f} mm tall. The gantry stops at {printer.max_height} mm.")

    mo.md(
        "\n\n".join(["### ⚠️ " + p for p in _problems])
        if _problems
        else f"Fits. **{max(_xs) - min(_xs):.0f} × {max(_ys) - min(_ys):.0f} × {_z:.0f} mm**, "
        f"first layer at z = {printer.initial_z:.2f} mm."
    )
    return


@app.cell(hide_code=True)
def _():
    name = mo.ui.text(value="spiral", label="Name")
    save = mo.ui.run_button(label="Save G-code")
    mo.hstack([name, save], justify="start", gap=1)
    return name, save


@app.cell(hide_code=True)
def _(name, printer, save, steps):
    mo.md(f"Saved to `output/{save_gcode(steps, name.value, printer).name}`") if save.value else None
    return


@app.cell(hide_code=True)
def _():
    mo.md(
        """
        ---

        Set layer height to `0.1` and extrusion width to `1.45`. The preview draws wide
        flat ribbons stacked close together and reports no problem. On a machine there is
        nowhere for that much plastic to go: the bead is fourteen times wider than it is
        tall, so it spreads sideways into the previous lap and the nozzle ploughs through
        what it just laid.

        The preview checks the build volume. It does not check whether the extrusion is
        physically possible — it has no model of the plastic. Keep that distinction; day 3
        works in the gap.

        Next: `b-continuous.py`, where z stops stepping and starts climbing.
        """
    )
    return


if __name__ == "__main__":
    app.run()
