#!/usr/bin/make -f

PYTHON = python3
CYTHON = $(PYTHON) -m cython
CYTHONFLAGS=-3

TEST_DATSET = tests/$(shell grep N1 tests/test_all.py | cut -d '"' -f 2)

EPRAPIROOT = extern/epr-api

.PHONY: default ext cythonize sdist eprsrc fullsdist doc clean distclean \
        check debug upload coverage ext-coverage coverage-report

default: ext

ext: epr/epr.pyx
	$(PYTHON) setup.py build_ext --inplace --epr-api-src=$(EPRAPIROOT)/src

cythonize: epr/_epr.c

epr/_epr.c: epr/epr.pyx
	$(CYTHON) $(CYTHONFLAGS) -o epr/_epr.c epr/epr.pyx

sdist: doc
	$(PYTHON) -m build --sdist

LICENSES/epr-api.txt:
	mkdir LICENSES
	cp $(EPRAPIROOT)/LICENSE.txt LICENSES/epr-api.txt

eprsrc: LICENSES/epr-api.txt

fullsdist: doc eprsrc
	$(PYTHON) -m build --sdist

upload: fullsdist
	twine check dist/pyepr-*.tar.gz
	twine upload dist/pyepr-*.tar.gz

doc:
	$(MAKE) -C doc html

clean:
	$(PYTHON) setup.py clean --all
	$(RM) -r build dist pyepr.*-info wheelhouse
	$(RM) -r $$(find . -name __pycache__)
	$(RM) MANIFEST epr/*.c epr/*.o epr/*.so
	$(RM) tests/*.py[co]
	$(MAKE) -C doc clean
	$(RM) -r doc/_build
	find . -name '*~' -delete
	$(RM) *.c *.o *.html .coverage coverage.xml
	$(RM) epr/epr.html
	$(RM) -r htmlcov .pytest_cache .hypothesis
	$(RM) epr.p*        # workaround for Cython.Coverage bug #1985

distclean: clean
	$(RM) $(TEST_DATSET)
	$(RM) -r LICENSES
	$(RM) -r .eggs
	$(RM) -r .ipynb_checkpoints .ruff_cache

check: ext
	env PYTHONPATH=. $(PYTHON) tests/test_all.py --verbose

ext-coverage: epr/epr.pyx
	env PYEPR_COVERAGE=TRUE $(PYTHON) setup.py build_ext --inplace

coverage: clean ext-coverage
	env PYTHONPATH=. $(PYTHON) -m pytest --cov --cov-report=term --cov-report=html

debug:
	$(PYTHON)d setup.py build_ext --inplace --debug

wheels:
	# make distclean
	# python3 -m pip install -U cibuildwheel
	python3 -m cibuildwheel --output-dir wheelhouse --platform linux
