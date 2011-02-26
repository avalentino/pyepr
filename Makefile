#!/usr/bin/make -f

.PHONY: default clean distclean check debug

default:
	python setup.py build_ext --inplace

clean:
	python setup.py clean
	$(RM) src/*.py[co] tests/*.py[co]

distclean: clean
	$(RM) src/*.c src/*.o *.so
	#$(RM) tests/*.N1

check:
	cd tests && python test_all.py --verbose

debug:
	python setup.py build_ext --inplace --debug
