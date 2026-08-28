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
    mo.md(f"""
    # Day 2a - Width, height, and the bed

    Yesterday's path was a line, and a line has no thickness. What the printer lays down
    is a bead roughly {PRINTER.extrusion_width} mm wide and {PRINTER.extrusion_height} mm
    tall, pressed flat against whatever is under it.

    Yesterday's spiral climbed a little with every point. This one holds z flat for a
    whole lap and steps up between laps — layers, the way a normal print is built. And
    the bead is no longer one size: **Flow** varies it along the path.
    """)
    return


@app.cell(hide_code=True)
def _():
    extrusion_width = mo.ui.slider(0.3, 2.0, value=PRINTER.extrusion_width, step=0.05, label="Extrusion width (mm)")
    extrusion_height = mo.ui.slider(0.1, 0.8, value=PRINTER.extrusion_height, step=0.02, label="Layer height (mm)")

    turns = mo.ui.slider(1, 80, value=30, label="Turns")
    start_radius = mo.ui.slider(1, 100, value=15, label="Starting radius (mm)")
    radius_growth = mo.ui.slider(-2.0, 4.0, value=0.4, step=0.1, label="Radius growth per turn (mm)")

    flow_variation = mo.ui.slider(0.0, 2.5, value=0.0, step=0.05, label="Variation")
    flow_cycles = mo.ui.slider(0.0, 24.0, value=6.0, step=0.5, label="Bulges per lap")
    flow_drift = mo.ui.slider(-1.0, 1.5, value=0.0, step=0.1, label="Drift from bed to top")

    controls = mo.accordion(
        {
            "Shape": mo.vstack([turns, start_radius, radius_growth]),
            "The machine": mo.vstack(
                [
                    extrusion_width,
                    extrusion_height,
                    mo.md(
                        """
                        Extrusion width is wider than the nozzle bore, because the
                        plastic is pressed sideways as it goes down. A workable bead is
                        2 to 4 times as wide as it is tall; this profile is 1.45 by 0.48,
                        about 3 to 1.

                        Layer height doubles as the rise between laps here — there is no
                        separate setting. Each lap sits directly on the one below.
                        """
                    ),
                ]
            ),
            "Flow": mo.vstack(
                [
                    flow_variation,
                    flow_cycles,
                    flow_drift,
                    mo.md(
                        """
                        Extrusion width above is one number for the whole path. These
                        three change it *along* the path — the bead gets fatter and
                        thinner as the nozzle goes round.

                        **Variation** is how far it swings. `0` is off.

                        **Bulges per lap** is where the fun is. A whole number comes back
                        to the same place every lap, so the bulges stack into a vertical
                        rib. Half a number lands opposite each lap. Anything else drifts
                        round and spirals up the wall.

                        **Drift** ramps the flow from bed to top. Negative starves the
                        top of the object.
                        """
                    ),
                ]
            ),
        },
        lazy=False,
    )
    controls
    return (
        extrusion_height,
        extrusion_width,
        flow_cycles,
        flow_drift,
        flow_variation,
        radius_growth,
        start_radius,
        turns,
    )


@app.cell
def _(
    extrusion_height,
    extrusion_width,
    flow_cycles,
    flow_drift,
    flow_variation,
    radius_growth,
    start_radius,
    turns,
):
    printer = PRINTER.but(
        extrusion_width=extrusion_width.value,
        extrusion_height=extrusion_height.value,
    )

    centre = printer.centre()
    points_per_turn = 48
    total_points = turns.value * points_per_turn

    steps = []
    bead_widths = []
    for j in range(turns.value):
        fraction_all_turns = j/turns.value
        for i in range(points_per_turn):   
            # a layer is flat. lap is which one we're on, and the leftover fraction of a
            # turn is where we are around it.
            fraction_in_turn = i/points_per_turn
            angle = fraction_in_turn * math.tau
    
            radius = start_radius.value + j * radius_growth.value
            z = centre.z + j * printer.extrusion_height
    
            # how much plastic on this segment. the bead size is a per-point quantity, not
            # a setting — that is the whole point of this cell.
            # note this uses turn, not angle: angle restarts every lap, turn doesn't, and
            # that difference is what makes a whole number of bulges stack into a rib.
            pulse = math.sin(fraction_in_turn * math.tau * flow_cycles.value)
            flow = 1.0 + flow_drift.value * fraction_all_turns + flow_variation.value * pulse
            if flow < 0.05:
                flow = 0.05  # never ask the extruder for negative plastic
    
            bead_width = printer.extrusion_width * flow
            bead_widths.append(bead_width)
    
            steps.append(fc.ExtrusionGeometry(width=bead_width, height=printer.extrusion_height))
            steps.append(fc.Point(x=centre.x + radius * math.cos(angle), y=centre.y + radius * math.sin(angle), z=z))
    return bead_widths, printer, steps


@app.cell(hide_code=True)
def _(printer, steps):
    plot_steps(steps, plot_controls(printer))
    return


@app.cell(hide_code=True)
def _(bead_widths, printer, steps):
    _points = [s for s in steps if isinstance(s, fc.Point)]
    _xs = [p.x for p in _points]
    _ys = [p.y for p in _points]
    _z = max(p.z for p in _points)

    _thinnest = min(bead_widths)
    _fattest = max(bead_widths)

    _problems = []
    if min(_xs) < 0 or max(_xs) > printer.bed_width or min(_ys) < 0 or max(_ys) > printer.bed_depth:
        _problems.append(f"It runs off the bed ({printer.bed_width} × {printer.bed_depth} mm).")
    if _z > printer.max_height:
        _problems.append(f"It's {_z:.0f} mm tall. The gantry stops at {printer.max_height} mm.")

    # a bead wants to be 2 to 4 times as wide as it is tall. outside that it either has
    # nowhere to spread or nothing holding it down.
    if _fattest > printer.extrusion_height * 4:
        _problems.append(
            f"The fattest bead is {_fattest:.2f} mm on a {printer.extrusion_height:.2f} mm layer — "
            f"{_fattest / printer.extrusion_height:.1f} times as wide as tall. That plastic has "
            "nowhere to go but sideways into the lap next to it, and then under the nozzle."
        )
    if _thinnest < printer.extrusion_height * 2:
        _problems.append(
            f"The thinnest bead is {_thinnest:.2f} mm — only "
            f"{_thinnest / printer.extrusion_height:.1f} times its own height. A bead that narrow "
            "stands up rather than lying down, and the wall goes porous."
        )

    mo.md(
        "\n\n".join(["### " + p for p in _problems])
        if _problems
        else f"Fits. **{max(_xs) - min(_xs):.0f} × {max(_ys) - min(_ys):.0f} × {_z:.0f} mm**, "
        f"first layer at z = {printer.initial_z:.2f} mm. "
        f"Bead {_thinnest:.2f}-{_fattest:.2f} mm on a {printer.extrusion_height:.2f} mm layer."
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
    mo.md("""
    ---

    Set layer height to `0.1` and extrusion width to `1.45`, with variation at `0`. The
    preview draws wide flat ribbons stacked close together and reports no problem. On a
    machine there is nowhere for that much plastic to go: the bead is fourteen times
    wider than it is tall, so it spreads sideways into the previous lap and the nozzle
    ploughs through what it just laid.

    The readout catches that one, because it is a number about the bead. It cannot catch
    what happens to that plastic afterwards — where it sags, what it sticks to, whether
    the nozzle drags it. The preview draws the path, not the material. Day 3 works in
    that gap on purpose.

    Next: `b-continuous.py`, where z stops stepping and starts climbing.
    """)
    return


if __name__ == "__main__":
    app.run()
