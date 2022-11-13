"""
Pylettize/Core.

This module contains the core functionality for pylettize to function.
"""
from typing import List

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
    """Compute a normalized distance map for an image to a given color value."""
    dist: npt.NDArray[np.float32] = np.linalg.norm(im - color, axis=2)
    return dist / (EPSILON + np.max(dist))


def similarity_map(
    im: npt.NDArray[np.float32], palette: List[npt.NDArray[np.float32]]
) -> npt.NDArray[np.float32]:
    """Compute a map of similarity values between an image and palette."""
    distance_map = np.stack([dist_to_color(im, color) for color in palette])
    return 1.0 - distance_map


def weight_map(
    im: npt.NDArray[np.float32],
    palette: List[npt.NDArray[np.float32]],
    temperature: float,
) -> npt.NDArray[np.float32]:
    """Compute temperature scaled softmax weights betwen an image and palette."""
    sim_map = similarity_map(im, palette)
    weight_map = np.exp(sim_map / temperature)
    weight_map /= np.sum(weight_map, axis=0)
    return weight_map


def hard_blending(
    dist_map: npt.NDArray[np.float32], palette: List[npt.NDArray[np.float32]]
) -> npt.NDArray[np.float32]:
    """Blend with the palette using hard lookup."""
    palette_array = np.array(palette)
    lookup: npt.NDArray[np.uint] = np.argmax(dist_map, axis=0)
    return palette_array[lookup]


def linear_blending(
    weights: npt.NDArray[np.float32], palette: List[npt.NDArray[np.float32]]
) -> npt.NDArray[np.float32]:
    """Blend with the palette using soft linear blending."""
    palette_array = np.array(palette)
    return np.transpose(weights, axes=[1, 2, 0]) @ palette_array
