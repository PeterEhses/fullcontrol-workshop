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
    mo.md("""
    # Day 2b - One continuous path

    The last notebook did a lap, stopped, stepped up and did the next lap. That step is a
    seam and a retraction, once per layer, all the way up. Here z climbs by a fraction of
    a layer at every segment instead, so the path never stops: one line of plastic from
    the bed to the rim. Slicers call this vase mode; it is what happens when you never
    reset z.
    """)
    return


@app.cell(hide_code=True)
def _():
    profile = mo.ui.dropdown(
        options=["cylinder", "cone", "sphere", "vase", "hourglass"],
        value="vase",
        label="Profile",
    )
    height = mo.ui.slider(5, 150, value=60, label="Height (mm)")
    base_radius = mo.ui.slider(3, 60, value=20, label="Radius (mm)")
    segments = mo.ui.slider(3, 128, value=64, label="Segments per lap")

    mo.vstack([profile, height, base_radius, segments])
    return base_radius, height, profile, segments


@app.cell
def _(base_radius, height, profile, segments):
    # radius as a function of how far up we are (0 at the bed, 1 at the top).
    # this one function is the whole silhouette.
    def radius_at(fraction):
        if profile.value == "cylinder":
            return 1.0
        if profile.value == "cone":
            return 1.0 - fraction
        if profile.value == "sphere":
            return math.sin(fraction * math.pi)
        if profile.value == "vase":
            return 0.6 + 0.4 * math.sin(fraction * math.pi * 2.5)
        return abs(math.cos(fraction * math.pi))  # hourglass

    centre = PRINTER.centre()
    laps = int(height.value / PRINTER.extrusion_height)
    total_points = laps * segments.value

    steps = []
    for i in range(total_points + 1):
        fraction = i / total_points
        angle = (i / segments.value) * math.tau

        radius = base_radius.value * radius_at(fraction)

        steps.append(
            fc.Point(
                x=centre.x + radius * math.cos(angle),
                y=centre.y + radius * math.sin(angle),
                # z climbs a fraction of a layer with every segment, not a whole layer
                # every lap. that continuous creep is the entire trick.
                z=centre.z + fraction * height.value,
            )
        )
    return laps, steps


@app.cell(hide_code=True)
def _(steps):
    plot_steps(steps)
    return


@app.cell(hide_code=True)
def _(laps, steps):
    mo.md(f"""
    **{laps} laps, {len(steps)} points, one unbroken path.** No travel moves, no retractions, no layer changes — the extruder never stops turning.
    """)
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


@app.cell(hide_code=True)
def _():
    mo.md("""
    ## Work through these

    1. Each profile in turn. Note the height at which the wall leans furthest outward.
    2. Segments per lap down to `5`. Still one continuous path, now a pentagonal vessel.
    3. In `radius_at`, add `+ 0.05 * math.sin(fraction * math.pi * 8)` to the vase line —
       eight ribs up the height.
    4. Add `+ fraction * math.tau` to `angle` in the loop. The vessel twists once from bed
       to rim.
    5. Choose sphere and look at the bottom. `math.sin(0)` is 0, so the first lap has no
       radius at all and the vessel stands on a point. Add this as the first line of
       `radius_at`:

       ```python
       if fraction < 0.15:
           fraction = 0.15
       ```

       The bottom is now a flat disc. That is the first code in the workshop that checks
       where it is before deciding what to do; day 4 is made of them.

    ---

    Each lap is held up by the one below, so what matters is how far it sits outside that
    one. Past about half an extrusion width per lap — roughly 0.7 mm here — part of the
    bead has nothing under it and sags on the way down.

    `e1-silhouette.py` and `e2-vessel.py` are next. Day 3 measures that overhang, then
    goes past it on purpose.
    """)
    return


if __name__ == "__main__":
    app.run()
