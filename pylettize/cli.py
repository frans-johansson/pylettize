"""
Pylettize. Image re-palettizer written in Python.

Palettes:
    Any text file with line-separated hex-colors can be supplied as the palette.
    In addition, the following named default palettes are available
    * gruvbox    The classic Gruvbox color scheme
    * obama      Colors from the "Hope" posters
    * primaries  RGB and CMY

Blending strategies:
    Pylettize provides two main blending strategies
    * hard  Using a binary mapping from input pixel color to palette color
    * soft  Using a linear combination of palette colors in each pixel
            The degree of "softness" is determined with the -T temperature option

Usage:
    pylettize -h
    pylettize hard <img> [-p] <palette> [-o <output>]
    pylettize soft <img> [-p] <palette> [-o <output> -T <temperature>]

-h, --help                                     Show this screen
-p, --palette-file                             Use a provided text file as palette
-o <output>, --output=<output>                 Output file [default: pylettized.png]
-T <temperature>, --temperature=<temperature>  Blending temperature [default: 0.5]
"""

import sys
from importlib import resources
from typing import Any, Dict, List

import numpy as np
import skimage.io as imio
from docopt import docopt

from pylettize.pylettize import (
    dist_to_color,
    hard_blending,
    hex_to_rgb,
    linear_blending,
)


def run(argv: List[str]):
    """Run the pylettize CLI with a given list of argument values."""
    args: Dict[str, Any] = docopt(str(__doc__), argv)

    # Get the input image
    input_img = imio.imread(args["<img>"]) / 255.0

    # Get palette
    if args["--palette-file"]:
        raise NotImplementedError("Custom palette files not supported yet")
    else:
        palette_file = resources.open_text("pylettize.palettes", args["<palette>"])

    with palette_file as file:
        palette = np.array(list(map(hex_to_rgb, file)))

    # Compute the distance map and corresponding palette lookup
    dist_map = np.stack([dist_to_color(input_img, color) for color in palette])

    # Do the blending
    if args["hard"]:
        mapped_im = hard_blending(dist_map, palette)
    elif args["soft"]:
        # Apply temperature scaled softmax
        temp: float = float(args["--temperature"])
        weight_map = np.exp((1.0 - dist_map) / temp)
        weight_map /= np.sum(weight_map, axis=0)
        mapped_im = linear_blending(weight_map, palette)
    else:
        raise AssertionError(
            """
            Could not resolve the blending strategy.
            You have stumbled upon a bug! Feel free to report it at
            https://github.com/frans-johansson/pylettize/issues.
            """
        )

    # Save output image
    output_img = (mapped_im * 255).astype(np.uint8)
    imio.imsave(args["--output"], output_img)

    # Debugging
    # for i, im in enumerate(dist_map):
    #     imio.imsave(f"dist_map_{i}.png", im)


def _console_entry_point():
    """Invoke the CLI externally."""
    run(sys.argv[1:])


if __name__ == "__main__":
    _console_entry_point()
