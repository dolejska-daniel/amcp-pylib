PYTHON ?= python

.PHONY: all build check clean lint smoke test

all: build

build:
	$(PYTHON) -m build

check: build
	$(PYTHON) -m twine check dist/*

lint:
	$(PYTHON) -m ruff check amcp_pylib tests

smoke: build
	$(PYTHON) -m pip install --no-index --find-links dist --target .smoke amcp-pylib
	cd .. && PYTHONPATH="$(CURDIR)/.smoke" $(PYTHON) -c "import importlib.util; from amcp_pylib.module.query import VERSION; assert importlib.util.find_spec('amcp_pylib.tests') is None; assert str(VERSION(component='server')).strip() == 'VERSION \"server\"'; assert str(VERSION()).strip() == 'VERSION'"

test:
	$(PYTHON) -m pytest

clean:
	rm -Rf *.egg-info .smoke build dist
