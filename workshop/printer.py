"""The printer profile the lessons share, plus the two `fc` control objects built from it.

Values are for a Prusa MK4S. If you're on something else, change them here once and every
lesson follows. `printer_name='generic'` keeps fullcontrol from emitting machine-specific
start G-code — your slicer's own start script is usually better than anything we'd guess.
"""

from dataclasses import dataclass, replace
from datetime import datetime
from pathlib import Path

import fullcontrol as fc

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "output"


@dataclass(frozen=True)
class Printer:
    # bed, in mm
    bed_width: float = 250
    bed_depth: float = 210
    max_height: float = 220

    # what actually comes out of the nozzle. EW is wider than the nozzle because the
    # plastic squashes sideways as it's pressed down.
    extrusion_width: float = 1.45
    extrusion_height: float = 0.48

    nozzle_temp: int = 215
    bed_temp: int = 60
    print_speed: int = 1000
    fan_percent: int = 0

    printer_name: str = "generic"

    @property
    def initial_z(self) -> float:
        # first layer sits a little lower than a full layer height, so it's squished
        # into the bed and actually sticks
        return self.extrusion_height * 0.6

    def centre(self, z: float | None = None) -> fc.Point:
        """Middle of the bed. Where you almost always want to start."""
        return fc.Point(x=self.bed_width / 2, y=self.bed_depth / 2, z=self.initial_z if z is None else z)

    def but(self, **changes) -> "Printer":
        """A copy with some values changed — for lessons that deliberately push them."""
        return replace(self, **changes)


PRINTER = Printer()


def _extrusion(printer: Printer) -> dict:
    return {
        "extrusion_width": printer.extrusion_width,
        "extrusion_height": printer.extrusion_height,
    }


def plot_controls(printer: Printer = PRINTER, **overrides) -> fc.PlotControls:
    """Tube-style preview at the real extrusion size, so the plot has the volume the print will."""
    settings = dict(
        raw_data=True,
        style="tube",
        tube_sides=6,
        # colour the path by print order, so you can see where it starts and where it goes
        color_type="print_sequence",
        zoom=0.6,
        initialization_data=_extrusion(printer),
    )
    settings.update(overrides)
    return fc.PlotControls(**settings)


def gcode_controls(
    printer: Printer = PRINTER, save_as: str | None = None, primer: str = "travel"
) -> fc.GcodeControls:
    return fc.GcodeControls(
        printer_name=printer.printer_name,
        save_as=save_as,
        include_date=False,  # we add our own timestamp in save_gcode, so we know the filename
        initialization_data={
            "primer": primer,
            "print_speed": printer.print_speed,
            "nozzle_temp": printer.nozzle_temp,
            "bed_temp": printer.bed_temp,
            "fan_percent": printer.fan_percent,
            **_extrusion(printer),
        },
    )


def to_gcode(steps, printer: Printer = PRINTER, primer: str = "travel") -> str:
    """The G-code as a string, without writing anything to disk."""
    return fc.transform(steps, "gcode", gcode_controls(printer, primer=primer), show_tips=False)


def save_gcode(steps, name: str, printer: Printer = PRINTER) -> Path:
    """Write into `<repo>/output/` and return where it landed.

    Timestamped, so running it again doesn't quietly eat your last attempt.
    """
    OUTPUT_DIR.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d__%H-%M-%S")
    target = OUTPUT_DIR / f"{name or 'untitled'}__{stamp}"
    fc.transform(steps, "gcode", gcode_controls(printer, save_as=str(target)), show_tips=False)
    return target.with_suffix(".gcode")
