import pathlib
import re
from typing import Any

from pycodesearch import cli


def test_smoke() -> None:
    pass


def test_cli() -> None:
    paths = [pathlib.Path(__file__)]
    part: Any = "str"
    regexp = re.compile("str")
    options = cli.Options(False, False)

    cli.search_all(paths, part, regexp, options)
