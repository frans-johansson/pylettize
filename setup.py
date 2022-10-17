from distutils.core import setup

setup(
    name="pylettize",
    version="pre-0.1",
    py_modules=["pylettize"],
    data_files=[
        ("palettes", ["palettes/obama", "palettes/primaries", "palettes/gruvbox"])
    ],
)
