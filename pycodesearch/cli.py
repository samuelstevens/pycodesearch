import argparse
import ast
import os
import pathlib
import re
from typing import Any, Callable, Iterator, List, Optional, Union

from .types import Literal

Part = Literal["all", "str"]


def simple_log(*args: Any, **kwargs: Any) -> None:
    print(*args, **kwargs)


class File:
    def __init__(self, content: str, path: pathlib.Path):
        self.content = content
        self.path = path

    def parse(self) -> Optional[ast.AST]:
        try:
            return ast.parse(self.content, self.path)  # type: ignore
        except SyntaxError as err:
            simple_log(f"Error parsing {self.path}:", err)
            return None

    def __getitem__(self, i: int) -> str:
        lines = [""] + self.content.split("\n")
        return lines[i]


def _from_file(path: pathlib.Path) -> Optional[File]:
    assert not path.is_dir()
    if path.suffix != ".py":
        return None

    with open(path) as fd:
        return File(fd.read(), path)


def _from_dir(path: pathlib.Path) -> Iterator[File]:
    assert path.is_dir()
    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            filepath = pathlib.Path(dirpath) / filename
            file = _from_file(filepath)
            if file is not None:
                yield file


class Options:
    def __init__(self, only_filenames: bool, invert_match: bool):
        self.only_filenames = only_filenames
        self.invert_match = invert_match


def new_options(args: argparse.Namespace) -> Options:
    return Options(args.only_filenames, args.invert_match)


def load_files(paths: List[pathlib.Path]) -> Iterator[File]:
    for path in paths:
        if path.is_dir():
            yield from _from_dir(path)
        else:
            file = _from_file(path)
            if file is not None:
                yield file


class Searcher(ast.NodeVisitor):
    def __init__(self, file: File, regexp: "re.Pattern[str]", options: Options):
        self.file = file
        self.regexp = regexp
        self.options = options

    def search(self, value: str) -> Union[bool, "re.Match[str]"]:
        match = self.regexp.search(value)
        if match is None:
            if self.options.invert_match:
                return True
            else:
                return False
        else:
            if self.options.invert_match:
                return False
            else:
                return match

    def report(self, node: ast.AST, printfn: Callable[..., None]) -> None:
        printfn(self.file.path)

        if self.options.only_filenames:
            return

        end_lineno = node.lineno
        if hasattr(node, "end_lineno") and node.end_lineno is not None:
            end_lineno = node.end_lineno

        for lineno in range(node.lineno, end_lineno + 1):
            printfn(f"{lineno}:{self.file[lineno]}")


class String(Searcher):
    def generic_visit(self, node: ast.AST) -> None:
        super().generic_visit(node)

        value = None

        if hasattr(node, "value") and isinstance(node.value, str):  # type: ignore
            value = node.value  # type: ignore

        if hasattr(node, "s") and isinstance(node.s, str):  # type: ignore
            value = node.s  # type: ignore

        if value is None:
            return

        match = self.search(value)
        if not match:
            return

        self.report(node, print)

        self.report(node, print)


def search(file: File, part: Part, regexp: "re.Pattern[str]", options: Options) -> None:
    tree = file.parse()
    if tree is None:
        return

    if part == "str":
        visitor = String(file, regexp, options)
    else:
        assert part is None

    visitor.visit(tree)


def search_all(
    paths: List[pathlib.Path], part: Part, regexp: "re.Pattern[str]", options: Options
) -> None:
    for file in load_files(paths):
        search(file, part, regexp, options)


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("regexp", help="Regular expression pattern to search for.")
    parser.add_argument(
        "part",
        choices=["str", "all"],
        help="What part of the codebase to look in. 'str' looks in string literals. 'all' looks at everything.",
    )
    parser.add_argument(
        "paths", nargs="+", help="File or directory containing paths to search"
    )
    parser.add_argument(
        "-l",
        "--only-filenames",
        action="store_true",
        help="Only prints the filenames with a match.",
    )
    parser.add_argument(
        "-v",
        "--invert-match",
        action="store_true",
        help="Invert matching. Show nodes that do not match the given patterns.",
    )

    return parser


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()

    paths = [pathlib.Path(p) for p in args.paths]
    regexp = re.compile(args.regexp)
    options = new_options(args)

    search_all(paths, args.part, regexp, options)


if __name__ == "__main__":
    main()
