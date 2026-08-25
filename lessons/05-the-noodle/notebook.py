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
        # 05 · The noodle

        Every setting you've met so far has a range the machine is happy with. Below is
        the same vessel from lesson 04 with five ways out of that range.

        Turn them up. Nothing here is a mistake — you're driving.
        """
    )
    return


@app.cell(hide_code=True)
def _():
    lean = mo.ui.slider(0.0, 3.0, value=0.0, step=0.05, label="Lean outward (mm per lap)")
    flow = mo.ui.slider(0.1, 4.0, value=1.0, step=0.1, label="Flow ×")
    wobble = mo.ui.slider(0.0, 6.0, value=0.0, step=0.1, label="Z wobble (mm)")
    wobble_freq = mo.ui.slider(1, 16, value=3, label="Wobbles per lap")
    speed = mo.ui.slider(0.2, 8.0, value=1.0, step=0.1, label="Speed ×")
    gap_every = mo.ui.slider(0, 40, value=0, label="Lift off every … segments")

    height = mo.ui.slider(5, 120, value=40, label="Height (mm)")
    radius = mo.ui.slider(3, 50, value=15, label="Radius (mm)")
    segments = mo.ui.slider(3, 128, value=48, label="Segments per lap")

    controls = mo.accordion(
        {
            "① Overhang — lean past what's underneath": mo.vstack(
                [
                    lean,
                    mo.md(
                        "Each lap sits on the one below. Push it outward faster than the "
                        "extrusion is wide and there is nothing under the outer edge. "
                        "It droops on the way down and freezes wherever it lands."
                    ),
                ]
            ),
            "② Flow — more or less plastic than the path needs": mo.vstack(
                [
                    flow,
                    mo.md(
                        "Below `1` the bead thins and breaks into a dotted line. Above `2` "
                        "there's nowhere for the excess to go, so it piles up and the nozzle "
                        "drags through it."
                    ),
                ]
            ),
            "③ Wobble — move z inside a lap": mo.vstack(
                [
                    wobble,
                    wobble_freq,
                    mo.md(
                        "Nothing says z has to hold still while x and y move. Once it "
                        "doesn't, 'layer' stops being a useful word for what you're making."
                    ),
                ]
            ),
            "④ Speed — outrun the extruder": mo.vstack(
                [
                    speed,
                    mo.md(
                        "The nozzle can move faster than melted plastic can leave it. "
                        "Past that point the bead stretches into a thread."
                    ),
                ]
            ),
            "⑤ Air — stop extruding, keep moving": mo.vstack(
                [
                    gap_every,
                    mo.md(
                        "Extruder off, nozzle still travelling. Pressure in the nozzle keeps "
                        "pushing anyway and trails a thread behind. Slicers spend a lot of "
                        "effort hiding this."
                    ),
                ]
            ),
            "Shape": mo.vstack([height, radius, segments]),
        },
        lazy=False,
    )
    controls
    return flow, gap_every, height, lean, radius, segments, speed, wobble, wobble_freq


@app.cell(hide_code=True)
def _():
    show_code = mo.ui.checkbox(label="Show code")
    show_code
    return (show_code,)


@app.cell
def _(flow, gap_every, height, lean, radius, segments, show_code, speed, wobble, wobble_freq):
    centre = PRINTER.centre()
    laps = max(1, int(height.value / PRINTER.extrusion_height))
    total_points = laps * segments.value

    steps = [
        fc.ExtrusionGeometry(width=PRINTER.extrusion_width * flow.value, height=PRINTER.extrusion_height),
        fc.Printer(print_speed=int(PRINTER.print_speed * speed.value)),
    ]

    extruder_is_on = True
    for i in range(total_points + 1):
        lap = i / segments.value
        fraction = i / total_points
        angle = lap * math.tau

        r = radius.value + lap * lean.value

        z = centre.z + fraction * height.value
        if wobble.value:
            z += wobble.value * math.sin(angle * wobble_freq.value)

        # ⑤ toggle the extruder off for one segment at a time
        if gap_every.value:
            should_be_on = (i % gap_every.value) != 0
            if should_be_on != extruder_is_on:
                steps.append(fc.Extruder(on=should_be_on))
                extruder_is_on = should_be_on

        steps.append(fc.Point(x=centre.x + r * math.cos(angle), y=centre.y + r * math.sin(angle), z=z))

    mo.show_code() if show_code.value else None
    return laps, steps


@app.cell(hide_code=True)
def _(steps):
    plot_steps(steps)
    return


@app.cell(hide_code=True)
def _(flow, lean, speed):
    _unsupported = lean.value / PRINTER.extrusion_width

    _notes = []
    if _unsupported > 0:
        _notes.append(f"**{_unsupported:.0%} of each lap hangs over nothing.** Past ~50% it stops being a wall.")
    if flow.value < 0.6:
        _notes.append("**Starved.** Not enough plastic to make a continuous bead.")
    if flow.value > 2.0:
        _notes.append(f"**{flow.value:.1f}× the plastic the path has room for.** It has to go somewhere.")
    if speed.value > 2.5:
        _notes.append("**Faster than the melt.** The bead thins and eventually gives up.")

    mo.md("\n\n".join(_notes) if _notes else "All five within spec. This one would print cleanly.")
    return


@app.cell(hide_code=True)
def _():
    name = mo.ui.text(value="noodle", label="Name")
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
        ---

        ## Keep a list

        Write down which settings gave you something you'd want again. Not "which ones
        worked" — which ones were *interesting*. Those two lists are different and
        tomorrow only needs the second one.

        **Who decided these were faults?**

        Nothing you just made is broken. It's outside a specification, and that
        specification was written by people trying to make prints that look like
        injection mouldings. That was their problem.
        """
    )
    return


if __name__ == "__main__":
    app.run()
