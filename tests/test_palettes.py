"""Pylettize palettes test module."""
from unittest import mock

import pytest

from pylettize import palettes


def test_default_palettes():
    """We should get non-empty, non-crash results for all default palettes."""
    for palette_name in palettes.OPTIONS:
        palette = palettes.get_default_palette(palette_name)
        assert len(palette) > 0


@pytest.fixture
def mocked_palette_file():
    """Mock out reading the palette file."""
    mocked_enter = mock.MagicMock()
    mocked_enter.__enter__.return_value = ["#ff0000", "#00ff00", "#0000ff"]
    mocked_open = mock.Mock(return_value=mocked_enter)
    mocked_path = mock.Mock()
    mocked_path.open = mocked_open
    return mocked_path


def test_palette_from_file(mocked_palette_file):
    """Make sure reading from file works."""
    palette = palettes.get_palette_from_file(mocked_palette_file)
    mocked_palette_file.open.assert_called_once()
    assert len(palette) == 3
