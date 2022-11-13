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

from pathlib import Path
from typing import Any, Dict

import numpy as np
import skimage.io as imio
from docopt import docopt

from pylettize.palettes import get_default_palette, get_palette_from_file
from pylettize.pylettize import (
    hard_blending,
    linear_blending,
    similarity_map,
    weight_map,
)


def run() -> None:
    """Run the pylettize CLI with a given list of argument values."""
    args: Dict[str, Any] = docopt(str(__doc__))

    # Get the input image
    input_img = imio.imread(args["<img>"]) / 255.0

    # Get palette
    if args["--palette-file"]:
        palette_file = Path(args["<palette>"])
        assert palette_file.exists(), f"Could not find palette file '{palette_file}'"
        palette = get_palette_from_file(palette_file)
    else:
        palette = get_default_palette(args["<palette>"])

    # Do the blending
    if args["hard"]:
        sim_map = similarity_map(input_img, palette)
        mapped_im = hard_blending(sim_map, palette)
    elif args["soft"]:
        # Apply temperature scaled softmax
        temperature = float(args["--temperature"])
        weights = weight_map(input_img, palette, temperature)
        mapped_im = linear_blending(weights, palette)
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


if __name__ == "__main__":
    run()
