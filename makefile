all: fmt lint types test tox

fmt: FORCE
	isort pycodesearch test
	black pycodesearch test

lint: FORCE
	flake8 pycodesearch test

types: FORCE
	mypy --strict pycodesearch test

test: FORCE
	python -m pytest test

tox: FORCE
	tox

FORCE:
