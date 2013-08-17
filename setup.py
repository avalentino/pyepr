#!/usr/bin/env python
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

from __future__ import print_function

import os
import re
import sys
import glob

from distutils.core import setup
from distutils.extension import Extension

source = []
libraries = []
include_dirs = []
eprsrcdir = None


try:
    from Cython.Distutils import build_ext
    sources = [os.path.join('src', 'epr.pyx')]
except ImportError:
    from distutils.command.build_ext import build_ext
    sources = [os.path.join('src', 'epr.c')]


from numpy.distutils.misc_util import get_numpy_include_dirs
include_dirs.extend(get_numpy_include_dirs())


# command line arguments management
for arg in list(sys.argv):
    if arg.startswith('--epr-api-src='):
        eprsrcdir = os.path.expanduser(arg.split('=')[1])
        if eprsrcdir.lower() == 'none':
            eprsrcdir = False
        sys.argv.remove(arg)


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
    print('using pre-built dynamic libraray for EPR C API')


def get_version():
    filename = os.path.join('src', 'epr.pyx')
    data = open(filename).read()

    mobj = re.search(
        r"^__version__\s*=\s*\'(?P<version>\d+(\.\d+)*(\+|(\-)?dev)?)\'",
        data, re.MULTILINE)

    return mobj.group('version')


setup(
    name='pyepr',
    version=get_version(),
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
    ext_modules=[
        Extension(
            'epr',
            sources=sources,
            include_dirs=include_dirs,
            libraries=libraries,
            #define_macros=[('NPY_NO_DEPRECATED_API', 'NPY_1_7_API_VERSION'),],
            #extra_compile_args=['-Wno-strict-prototypes', '-ansi'],
        ),
    ],
    requires=['numpy'],
)
