#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011-2015, Antonio Valentino <antonio.valentino@tiscali.it>
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

from __future__ import print_function

import os
import re
import sys
import glob


def get_version(filename):
    with open(filename) as fd:
        data = fd.read()

    mobj = re.search(
        '''^__version__\s*=\s*(?P<q>['"])(?P<version>\d+(\.\d+)*.*)(?P=q)''',
        data, re.MULTILINE)

    return mobj.group('version')


def get_use_setuptools():
    use_setuptools = os.environ.get('USE_SETUPTOOLS', True)
    if str(use_setuptools).lower() in ('false', 'off', 'n', 'no', '0'):
        use_setuptools = False
        print('USE_SETUPTOOLS: {}'.format(use_setuptools))
    else:
        use_setuptools = True

    return use_setuptools


try:
    if not get_use_setuptools():
        raise ImportError

    from setuptools import setup, Extension
    HAVE_SETUPTOOLS = True
except ImportError:
    from distutils.core import setup
    from distutils.extension import Extension
    HAVE_SETUPTOOLS = False
print('HAVE_SETUPTOOLS: {}'.format(HAVE_SETUPTOOLS))


try:
    from Cython.Distutils import build_ext
    sources = [os.path.join('src', 'epr.pyx')]
except ImportError:
    from distutils.command.build_ext import build_ext
    sources = [os.path.join('src', 'epr.c')]


def get_extension():
    source = []
    libraries = []
    include_dirs = []

    from numpy.distutils.misc_util import get_numpy_include_dirs
    include_dirs.extend(get_numpy_include_dirs())

    # command line arguments management
    eprsrcdir = None
    for arg in list(sys.argv):
        if arg.startswith('--epr-api-src='):
            eprsrcdir = os.path.expanduser(arg.split('=')[1])
            if eprsrcdir.lower() == 'none':
                eprsrcdir = False
            sys.argv.remove(arg)
            break

    # check for local epr-api sources
    if eprsrcdir is None:
        if os.path.isdir('epr-api-src'):
            eprsrcdir = 'epr-api-src'

    if eprsrcdir:
        include_dirs.append(eprsrcdir)
        sources.extend(glob.glob(os.path.join(eprsrcdir, 'epr_*.c')))
        #libraries.append('m')
        print('using EPR C API sources at "{}"'.format(eprsrcdir))
    else:
        libraries.append('epr_api')
        print('using pre-built dynamic library for EPR C API')

    ect = Extension(
        'epr',
        sources=sources,
        include_dirs=include_dirs,
        libraries=libraries,
        #define_macros=[('NPY_NO_DEPRECATED_API', 'NPY_1_7_API_VERSION'),],
    )

    return ext


KWARGS = dict(
    name='pyepr',
    version=get_version(os.path.join('src', 'epr.pyx')),
    author='Antonio Valentino',
    author_email='antonio.valentino@tiscali.it',
    url='http://avalentino.github.com/pyepr',
    description='Python ENVISAT Product Reader API',
    long_description='''PyEPR provides Python_ bindings for the ENVISAT
Product Reader C API (`EPR API`_) for reading satellite data from ENVISAT_
ESA_ (European Space Agency) mission.

PyEPR, as well as the `EPR API`_ for C, supports ENVISAT_ MERIS, AATSR
Level 1B and Level 2 and also ASAR data products. It provides access to
the data either on a geophysical (decoded, ready-to-use pixel samples)
or on a raw data layer. The raw data access makes it possible to read
any data field contained in a product file.

.. _Python: http://www.python.org
.. _`EPR API`: https://github.com/bcdev/epr-api
.. _ENVISAT: http://envisat.esa.int
.. _ESA: http://earth.esa.int
''',
    download_url='http://pypi.python.org/pypi/pyepr',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Cython',
        'Topic :: Software Development :: Libraries',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: GIS',
    ],
    platforms=['any'],
    license='GPL3',
    cmdclass={'build_ext': build_ext},
    requires=['numpy'],
)


def setup_package():
    ext = get_extension()
    KWARGS['ext_modules'] = [ext]

    if HAVE_SETUPTOOLS:
        KWARGS.setdefault('setup_requires', []).append('numpy')
        KWARGS.setdefault('install_requires', []).append('numpy')

    setup(**KWARGS)


if __name__ == '__main__':
    setup_package()
