PYTHON ?= python

.PHONY: all build check clean lint smoke test

all: build

build:
	$(PYTHON) -m build

check: build
	$(PYTHON) -m twine check dist/*

lint:
	$(PYTHON) -m ruff check amcp_pylib

smoke: build
	$(PYTHON) -m pip install --no-index --find-links dist --target .smoke amcp-pylib
	$(PYTHON) -c "import sys; sys.path.insert(0, '.smoke'); from amcp_pylib.module.query import VERSION; assert str(VERSION(component='server')).strip() == 'VERSION \"server\"'; assert str(VERSION()).strip() == 'VERSION'"

test:
	$(PYTHON) -m pytest

clean:
	rm -Rf *.egg-info .smoke build dist
