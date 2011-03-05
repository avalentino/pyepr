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
TEST_DATSET = tests/ASA_IMP_1PNUPA20060202_062233_000000152044_00435_20529_3110.N1

.PHONY: default clean distclean check debug data

default: epr.so

clean:
	python setup.py clean
	$(RM) src/*.py[co] tests/*.py[co] README.html

distclean: clean
	$(RM) -r build dist
	$(RM) MANIFEST src/*.c src/*.o *.so
	#$(RM) tests/*.N1

check: epr.so $(TEST_DATSET)
	cd tests && python test_all.py --verbose

debug:
	python setup.py build_ext --inplace --debug

data: $(TEST_DATSET)

epr.so: src/epr.pyx
	python setup.py build_ext --inplace

$(TEST_DATSET):
	wget -P tests $(TEST_DATSET_URL)
	gunzip $@

README.html: README.txt
	rst2html -s -d -g --title "Python EPR API" --cloak-email-addresses $< $@
