#!/usr/bin/make -f
# -*- coding: utf-8 -*-

# Copyright (C) 2011-2013, Antonio Valentino <antonio.valentino@tiscali.it>
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

PYTHON = python
CYTHON = cython
TEST_DATSET_URL = "http://earth.esa.int/services/sample_products/meris/LRC/L2/MER_LRC_2PTGMV20000620_104318_00000104X000_00000_00000_0001.N1.gz"
TEST_DATSET = test/MER_LRC_2PTGMV20000620_104318_00000104X000_00000_00000_0001.N1

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

upload: doc cythonize eprsrc
	$(PYTHON) setup.py sdist upload -s -i 24B76CFE

doc:
	$(MAKE) -C doc html

clean:
	$(PYTHON) setup.py clean --all
	$(RM) tests/*.py[co] doc/sphinxext/*.py[co] README.html
	$(MAKE) -C doc clean
	find . -name '*~' -delete

distclean: clean
	$(RM) -r build dist pyepr.egg-info
	$(RM) MANIFEST src/*.c src/*.o *.so
	$(RM) $(TEST_DATSET)
	$(RM) -r doc/html
	$(RM) -r LICENSES epr-api-src

check: ext $(TEST_DATSET)
	$(PYTHON) test/test_all.py --verbose

debug:
	$(PYTHON) setup.py build_ext --inplace --debug

data: $(TEST_DATSET)

$(TEST_DATSET):
	wget -P test $(TEST_DATSET_URL)
	gunzip $@
