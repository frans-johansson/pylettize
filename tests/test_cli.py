"""Pylettize cli test module."""

import pytest

from pylettize import cli


def test_help_flag_works(monkeypatch, capfd):
    """Make sure the help message is printed if the -h flag is provided."""
    monkeypatch.setattr("sys.argv", ["pylettize", "-h"])

    with pytest.raises(SystemExit) as e:
        cli.run()

    assert e.type == SystemExit

    out, _ = capfd.readouterr()
    assert "Usage:" in out  # Just to make sure the help screen was printed
