"""
Pylettize/Core.

This module contains the core functionality for pylettize to function.
"""
import numpy as np
import numpy.typing as npt

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
