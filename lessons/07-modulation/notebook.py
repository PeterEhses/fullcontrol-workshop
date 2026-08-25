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
    mo.md(
        """
        # 07 · Stacking modulations

        Every point so far has come out of the same two questions: how far from the
        centre, and how high. Everything else — the star, the twist, the bumps, the flat
        bottom — is a small function nudging one of those two numbers.

        None of them know about each other. You stack them and see what you get.

        `reference/bauble.py` is four of these on top of a sphere. That's all it is.
        """
    )
    return


@app.cell(hide_code=True)
def _():
    profile = mo.ui.dropdown(
        options=["sphere", "cylinder", "cone", "vase"], value="sphere", label="Silhouette"
    )
    height = mo.ui.slider(10, 150, value=60, label="Height (mm)")
    radius = mo.ui.slider(5, 60, value=25, label="Radius (mm)")
    segments = mo.ui.slider(8, 128, value=64, label="Segments per lap")
    flat_base = mo.ui.slider(0, 40, value=10, label="Flattened bottom laps")

    points = mo.ui.slider(0, 12, value=5, label="Points")
    point_depth = mo.ui.slider(-0.5, 0.5, value=-0.2, step=0.02, label="Point depth")

    twist = mo.ui.slider(-4.0, 4.0, value=0.5, step=0.05, label="Turns over full height")

    bump_size = mo.ui.slider(0.0, 8.0, value=0.0, step=0.1, label="Bump size (mm)")
    bump_every = mo.ui.slider(0, 64, value=12, label="One bump every … points")

    controls = mo.accordion(
        {
            "Base shape": mo.vstack(
                [
                    profile,
                    height,
                    radius,
                    segments,
                    flat_base,
                    mo.md(
                        "**Flattened bottom laps** hold the radius steady near the bed instead "
                        "of tapering to a point. A sphere printed honestly starts at zero "
                        "radius, which is nothing to stand on."
                    ),
                ]
            ),
            "Cross-section — a star instead of a circle": mo.vstack(
                [
                    points,
                    point_depth,
                    mo.md(
                        "The radius gains a sine wave that goes round `points` times per lap. "
                        "Negative depth pushes the spikes in rather than out — same wave, "
                        "half a phase apart."
                    ),
                ]
            ),
            "Twist": mo.vstack(
                [
                    twist,
                    mo.md("Rotate each lap slightly further than the last. Cross-section spirals up."),
                ]
            ),
            "Bumps": mo.vstack(
                [
                    bump_size,
                    bump_every,
                    mo.md(
                        "Kick the radius outward at one point and back the next. Because it's "
                        "one continuous path, the loop that leaves and returns is a physical "
                        "loop of plastic sticking out."
                    ),
                ]
            ),
        },
        lazy=False,
    )
    controls
    return (
        bump_every,
        bump_size,
        flat_base,
        height,
        point_depth,
        points,
        profile,
        radius,
        segments,
        twist,
    )


@app.cell(hide_code=True)
def _():
    show_code = mo.ui.checkbox(label="Show code")
    show_code
    return (show_code,)


@app.cell
def _(
    bump_every,
    bump_size,
    flat_base,
    height,
    point_depth,
    points,
    profile,
    radius,
    segments,
    show_code,
    twist,
):
    def silhouette(fraction):
        if profile.value == "cylinder":
            return 1.0
        if profile.value == "cone":
            return 1.0 - fraction
        if profile.value == "vase":
            return 0.6 + 0.4 * math.sin(fraction * math.pi * 2.5)
        return math.sin(fraction * math.pi)  # sphere

    centre = PRINTER.centre()
    laps = max(1, int(height.value / PRINTER.extrusion_height))
    total_points = laps * segments.value

    # radius the silhouette reaches once the flat base ends — held constant below that
    base_fraction = min(flat_base.value, laps) / laps
    base_radius = radius.value * silhouette(base_fraction)

    steps = []
    for i in range(total_points + 1):
        lap = i / segments.value
        fraction = i / total_points
        round_the_lap = lap % 1.0

        angle = round_the_lap * math.tau + fraction * twist.value * math.tau

        if fraction < base_fraction:
            r = base_radius
        else:
            r = radius.value * silhouette(fraction)

        if points.value:
            r += r * point_depth.value * math.sin(round_the_lap * math.tau * points.value)

        if bump_size.value and bump_every.value and i % bump_every.value == 0:
            r += bump_size.value

        steps.append(
            fc.Point(
                x=centre.x + r * math.cos(angle),
                y=centre.y + r * math.sin(angle),
                z=centre.z + fraction * height.value,
            )
        )

    mo.show_code() if show_code.value else None
    return (steps,)


@app.cell(hide_code=True)
def _(steps):
    plot_steps(steps)
    return


@app.cell(hide_code=True)
def _():
    name = mo.ui.text(value="modulated", label="Name")
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
        ## Add a fifth

        Four modulations are in there. Write one more into the loop — anything that
        changes `r`, `angle` or `z` as a function of where you are.

        Some that go somewhere: a wave that only exists above half height; a radius that
        depends on the *previous* radius; a twist that reverses halfway up; a bump size
        that grows as you climb.

        ---

        **The order you apply them in changes the result.** Twist-then-star is not
        star-then-twist. Move a line and find out.
        """
    )
    return


if __name__ == "__main__":
    app.run()
