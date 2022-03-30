all: fmt lint types

fmt:
	isort pysearch
	black pysearch

lint:
	flake8 pysearch

types:
	mypy --strict pysearch
