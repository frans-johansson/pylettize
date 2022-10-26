"""Pylettize, main test module."""

import operator

import numpy as np

from pylettize import dist_to_color, hex_to_rgb


def test_converting_hex_to_rgb():
    """Ensure a given hex rgb string is converted to an RGB f32 vector."""
    to_test = {
        "#ff0000": np.array([1, 0, 0], dtype=np.float32),
        "#00ff00": np.array([0, 1, 0], dtype=np.float32),
        "#0000ff": np.array([0, 0, 1], dtype=np.float32),
        "#ffff00": np.array([1, 1, 0], dtype=np.float32),
        "#00ffff": np.array([0, 1, 1], dtype=np.float32),
        "#ff00ff": np.array([1, 0, 1], dtype=np.float32),
    }

    for hex, expected_value in to_test.items():
        np.testing.assert_almost_equal(hex_to_rgb(hex), expected_value)


def test_distance_maps():
    """Ensure computed distance maps are reasonable."""
    color_a = np.array([1, 0, 0], dtype=np.float32)
    color_b = np.array([0, 1, 1], dtype=np.float32)
    image = np.full(shape=(5, 5, 3), fill_value=color_a, dtype=np.float32)

    dist_map_to_a = dist_to_color(image, color_a)
    dist_map_to_b = dist_to_color(image, color_b)

    np.testing.assert_allclose(dist_map_to_a, 0)
    np.testing.assert_array_compare(operator.__gt__, dist_map_to_b, 0)
