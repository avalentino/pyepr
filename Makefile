#!/usr/bin/make -f

.PHONY: default clean distclean

default:
	python setup.py build_ext --inplace

clean:
	python setup.py clean
	$(RM) epr/*.py[co] tests/*.py[co]

distclean: clean
	$(RM) epr/*.c epr/*.o epr/*.so
	#$(RM) tests/*.N1
