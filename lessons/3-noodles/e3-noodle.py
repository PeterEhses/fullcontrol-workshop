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
    # Day 3 · Exercise 3 — a shape that isn't on the list

    Three cells, all yours: the die, where the quirk applies, and the loop.

    `section_at` gets `round_the_tube` **and** `along`, so unlike a real die it can change
    down the length of the noodle.

    Make something the dropdown couldn't, with one quirk placed somewhere you chose.
    Write down the numbers if you want it back.
    """)
    return


@app.cell
def _():
    def section_at(round_the_tube, along):
        """Radius in mm. Both arguments run 0 to 1."""
        return 10.0
    return (section_at,)


@app.cell
def _():
    def amount_at(along, degrees):
        """How strongly the quirk applies here. 0 to 1."""
        return 0.0
    return (amount_at,)


@app.cell
def _(amount_at, section_at):
    length = 60
    segments = 72

    origin = PRINTER.centre()
    laps = max(1, int(length / PRINTER.extrusion_height))
    total_points = laps * segments

    steps = [fc.ExtrusionGeometry(width=PRINTER.extrusion_width, height=PRINTER.extrusion_height)]
    flow = 1.0

    for i in range(total_points + 1):
        along = i / total_points
        round_the_tube = (i / segments) % 1.0
        angle = round_the_tube * math.tau
        degrees = math.degrees(angle) % 360

        r = section_at(round_the_tube, along)
        z = origin.z + along * length

        # the quirk here is extra flow — swap it for fc.Extruder(on=False) or
        # fc.Printer(print_speed=...) if you want a different one
        wanted = 1.0 + amount_at(along, degrees) * 2.5
        if abs(wanted - flow) > 0.01:
            steps.append(fc.ExtrusionGeometry(width=PRINTER.extrusion_width * wanted, height=PRINTER.extrusion_height))
            flow = wanted

        steps.append(fc.Point(x=origin.x + r * math.cos(angle), y=origin.y + r * math.sin(angle), z=z))
    return (steps,)


@app.cell(hide_code=True)
def _(steps):
    plot_steps(steps)
    return


@app.cell(hide_code=True)
def _(steps):
    _points = [s for s in steps if isinstance(s, fc.Point)]
    _xs = [p.x for p in _points]
    _ys = [p.y for p in _points]

    mo.md(
        "### ⚠️ This runs off the bed."
        if min(_xs) < 0 or max(_xs) > PRINTER.bed_width or min(_ys) < 0 or max(_ys) > PRINTER.bed_depth
        else f"{max(_xs) - min(_xs):.0f} × {max(_ys) - min(_ys):.0f} × {max(p.z for p in _points):.0f} mm"
    )
    return


@app.cell(hide_code=True)
def _():
    name = mo.ui.text(value="noodle", label="Name")
    save = mo.ui.run_button(label="Save G-code")
    mo.hstack([name, save], justify="start", gap=1)
    return name, save


@app.cell(hide_code=True)
def _(name, save, steps):
    mo.md(f"Saved to `output/{save_gcode(steps, name.value).name}`") if save.value else None
    return


if __name__ == "__main__":
    app.run()
