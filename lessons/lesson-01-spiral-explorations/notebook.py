import marimo

__generated_with = "0.17.8"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import fullcontrol as fc
    import math
    return fc, math, mo


@app.cell
def _(mo):
    mo.md("""
    # Lesson 01: Spiral Explorations

    Design spirals by controlling the printer's path directly!
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Interactive Controls
    """)
    return


@app.cell
def _(mo):
    # Create sliders for experimentation
    turns_slider = mo.ui.slider(5, 50, value=20, label="Number of turns")
    radius_growth_slider = mo.ui.slider(0.1, 2.0, value=0.5, step=0.1, label="Radius growth per turn")
    height_per_turn_slider = mo.ui.slider(0.1, 1.0, value=0.2, step=0.05, label="Height per turn (mm)")

    mo.vstack([turns_slider, radius_growth_slider, height_per_turn_slider])
    return height_per_turn_slider, radius_growth_slider, turns_slider


@app.cell
def _(mo):
    mo.md("""
    ## Your Spiral
    """)
    return


@app.cell
def _(fc, height_per_turn_slider, math, radius_growth_slider, turns_slider):
    # Generate spiral points
    steps = []

    num_turns = turns_slider.value
    radius_growth = radius_growth_slider.value
    height_per_turn = height_per_turn_slider.value

    points_per_turn = 20  # Smoother curves with more points
    total_points = num_turns * points_per_turn

    for i in range(total_points):
        # Calculate angle (in radians)
        angle = (i / points_per_turn) * 2 * math.pi

        # Calculate radius (grows with each turn)
        turn_number = i / points_per_turn
        radius = turn_number * radius_growth

        # Calculate x, y from polar coordinates
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)

        # Calculate z (height)
        z = turn_number * height_per_turn

        steps.append(fc.Point(x=x, y=y, z=z))

    # Visualize the spiral
    fc.transform(steps, 'plot')
    return (steps,)


@app.cell
def _(mo):
    mo.md("""
    ## Experiment Ideas

    Try these variations:
    - **Cone shape**: Keep radius constant, only increase Z
    - **Flat spiral**: Set height_per_turn to 0
    - **Steep tower**: Increase height_per_turn to 1.0
    - **Reverse spiral**: Use negative radius_growth

    What happens when you change the starting radius or add an offset to x/y?
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Generate G-code (Optional)
    """)
    return


@app.cell
def _(mo):
    show_gcode = mo.ui.checkbox(label="Show G-code output")
    show_gcode
    return (show_gcode,)


@app.cell
def _(fc, show_gcode, steps):
    # Generate G-code if checkbox is checked
    if show_gcode.value:
        gcode = fc.transform(steps, 'gcode')
        gcode[:500] + "\n\n... (truncated) ..."  # Show first 500 characters
    else:
        "Check the box above to see G-code"
    return (gcode,)


@app.cell
def _(gcode, mo):
    mo.md(f"""
    {gcode}
    """)
    return


if __name__ == "__main__":
    app.run()
