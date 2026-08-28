import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")

with app.setup:
    import math

    import marimo as mo
    import fullcontrol as fc

    from workshop import PRINTER, plot_controls, plot_steps, save_gcode, to_gcode


@app.cell
def _():
    mo.md("""
    # Reference - Bauble

    A sphere with four modulations stacked on it: a flattened base, a star cross-section,
    a twist up the height, and a bump every n-th point. Same species as day 3's noodles on
    a different silhouette, and nothing in it is past day 3.
    """)
    return


@app.cell(hide_code=True)
def _():
    EW = PRINTER.extrusion_width
    EH = PRINTER.extrusion_height
    initial_z = PRINTER.initial_z
    max_width = PRINTER.bed_width
    max_depth = PRINTER.bed_depth
    return EH, EW, initial_z, max_depth, max_width


@app.cell
def _():
    mo.md("""
    ## Controls
    """)
    return


@app.cell(hide_code=True)
def _():
    ui_design_name        = mo.ui.text(value="dan", label="Design name")
    ui_segments_per_layer = mo.ui.number(3, 128, value=64, step=1, label="Segments per layer")
    ui_flat_layers        = mo.ui.number(0, 20, value=5, step=1, label="Flattened bottom layers")

    ui_base_radius        = mo.ui.number(1.0, 50.0, value=12.0, step=0.5, label="Base radius")
    ui_sphere_height      = mo.ui.number(1.0, 100.0, value=30.0, step=1.0, label="Sphere height")

    ui_star_points        = mo.ui.number(0, 12, value=5, step=1, label="Star points")
    ui_star_offset        = mo.ui.number(-1.0, 1.0, value=-0.25, step=0.05, label="Star offset")

    ui_twist              = mo.ui.number(0.0, 10.0, value=0.4, step=0.05, label="Total twists")

    ui_loop_intensity     = mo.ui.number(0.0, 10.0, value=3.0, step=0.1, label="Loop intensity")
    ui_loop_frequency     = mo.ui.number(0, 128, value=12, step=1, label="Loop frequency")

    ui_r                  = mo.ui.number(0.0, 1.0, value=0.6, step=0.01, label="Color R")
    ui_g                  = mo.ui.number(0.0, 1.0, value=0.6, step=0.01, label="Color G")
    ui_b                  = mo.ui.number(0.0, 1.0, value=0.6, step=0.01, label="Color B")

    # --- Accordion with embedded help text ---
    accordion = mo.accordion({
        "Segments & Layers": mo.vstack([
            ui_segments_per_layer,
            ui_flat_layers,
            mo.md("""
            Segments per layer is how many points go round each slice: low is a visible
            polygon, high is a smooth circle.

            Flattened bottom layers ignore the taper and hold the radius they start at, so
            the bauble stands on a disc instead of a point. Set it to 0 to see why it is
            there.
            """)
        ]),

        "Size & Shape": mo.vstack([
            ui_base_radius,
            ui_sphere_height,
            mo.md("""
            Base radius is the widest point, sphere height the total height. Height about
            twice the radius gives a sphere; anything else is an egg.
            """)
        ]),

        "Star Modulation": mo.vstack([
            ui_star_points,
            ui_star_offset,
            mo.md("""
            Star points is how many spikes the cross-section has, 0 for a circle. Star
            offset shifts them in or out, -1 to 1. It is a sine wave, so 1.0 and -1.0 give
            the same shape half a period apart.
            """)
        ]),

        "Twist": mo.vstack([
            ui_twist,
            mo.md("""
            Full rotations from bed to top. 0 is vertical, anything above it shears the
            star into a helix.
            """)
        ]),

        "Loop Bumps": mo.vstack([
            ui_loop_intensity,
            ui_loop_frequency,
            mo.md("""
            Every n-th point gets pushed out by the intensity, which puts a row of bumps up
            the object. Frequency 0 turns them off.
            """)
        ]),

        "Color": mo.vstack([
            ui_r,
            ui_g,
            ui_b,
            mo.md("""
            Preview colour only, 0.0-1.0 each. It does not reach the G-code.
            """)
        ]),
    })

    mo.vstack([
        ui_design_name,
        accordion
    ])
    return (
        ui_b,
        ui_base_radius,
        ui_design_name,
        ui_flat_layers,
        ui_g,
        ui_loop_frequency,
        ui_loop_intensity,
        ui_r,
        ui_segments_per_layer,
        ui_sphere_height,
        ui_star_offset,
        ui_star_points,
        ui_twist,
    )


@app.cell(hide_code=True)
def _(
    ui_b,
    ui_base_radius,
    ui_design_name,
    ui_flat_layers,
    ui_g,
    ui_loop_frequency,
    ui_loop_intensity,
    ui_r,
    ui_segments_per_layer,
    ui_sphere_height,
    ui_star_offset,
    ui_star_points,
    ui_twist,
):
    design_name = ui_design_name.value

    segments_per_layer = ui_segments_per_layer.value  # 64    # number of segments around each layer
    flat_layers = ui_flat_layers.value                # 5     # number of layers to flatten at the

    base_radius = ui_base_radius.value                # 12.0  # stable base radius
    sphere_height = ui_sphere_height.value            # 30    # total height of object
    star_points = ui_star_points.value                # 5     # 0 = off, >0 = star-shaped cross-section
    star_offset = ui_star_offset.value                # -.25  # fraction (between -1.0 .. 1.0) shifts star inward/outward
    twist = ui_twist.value                            # 2/5   # total full rotations from bottom to top

    loop_intensity = ui_loop_intensity.value          # 3     # radial out-set on interval hits
    loop_frequency = ui_loop_frequency.value          # 12    # 0 = off, otherwise "every n-th segment"

    color = [ui_r.value, ui_g.value, ui_b.value]      # [0.6, 0.6, 0.6]  # r,g,b color of the object
    return (
        base_radius,
        color,
        design_name,
        flat_layers,
        loop_frequency,
        loop_intensity,
        segments_per_layer,
        sphere_height,
        star_offset,
        star_points,
        twist,
    )


@app.cell(hide_code=True)
def _():
    show_code = mo.ui.checkbox(label="Show Code", value=False)
    show_code
    return (show_code,)


@app.cell(hide_code=True)
def _(
    EH,
    base_radius,
    color,
    flat_layers,
    initial_z,
    loop_frequency,
    loop_intensity,
    max_depth,
    max_width,
    segments_per_layer,
    show_code,
    sphere_height,
    star_offset,
    star_points,
    twist,
):
    steps = []
    center = fc.Point(x=max_width/2, y=max_depth/2, z=initial_z)

    layers = int(sphere_height / EH)
    r_flat = base_radius * math.sin(math.pi * (flat_layers / layers))
    total_twist_radians = twist * math.tau

    # start half a turn away from the first loop point, so the seam isn't on top of it
    steps.append(fc.polar_to_point(center, r_flat, math.pi + total_twist_radians * (0 / layers)))
    steps[0].color = color

    # one full circle first, so the bottom layer closes before the spiral starts
    for j in range(segments_per_layer):
        angle = (j / segments_per_layer) * math.tau + total_twist_radians * (0 / layers)
        steps.append(fc.polar_to_point(center, r_flat, angle))

    for i in range(layers * segments_per_layer + 1):
        layer_idx = i // segments_per_layer
        layer_fraction = (i % segments_per_layer) / segments_per_layer
        total_fraction = (layer_idx + layer_fraction) / layers

        angle = layer_fraction * math.tau + total_fraction * total_twist_radians

        # the bottom few layers hold the radius they start at, so the bauble stands on a
        # disc rather than a point
        if layer_idx < flat_layers:
            radius = r_flat
        else:
            radius = base_radius * math.sin(math.pi * total_fraction)

            if loop_frequency > 0 and (i % loop_frequency == 0):
                # near the top and bottom the radius is smaller than the bump, so scale
                # the bump down rather than going negative
                if radius > abs(loop_intensity):
                    radius += loop_intensity
                else:
                    radius += loop_intensity * (radius / abs(loop_intensity))

        if star_points > 0 and star_offset != 0:
            radius += radius * star_offset * math.sin(layer_fraction * math.tau * star_points)

        center.z = sphere_height * total_fraction + initial_z
        steps.append(fc.polar_to_point(center, radius, angle))

    output = None
    if show_code.value:
        output = mo.show_code()
    output
    return (steps,)


@app.cell
def _():
    mo.md("""
    ## Result
    """)
    return


@app.cell(hide_code=True)
def _(steps):
    plot_steps(steps, plot_controls())
    return


@app.cell
def _():
    mo.md("""
    ## G-code
    """)
    return


@app.cell(hide_code=True)
def _(design_name, steps):
    def save_gcode_callback(_):
        save_gcode(steps, design_name)

    mo.ui.button(label="Save GCode", on_click=save_gcode_callback)
    return


@app.cell(hide_code=True)
def _():
    show_gcode = mo.ui.checkbox(label="Show G-code output")
    show_gcode
    return (show_gcode,)


@app.cell(hide_code=True)
def _(show_gcode, steps):
    if show_gcode.value:
        display_gcode = to_gcode(steps)[:1000] + "  ... (truncated) ..."
    else:
        display_gcode = "Check the box above to see G-code"
    return (display_gcode,)


@app.cell
def _(display_gcode):
    mo.md(f"""
    {display_gcode}
    """)
    return


if __name__ == "__main__":
    app.run()
