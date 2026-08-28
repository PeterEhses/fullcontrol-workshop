import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")

with app.setup:
    import math
    import random

    import marimo as mo
    import fullcontrol as fc

    from workshop import PRINTER, plot_controls, plot_steps, save_gcode


@app.cell(hide_code=True)
def _():
    mo.md("""
    # Reference - Coral

    Every vessel so far has been a formula. You give it a height and an angle and it
    returns a radius — layer 90 does not need to know what layer 89 did, because both are
    worked out from the same equation.

    This one is not a formula. A single closed loop of points starts as a circle, and each
    layer it grows (outward, or inward wherever it faces that way), smooths itself, pushes
    apart wherever it has folded back near itself, and re-spaces its points so none drift
    too far apart. Then the nozzle prints where the loop currently is, z rises by one layer
    height, and it happens again.

    So the layer being printed is the current state of a simulation, and the object is the
    record of it. The growth rule is the one behind coral, frost on a window and the edge
    of a bacterial colony: growth arrives from outside, so a bump that sticks out collects
    more of it than a hollow does, and the difference feeds itself.

    None of the Python below is new. It is the day 4 loop that looks back at its own
    output, run 125 times over.
    """)
    return


@app.cell(hide_code=True)
def _():
    height = mo.ui.slider(20, 140, value=60, label="Height (mm)")
    base_radius = mo.ui.slider(4, 40, value=10, label="Starting radius (mm)")
    envelope = mo.ui.slider(15, 100, value=55, label="Envelope — how far out it may reach (mm)")
    floor = mo.ui.checkbox(value=True, label="Spiral floor")

    growth_per_layer = mo.ui.slider(0.0, 0.8, value=0.30, step=0.01, label="Growth per layer (mm)")
    taper = mo.ui.slider(0.0, 2.0, value=0.6, step=0.05, label="Growth left at the rim (×)")
    tip_advantage = mo.ui.slider(0.0, 10.0, value=4.0, step=0.5, label="Tip advantage")
    bias = mo.ui.slider(-1.0, 1.0, value=1.0, step=0.05, label="Bias — outward (1) to inward (-1)")
    vigour_spread = mo.ui.slider(0.0, 1.0, value=0.5, step=0.05, label="Vigour spread")
    mutation = mo.ui.slider(0.0, 0.5, value=0.15, step=0.01, label="Mutation when a point splits")

    sense_radius = mo.ui.slider(2.0, 30.0, value=12.0, step=0.5, label="How far a point can see (mm)")
    crowd_limit = mo.ui.slider(1, 20, value=4, label="Neighbours in sight that stop it entirely")
    smoothing = mo.ui.slider(0.0, 0.9, value=0.35, step=0.05, label="Smoothing")

    wall_gap = mo.ui.slider(1.0, 4.0, value=1.6, step=0.1, label="Keep-apart distance (× bead width)")
    step_limit = mo.ui.slider(0.1, 1.5, value=0.5, step=0.05, label="Allowed move per layer (× bead width)")

    seed = mo.ui.number(0, 9999, value=3, label="Seed")

    mo.accordion(
        {
            "The vessel": mo.vstack(
                [
                    height,
                    base_radius,
                    envelope,
                    floor,
                    mo.md(
                        "The envelope is a hard circular limit around the centre of the bed. It "
                        "is not part of the growth model — it is there so the vessel cannot walk "
                        "off the bed, and arms that reach it flatten against it.\n\n"
                        "Spiral floor fills the first layer before the wall starts: one "
                        "Archimedean spiral out from the centre, a bead width per turn, stopping "
                        "half a bead short of where the wall will land. Without it you get an "
                        "open tube, which is the day 2 vessel and holds nothing."
                    ),
                ]
            ),
            "Growth — how much arrives, and where": mo.vstack(
                [
                    growth_per_layer,
                    taper,
                    tip_advantage,
                    bias,
                    vigour_spread,
                    mutation,
                    mo.md(
                        "Growth per layer is how far an unobstructed point moves outward each "
                        "layer, before anything else gets a say.\n\n"
                        "Growth left at the rim scales that with height. `1.0` keeps growing "
                        "all the way up and the vessel opens like a bowl; `0.0` stops it and the "
                        "arms finish as vertical fins.\n\n"
                        "Tip advantage is the mechanism. A point bulging outward past its two "
                        "neighbours grows faster; one sitting in a hollow grows slower. At `0` the "
                        "loop stays a circle however long you run it — everything else here is "
                        "only interesting because of this number.\n\n"
                        "Bias is which way a point faces. Every point grows either outward or "
                        "inward, and the bias sets the odds at the start: `1.0` and all of them "
                        "face out, `0.0` and it is a coin toss each, `-1.0` and they all face in "
                        "and the vessel closes as it rises instead of opening.\n\n"
                        "In between, inward-facing regions hold their ground while their "
                        "neighbours advance past them, so you get fewer, longer limbs and less "
                        "body between them. Outward still wins on anything short of `-1.0`, and "
                        "not because it grows faster: a region that advances stretches the loop "
                        "and is given new points, one that retreats is squeezed and loses them. "
                        "Whichever way a region faces, it passes that on to the points it "
                        "gains — so the population tilts outward on its own.\n\n"
                        "Tip advantage follows whichever way a point faces, so an inward-facing "
                        "point runs fastest at the deepest part of its own hollow. A tip is a tip "
                        "whichever way the front is moving.\n\n"
                        "Vigour is how fast a point grows, randomly `1 +/-` the spread at "
                        "the start. When the loop stretches and a new point is born between two "
                        "old ones it inherits the average of their vigour, plus a little "
                        "mutation, and the facing of one or the other outright. A point that "
                        "happened to be lucky founds an arm, and the arm keeps its character all "
                        "the way up."
                    ),
                ]
            ),
            "Screening — why it stops": mo.vstack(
                [
                    sense_radius,
                    crowd_limit,
                    smoothing,
                    mo.md(
                        "Each point counts the parts of the loop it can see and is not attached "
                        "to — the arm it is standing on does not count. At crowd limit of "
                        "them it stops growing altogether.\n\n"
                        "This is what turns a fringe into arms. Once two bumps have separated, "
                        "the trench between them is screened by both, so it stalls while the "
                        "bumps carry on. Sight radius is the scale the arms space themselves at, "
                        "and it has an upper end: at `20 mm` a point can see clear across the "
                        "vessel's own mouth, screens itself, and nothing grows at all.\n\n"
                        "Smoothing pulls every point toward the midpoint of its neighbours — "
                        "surface tension, working against the tip advantage. It is what keeps the "
                        "tip advantage acting at the scale of an arm rather than the scale of a "
                        "point: too little and the loop grows a sawtooth that starves everything "
                        "around it, leaving a few thin spindly arms, and below about `0.15` it "
                        "crinkles and stalls near where it started. Above `0.55` it swallows the "
                        "arms before they form."
                    ),
                ]
            ),
            "What the printer allows": mo.vstack(
                [
                    wall_gap,
                    step_limit,
                    mo.md(
                        "Keep-apart distance is the repulsion. Two stretches of loop that come "
                        "closer than this push each other away, which is why arms never cross and "
                        "why there is always a gap the nozzle fits into. Below `1.0 ×` the walls "
                        "run into each other.\n\n"
                        "Allowed move per layer is the day 4 overhang limiter, and it is the "
                        "reason any of this prints. No point may move further sideways in one "
                        "layer than this, so every bead lands mostly on the one below. Growth, "
                        "smoothing and repulsion all get clipped by it: the simulation proposes, "
                        "the machine decides."
                    ),
                ]
            ),
            "Seed": mo.vstack(
                [
                    seed,
                    mo.md(
                        "The starting vigours and the mutations come from this. Same seed, same "
                        "vessel, every time. Change it and you get a different individual of the "
                        "same species."
                    ),
                ]
            ),
        },
        lazy=False,
    )
    return (
        base_radius,
        bias,
        crowd_limit,
        envelope,
        floor,
        growth_per_layer,
        height,
        mutation,
        seed,
        sense_radius,
        smoothing,
        step_limit,
        taper,
        tip_advantage,
        vigour_spread,
        wall_gap,
    )


@app.cell
def _(
    base_radius,
    bias,
    crowd_limit,
    envelope,
    growth_per_layer,
    height,
    mutation,
    seed,
    sense_radius,
    smoothing,
    step_limit,
    taper,
    tip_advantage,
    vigour_spread,
    wall_gap,
):
    # The simulation. One closed loop of points, five passes over it per layer. It all
    # happens in millimetres on the bed — these are print coordinates from the first line,
    # not an abstract space that gets scaled to fit later.

    rng = random.Random(int(seed.value))
    centre = PRINTER.centre()
    spacing = PRINTER.extrusion_width
    layers = max(2, int(height.value / PRINTER.extrusion_height))

    allowed_move = PRINTER.extrusion_width * step_limit.value
    keep_apart = PRINTER.extrusion_width * wall_gap.value

    def index_gap(i, j, count):
        """How far apart two points are along the loop, going the short way round."""
        gap = abs(i - j)
        return min(gap, count - gap)

    # Checking every point against every other one is half a million distance calculations
    # per layer, and the notebook stops being usable. Instead drop the points into squares
    # of a coarse grid, and only ever look in the nine squares around you.
    def build_grid(xs, ys, cell_size):
        squares = {}
        for i in range(len(xs)):
            key = (int(xs[i] // cell_size), int(ys[i] // cell_size))
            squares.setdefault(key, []).append(i)
        return squares

    def nearby(squares, cell_size, x, y):
        found = []
        gx = int(x // cell_size)
        gy = int(y // cell_size)
        for a in (gx - 1, gx, gx + 1):
            for b in (gy - 1, gy, gy + 1):
                bucket = squares.get((a, b))
                if bucket is not None:
                    found.extend(bucket)
        return found

    # A circle, points one bead width apart. Each point carries two things it will pass
    # on: how fast it grows, and which way it faces. The bias decides how many of them
    # start out facing inward.
    start_count = max(8, int(math.tau * base_radius.value / spacing))
    facing_out = (1 + bias.value) / 2
    xs = []
    ys = []
    vigour = []
    facing = []
    for point in range(start_count):
        angle = (point / start_count) * math.tau
        xs.append(centre.x + base_radius.value * math.cos(angle))
        ys.append(centre.y + base_radius.value * math.sin(angle))
        vigour.append(1 + vigour_spread.value * (rng.random() * 2 - 1))
        facing.append(1 if rng.random() < facing_out else -1)

    contours = []
    steepest_move = 0.0

    for layer in range(layers):
        count = len(xs)
        was_x = list(xs)
        was_y = list(ys)

        # points this close along the loop are your own arm, not something you have folded
        # back onto — they neither screen you nor push you away
        own_arm = int(sense_radius.value / spacing) + 1
        own_wall = int(keep_apart / spacing) + 1
        cell_size = max(sense_radius.value, keep_apart)
        squares = build_grid(xs, ys, cell_size)

        # 1 - grow. Outward, faster at tips, slower where the loop is crowded.
        grown_x = list(xs)
        grown_y = list(ys)
        height_fraction = layer / layers
        arriving = growth_per_layer.value * (1 + (taper.value - 1) * height_fraction)

        for i in range(count):
            before_x = xs[i - 1]
            before_y = ys[i - 1]
            after_x = xs[(i + 1) % count]
            after_y = ys[(i + 1) % count]

            # the loop runs anticlockwise, so this normal points out of it
            along_x = after_x - before_x
            along_y = after_y - before_y
            length = math.hypot(along_x, along_y) or 1
            out_x = along_y / length
            out_y = -along_x / length

            # how far this point sticks out past the straight line between its two
            # neighbours, in bead widths. Positive on a bump, negative in a hollow.
            mid_x = (before_x + after_x) / 2
            mid_y = (before_y + after_y) / 2
            bulge = -((mid_x - xs[i]) * out_x + (mid_y - ys[i]) * out_y) / spacing

            crowd = 0
            for j in nearby(squares, cell_size, xs[i], ys[i]):
                if index_gap(i, j, count) <= own_arm:
                    continue
                if math.dist((xs[i], ys[i]), (xs[j], ys[j])) < sense_radius.value:
                    crowd += 1
            screening = max(0.0, 1 - crowd / crowd_limit.value)

            # the tip advantage follows the way this point faces, so a point growing
            # inward runs fastest at the deepest part of its own hollow
            tip = max(0.0, 1 + tip_advantage.value * bulge * facing[i])

            amount = arriving * vigour[i] * facing[i] * tip * screening
            grown_x[i] = xs[i] + out_x * amount
            grown_y[i] = ys[i] + out_y * amount

        xs = grown_x
        ys = grown_y

        # 2 - smooth. Every point moves part of the way to the midpoint of its neighbours.
        smooth_x = list(xs)
        smooth_y = list(ys)
        for i in range(count):
            mid_x = (xs[i - 1] + xs[(i + 1) % count]) / 2
            mid_y = (ys[i - 1] + ys[(i + 1) % count]) / 2
            smooth_x[i] = xs[i] + smoothing.value * (mid_x - xs[i])
            smooth_y[i] = ys[i] + smoothing.value * (mid_y - ys[i])
        xs = smooth_x
        ys = smooth_y

        # 3 - push apart. Where the loop has folded back near itself, those are two walls
        # with a gap between them, and the gap has to stay wide enough for the nozzle.
        squares = build_grid(xs, ys, cell_size)
        pushed_x = list(xs)
        pushed_y = list(ys)
        for i in range(count):
            for j in nearby(squares, cell_size, xs[i], ys[i]):
                if j == i or index_gap(i, j, count) <= own_wall:
                    continue
                away_x = xs[i] - xs[j]
                away_y = ys[i] - ys[j]
                distance = math.hypot(away_x, away_y)
                if 0.001 < distance < keep_apart:
                    # a third of the shortfall, because the other point is pushing too and
                    # the whole thing runs again next layer
                    push = (keep_apart - distance) / distance * 0.3
                    pushed_x[i] += away_x * push
                    pushed_y[i] += away_y * push
        xs = pushed_x
        ys = pushed_y

        # 4 - clip. Whatever the three passes above decided, no point may move further in
        # one layer than the bead can overhang, and none may leave the envelope.
        for i in range(count):
            moved_x = xs[i] - was_x[i]
            moved_y = ys[i] - was_y[i]
            moved = math.hypot(moved_x, moved_y)
            if moved > allowed_move:
                xs[i] = was_x[i] + moved_x / moved * allowed_move
                ys[i] = was_y[i] + moved_y / moved * allowed_move
                moved = allowed_move
            steepest_move = max(steepest_move, moved)

            from_centre = math.hypot(xs[i] - centre.x, ys[i] - centre.y)
            if from_centre > envelope.value:
                xs[i] = centre.x + (xs[i] - centre.x) / from_centre * envelope.value
                ys[i] = centre.y + (ys[i] - centre.y) / from_centre * envelope.value

        # 5 - re-space. The loop is longer than it was, so it needs more points; where it
        # has been squeezed together it needs fewer. New points are born here, between the
        # two they inherit from: vigour is the average of the pair, but facing is taken
        # whole from one of them, so an inward region keeps a hard edge instead of fading
        # into the outward one beside it.
        spaced_x = []
        spaced_y = []
        spaced_vigour = []
        spaced_facing = []
        for i in range(count):
            j = (i + 1) % count
            spaced_x.append(xs[i])
            spaced_y.append(ys[i])
            spaced_vigour.append(vigour[i])
            spaced_facing.append(facing[i])

            if math.dist((xs[i], ys[i]), (xs[j], ys[j])) > spacing * 1.5:
                inherited = (vigour[i] + vigour[j]) / 2 + mutation.value * (rng.random() * 2 - 1)
                spaced_x.append((xs[i] + xs[j]) / 2)
                spaced_y.append((ys[i] + ys[j]) / 2)
                spaced_vigour.append(min(2.5, max(0.0, inherited)))
                spaced_facing.append(facing[i] if rng.random() < 0.5 else facing[j])

        xs = []
        ys = []
        vigour = []
        facing = []
        for i in range(len(spaced_x)):
            if xs and math.dist((xs[-1], ys[-1]), (spaced_x[i], spaced_y[i])) < spacing * 0.5:
                continue
            xs.append(spaced_x[i])
            ys.append(spaced_y[i])
            vigour.append(spaced_vigour[i])
            facing.append(spaced_facing[i])

        contours.append((list(xs), list(ys)))
    return centre, contours, layers, steepest_move


@app.cell
def _(centre, contours, floor, layers):
    # The growing is over and the printing hasn't started. Now the stack of loops becomes
    # one continuous path: the floor, then the first layer flat on the bed so it sticks,
    # then z climbing through each loop the way it has since day 2.

    bead = PRINTER.extrusion_width
    layer_height = PRINTER.extrusion_height
    steps = []

    if floor.value:
        # An Archimedean spiral out from the centre, filling the bottom before the wall
        # goes up around it. It has to stop half a bead short of the tightest part of the
        # wall, so work out how many whole turns fit in that and spread them across it —
        # otherwise the last turn stops wherever it happens to and leaves a bare ring.
        wall_x, wall_y = contours[0]
        room = None
        for node in range(len(wall_x)):
            reach = math.hypot(wall_x[node] - centre.x, wall_y[node] - centre.y)
            if room is None or reach < room:
                room = reach
        room -= bead * 0.5

        turns = max(1, int(room / bead))
        pitch = room / turns

        turn = 0.0
        while turn < turns * math.tau:
            spiral_radius = pitch * turn / math.tau
            steps.append(
                fc.Point(
                    x=centre.x + spiral_radius * math.cos(turn),
                    y=centre.y + spiral_radius * math.sin(turn),
                    z=centre.z,
                )
            )
            # small enough a step that each chord is about a bead long, so the spiral is
            # drawn as finely near the centre as it is at the edge
            turn += bead / max(spiral_radius, bead)

    for printing_layer in range(layers):
        loop_x, loop_y = contours[printing_layer]
        node_count = len(loop_x)

        # Each loop is its own list of points with its own arbitrary starting position, so
        # start printing it at whichever point is nearest the nozzle. Without this the
        # seam jumps around and drags a scar across the vessel every layer.
        start = 0
        if steps:
            here = steps[-1]
            shortest = None
            for node in range(node_count):
                gap = math.dist((loop_x[node], loop_y[node]), (here.x, here.y))
                if shortest is None or gap < shortest:
                    shortest = gap
                    start = node

        # the bottom layer stays flat and closes on itself; every layer above it climbs
        if printing_layer == 0:
            for along in range(node_count + 1):
                node = (start + along) % node_count
                steps.append(fc.Point(x=loop_x[node], y=loop_y[node], z=centre.z))
            continue

        base_z = centre.z + printing_layer * layer_height
        for along in range(node_count):
            node = (start + along) % node_count
            steps.append(
                fc.Point(
                    x=loop_x[node],
                    y=loop_y[node],
                    z=base_z + layer_height * (along / node_count),
                )
            )
    return (steps,)


@app.cell(hide_code=True)
def _():
    preview = mo.ui.radio(
        options={"Centre line — fast": "line", "Real bead width — heavy": "tube"},
        value="Centre line — fast",
        inline=True,
        label="Preview",
    )
    preview
    return (preview,)


@app.cell(hide_code=True)
def _(preview, steps):
    # Every other notebook previews at real bead width. This one is 27,000 points, and a
    # tube around each of them is about 16 MB of mesh — past what marimo will send to the
    # browser, and slow to spin around once it gets there. The centre line is a fiftieth
    # of that, so it is the default here and the tube is on request.
    _mesh_estimate = len(steps) * 570

    if preview.value == "tube" and _mesh_estimate < 8_000_000:
        _view = plot_steps(steps)
    elif preview.value == "tube":
        _view = mo.vstack(
            [
                mo.md(
                    f"A tube around every point would be about **{_mesh_estimate / 1e6:.0f} MB** "
                    "of mesh, past marimo's 8 MB output limit — centre line shown instead. Drop "
                    "the height to around `30 mm` to see this one at bead width."
                ),
                plot_steps(steps, plot_controls(style="line")),
            ]
        )
    else:
        _view = plot_steps(steps, plot_controls(style="line"))

    _view
    return


@app.cell(hide_code=True)
def _(contours, layers, steepest_move, steps):
    _xs = [p.x for p in steps]
    _ys = [p.y for p in steps]
    _top = max(p.z for p in steps)

    _length = 0.0
    for _i in range(1, len(steps)):
        _length += math.dist(
            (steps[_i].x, steps[_i].y, steps[_i].z),
            (steps[_i - 1].x, steps[_i - 1].y, steps[_i - 1].z),
        )

    _notes = [
        f"**{max(_xs) - min(_xs):.0f} × {max(_ys) - min(_ys):.0f} × {_top:.0f} mm**, "
        f"{layers} layers, {len(steps):,} points.",
        f"The loop started with {len(contours[0][0])} points and finished with "
        f"{len(contours[-1][0])}. That is the perimeter divided by the bead width, so it is "
        "also how much wall each layer has to print.",
        f"One continuous bead **{_length / 1000:.1f} m** long — around "
        f"**{_length / PRINTER.print_speed:.0f} minutes** at {PRINTER.print_speed} mm/min, "
        "before the printer's own acceleration limits get involved.",
        f"Steepest sideways move: **{steepest_move:.2f} mm per layer** against a "
        f"{PRINTER.extrusion_width} mm bead.",
    ]

    if min(_xs) < 0 or max(_xs) > PRINTER.bed_width or min(_ys) < 0 or max(_ys) > PRINTER.bed_depth:
        _notes.append("### It runs off the bed. Bring the envelope in.")
    if _top > PRINTER.max_height:
        _notes.append(f"### Taller than the {PRINTER.max_height} mm the gantry allows.")

    mo.md("\n\n".join(_notes))
    return


@app.cell(hide_code=True)
def _():
    name = mo.ui.text(value="coral", label="Name")
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

    1. Tip advantage to `0`. Everything else stays. The loop grows outward into a
       slightly lumpy disc and never breaks into arms, while screening, vigour, mutation
       and repulsion all keep running. None of them can break the symmetry on their own.
    2. Back to `4`, then smoothing at `0.2`, `0.45` and `0.6`. Three different
       objects: four long thin arms, a body with a dozen short fat ones, a rounded blob
       with none. Surface tension against tip advantage, and nothing else changed.
    3. Sight radius `4`, then `20`, crowd limit unchanged. At `4` you get a disc cut
       by narrow slits — screening only reaches across a trench, so trenches are all you
       get. At `20` every point can see the far side of the vessel, everything screens
       everything, growth stops on layer one and smoothing slowly pulls the loop in.
    4. Allowed move per layer to `1.2 ×`. The form gets what it wants: arms flare out
       within a third of the height. The readout will say around `1.1 mm` per layer
       against a `1.45 mm` bead, so on a real printer the flare droops and then drops.
    5. Keep-apart distance `1.0 ×`, then `3.0 ×`. At `1.0` the two walls of a cleft
       come within a bead of each other and fuse. At `3.0` every cleft is a wide open
       channel, and there is room for fewer arms.
    6. Bias `0.5`, then `0.0`, then `-1.0`. Six arms becomes four long limbs on a
       small body, then a pair of sprawling ones, then no limbs at all and a vessel that
       closes as it rises. Only `-1.0` reverses it: at `-0.5` most points face inward and
       the thing still spreads, because advancing regions are handed the new points and
       retreating ones lose theirs.
    7. Floor off. The vessel becomes an open tube — the day 2 vessel, six arms wide.
    8. Seeds `1` through `10` at the defaults. Same rules, same parameters, ten
       different vessels — and none of them is a variant of a base shape, because there is
       no base shape.

    ---

    ## Where the printability comes from

    This vessel is not printable because it was designed to be. It is printable because
    three of the numbers above belong to the machine rather than to the shape:

    - point spacing is one bead width, so the loop is always sampled finely enough to print;
    - keep-apart distance is more than one bead width, so two walls never want the same
      space;
    - allowed move per layer is a fraction of a bead width, so every bead lands on the one
      below.

    Take those three out and the simulation still runs and still produces coral. It just
    produces coral no printer can make. The growth model has no idea it is a toolpath —
    those three constraints are the whole translation.

    A different growth rule in the same loop is a different family of objects. Replace the
    tip advantage with a pull toward an attractor and you have day 4a again, arrived at
    from the other end.
    """)
    return


if __name__ == "__main__":
    app.run()
