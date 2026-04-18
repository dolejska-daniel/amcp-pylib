PYTHON ?= python

.PHONY: all build check clean test

all: build

build:
	$(PYTHON) -m build

check: build
	$(PYTHON) -m twine check dist/*

test:
	$(PYTHON) -m pytest

clean:
	rm -Rf *.egg-info build dist
