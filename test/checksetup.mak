#!/usr/bin/make -f

ROOT = CHECKSETUP_ROOT

VERSION = $(shell grep "__version__ =" ../src/epr.pyx | cut -d \' -f 2)
PKGDIST = pyepr-$(VERSION).tar.gz
PYTHON = python
PYVER = 3.4.2
CONDA = conda
CONDAOPTS = --use-index-cache -m -y


.PHONY: \
	clean distclean cache check \
	check-nosetuptools check-setuptoolsoff check-setuptools \
	check-pip check-wheel


check: \
	check-nosetuptools \
	check-setuptoolsoff \
	check-setuptools \
	check-pip \
	check-wheel


check-nosetuptools: \
	check_nosetuptools_nonumpy_nocython \
	check_nosetuptools_numpy_nocython_c \
	check_nosetuptools_numpy_cython


check-setuptoolsoff: \
	check_setuptoolsoff_nonumpy_nocython \
	check_setuptoolsoff_numpy_nocython_c \
	check_setuptoolsoff_numpy_cython


check-setuptools: \
	check_setuptools_nonumpy_nocython \
	#check_setuptools_nonumpy_nocython_c \
	check_setuptools_numpy_cython_c


check-pip: \
	check_pip_nonumpy_nocython \
	check_pip_nonumpy_nocython_c \
	check_pip_numpy_cython_c


check-wheel: check_wheel


$(ROOT):
	mkdir -p $(ROOT)


$(ROOT)/cache-done:
	$(CONDA) create -p $(ROOT)/dummyenv -m -y \
		python=$(PYVER) setuptools pip numpy cython
	$(ROOT)/dummyenv/bin/pip install --download $(ROOT) --use-wheel wheel
	$(ROOT)/dummyenv/bin/pip install --download $(ROOT) numpy cython
	$(RM) -r $(ROOT)/dummyenv
	touch $@


$(ROOT)/$(PKGDIST): $(ROOT)
	#$(MAKE) -C .. distclean
	$(MAKE) -C .. sdist
	cp ../dist/$(PKGDIST) $(ROOT)


cache: $(ROOT)/cache-done $(ROOT)/$(PKGDIST)


clean:
	$(RM) -r $(ROOT)/check_*


distclean:
	$(RM) -r $(ROOT)


# no setuptools ###############################################################
check_nosetuptools_nonumpy_nocython: $(ROOT) cache
	$(RM) -r $(ROOT)/$@
	$(CONDA) create $(CONDAOPTS) -p $(ROOT)/$@ python=$(PYVER)
	tar -C $(ROOT)/$@ -xvzf $(ROOT)/$(PKGDIST)
	rm $(ROOT)/$@/pyepr-$(VERSION)/src/*.c
	cd $(ROOT)/$@/pyepr-$(VERSION);\
	../bin/$(PYTHON) setup.py install;\
	if [ ! $$? ]; then false; else true; fi
	@echo "EXPECTED FAILURE"


check_nosetuptools_numpy_nocython_c: $(ROOT) cache
	$(RM) -r $(ROOT)/$@
	$(CONDA) create $(CONDAOPTS) -p $(ROOT)/$@ python=$(PYVER) numpy
	tar -C $(ROOT)/$@ -xvzf $(ROOT)/$(PKGDIST)
	cd $(ROOT)/$@/pyepr-$(VERSION);\
	../bin/$(PYTHON) setup.py install


check_nosetuptools_numpy_cython: $(ROOT) cache
	$(RM) -r $(ROOT)/$@
	$(CONDA) create $(CONDAOPTS) -p $(ROOT)/$@ python=$(PYVER) numpy cython
	tar -C $(ROOT)/$@ -xvzf $(ROOT)/$(PKGDIST)
	rm $(ROOT)/$@/pyepr-$(VERSION)/src/*.c
	cd $(ROOT)/$@/pyepr-$(VERSION);\
	../bin/$(PYTHON) setup.py install


# setuptools off ##############################################################
check_setuptoolsoff_nonumpy_nocython: $(ROOT) cache
	$(RM) -r $(ROOT)/$@
	$(CONDA) create $(CONDAOPTS) -p $(ROOT)/$@ python=$(PYVER) setuptools
	tar -C $(ROOT)/$@ -xvzf $(ROOT)/$(PKGDIST)
	rm $(ROOT)/$@/pyepr-$(VERSION)/src/*.c
	cd $(ROOT)/$@/pyepr-$(VERSION);\
	env USE_SETUPTOOLS=FALSE ../bin/$(PYTHON) setup.py install;\
	if [ ! $$? ]; then false; else true; fi
	@echo "EXPECTED FAILURE"


check_setuptoolsoff_numpy_nocython_c: $(ROOT) cache
	$(RM) -r $(ROOT)/$@
	$(CONDA) create $(CONDAOPTS) -p $(ROOT)/$@ python=$(PYVER) setuptools numpy
	tar -C $(ROOT)/$@ -xvzf $(ROOT)/$(PKGDIST)
	cd $(ROOT)/$@/pyepr-$(VERSION);\
	env USE_SETUPTOOLS=FALSE ../bin/$(PYTHON) setup.py install


check_setuptoolsoff_numpy_cython: $(ROOT) cache
	$(RM) -r $(ROOT)/$@
	$(CONDA) create $(CONDAOPTS) -p $(ROOT)/$@ python=$(PYVER) setuptools numpy cython
	tar -C $(ROOT)/$@ -xvzf $(ROOT)/$(PKGDIST)
	rm $(ROOT)/$@/pyepr-$(VERSION)/src/*.c
	cd $(ROOT)/$@/pyepr-$(VERSION);\
	env USE_SETUPTOOLS=FALSE ../bin/$(PYTHON) setup.py install


# setuptools ##################################################################
check_setuptools_nonumpy_nocython: $(ROOT) cache
	$(RM) -r $(ROOT)/$@
	$(CONDA) create $(CONDAOPTS) -p $(ROOT)/$@ python=$(PYVER) setuptools
	tar -C $(ROOT)/$@ -xvzf $(ROOT)/$(PKGDIST)
	rm $(ROOT)/$@/pyepr-$(VERSION)/src/*.c
	cd $(ROOT)/$@/pyepr-$(VERSION);\
	../bin/$(PYTHON) setup.py install;\
	if [ ! $$? ]; then false; else true; fi
	@echo "EXPECTED FAILURE"


# @TODO: check
#check_setuptools_nonumpy_nocython_c: $(ROOT) cache
#	$(RM) -r $(ROOT)/$@
#	$(CONDA) create $(CONDAOPTS) -p $(ROOT)/$@ python=$(PYVER) setuptools
#	tar -C $(ROOT)/$@ -xvzf $(ROOT)/$(PKGDIST)
#	cd $(ROOT)/$@/pyepr-$(VERSION);\
#	../bin/$(PYTHON) setup.py install


check_setuptools_numpy_cython_c: $(ROOT) cache
	$(RM) -r $(ROOT)/$@
	$(CONDA) create $(CONDAOPTS) -p $(ROOT)/$@ python=$(PYVER) setuptools numpy cython
	tar -C $(ROOT)/$@ -xvzf $(ROOT)/$(PKGDIST)
	cd $(ROOT)/$@/pyepr-$(VERSION);\
	../bin/$(PYTHON) setup.py install


# pip #########################################################################
check_pip_nonumpy_nocython: $(ROOT) cache
	$(RM) -r $(ROOT)/$@
	$(CONDA) create $(CONDAOPTS) -p $(ROOT)/$@ python=$(PYVER) pip
	tar -C $(ROOT)/$@ -xvzf $(ROOT)/$(PKGDIST)
	rm $(ROOT)/$@/pyepr-$(VERSION)/src/*.c
	cd $(ROOT)/$@/pyepr-$(VERSION);\
	$(ROOT)/$@/bin/pip install -v --no-index --find-links=file://$(PWD)/$(ROOT) $(ROOT)/$@/pyepr-$(VERSION);\
	if [ ! $$? ]; then false; else true; fi
	@echo "EXPECTED FAILURE"


check_pip_nonumpy_nocython_c: $(ROOT) cache
	$(RM) -r $(ROOT)/$@
	$(CONDA) create $(CONDAOPTS) -p $(ROOT)/$@ python=$(PYVER) pip
	$(ROOT)/$@/bin/pip install -v --no-index --find-links=file://$(PWD)/$(ROOT) $(ROOT)/$(PKGDIST)


check_pip_numpy_cython_c: $(ROOT) cache
	$(RM) -r $(ROOT)/$@
	$(CONDA) create $(CONDAOPTS) -p $(ROOT)/$@ python=$(PYVER) pip cython numpy
	$(ROOT)/$@/bin/pip install -v --no-index --find-links=file://$(PWD)/$(ROOT) $(ROOT)/$(PKGDIST)


# wheel #######################################################################
check_wheel: $(ROOT) cache
	$(RM) -r $(ROOT)/$@
	$(CONDA) create $(CONDAOPTS) -p $(ROOT)/$@ python=$(PYVER) pip cython numpy
	$(ROOT)/$@/bin/pip install -v --no-index --find-links=file://$(PWD)/$(ROOT) wheel
	tar -C $(ROOT)/$@ -xvzf $(ROOT)/$(PKGDIST)
	cd $(ROOT)/$@/pyepr-$(VERSION);\
	../bin/$(PYTHON) setup.py bdist_wheel
