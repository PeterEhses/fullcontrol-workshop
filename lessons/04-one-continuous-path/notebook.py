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
        """
        # 04 · One continuous path

        A normal print does a lap, stops, steps up, does the next lap. Every step is a
        seam.

        Don't stop. Let z creep up *while* the path goes round. One line of plastic,
        from the bed to the top, with no beginning and end in between. Slicers call
        this vase mode; here it's just what happens when you never reset z.
        """
    )
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


@app.cell(hide_code=True)
def _():
    show_code = mo.ui.checkbox(label="Show code")
    show_code
    return (show_code,)


@app.cell
def _(base_radius, height, profile, segments, show_code):
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

    mo.show_code() if show_code.value else None
    return laps, steps


@app.cell(hide_code=True)
def _(steps):
    plot_steps(steps)
    return


@app.cell(hide_code=True)
def _(laps, steps):
    mo.md(
        f"**{laps} laps, {len(steps)} points, one unbroken path.** "
        "No travel moves, no retractions, no layer changes — the extruder never stops turning."
    )
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
    mo.md(
        """
        ## Things to try

        - Write your own `radius_at`. Anything that returns a number for a number works.
        - `math.sin(fraction * math.pi * 8)` — ribs.
        - Segments per lap down to `5` — a pentagonal vessel, still one path.
        - Add a little to `angle` as `fraction` grows, and the whole thing twists.

        ---

        Every lap is stuck to the one below it. Which is what holds it up.

        **So what happens to the bit that sticks out past the lap below?**
        """
    )
    return


if __name__ == "__main__":
    app.run()
