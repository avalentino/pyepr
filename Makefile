#!/usr/bin/make -f
# -*- coding: utf-8 -*-

# Copyright (C) 2011, Antonio Valentino <antonio.valentino@tiscali.it>
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

TEST_DATSET_URL = "http://earth.esa.int/services/sample_products/asar/IMP/ASA_IMP_1PNUPA20060202_062233_000000152044_00435_20529_3110.N1.gz"
TEST_DATSET = test/ASA_IMP_1PNUPA20060202_062233_000000152044_00435_20529_3110.N1

.PHONY: default sdist doc clean distclean check debug data

default: epr.so

sdist:
	python setup.py build_ext --inplace
	python setup.py clean
	$(RM) epr.so
	$(MAKE) -C doc html
	$(RM) -r doc/_build
	python setup.py sdist

doc:
	$(MAKE) -C doc html

clean:
	python setup.py clean
	$(RM) src/*.py[co] tests/*.py[co] README.html
	$(MAKE) -C doc clean
	$(RM) -r doc/_build

distclean: clean
	$(RM) -r build dist pyepr.egg-info
	$(RM) MANIFEST src/*.c src/*.o *.so
	#$(RM) tests/*.N1
	$(RM) -r doc/html

check: epr.so $(TEST_DATSET)
	cd test && python test_all.py --verbose

debug:
	python setup.py build_ext --inplace --debug

data: $(TEST_DATSET)

epr.so: src/epr.pyx
	python setup.py build_ext --inplace

$(TEST_DATSET):
	wget -P test $(TEST_DATSET_URL)
	gunzip $@
