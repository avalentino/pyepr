#!/usr/bin/make -f
# -*- coding: utf-8 -*-

# Copyright (C) 2011-2018, Antonio Valentino <antonio.valentino@tiscali.it>
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
CYTHON = cython3
TEST_DATSET_URL = "http://earth.esa.int/services/sample_products/meris/LRC/L2/MER_LRC_2PTGMV20000620_104318_00000104X000_00000_00000_0001.N1.gz"
TEST_DATSET = tests/MER_LRC_2PTGMV20000620_104318_00000104X000_00000_00000_0001.N1

EPRAPIROOT = ../epr-api

.PHONY: default ext cythonize sdist eprsrc fullsdist doc clean distclean \
        check debug data upload

default: ext

ext: src/epr.pyx
	$(PYTHON) setup.py build_ext --inplace

cythonize: src/epr.c

src/epr.c: src/epr.pyx
	$(CYTHON) src/epr.pyx

sdist: doc cythonize
	$(PYTHON) setup.py sdist

epr-api-src:
	mkdir -p epr-api-src
	cp $(EPRAPIROOT)/src/*.[ch] epr-api-src

LICENSES/epr-api.txt:
	mkdir LICENSES
	cp $(EPRAPIROOT)/LICENSE.txt LICENSES/epr-api.txt

eprsrc: epr-api-src LICENSES/epr-api.txt

fullsdist: doc cythonize eprsrc
	$(PYTHON) setup.py sdist

upload: fullsdist
	twine upload dist/pyepr-*.tar.gz

doc:
	$(MAKE) -C doc html
	$(RM) -r doc/html
	mv doc/_build/html doc/html

clean:
	$(PYTHON) setup.py clean --all
	$(RM) -r build dist pyepr.egg-info
	$(RM) -r $$(find doc -name __pycache__) $$(find tests -name __pycache__)
	$(RM) MANIFEST src/*.c src/*.o *.so
	$(RM) tests/*.py[co] doc/sphinxext/*.py[co] README.html
	$(MAKE) -C doc clean
	find . -name '*~' -delete

distclean: clean
	$(RM) $(TEST_DATSET)
	$(RM) -r doc/html
	$(RM) -r LICENSES epr-api-src
	$(MAKE) -C tests -f checksetup.mak distclean

check: ext $(TEST_DATSET)
	env PYTHONPATH=. $(PYTHON) tests/test_all.py --verbose

debug:
	$(PYTHON) setup.py build_ext --inplace --debug

data: $(TEST_DATSET)

$(TEST_DATSET):
	wget -P tests $(TEST_DATSET_URL)
	gunzip $@
