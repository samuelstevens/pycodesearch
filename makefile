all: fmt lint types

fmt:
	isort search
	black search

lint:
	flake8 search

types:
	mypy --strict search
