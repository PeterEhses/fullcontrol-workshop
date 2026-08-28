import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")

with app.setup:
    import math

    import marimo as mo
    import fullcontrol as fc

    from workshop import PRINTER, plot_steps, save_gcode

    # Pasta is extruded: dough pushed through a die. The die is the cross-section, and
    # the noodle is that cross-section dragged along a line. A die cannot change partway
    # along its length — that constraint is the subject of b-past-the-die.py.
    #
    # All eight shapes below are the same loop with different numbers.
    PASTA = {
        "Ziti — plain tube": dict(
            length=60, radius=9, ridges=0, ridge_depth=0.0, rings=0, ring_depth=0.0,
            twist=0.0, slant=0.0, bend=0.0, coil=0.0, coil_turns=0.0,
        ),
        "Rigatoni — straight ridges": dict(
            length=45, radius=10, ridges=14, ridge_depth=0.16, rings=0, ring_depth=0.0,
            twist=0.0, slant=0.0, bend=0.0, coil=0.0, coil_turns=0.0,
        ),
        "Penne — ridges, cut on the diagonal": dict(
            length=55, radius=8, ridges=12, ridge_depth=0.14, rings=0, ring_depth=0.0,
            twist=0.0, slant=7.0, bend=0.0, coil=0.0, coil_turns=0.0,
        ),
        "Fusilli — three twisted blades": dict(
            length=70, radius=8, ridges=3, ridge_depth=0.45, rings=0, ring_depth=0.0,
            twist=3.0, slant=0.0, bend=0.0, coil=0.0, coil_turns=0.0,
        ),
        "Maccheroni — the bent tube": dict(
            length=55, radius=7, ridges=0, ridge_depth=0.0, rings=0, ring_depth=0.0,
            twist=0.0, slant=0.0, bend=14.0, coil=0.0, coil_turns=0.0,
        ),
        "Cavatappi — corkscrew": dict(
            length=80, radius=6, ridges=10, ridge_depth=0.14, rings=0, ring_depth=0.0,
            twist=1.0, slant=0.0, bend=0.0, coil=9.0, coil_turns=2.5,
        ),
        "Radiatori — stacked frills": dict(
            length=40, radius=9, ridges=8, ridge_depth=0.5, rings=9, ring_depth=0.3,
            twist=0.0, slant=0.0, bend=0.0, coil=0.0, coil_turns=0.0,
        ),
        "Bucatini — thin, long, hollow": dict(
            length=120, radius=3.5, ridges=0, ridge_depth=0.0, rings=0, ring_depth=0.0,
            twist=0.0, slant=0.0, bend=0.0, coil=0.0, coil_turns=0.0,
        ),
    }


@app.cell(hide_code=True)
def _():
    mo.md("""
    # Day 3a - The die

    Pasta is extruded: dough is pushed through a metal die and comes out as a continuous
    shape, which is then cut. The die is a cross-section, and the noodle is that
    cross-section dragged along a line.

    Yesterday's vessel was the same operation — a circle dragged upward. The eight shapes
    in the dropdown are all one loop; only the numbers differ. Pick one and find out
    which number was doing the work.
    """)
    return


@app.cell(hide_code=True)
def _():
    shape = mo.ui.dropdown(options=list(PASTA), value="Rigatoni — straight ridges", label="Shape")
    shape
    return (shape,)


@app.cell(hide_code=True)
def _(shape):
    # changing the dropdown rebuilds these with the new shape's numbers, which is the
    # point — you get a starting noodle and then you push it around
    _p = PASTA[shape.value]

    length = mo.ui.slider(10, 150, value=_p["length"], label="Length (mm)")
    radius = mo.ui.slider(2.0, 30.0, value=_p["radius"], step=0.5, label="Radius (mm)")
    segments = mo.ui.slider(8, 160, value=72, label="Segments per lap")

    ridges = mo.ui.slider(0, 30, value=_p["ridges"], label="Ridges")
    ridge_depth = mo.ui.slider(0.0, 0.8, value=_p["ridge_depth"], step=0.02, label="Ridge depth")

    rings = mo.ui.slider(0, 30, value=_p["rings"], label="Rings")
    ring_depth = mo.ui.slider(0.0, 0.8, value=_p["ring_depth"], step=0.02, label="Ring depth")

    twist = mo.ui.slider(-6.0, 6.0, value=_p["twist"], step=0.1, label="Twist (turns)")
    slant = mo.ui.slider(0.0, 20.0, value=_p["slant"], step=0.5, label="Slant of the cut (mm)")

    bend = mo.ui.slider(-40.0, 40.0, value=_p["bend"], step=0.5, label="Bend (mm sideways)")
    coil = mo.ui.slider(0.0, 30.0, value=_p["coil"], step=0.5, label="Coil radius (mm)")
    coil_turns = mo.ui.slider(0.0, 6.0, value=_p["coil_turns"], step=0.1, label="Coil turns")

    mo.accordion(
        {
            "The tube": mo.vstack([length, radius, segments]),
            "Around — ridges": mo.vstack(
                [
                    ridges,
                    ridge_depth,
                    mo.md(
                        "A wave added to the radius, repeating a whole number of times "
                        "around the tube. `14` shallow ones is rigatoni; `3` deep ones is "
                        "fusilli. This is the die: fixed for the whole length."
                    ),
                ]
            ),
            "Along — rings": mo.vstack(
                [
                    rings,
                    ring_depth,
                    mo.md("The same wave, running up the tube instead of round it. Both at once is radiatori."),
                ]
            ),
            "Twist and cut": mo.vstack(
                [
                    twist,
                    slant,
                    mo.md(
                        "**Twist** rotates the cross-section as it climbs — a straight blade "
                        "becomes a spiral one.\n\n"
                        "**Slant** cuts the top off on a diagonal. The path keeps spiralling "
                        "all the way up either way — it just stops laying plastic once it is "
                        "past the cut on that side. Watch the thin travel lines appear at the top."
                    ),
                ]
            ),
            "Where the tube goes": mo.vstack(
                [
                    bend,
                    coil,
                    coil_turns,
                    mo.md(
                        "So far the tube has gone straight up. **Bend** leans the axis "
                        "sideways as it rises; **coil** sends it round a helix.\n\n"
                        "The cross-section code is untouched — only the position of its "
                        "centre changes. Day 4 is built on that separation."
                    ),
                ]
            ),
        },
        lazy=False,
    )
    return (
        bend,
        coil,
        coil_turns,
        length,
        radius,
        ridge_depth,
        ridges,
        ring_depth,
        rings,
        segments,
        slant,
        twist,
    )


@app.cell
def _(
    bend,
    coil,
    coil_turns,
    length,
    radius,
    ridge_depth,
    ridges,
    ring_depth,
    rings,
    segments,
    slant,
    twist,
):
    origin = PRINTER.centre()
    laps = max(1, int(length.value / PRINTER.extrusion_height))
    total_points = laps * segments.value

    steps = [fc.Extruder(on=True)]
    extruding = True

    for i in range(total_points + 1):
        lap = i / segments.value
        fraction = i / total_points

        round_the_tube = lap % 1.0
        angle = round_the_tube * math.tau + fraction * twist.value * math.tau

        # the die: a circle with a wave added to it
        r = radius.value
        if ridges.value:
            r += radius.value * ridge_depth.value * math.sin(round_the_tube * math.tau * ridges.value)
        if rings.value:
            r += radius.value * ring_depth.value * math.sin(fraction * math.tau * rings.value)

        # where the middle of the tube is at this height. straight up unless you say otherwise.
        axis_x = bend.value * fraction**2
        axis_y = 0.0
        if coil.value:
            coil_angle = fraction * coil_turns.value * math.tau
            axis_x += coil.value * (math.cos(coil_angle) - 1)
            axis_y += coil.value * math.sin(coil_angle)

        z = origin.z + fraction * length.value

        # penne's diagonal end: the tube is shorter on one side. the path still spirals
        # all the way up, it just stops laying plastic once it's past the cut.
        if slant.value:
            cut_height = length.value - slant.value * (1 - math.cos(angle)) / 2
            should_extrude = (fraction * length.value) <= cut_height
            if should_extrude != extruding:
                steps.append(fc.Extruder(on=should_extrude))
                extruding = should_extrude

        steps.append(
            fc.Point(
                x=origin.x + axis_x + r * math.cos(angle),
                y=origin.y + axis_y + r * math.sin(angle),
                z=z,
            )
        )
    return laps, steps


@app.cell(hide_code=True)
def _(steps):
    plot_steps(steps)
    return


@app.cell(hide_code=True)
def _(bend, coil, laps, radius, ridge_depth, steps):
    # how far the wall shifts sideways between one lap and the next
    _drift = (abs(bend.value) + coil.value * 2) / max(laps, 1)
    _overhang = _drift / PRINTER.extrusion_width

    _notes = [f"**{len(steps)} points**, one continuous path, {laps} laps."]
    if _overhang > 0.35:
        _notes.append(
            f"Each lap sits about **{_overhang:.0%}** off the one below it. Past roughly half "
            "an extrusion width there's nothing underneath the outer edge, and it starts to "
            "droop on the way down."
        )
    if radius.value * (1 - ridge_depth.value) < PRINTER.extrusion_width:
        _notes.append(
            "The ridges are cutting deeper than the wall is thick. The valleys will collide "
            "with themselves."
        )

    mo.md("\n\n".join(_notes))
    return


@app.cell(hide_code=True)
def _(shape):
    name = mo.ui.text(value=shape.value.split(" —")[0].lower(), label="Name")
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

    1. Rigatoni. Raise ridge depth until the readout warns that the valleys are cutting
       deeper than the wall is thick, and look at what the preview does there.
    2. From rigatoni, add twist. Nothing structural changed and it is now fusilli.
    3. Bend, then coil. The cross-section code is untouched; only the centre moves.
    4. Push bend and coil until the noodle stops standing up. The readout gives the
       overhang per lap as a percentage of extrusion width. Past about 50% there is
       nothing under the outer edge of the bead.
    5. Segments per lap to `5`, on any shape.

    ---

    Each shape in the dropdown exists because a factory can extrude it, cut it, dry it
    without cracking, box it without breaking, and cook it evenly. Those are real
    constraints on a real product and none of them apply here.

    The one constraint that does apply is the die itself: a single fixed cross-section
    for the whole length. `b-past-the-die.py` removes it.
    """)
    return


if __name__ == "__main__":
    app.run()
