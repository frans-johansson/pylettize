"""Pylettize, main test module."""

import operator

import numpy as np

from pylettize import pylettize


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
        np.testing.assert_almost_equal(pylettize.hex_to_rgb(hex), expected_value)


def test_distance_maps():
    """Ensure computed distance maps are reasonable."""
    color_a = np.array([1, 0, 0], dtype=np.float32)
    color_b = np.array([0, 1, 1], dtype=np.float32)
    image = np.full(shape=(5, 5, 3), fill_value=color_a, dtype=np.float32)

    dist_map_to_a = pylettize.dist_to_color(image, color_a)
    dist_map_to_b = pylettize.dist_to_color(image, color_b)

    np.testing.assert_allclose(dist_map_to_a, 0)
    np.testing.assert_array_compare(operator.__gt__, dist_map_to_b, 0)


def test_minimal_and_maximal_similarity():
    """Test color similarity to itself and its complement."""
    to_test = [
        # (Color, Complement)
        ([0, 0, 0], [1, 1, 1]),
        ([1, 0, 0], [0, 1, 1]),
        ([0, 1, 0], [1, 0, 1]),
        ([0, 0, 1], [1, 1, 0]),
    ]

    for color, complement in to_test:
        image = np.array(color, dtype=np.float32)[None, None, ...]  # (1, 1, 3)
        self_palette = [np.array(color, dtype=np.float32)]
        complement_palette = [np.array(complement, dtype=np.float32)]

        similarity_to_self = pylettize.similarity_map(image, self_palette)
        similarity_to_complement = pylettize.similarity_map(image, complement_palette)

        assert similarity_to_self == 1.0  # A color is completely similar to itself
        assert similarity_to_complement == 0.0  # ... and dissimilar to its complement


def test_temperature_affects_weights():
    """Make sure a higher temperature spreads out weights across palette."""
    image = np.array(
        [
            [[1, 1, 0], [1, 0, 1]],
            [[0, 0, 0], [0, 1, 0]],
        ],
        dtype=np.float32,
    )
    palette = [
        np.array([1, 0, 0], dtype=np.float32),
        np.array([0, 0.5, 1], dtype=np.float32),
    ]

    high_temperature = pylettize.weight_map(image, palette, 10)
    low_temperature = pylettize.weight_map(image, palette, 1)

    high_palette_diff = np.abs(high_temperature[0, ...] - high_temperature[1, ...])
    low_palette_diff = np.abs(low_temperature[0, ...] - low_temperature[1, ...])

    assert np.all(low_palette_diff > high_palette_diff)
