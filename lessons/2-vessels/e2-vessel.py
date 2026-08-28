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
    # Day 2 · Exercise 2 — a vessel of your own

    Both cells are yours: the silhouette, and the loop that uses it.

    A silhouette no dropdown offers. Print it if there's a machine.

    The readout under the plot gives the steepest outward step per lap. Past half an
    extrusion width the bead has nothing under its outer edge.
    """)
    return


@app.cell
def _():
    def radius_at(fraction):
        """0 at the bed, 1 at the rim. Return a multiplier for the radius."""
        return 1.0
    return (radius_at,)


@app.cell
def _(radius_at):
    height = 70
    radius = 25
    segments = 64

    centre = PRINTER.centre()
    laps = max(1, int(height / PRINTER.extrusion_height))
    total_points = laps * segments

    steps = []
    for i in range(total_points + 1):
        fraction = i / total_points
        angle = (i / segments) * math.tau

        r = radius * radius_at(fraction)
        z = centre.z + fraction * height

        steps.append(fc.Point(x=centre.x + r * math.cos(angle), y=centre.y + r * math.sin(angle), z=z))
    return laps, segments, steps


@app.cell(hide_code=True)
def _(steps):
    plot_steps(steps)
    return


@app.cell(hide_code=True)
def _(laps, segments, steps):
    _centre = PRINTER.centre()
    _radii = [math.hypot(p.x - _centre.x, p.y - _centre.y) for p in steps]
    _z = max(p.z for p in steps)

    # only growing outward overhangs; shrinking inward is fully supported
    _steepest = max((_radii[i + segments] - _radii[i] for i in range(len(_radii) - segments)), default=0.0)
    _allowed = PRINTER.extrusion_width / 2

    _notes = [f"{2 * max(_radii):.0f} mm across, {_z:.0f} mm tall, {laps} laps."]
    _notes.append(
        f"Steepest outward step: **{_steepest:.2f} mm per lap**"
        + (f" — past the {_allowed:.2f} mm this bead can bridge." if _steepest > _allowed else ".")
    )

    mo.md("\n\n".join(_notes))
    return


@app.cell(hide_code=True)
def _():
    name = mo.ui.text(value="vessel", label="Name")
    save = mo.ui.run_button(label="Save G-code")
    mo.hstack([name, save], justify="start", gap=1)
    return name, save


@app.cell(hide_code=True)
def _(name, save, steps):
    mo.md(f"Saved to `output/{save_gcode(steps, name.value).name}`") if save.value else None
    return


if __name__ == "__main__":
    app.run()
