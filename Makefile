#!/usr/bin/make -f

PYTHON=python3
TARGET=epr

CYTHON=$(PYTHON) -m cython
CYTHONFLAGS=-3

TEST_DATSET = tests/$(shell grep N1 tests/test_all.py | cut -d '"' -f 2)

EPRAPIROOT = extern/epr-api

.PHONY: default help dist check fullcheck coverage clean cleaner distclean \
        lint docs ext wheels \
        debug cythonize ext-coverage coverage-report

default: help

help:
	@echo "Usage: make <TARGET>"
	@echo "Available targets:"
	@echo "  help      - print this help message"
	@echo "  dist      - generate the distribution packages (source and wheel)"
	@echo "  check     - run a full test (using pytest)"
	@echo "  fullcheck - run a full test (using tox)"
	@echo "  coverage  - run tests and generate the coverage report"
	@echo "  clean     - clean build artifacts"
	@echo "  cleaner   - clean cache files and working directories of al tools"
	@echo "  distclean - clean all the generated files"
	@echo "  lint      - perform check with code linter (flake8, black)"
	@echo "  docs      - generate the sphinx documentation"
	@echo "  ext       - build Python extensions in-place"
	@echo "  wheels    - build Python wheels"
	@echo "  cythonize - generate cython C extensions"
	@echo "  debug     - generate debug build"
	@echo "  ext-coverage    - build the extension in-place with tracing enabled"
	@echo "  coverage-report - generate the coverage report"

dist:
	$(PYTHON) -m build
	$(PYTHON) -m twine check dist/*

check: ext
	env PYTHONPATH=src $(PYTHON) tests/test_all.py --verbose

fullcheck:
	$(PYTHON) -m tox run

coverage: clean ext-coverage
	env PYTHONPATH=src $(PYTHON) -m pytest --doctest-modules --cov=$(TARGET) --cov-report=html --cov-report=term src/$(TARGET) tests

clean:
	$(PYTHON) setup.py clean --all
	$(RM) -r src/*.*-info build
	find . -name __pycache__ -type d -exec $(RM) -r {} +
	# $(RM) -r __pycache__ */__pycache__ */*/__pycache__ */*/*/__pycache__
	$(RM) src/$(TARGET)/*.c src/$(TARGET)/*.cpp src/$(TARGET)/*.so src/$(TARGET)/*.o
	if [ -f docs/Makefile ] ; then $(MAKE) -C docs clean; fi
	$(RM) -r docs/_build
	$(RM) MANIFEST
	find . -name '*~' -delete
	$(RM) src/epr/epr.html
	$(RM) epr.p*        # workaround for Cython.Coverage bug #1985

cleaner: clean
	$(RM) -r .coverage htmlcov
	$(RM) -r .pytest_cache
	$(RM) -r .tox
	$(RM) -r .mypy_cache
	$(RM) -r .ruff_cache
	$(RM) -r .ipynb_checkpoints
	$(RM) -r .hypothesis

distclean: cleaner
	$(RM) -r dist
	$(RM) -r wheelhouse
	$(RM) $(TEST_DATSET)

lint:
	$(PYTHON) -m flake8 --count --statistics src/$(TARGET) tests
	$(PYTHON) -m pydocstyle --count src/$(TARGET)
	# $(PYTHON) -m isort --check src/$(TARGET) tests
	$(PYTHON) -m black --check src/$(TARGET) tests
	# $(PYTHON) -m mypy --check-untyped-defs --ignore-missing-imports src/$(TARGET)
	ruff check src/$(TARGET) tests

docs:
	mkdir -p docs/_static
	$(MAKE) -C docs html
	$(MAKE) -C docs linkcheck
	$(MAKE) -C docs spelling

ext: src/epr/epr.pyx
	$(PYTHON) setup.py build_ext --inplace --epr-api-src=$(EPRAPIROOT)/src

cythonize: src/epr/_epr.c

src/epr/_epr.c: src/epr/epr.pyx
	$(CYTHON) $(CYTHONFLAGS) -o src/epr/_epr.c src/epr/epr.pyx

ext-coverage: src/epr/epr.pyx
	env PYEPR_COVERAGE=TRUE $(PYTHON) setup.py build_ext --inplace

debug:
	$(PYTHON)d setup.py build_ext --inplace --debug

wheels:
	# Requires docker
	python3 -m cibuildwheel --platform auto
