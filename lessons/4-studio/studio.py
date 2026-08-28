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
    # Day 4 - Studio

    Printer profile, preview, build-volume check and export are wired up. The generation
    cell below is empty.

    There is no example to work from today and no product type given. Build something
    that uses at least one quirk from day 3 deliberately — placed where you want it, at
    a value you can state.
    """)
    return


@app.cell(hide_code=True)
def _():
    height = mo.ui.slider(10, 150, value=50, label="Height (mm)")
    radius = mo.ui.slider(5, 60, value=20, label="Radius (mm)")
    segments = mo.ui.slider(3, 128, value=64, label="Segments per lap")
    knob = mo.ui.slider(0.0, 1.0, value=0.5, step=0.01, label="Spare knob")

    mo.vstack([height, radius, segments, knob])
    return height, radius, segments


@app.cell
def _(height, radius, segments):
    centre = PRINTER.centre()
    laps = max(1, int(height.value / PRINTER.extrusion_height))
    total_points = laps * segments.value

    steps = []
    for i in range(total_points + 1):
        lap = i / segments.value
        fraction = i / total_points
        angle = lap * math.tau

        r = radius.value
        z = centre.z + fraction * height.value

        # your work goes here

        # end of your work

        steps.append(fc.Point(x=centre.x + r * math.cos(angle), y=centre.y + r * math.sin(angle), z=z))
    return (steps,)


@app.cell(hide_code=True)
def _(steps):
    plot_steps(steps)
    return


@app.cell(hide_code=True)
def _(steps):
    _xs = [p.x for p in steps if isinstance(p, fc.Point)]
    _ys = [p.y for p in steps if isinstance(p, fc.Point)]
    _zs = [p.z for p in steps if isinstance(p, fc.Point)]

    _off_bed = min(_xs) < 0 or max(_xs) > PRINTER.bed_width or min(_ys) < 0 or max(_ys) > PRINTER.bed_depth
    _too_tall = max(_zs) > PRINTER.max_height

    mo.md(
        "### This runs outside the build volume."
        if (_off_bed or _too_tall)
        else f"{max(_xs) - min(_xs):.0f} × {max(_ys) - min(_ys):.0f} × {max(_zs):.0f} mm - {len(steps)} steps"
    )
    return


@app.cell(hide_code=True)
def _():
    name = mo.ui.text(value="studio", label="Name")
    save = mo.ui.run_button(label="Save G-code")
    mo.hstack([name, save], justify="start", gap=1)
    return name, save


@app.cell(hide_code=True)
def _(name, save, steps):
    mo.md(f"Saved to `output/{save_gcode(steps, name.value).name}`") if save.value else None
    return


@app.cell(hide_code=True)
def _():
    mo.md("""
    ---

    Things you have available:

    `PRINTER.extrusion_width`, `.extrusion_height`, `.initial_z`, `.centre()`,
    `.bed_width`, `.bed_depth`, `.max_height`

    `PRINTER.but(print_speed=3000)` — a copy with something changed, for
    `plot_steps(steps, plot_controls(printer))` and `save_gcode(steps, name, printer)`.

    Mid-path changes go into `steps` alongside the points:

    - `fc.ExtrusionGeometry(width=..., height=...)` — flow from here on
    - `fc.Printer(print_speed=...)` — speed from here on
    - `fc.Extruder(on=False)` — stop extruding, keep moving
    """)
    return


if __name__ == "__main__":
    app.run()
