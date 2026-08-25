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
    # ✨ 𝓒𝓱𝓻𝓲𝓼𝓽𝓶𝓪𝓼 𝓢𝓹𝓮𝓬𝓲𝓪𝓵 ✨

    Bulbous creations!
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
    # --- create sliders first ---
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
    **Segments per layer:** Number of points around each circular slice.  
    Low → blocky circle  
    High → smooth circle  

    **Flattened bottom layers:** Number of bottom layers ignoring taper.  
    More → flatter base  
    Less → spherical bottom
    """)
        ]),

        "Size & Shape": mo.vstack([
            ui_base_radius,
            ui_sphere_height,
            mo.md("""
    **Base radius:** Width of the bauble at its widest point.  
    **Sphere height:** Vertical height of the object.  
    For a sphere, height ≈ 2 × radius
    """)
        ]),

        "Star Modulation": mo.vstack([
            ui_star_points,
            ui_star_offset,
            mo.md("""
    **Star points:** Number of spikes in the cross-section (0 = circle).  
    **Star offset:** Inward/outward shift of spikes (-1 to 1).  
    (This is actually a sinus wave, so 1.0 and -1.0 are equivalent with a phase shift.)
    """)
        ]),

        "Twist": mo.vstack([
            ui_twist,
            mo.md("""
    **Total twists:** Number of full rotations along height.  
    0 → straight vertical  
    >0 → helical rotation
    """)
        ]),

        "Loop Bumps": mo.vstack([
            ui_loop_intensity,
            ui_loop_frequency,
            mo.md("""
    **Loop intensity:** Radial offset applied every n-th point.  
    **Loop frequency:** How often the bumps appear.  
    0 disables bumps
    """)
        ]),

        "Color": mo.vstack([
            ui_r,
            ui_g,
            ui_b,
            mo.md("""
    **R/G/B:** Color of the preview (0.0–1.0 each).  
    [1,0,0] → red, [0,1,0] → green, [0,0,1] → blue
    """)
        ]),
    })

    # jam together name and accordion
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

    # --- bauble controls ---
    segments_per_layer = ui_segments_per_layer.value  # 64    # number of segments around each layer
    flat_layers = ui_flat_layers.value                # 5     # number of layers to flatten at the

    base_radius = ui_base_radius.value                # 12.0  # stable base radius
    sphere_height = ui_sphere_height.value            # 30    # total height of object
    star_points = ui_star_points.value                # 5     # 0 = off, >0 = star-shaped cross-section
    star_offset = ui_star_offset.value                # -.25  # fraction (between -1.0 .. 1.0) shifts star inward/outward
    twist = ui_twist.value                            # 2/5   # total full rotations from bottom to top

    loop_intensity = ui_loop_intensity.value          # 3     # radial out-set on interval hits
    loop_frequency = ui_loop_frequency.value          # 12    # 0 = off, otherwise “every n-th segment”

    color = [ui_r.value, ui_g.value, ui_b.value]      # [0.6, 0.6, 0.6]  # r,g,b color of the object
    # ------------------------
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
    # Generate spiral points

    # start out with an empty list of steps
    steps = []

    # this is the middle of our printbed
    center = fc.Point(x=max_width/2, y=max_depth/2, z=initial_z)


    # --- compute once and forget ---
    layers = int(sphere_height / EH)
    r_flat = base_radius * math.sin(math.pi * (flat_layers / layers))
    total_twist_radians = twist * math.tau  # full rotations in radians
    # -------------------------------

    # Loop through all points across all layers

    # add a single starting point oposite of the first loop point
    steps.append(fc.polar_to_point(center, r_flat, math.pi + total_twist_radians * (0 / layers)))
    steps[0].color = color
    # do a circle so the first layer is complete
    for j in range(segments_per_layer):
        angle = (j / segments_per_layer) * math.tau + total_twist_radians * (0 / layers)
        steps.append(fc.polar_to_point(center, r_flat, angle))

    # now do the rest of the layers
    for i in range(layers * segments_per_layer + 1):
        # fractional positions
        layer_idx = i // segments_per_layer
        layer_fraction = (i % segments_per_layer) / segments_per_layer
        total_fraction = (layer_idx + layer_fraction) / layers

        # angle around the circle
        angle = layer_fraction * math.tau + total_fraction * total_twist_radians

        # compute spherical radius
        if layer_idx < flat_layers:
            # use radius at layer 'flat_layers' for first n layers
            flat_fraction = flat_layers / layers
            radius = r_flat
        else:
            radius = base_radius * math.sin(math.pi * total_fraction)

            # add loop bumps every nth point
            if loop_frequency > 0 and (i % loop_frequency == 0):
                # if the radius is smaller than the loop intensity, scale it down to avoid negative radius
                if radius > abs(loop_intensity):
                    radius += loop_intensity
                else:
                    radius += loop_intensity * (radius / abs(loop_intensity))
            # add star modulation if star_points > 0
        if star_points > 0 and star_offset != 0:
            radius += radius * star_offset * math.sin(layer_fraction * math.tau * star_points)

        # vertical position
        center.z = sphere_height * total_fraction + initial_z

        # add the point
        steps.append(fc.polar_to_point(center, radius, angle))

    # -----------------------------------------
    # boilerplate to show this cell in app mode
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
    ## Generate G-code (Optional)
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
