"""
Pylettize, main module.

Maps each pixel in a given image to its nearest neighboring color,
from a given palette in RGB space in terms of the L2 norm.
"""
from importlib import resources

import numpy as np
import numpy.typing as npt
import skimage.data as test_images
import skimage.io as imio

OUTPUT_FILE = "output.png"
PALETTE_FILE = resources.open_text("pylettize.palettes", "obama")
INPUT_IMAGE = test_images.astronaut()
TEMPERATURE = 0.1
EPSILON = 1e-15


def hex_to_rgb(hex_str: str) -> npt.NDArray[np.float32]:
    """Convert an RGB hex string to a floating point RGB value on the range [0, 1]."""
    hex_rgb = [hex_str[1:3], hex_str[3:5], hex_str[5:7]]
    return np.array([int(hex_val, base=16) / 255 for hex_val in hex_rgb])


def dist_to_color(
    im: npt.NDArray[np.float32], color: npt.NDArray[np.float32]
) -> npt.NDArray[np.float32]:
    """Compute the distance map for a full color image to a given color value."""
    dist: npt.NDArray[np.float32] = np.linalg.norm(im - color, axis=2)
    return dist / (EPSILON + np.max(dist))


def hard_blending(
    weight_map: npt.NDArray[np.float32], palette: npt.NDArray[np.float32]
) -> npt.NDArray[np.float32]:
    """Blend with the palette using hard lookup."""
    lookup: npt.NDArray[np.uint] = np.argmax(weight_map, axis=0)
    return np.take(np.array(palette), lookup)


def linear_blending(
    weight_map: npt.NDArray[np.float32], palette: npt.NDArray[np.float32]
) -> npt.NDArray[np.float32]:
    """Blend with the palette using soft linear blending."""
    return np.transpose(weight_map, axes=[1, 2, 0]) @ palette


def main() -> None:
    """Execute the main functionality for pylettize."""
    # Read and convert the palette
    with PALETTE_FILE as file:
        palette = np.array(list(map(hex_to_rgb, file)))

    # Read and convert the image to f32
    im = (INPUT_IMAGE / 255).astype(np.float32)

    # Compute the distance map and corresponding palette lookup
    dist_map = np.stack([dist_to_color(im, color) for color in palette])

    # Apply temperature scaled softmax
    weight_map = np.exp((1.0 - dist_map) / TEMPERATURE)
    weight_map /= np.sum(weight_map, axis=0)

    # Do blending
    mapped_im = linear_blending(weight_map, palette)
    # mapped_im = hard_blending(weight_map, palette)

    # Convert the result back to u8 and save the image
    mapped_im *= 255
    mapped_im = mapped_im.astype(np.uint8)
    imio.imsave(OUTPUT_FILE, mapped_im)


if __name__ == "__main__":
    main()