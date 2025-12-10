import marimo

__generated_with = "0.17.8"
app = marimo.App(width="medium")

with app.setup:
    # Initialization code that ruimport marimo as mo
    import marimo as mo
    import fullcontrol as fc
    import math


@app.cell(hide_code=True)
def _():
    # plot function yanked from fullcontrol and massaged until it renders in marimo
    import numpy as np
    import plotly.graph_objects as go
    import os
    from fullcontrol.visualize.plot_data import PlotData
    from fullcontrol.visualize.controls import PlotControls
    from fullcontrol.visualize.tube_mesh import CylindersMesh, FlowTubeMesh, MeshExporter
    from fullcontrol.visualize.plotly import generate_mesh, local_max

    def plot(data: PlotData, controls: PlotControls):
        '''
        Plot data for x y z lines with RGB colors and annotations.
        The style of the plot is governed by the controls.

        Args:
            data (PlotData): The data to be plotted.
            controls (PlotControls): The controls for customizing the plot.

        Returns:
            None
        '''
    
        fig = go.Figure()
        cicd_testing = True if os.environ.get('FULLCONTROL_CICD_TESTING') == 'True' else False
        controls.raw_data = False
        controls.initialize()
        print(controls)
        if controls.tube_type is not None:
            Mesh = {'flow': FlowTubeMesh, 'cylinders': CylindersMesh}[controls.tube_type]
        else:  # Fall back to FlowTubeMesh if no tube_type is explicitly specified
            Mesh = FlowTubeMesh

        # generate line plots
        max_width = 0
        for path in data.paths:
            colors_now = [f'rgb({color[0]*255:.2f}, {color[1]*255:.2f}, {color[2]*255:.2f})' for color in path.colors]
            linewidth_now = controls.line_width * 2 if path.extruder.on == True else controls.line_width*0.5
            if path.extruder.on and controls.style == 'tube':
                sides, rounding_strength, flat_sides = controls.tube_sides, 0.4, False
                mesh = generate_mesh(path, linewidth_now, Mesh, sides, rounding_strength, flat_sides, colors_now)
                fig.add_trace(mesh.to_Mesh3d(colors=colors_now))
                max_width = max(max_width, local_max)
            elif not controls.hide_travel or path.extruder.on:  # plot travel lines for tube and line
                fig.add_trace(go.Scatter3d(mode='lines', x=path.xvals, y=path.yvals, z=path.zvals,
                                           showlegend=False, line=dict(width=linewidth_now, color=colors_now)))

        # find a bounding box, to create a plot with equally proportioned X Y Z scales (so a cuboid looks like a cuboid, not a cube)
        bounding_box_size = max(data.bounding_box.maxx-data.bounding_box.minx, data.bounding_box.maxy -
                                data.bounding_box.miny, data.bounding_box.maxz-min(0, data.bounding_box.minz))
        bounding_box_size += 0.002
        bounding_box_size += max_width

        # generate annotations
        annotations_pts = []
        annotations = []
        if controls.hide_annotations == False and not controls.neat_for_publishing:
        # if controls.hide_annotations == False:  # and not controls.neat_for_publishing:
            for annotation in data.annotations:
                x, y, z = (annotation[axis] for axis in 'xyz')
                annotations_pts.append([x, y, z])
                annotations.append(dict(
                    showarrow=False,
                    x=x, y=y, z=z,
                    text=annotation['label'],
                    yshift=10))
            xs, ys, zs = zip(*annotations_pts) if annotations_pts else [[]]*3
            fig.add_trace(go.Scatter3d(mode='markers', x=xs, y=ys, z=zs, showlegend=False, marker=dict(size=2, color='red')))

            # make sure the bounding box is big enough for the annotations
            # the 0.001 is to make sure the annotations don't lie on the boundary
            midx, midy, midz = (getattr(data.bounding_box, f'mid{axis}') for axis in 'xyz')
            range
            offset = 0.001
            offset_both_sides = 2 * offset
            for (x, y, z) in annotations_pts:
                if x < midx - bounding_box_size / 2 + offset:
                    bounding_box_size = 2 * (midx - x) + offset_both_sides
                if x > midx + bounding_box_size / 2 - offset:
                    bounding_box_size = 2 * (x - midx) + offset_both_sides
                if y < midy - bounding_box_size / 2 + offset:
                    bounding_box_size = 2 * (midy - y) + offset_both_sides
                if y > midy + bounding_box_size / 2 - offset:
                    bounding_box_size = 2 * (y - midy) + offset_both_sides
                if z < midz - bounding_box_size / 2 + offset:
                    bounding_box_size = 2 * (midz - z) + offset_both_sides
                if z > midz + bounding_box_size / 2 - offset:
                    bounding_box_size = 2 * (z - midz) + offset_both_sides

        relative_centre_z = 0.5*data.bounding_box.rangez/bounding_box_size
        camera_centre_z = -0.5 + relative_centre_z
        camera = dict(eye=dict(x=-0.5/controls.zoom, y=-1/controls.zoom, z=-0.5+0.5/controls.zoom),
                      center=dict(x=0, y=0, z=camera_centre_z))
        fig.update_layout(template='plotly_dark', paper_bgcolor="black", scene_aspectmode='cube',
                          scene=dict(annotations=annotations,
                                     xaxis=dict(backgroundcolor="black", nticks=10,
                                                range=[data.bounding_box.midx-bounding_box_size/2, data.bounding_box.midx+bounding_box_size/2],),
                                     yaxis=dict(backgroundcolor="black", nticks=10,
                                                range=[data.bounding_box.midy-bounding_box_size/2, data.bounding_box.midy+bounding_box_size/2],),
                                     zaxis=dict(backgroundcolor="black", nticks=10, range=[min(0, data.bounding_box.minz), bounding_box_size],),
                          ), scene_camera=camera, width=800, height=500, margin=dict(l=10, r=10, b=10, t=10, pad=4))
        if controls.hide_axes or controls.neat_for_publishing:
            for axis in ['xaxis', 'yaxis', 'zaxis']:
                fig.update_layout(
                    scene={axis: dict(showgrid=False, zeroline=False, visible=False)})
        if controls.neat_for_publishing:
            fig.update_layout(width=500, height=500)

        return fig
    return (plot,)


@app.cell
def _():
    mo.md("""
    # ✨ 𝓒𝓱𝓻𝓲𝓼𝓽𝓶𝓪𝓼 𝓢𝓹𝓮𝓬𝓲𝓪𝓵 ✨

    Bulbous creations!
    """)
    return


@app.cell
def _():
    # printer/gcode parameters for Prusa MK4s with 1.2mm nozzle

    nozzle_temp = 215
    bed_temp = 60
    print_speed = 1000
    fan_percent = 100
    printer_name='generic'

    max_width = 250  # maximum width of the design in mm
    max_depth = 210  # maximum depth of the design in mm
    max_height = 220  # maximum height of the design in mm

    # design parameters

    EW = 1.45 # extrusion width
    EH = 0.8 # extrusion height (and layer height)
    initial_z = EH*0.6 # initial nozzle position is set to 0.6x the extrusion height to get a bit of 'squish' for good bed adhesion

    mo.show_code()
    return (
        EH,
        EW,
        bed_temp,
        fan_percent,
        initial_z,
        max_depth,
        max_width,
        nozzle_temp,
        print_speed,
        printer_name,
    )


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


@app.cell
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


@app.cell
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
def _(EH, EW, plot, steps):
    # Visualize the spiral
    plot_controls = fc.PlotControls(raw_data=True, style='tube',tube_sides=6,color_type='manual',zoom=0.6,initialization_data={'extrusion_width': EW, 'extrusion_height': EH})

    mo.ui.plotly(plot(fc.visualize.steps2visualization.visualize(steps, plot_controls, True), plot_controls))
    return


@app.cell
def _():
    mo.md("""
    ## Generate G-code (Optional)
    """)
    return


@app.cell(hide_code=True)
def _(
    EH,
    EW,
    bed_temp,
    design_name,
    fan_percent,
    nozzle_temp,
    print_speed,
    printer_name,
    steps,
):
    # --- button callback to save GCode ---
    def save_gcode_callback(val):
        # Create GCodeControls as you do in your show_gcode block
        gcode_controls = fc.GcodeControls(
            printer_name=printer_name,
            save_as="output/"+design_name,
            initialization_data={
                'primer': 'front_lines_then_y',
                'print_speed': print_speed,
                'nozzle_temp': nozzle_temp,
                'bed_temp': bed_temp,
                'fan_percent': fan_percent,
                'extrusion_width': EW,
                'extrusion_height': EH
            }
        )
    
        # Transform steps to GCode
        gcode_to_save = fc.transform(steps, 'gcode', gcode_controls)
    
        # # Save directly to file
        # filename = f"{design_name}.gcode"
        # with open(filename, "w") as f:
        #     f.write(gcode_to_save)
    
        # print(f"GCode saved to {filename}")

    # --- create the button ---
    mo.ui.button(label="Save GCode", on_click=save_gcode_callback)
    return


@app.cell(hide_code=True)
def _():
    show_gcode = mo.ui.checkbox(label="Show G-code output")
    show_gcode
    return (show_gcode,)


@app.cell(hide_code=True)
def _(
    EH,
    EW,
    bed_temp,
    fan_percent,
    nozzle_temp,
    print_speed,
    printer_name,
    show_gcode,
    steps,
):
    # Generate G-code if checkbox is checked
    if show_gcode.value:
        gcode_controls = fc.GcodeControls(printer_name=printer_name,
        initialization_data={
            'primer': 'front_lines_then_y',
            'print_speed': print_speed,
            'nozzle_temp': nozzle_temp,
            'bed_temp': bed_temp,
            'fan_percent': fan_percent,
            'extrusion_width': EW,
            'extrusion_height': EH})
        gcode = fc.transform(steps, 'gcode', gcode_controls)
        display_gcode= gcode[:1000] + "\n\n... (truncated) ..."  # Show first 500 characters
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
