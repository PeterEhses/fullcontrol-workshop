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
    # Day 4a - Conditions

    You have been stacking modulations since day 3 — fusilli is ridges plus twist,
    cavatappi is ridges plus twist plus a coiled axis. Independent adjustments to the same
    two numbers, in one loop, none of them aware of each other. Most are smooth functions
    of position: give them a height and an angle and they return the same number every
    time, anywhere on the object.

    The four below each ask a question before deciding. They are in one cell; the loop
    that applies them is in the next one and is the loop you have had since day 2.
    """)
    return


@app.cell(hide_code=True)
def _():
    height = mo.ui.slider(20, 120, value=60, label="Height (mm)")
    radius = mo.ui.slider(8, 50, value=20, label="Radius (mm)")
    segments = mo.ui.slider(16, 160, value=96, label="Segments per lap")

    attractor_on = mo.ui.checkbox(value=True, label="Attractor")
    attractor_angle = mo.ui.slider(0, 360, value=90, step=5, label="Where it sits (°)")
    attractor_height = mo.ui.slider(0.0, 1.0, value=0.5, step=0.02, label="How high (0 = bed, 1 = rim)")
    attractor_offset = mo.ui.slider(0, 60, value=24, label="Distance from the axis (mm)")
    attractor_reach = mo.ui.slider(2, 60, value=25, label="Reach (mm)")
    attractor_strength = mo.ui.slider(-15.0, 15.0, value=10.0, step=0.5, label="Strength (mm)")

    spout_on = mo.ui.checkbox(value=False, label="Spout")
    spout_angle = mo.ui.slider(0, 360, value=270, step=5, label="Which side (°)")
    spout_width = mo.ui.slider(10, 180, value=70, step=5, label="How wide (°)")
    spout_start = mo.ui.slider(0.0, 1.0, value=0.7, step=0.02, label="Starts at height")
    spout_reach = mo.ui.slider(0.0, 25.0, value=12.0, step=0.5, label="How far it sticks out (mm)")
    spout_lip = mo.ui.slider(0.0, 20.0, value=6.0, step=0.5, label="How far the lip rises (mm)")

    flat_on = mo.ui.checkbox(value=False, label="Flat face")
    flat_offset = mo.ui.slider(-30.0, 30.0, value=8.0, step=0.5, label="Where the plane sits (mm)")

    limit_on = mo.ui.checkbox(value=False, label="Overhang limiter")
    limit_share = mo.ui.slider(0.1, 2.0, value=0.5, step=0.05, label="Allowed step, as a share of bead width")

    mo.accordion(
        {
            "Base shape": mo.vstack([height, radius, segments]),
            "1 - Attractor — how close is this to a point in space?": mo.vstack(
                [
                    attractor_on,
                    attractor_angle,
                    attractor_height,
                    attractor_offset,
                    attractor_reach,
                    attractor_strength,
                    mo.md(
                        "A point floating next to the vessel. Every point on the path measures "
                        "its distance to it, and the wall moves outward by an amount that fades "
                        "to nothing at the edge of the reach.\n\n"
                        "Negative strength pulls inward instead — the same question, the "
                        "opposite answer. This is the Grasshopper attractor, and it is four "
                        "lines of Python.\n\n"
                        "The reach has to span the gap between the attractor and the wall or "
                        "nothing happens at all. At the default distance that gap is 4 mm. A "
                        "condition that never fires looks exactly like one that isn't there."
                    ),
                ]
            ),
            "2 - Spout — is this inside the region I care about?": mo.vstack(
                [
                    spout_on,
                    spout_angle,
                    spout_width,
                    spout_start,
                    spout_reach,
                    spout_lip,
                    mo.md(
                        "You wrote this one on day 3. `amount_at` there was a height band and "
                        "an angle sector, and it drove flow and extrusion; here the identical "
                        "test drives shape instead.\n\n"
                        "The new thing is that one condition drives two properties: the wall "
                        "pushes out and the rim lifts together. That is what makes it read as a "
                        "spout rather than a bulge with a bump on it."
                    ),
                ]
            ),
            "3 - Flat face — did this end up somewhere I don't want?": mo.vstack(
                [
                    flat_on,
                    flat_offset,
                    mo.md(
                        "The first two decide before placing the point. This one checks the "
                        "point *after*: anything past the plane gets pulled back onto it, so "
                        "the cross-section goes from a circle to a D.\n\n"
                        "It works no matter what the others did, because it only looks at the "
                        "result. Slide it negative and it cuts most of the vessel away."
                    ),
                ]
            ),
            "4 - Overhang limiter — what did the path already do?": mo.vstack(
                [
                    limit_on,
                    limit_share,
                    mo.md(
                        "The other three ask about the point in front of them. This one looks "
                        "backwards: it compares this point to the one directly underneath "
                        "it, a full lap ago, and refuses to let the wall step out further than "
                        "the bead can bridge.\n\n"
                        "Turn the attractor up until it overhangs badly, then switch this on. "
                        "The bulge doesn't disappear — it gets spread over more laps, because "
                        "the limit is per lap. The printing constraint from day 2 is now a rule "
                        "the code enforces instead of a number you have to remember."
                    ),
                ]
            ),
        },
        lazy=False,
    )
    return (
        attractor_angle,
        attractor_height,
        attractor_offset,
        attractor_on,
        attractor_reach,
        attractor_strength,
        flat_offset,
        flat_on,
        height,
        limit_on,
        limit_share,
        radius,
        segments,
        spout_angle,
        spout_lip,
        spout_on,
        spout_reach,
        spout_start,
        spout_width,
    )


@app.cell
def _(
    attractor_angle,
    attractor_height,
    attractor_offset,
    attractor_reach,
    height,
    spout_angle,
    spout_start,
    spout_width,
):
    # The four questions. Each returns a number; none of them place a point.

    centre = PRINTER.centre()

    # the attractor is a fixed point in space, worked out once
    attractor_radians = math.radians(attractor_angle.value)
    attractor_x = centre.x + attractor_offset.value * math.cos(attractor_radians)
    attractor_y = centre.y + attractor_offset.value * math.sin(attractor_radians)
    attractor_z = centre.z + attractor_height.value * height.value

    def pull_at(x, y, z):
        """1 on top of the attractor, 0 at the edge of its reach and beyond."""
        distance = math.dist((x, y, z), (attractor_x, attractor_y, attractor_z))
        if distance > attractor_reach.value:
            return 0.0
        return 1 - distance / attractor_reach.value

    def angle_gap(a, b):
        """Shortest way round between two angles, in degrees."""
        return abs((a - b + 180) % 360 - 180)

    def spout_at(fraction, degrees):
        """1 at the tip of the spout, 0 outside the region entirely."""
        if fraction < spout_start.value:
            return 0.0
        gap = angle_gap(degrees, spout_angle.value)
        if gap > spout_width.value / 2:
            return 0.0

        up_the_wall = (fraction - spout_start.value) / max(1 - spout_start.value, 0.001)
        across_the_sector = 1 - gap / (spout_width.value / 2)
        return up_the_wall * across_the_sector
    return centre, pull_at, spout_at


@app.cell
def _(
    attractor_on,
    attractor_strength,
    centre,
    flat_offset,
    flat_on,
    height,
    limit_on,
    limit_share,
    pull_at,
    radius,
    segments,
    spout_at,
    spout_lip,
    spout_on,
    spout_reach,
):
    # The loop. Same shape as day 2 — the only difference is that four of these lines
    # ask a question first. The order they run in is the order they are written in.

    laps = max(1, int(height.value / PRINTER.extrusion_height))
    total_points = laps * segments.value

    radii = []
    steps = []

    for i in range(total_points + 1):
        fraction = i / total_points
        angle = (i / segments.value) * math.tau
        degrees = math.degrees(angle) % 360

        r = radius.value
        z = centre.z + fraction * height.value

        if spout_on.value:
            amount = spout_at(fraction, degrees)
            r += spout_reach.value * amount
            z += spout_lip.value * amount

        # measured from where the point would have been, so the attractor
        # doesn't chase its own effect
        if attractor_on.value:
            unmoved_x = centre.x + r * math.cos(angle)
            unmoved_y = centre.y + r * math.sin(angle)
            r += attractor_strength.value * pull_at(unmoved_x, unmoved_y, z)

        # looks back one full lap, to the point directly underneath this one
        if limit_on.value and len(radii) >= segments.value:
            underneath = radii[-segments.value]
            allowed = PRINTER.extrusion_width * limit_share.value
            if r - underneath > allowed:
                r = underneath + allowed

        radii.append(r)

        x = centre.x + r * math.cos(angle)
        y = centre.y + r * math.sin(angle)

        # last, because it corrects whatever the others did
        if flat_on.value and y > centre.y + flat_offset.value:
            y = centre.y + flat_offset.value

        steps.append(fc.Point(x=x, y=y, z=z))
    return laps, steps


@app.cell(hide_code=True)
def _(steps):
    plot_steps(steps)
    return


@app.cell(hide_code=True)
def _(laps, segments, steps):
    _xs = [p.x for p in steps]
    _ys = [p.y for p in steps]
    _z = max(p.z for p in steps)

    _centre = PRINTER.centre()
    _radii = [math.hypot(p.x - _centre.x, p.y - _centre.y) for p in steps]
    _per_lap = segments.value
    # only growing outward overhangs; a lap that shrinks inward sits fully supported
    _steepest = max(
        (_radii[i + _per_lap] - _radii[i] for i in range(len(_radii) - _per_lap)),
        default=0.0,
    )

    _notes = [f"**{max(_xs) - min(_xs):.0f} × {max(_ys) - min(_ys):.0f} × {_z:.0f} mm**, {laps} laps."]

    if min(_xs) < 0 or max(_xs) > PRINTER.bed_width or min(_ys) < 0 or max(_ys) > PRINTER.bed_depth:
        _notes.append("### It runs off the bed.")
    if _z > PRINTER.max_height:
        _notes.append(f"### Taller than the {PRINTER.max_height} mm the gantry allows.")

    _notes.append(
        f"Steepest **outward** movement: **{_steepest:.2f} mm per lap** against a "
        f"{PRINTER.extrusion_width} mm bead. Growing outward is what overhangs; a lap that "
        "shrinks inward is fully supported, so only growth is counted here."
    )

    mo.md("\n\n".join(_notes))
    return


@app.cell(hide_code=True)
def _():
    name = mo.ui.text(value="conditions", label="Name")
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

    1. Attractor alone. Move it around the vessel and up and down. Then set reach to `25`,
       `12` and `6` in turn and watch the steepest-outward number climb from about `0.19`
       to `0.58` mm per lap — the same bulge, delivered in fewer laps.
    2. Reach down to `3`. Nothing happens: the attractor sits 4 mm off the wall and the
       reach no longer spans the gap. The condition is still running, and never fires.
    3. Attractor strength negative: a dent instead of a bulge.
    4. Reach `6`, strength `15`. The readout says about `0.87` mm per lap, past the
       `0.72` a bead this wide can bridge. Switch the limiter on: the bulge is still
       there, the readout drops to exactly `0.72`, and the wall gets to the same place
       over more laps.
    5. Spout alone. Narrow it to `20°`, then widen it to `160°`. Somewhere in between it
       stops being a spout and becomes an oval vessel.
    6. Flat face on, spout on, spout angle `90` so it points at the plane. The spout gets
       sliced off, because the flat face runs last and doesn't care what put the point
       there.
    7. Move the flat-face block above the attractor block and re-run. The face is no
       longer flat.

    ---

    Three of these ask about the point in front of them. The limiter asks about a point
    the loop already placed, which is why it needs `radii` — a list of what happened.
    Once code can look at its own output, it can react to anything it has done.

    That is the last thing this workshop shows you. `studio.py` is next, and it is empty.
    """)
    return


if __name__ == "__main__":
    app.run()
