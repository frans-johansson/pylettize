"""
Default pylettize palettes.

The following default palettes are available:
- gruvbox
- obama
- primaries

These are nothing more than text files with RGB hex values, making
it quite easy to include more palettes to the default library in the future.
"""

from importlib import resources
from pathlib import Path
from typing import List

import numpy as np
import numpy.typing as npt

from pylettize.pylettize import hex_to_rgb

OPTIONS = ["gruvbox", "obama", "primaries"]


def get_default_palette(palette_name: str) -> List[npt.NDArray[np.float32]]:
    """Retrieve one of the default palettes."""
    assert (
        palette_name in OPTIONS
    ), f"'{palette_name}' not in the default palettes {OPTIONS}"
    palette_file = resources.open_text("pylettize.palettes", palette_name)
    with palette_file as file:
        return list(map(hex_to_rgb, file))


def get_palette_from_file(palette_file: Path) -> List[npt.NDArray[np.float32]]:
    """Parse and return the palette from a supplied text file."""
    with open(palette_file, "rt") as file:
        return list(map(hex_to_rgb, file))
