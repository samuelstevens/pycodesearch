# PySearch

Semantic code search over Python codebases.

## Installation

Install from [PyPI](https://pypi.org/project/pycodesearch/).

```sh
pipx install pycodesearch
```

## Usage

```sh
pycodesearch -h

# finds all instances of <regexp> in string literals in directory
pycodesearch <regexp> str .
```

## Development

```sh
pip install flake8-bugbear flake8 mypy isort black flit tox pytest
```

## Goals

- [ ] Add options besides just string literals (class/function/method/variable names)
- [ ] Figure out tox so that it *actually* tests with different versions of python.
