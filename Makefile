#!/usr/bin/make -f
# -*- coding: utf-8 -*-

# Copyright (C) 2011-2021, Antonio Valentino <antonio.valentino@tiscali.it>
#
# This file is part of PyEPR.
#
# PyEPR is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyEPR is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyEPR.  If not, see <http://www.gnu.org/licenses/>.

PYTHON = python3
CYTHON = $(PYTHON) -m cython
CYTHONFLAGS=$(shell $(CYTHON) --help | grep -o -- '--3str')

TEST_DATSET = tests/$(shell grep N1 tests/test_all.py | cut -d "'" -f 2)

EPRAPIROOT = extern/epr-api

.PHONY: default ext cythonize sdist eprsrc fullsdist doc clean distclean \
        check debug data upload manylinux coverage ext-coverage coverage-report

default: ext

ext: src/epr.pyx
	$(PYTHON) setup.py build_ext --inplace

cythonize: src/epr.c

src/epr.c: src/epr.pyx
	$(CYTHON) $(CYTHONFLAGS) src/epr.pyx

sdist: doc cythonize
	$(PYTHON) setup.py sdist

LICENSES/epr-api.txt:
	mkdir LICENSES
	cp $(EPRAPIROOT)/LICENSE.txt LICENSES/epr-api.txt

eprsrc: LICENSES/epr-api.txt

fullsdist: doc cythonize eprsrc
	$(PYTHON) setup.py sdist

upload: fullsdist
	twine check dist/pyepr-*.tar.gz
	twine upload dist/pyepr-*.tar.gz

doc:
	$(MAKE) -C doc html
	$(RM) -r doc/html
	mv doc/_build/html doc/html

clean:
	$(PYTHON) setup.py clean --all
	$(RM) -r build dist pyepr.egg-info wheelhouse
	$(RM) -r $$(find doc -name __pycache__) $$(find tests -name __pycache__)
	$(RM) MANIFEST src/*.c src/*.o *.so
	$(RM) tests/*.py[co] doc/sphinxext/*.py[co] README.html
	$(MAKE) -C doc clean
	$(RM) -r doc/_build
	find . -name '*~' -delete
	$(RM) *.c *.o *.html .coverage coverage.xml
	$(RM) src/epr.html
	$(RM) -r htmlcov .pytest_cache .hypothesis
	$(RM) epr.p*        # workaround for Cython.Coverage bug #1985

distclean: clean
	$(RM) $(TEST_DATSET)
	$(RM) -r doc/html
	$(RM) -r LICENSES
	$(MAKE) -C tests -f checksetup.mak distclean
	$(RM) -r .eggs

check: ext
	env PYTHONPATH=. $(PYTHON) tests/test_all.py --verbose

ext-coverage: src/epr.pyx
	env PYEPR_COVERAGE=TRUE $(PYTHON) setup.py build_ext --inplace

coverage: clean ext-coverage
	ln -s src/epr.p* .  # workaround for Cython.Coverage bug #1985
	env PYEPR_COVERAGE=TRUE PYTHONPATH=. \
		$(PYTHON) -m coverage run --branch --source=src setup.py test
	env PYTHONPATH=. $(PYTHON) -m coverage report

coverage-report: coverage
	env PYTHONPATH=. $(PYTHON) -m cython -E CYTHON_TRACE_NOGIL=1 \
		-X linetrace=True -X language_level=3str \
		--annotate-coverage coverage.xml src/epr.pyx
	env PYTHONPATH=. $(PYTHON) -m coverage xml -i
	env PYTHONPATH=. $(PYTHON) -m coverage html -i
	cp src/epr.html htmlcov

debug:
	$(PYTHON)d setup.py build_ext --inplace --debug

wheels:
	# make distclean
	# python3 -m pip install -U cibuildwheel
	python3 -m cibuildwheel --output-dir wheelhouse --platform linux
