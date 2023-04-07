"""Pylettize palettes test module."""

import contextlib
import pathlib

import pytest

from pylettize import palettes


def test_default_palettes():
    for palette_name in palettes.OPTIONS:
        palette = palettes.get_default_palette(palette_name)
        assert len(palette) > 0


@pytest.fixture
def patched_palette_file(monkeypatch):

    @contextlib.contextmanager
    def mocked_file_open(filename, mode):
        yield ["#ff0000", "#00ff00", "#0000ff"]

    monkeypatch.setattr("pathlib.Path.open", mocked_file_open)


def test_palette_from_file(patched_palette_file):
    path = pathlib.Path("SomeFile.txt")
    palette = palettes.get_palette_from_file(path)
    assert len(palette) == 3
