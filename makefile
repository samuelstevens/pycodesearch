all: fmt lint types test tox

fmt: FORCE
	isort pycodesearch
	black pycodesearch

lint: FORCE
	flake8 pycodesearch

types: FORCE
	mypy --strict pycodesearch

test: FORCE
	pytest

tox: FORCE
	tox

FORCE:
