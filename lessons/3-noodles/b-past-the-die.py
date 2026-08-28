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
    # Day 3b · Past the die

    A die produces one cross-section for the whole length of the noodle. That is what a
    die is, and it is the constraint every shape in `a-cross-section.py` was built under.

    A printer has no die. The cross-section can change anywhere along the path, and so
    can things a die has no access to at all: how much plastic comes out, how fast the
    nozzle moves, whether it extrudes at all.

    Four of those are below. Each one takes a **region** — a band of height and a slice
    of the circle — so it applies somewhere specific instead of everywhere. Outside the
    region the object prints normally.
    """)
    return


@app.cell(hide_code=True)
def _():
    quirk = mo.ui.dropdown(
        options={
            "Bulge — extra plastic": "flow",
            "Ripple — z moves inside the lap": "wobble",
            "Flare — lean out past support": "lean",
            "Threads — extruder off, still moving": "air",
        },
        value="Bulge — extra plastic",
        label="Quirk",
    )
    strength = mo.ui.slider(0.0, 1.0, value=0.6, step=0.05, label="Strength")
    band = mo.ui.range_slider(0.0, 1.0, value=[0.35, 0.6], step=0.05, label="Height band")
    sector = mo.ui.range_slider(0, 360, value=[0, 360], step=15, label="Angle sector (°)")
    feather = mo.ui.checkbox(value=True, label="Fade in and out at the edges")

    height = mo.ui.slider(10, 120, value=50, label="Height (mm)")
    radius = mo.ui.slider(5, 50, value=18, label="Radius (mm)")
    segments = mo.ui.slider(8, 128, value=64, label="Segments per lap")

    controls = mo.accordion(
        {
            "The quirk": mo.vstack([quirk, strength]),
            "Where it happens": mo.vstack(
                [
                    band,
                    sector,
                    feather,
                    mo.md(
                        "**Height band** is a fraction of the total height — `0` is the bed, "
                        "`1` is the top.\n\n"
                        "**Angle sector** narrows it to one side of the object. Leave it at "
                        "`0–360` to go all the way round.\n\n"
                        "**Fade** ramps the strength up and back down instead of switching it. "
                        "Hard edges are also a choice — try it off."
                    ),
                ]
            ),
            "Shape": mo.vstack([height, radius, segments]),
        },
        lazy=False,
    )
    controls
    return band, feather, height, quirk, radius, sector, segments, strength


@app.cell
def _(band, feather, height, quirk, radius, sector, segments, strength):
    centre = PRINTER.centre()
    laps = max(1, int(height.value / PRINTER.extrusion_height))
    total_points = laps * segments.value

    low, high = band.value
    sector_from, sector_to = sector.value

    # how strongly the quirk applies at this point: 0 outside the region, up to
    # `strength` inside it. this function is the actual subject of the lesson.
    def amount_at(fraction, degrees):
        if not (low <= fraction <= high):
            return 0.0
        if not (sector_from <= degrees <= sector_to):
            return 0.0
        if not feather.value or high == low:
            return strength.value
        # triangular ramp: 0 at both edges of the band, full in the middle
        through = (fraction - low) / (high - low)
        return strength.value * (1 - abs(through * 2 - 1))

    steps = [fc.ExtrusionGeometry(width=PRINTER.extrusion_width, height=PRINTER.extrusion_height)]
    current_flow = 1.0
    extruder_is_on = True

    for i in range(total_points + 1):
        lap = i / segments.value
        fraction = i / total_points
        angle = lap * math.tau
        degrees = math.degrees(angle) % 360

        amount = amount_at(fraction, degrees)

        r = radius.value
        z = centre.z + fraction * height.value

        if quirk.value == "lean":
            r += amount * 12
        elif quirk.value == "wobble":
            z += amount * 4 * math.sin(angle * 6)
        elif quirk.value == "flow":
            wanted_flow = 1.0 + amount * 2.5
            if abs(wanted_flow - current_flow) > 0.01:
                steps.append(
                    fc.ExtrusionGeometry(
                        width=PRINTER.extrusion_width * wanted_flow, height=PRINTER.extrusion_height
                    )
                )
                current_flow = wanted_flow
        elif quirk.value == "air":
            # off for a fraction of the segments, proportional to strength
            should_be_on = not (amount > 0 and (i % 6) < round(amount * 4))
            if should_be_on != extruder_is_on:
                steps.append(fc.Extruder(on=should_be_on))
                extruder_is_on = should_be_on

        steps.append(fc.Point(x=centre.x + r * math.cos(angle), y=centre.y + r * math.sin(angle), z=z))

    if not extruder_is_on:
        steps.append(fc.Extruder(on=True))
    return (steps,)


@app.cell(hide_code=True)
def _(steps):
    plot_steps(steps)
    return


@app.cell(hide_code=True)
def _():
    name = mo.ui.text(value="quirk", label="Name")
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

    1. Each quirk on its own, full height band, full sector, strength around `0.6`.
       Note what each one does to the preview.
    2. Narrow the sector to `0–90`. The same quirk now applies to one side only.
    3. Turn fade off. A hard edge at the band boundary is a different object from a
       ramp, and both are choices.
    4. Place two quirks at stated positions on one object and write down the values you
       used. Being able to reproduce it is the difference between a result and an
       accident.

    ---

    `amount_at` returns a number for a position: it is what decides where a quirk applies
    and how strongly. Right now it is a height band and an angle sector. It could depend
    on anything you can compute from the position — a spiral, a repeating pattern, the
    distance from a point.

    In `e2-place-it.py` you write it yourself.
    """)
    return


if __name__ == "__main__":
    app.run()
