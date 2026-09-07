"""Utility functions and theme definitions for
color conversion and UI styling."""

import typing


def rgb(r: int, g: int, b: int, a: int = 255) -> int:
    """Convert RGBA color channels (0-255) into
    a single 32-bit ARGB integer."""
    return (a << 24) | (r << 16) | (g << 8) | b


THEMES: list[dict[str, typing.Any]] = [
    {
        "name": "TELEGRAM",
        "wall": rgb(24, 34, 45),
        "path": rgb(187, 187, 187),
        "start_cell": rgb(133, 178, 255),
        "end_cell": rgb(255, 111, 97),
        "sidebar": rgb(14, 22, 33),
        "button": rgb(82, 136, 193),
    },
    # {
    #     "name": "CYBERPUNK",
    #     "wall": rgb(25, 10, 35),
    #     "path": rgb(0, 255, 150),
    #     "start_cell": rgb(255, 0, 127),
    #     "end_cell": rgb(76, 0, 153),
    #     "sidebar": rgb(15, 5, 20),
    #     "button": rgb(255, 0, 128),
    # },
    {
        "name": "DISCORD",
        "wall": rgb(43, 45, 49),
        "path": rgb(244, 127, 255),
        "start_cell": rgb(114, 137, 218),
        "end_cell": rgb(153, 170, 181),
        "sidebar": rgb(30, 31, 34),
        "button": rgb(88, 101, 242),
    }
]
