#!/bin/bash
# Based on: https://github.com/pypa/python-manylinux-demo 9700d97 17 Dec 2016
#
# It is assumed that the docker image has been run as follows::
#
#   $ make fullsdist
#   $ docker pull quay.io/pypa/manylinux1_x86_64
#   $ docker run --rm -v $(pwd):/io quay.io/pypa/manylinux1_x86_64 /io/build-manylinux-wheels.sh
#
# For interactive sessions please use::
#
#   $ make fullsdist
#   $ docker pull quay.io/pypa/manylinux1_x86_64
#   $ docker run -it -v $(pwd):/io quay.io/pypa/manylinux1_x86_64
#   $ cd /io
#   $ sh build-manylinux-wheels.sh

set -e -x

PKG=pyepr

# Compile wheels
for PYBIN in /opt/python/*/bin; do
    "${PYBIN}/pip" install -r /io/requirements.txt
    "${PYBIN}/pip" wheel /io/dist/${PKG}*.tar.gz -w wheelhouse/
done

# Bundle external shared libraries into the wheels
for whl in wheelhouse/${PKG}*.whl; do
    auditwheel repair "${whl}" -w /io/wheelhouse/
done

# Install packages and test
for PYBIN in /opt/python/*/bin/; do
    "${PYBIN}/pip" install ${PKG} --no-index -f /io/wheelhouse
    "${PYBIN}/python" /io/tests/test_all.py -v
done
