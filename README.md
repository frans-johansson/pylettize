# Any image in any colormap 🎨🐍

![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/frans-johansson/pylettize)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![GitHub](https://img.shields.io/github/license/frans-johansson/pylettize)
[![Coverage Status](https://coveralls.io/repos/github/frans-johansson/pylettize/badge.svg?branch=main)](https://coveralls.io/github/frans-johansson/pylettize?branch=main)

Have you ever been in the middle of creating the ultimate *aesthetic* set up only to find that your favorite wallpaper does not vibe with your new color scheme? Well, fret not, `pylettize` is here for you. This is a simple piece of software allowing you to apply custom color palettes to any image you can think of. Need that classic Bliss™️ re-cast in Gruvbox colors? Look no further!

![The original (boring) Bliss wallpaper](doc/bliss.png)
![The Bliss wallpaper in the Gruvbox aesthetic](doc/bliss_gruvbox.png)


> **Note:** This project is still in development, without a clear release date set. It is useable at the moment, but might require a bit of hacking on your end if you want it to work exactly as you want. If you want to contribute in any way shape or form, check out the contribution guidelines below!

## Usage
*TODO: Include usage when the project is more useable*

## Features
*TODO: Demonstrate some of the features here*

## Contribution guidelines
To get started, make sure you have the following requirements satisfied on your machine:

- `pip v22.2.2`
- `pipenv v2022.10.12`
- Any `python3` version, but 3.8 is recommended

Set up a local virtual environment by running `pipenv install --dev` in the project root directory (where the Pipfile is). You can then activate this environment by running `pipenv shell` in the same directory. To check if this step worked, try running `which python` and verify that you get a path to some sort of "virtualenv" as output.

Optionally, but highly recommended to avoid headaches when submitting PRs, is to set up pre-commit hooks with `pre-commit install` in the project root (where the .pre-commit-config.yaml file is). This should ensure that your PR at least has style compliant code ✨. If you'd like to be told your code is bad before commiting, feel free to set up linting in your editor of choice. We use `flake8` with a bunch of plugins (including `mypy` and `isort`) to run the style checks, so ideally you'd want to use `flake8` locally for linting as well. In Visual Studio Code, adding the following to your settings file should suffice:

```json
{
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
}
```

This will also enable you to format your code with our formatter of choice `black` in the editor.

We use `pytest` as our testing framework. It should be set up such that you can simply run `pytest`.

Feel free to submit PRs with any additions you'd like to see made to the project! We only ask that you stick to the coding guidelines (i.e. what flake8 tells you to do), and that you associate each PR with some Issue. If there isn't an issue yet for what you want to add, create one! Don't worry too much about how to format these, or what labels to use. Simply try to convey what it is you're looking to implement, change or fix.
