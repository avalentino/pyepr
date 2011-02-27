#!/usr/bin/make -f

TEST_DATSET_URL = "http://earth.esa.int/services/sample_products/asar/IMP/ASA_IMP_1PNUPA20060202_062233_000000152044_00435_20529_3110.N1.gz"
TEST_DATSET = tests/ASA_IMP_1PNUPA20060202_062233_000000152044_00435_20529_3110.N1

.PHONY: default clean distclean check debug data

default: epr.so

clean:
	python setup.py clean
	$(RM) src/*.py[co] tests/*.py[co]

distclean: clean
	$(RM) src/*.c src/*.o *.so
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
