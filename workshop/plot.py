"""FullControl's plotly renderer, adapted to return a figure instead of showing one.

Upstream `fullcontrol.visualize.plotly.plot()` ends in `fig.show()`, which opens its own
window and gives marimo nothing to render. This is that function with the tail changed to
`return fig`. Adapted from fullcontrol 0.1.2 — if a newer version changes the plot
internals, this file needs a look.
"""

import os

import plotly.graph_objects as go

import fullcontrol as fc
import fullcontrol.visualize
from fullcontrol.visualize.controls import PlotControls
from fullcontrol.visualize.plot_data import PlotData
from fullcontrol.visualize.plotly import generate_mesh
from fullcontrol.visualize.tube_mesh import CylindersMesh, FlowTubeMesh


def plot(data: PlotData, controls: PlotControls) -> go.Figure:
    fig = go.Figure()
    controls.raw_data = False
    controls.initialize()

    if controls.tube_type is not None:
        Mesh = {"flow": FlowTubeMesh, "cylinders": CylindersMesh}[controls.tube_type]
    else:
        Mesh = FlowTubeMesh

    for path in data.paths:
        colors_now = [
            f"rgb({color[0] * 255:.2f}, {color[1] * 255:.2f}, {color[2] * 255:.2f})"
            for color in path.colors
        ]
        # travel moves are drawn thin so they read as "not printing"
        linewidth_now = controls.line_width * 2 if path.extruder.on else controls.line_width * 0.5

        if path.extruder.on and controls.style == "tube":
            mesh = generate_mesh(path, linewidth_now, Mesh, controls.tube_sides, 0.4, False, colors_now)
            fig.add_trace(mesh.to_Mesh3d(colors=colors_now))
        elif not controls.hide_travel or path.extruder.on:
            fig.add_trace(
                go.Scatter3d(
                    mode="lines",
                    x=path.xvals,
                    y=path.yvals,
                    z=path.zvals,
                    showlegend=False,
                    line=dict(width=linewidth_now, color=colors_now),
                )
            )

    # one bounding cube for all three axes, so a tall thin object still looks tall and thin
    bb = data.bounding_box
    bounding_box_size = max(bb.maxx - bb.minx, bb.maxy - bb.miny, bb.maxz - min(0, bb.minz)) + 0.002

    annotations_pts = []
    annotations = []
    if not controls.hide_annotations and not controls.neat_for_publishing:
        for annotation in data.annotations:
            x, y, z = (annotation[axis] for axis in "xyz")
            annotations_pts.append([x, y, z])
            annotations.append(dict(showarrow=False, x=x, y=y, z=z, text=annotation["label"], yshift=10))

        xs, ys, zs = zip(*annotations_pts) if annotations_pts else [[]] * 3
        fig.add_trace(
            go.Scatter3d(mode="markers", x=xs, y=ys, z=zs, showlegend=False, marker=dict(size=2, color="red"))
        )

        # grow the box until every annotation is inside it, with a hair of margin
        midx, midy, midz = (getattr(bb, f"mid{axis}") for axis in "xyz")
        offset = 0.001
        for x, y, z in annotations_pts:
            for value, mid in ((x, midx), (y, midy), (z, midz)):
                if value < mid - bounding_box_size / 2 + offset:
                    bounding_box_size = 2 * (mid - value) + 2 * offset
                if value > mid + bounding_box_size / 2 - offset:
                    bounding_box_size = 2 * (value - mid) + 2 * offset

    camera = dict(
        eye=dict(x=-0.5 / controls.zoom, y=-1 / controls.zoom, z=-0.5 + 0.5 / controls.zoom),
        center=dict(x=0, y=0, z=-0.5 + 0.5 * bb.rangez / bounding_box_size),
    )
    axis_style = dict(backgroundcolor="black", nticks=10)
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="black",
        scene_aspectmode="cube",
        scene=dict(
            annotations=annotations,
            xaxis=dict(**axis_style, range=[bb.midx - bounding_box_size / 2, bb.midx + bounding_box_size / 2]),
            yaxis=dict(**axis_style, range=[bb.midy - bounding_box_size / 2, bb.midy + bounding_box_size / 2]),
            zaxis=dict(**axis_style, range=[min(0, bb.minz), bounding_box_size]),
        ),
        scene_camera=camera,
        width=800,
        height=500,
        margin=dict(l=10, r=10, b=10, t=10, pad=4),
    )
    if controls.hide_axes or controls.neat_for_publishing:
        for axis in ("xaxis", "yaxis", "zaxis"):
            fig.update_layout(scene={axis: dict(showgrid=False, zeroline=False, visible=False)})
    if controls.neat_for_publishing:
        fig.update_layout(width=500, height=500)

    return fig


def plot_steps(steps, controls: PlotControls | None = None):
    """Render a list of steps and hand marimo something it can display."""
    import marimo as mo

    if controls is None:
        from workshop.printer import plot_controls

        controls = plot_controls()

    data = fc.visualize.steps2visualization.visualize(steps, controls, True)
    return mo.ui.plotly(plot(data, controls))
