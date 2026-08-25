"""Shared bits every lesson needs, so the notebooks can stay about the geometry."""

from workshop.plot import plot_steps
from workshop.printer import PRINTER, Printer, gcode_controls, plot_controls, save_gcode, to_gcode

__all__ = [
    "PRINTER",
    "Printer",
    "gcode_controls",
    "plot_controls",
    "plot_steps",
    "save_gcode",
    "to_gcode",
]
