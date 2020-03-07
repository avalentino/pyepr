#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2011-2020, Antonio Valentino <antonio.valentino@tiscali.it>
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

import os
import sys
import glob

from setuptools import setup, Extension

try:
    import Cython
    print('CYTHON_VERSION: {}'.format(Cython.__version__))
    del Cython
except ImportError:
    print('CYTHON not installed')


def get_version(filename, strip_extra=False):
    import re
    from distutils.version import LooseVersion

    with open(filename) as fd:
        data = fd.read()

    mobj = re.search(
        r'''^__version__\s*=\s*(?P<quote>['"])(?P<version>.*)(?P=quote)''',
        data, re.MULTILINE)
    version = LooseVersion(mobj.group('version'))

    if strip_extra:
        return '.'.join(map(str, version.version[:3]))
    else:
        return version.vstring


def get_extension(eprsrcdir=None, coverage=False):
    if eprsrcdir:
        print('EPR_API: using EPR C API sources at "{}"'.format(eprsrcdir))
        extra_sources = glob.glob(f'{eprsrcdir}/epr_*.c')
        include_dirs = [eprsrcdir]
        libraries = []
    else:
        print('EPR_API: using pre-built dynamic library for EPR C API')
        extra_sources = []
        include_dirs = []
        libraries = ['epr_api']

    define_macros = [('NPY_NO_DEPRECATED_API', 'NPY_1_7_API_VERSION')]
    if coverage:
        define_macros.extend([('CYTHON_TRACE_NOGIL', '1')])

    ext = Extension(
        'epr',
        sources=[os.path.join('src', 'epr.pyx')] + extra_sources,
        include_dirs=include_dirs,
        libraries=libraries,
        language='c',
        define_macros=define_macros,
    )

    # compiler directives
    language_level = '3str'
    ext.cython_directives = dict(language_level=language_level)
    print('CYTHON_LANGUAGE_LEVEL: {}'.format(language_level))

    if coverage:
        ext.cython_directives['linetrace'] = True

    return ext


config = dict(
    name='pyepr',
    version=get_version(os.path.join('src', 'epr.pyx')),
    description='Python ENVISAT Product Reader API',
    long_description='''PyEPR provides Python_ bindings for the ENVISAT
Product Reader C API (`EPR API`_) for reading satellite data from ENVISAT_
ESA_ (European Space Agency) mission.

PyEPR, as well as the `EPR API`_ for C, supports ENVISAT_ MERIS, AATSR
Level 1B and Level 2 and also ASAR data products. It provides access to
the data either on a geophysical (decoded, ready-to-use pixel samples)
or on a raw data layer. The raw data access makes it possible to read
any data field contained in a product file.

.. _Python: https://www.python.org
.. _`EPR API`: https://github.com/bcdev/epr-api
.. _ENVISAT: https://envisat.esa.int
.. _ESA: https://earth.esa.int
''',
    long_description_content_type='text/x-rst',
    url='http://avalentino.github.com/pyepr',
    download_url='http://pypi.python.org/pypi/pyepr',
    author='Antonio Valentino',
    author_email='antonio.valentino@tiscali.it',
    license='GPL3',
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
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Cython',
        'Topic :: Software Development :: Libraries',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: GIS',
    ],
    keywords='satellite reader envisat',
    project_urls={
        'Documentation': 'http://avalentino.github.io/pyepr/html/index.html',
        'Source': 'https://github.com/avalentino/pyepr/',
        'Tracker': 'https://github.com/avalentino/pyepr/issues',
    },
    # ext_modules=[],
    setup_requires=['numpy>=1.7'],
    install_requires=['numpy>=1.7'],
    python_requires='>=3.5, <4',
    zip_safe=False,
)


def setup_package(config, eprsrcdir=None, coverage=False):
    if not os.path.exists(os.path.join('src', 'eps.c')):
        config.setdefault('setup_requires', []).append('cython>=0.29')

    config['ext_modules'] = [get_extension(eprsrcdir, coverage)]

    setup(**config)


if __name__ == '__main__':
    PYEPR_COVERAGE_STR = os.environ.get('PYEPR_COVERAGE', '').upper()
    DEFAULT_COVERAGE = bool(
        PYEPR_COVERAGE_STR in ('Y', 'YES', 'TRUE', 'OK', 'ON', '1'))
    DEFAULT_EPRAPI_SRC = 'epr-api-src' if os.path.exists('epr-api-src') else ''
    DEFAULT_EPRAPI_SRC = os.environ.get('PYEPR_EPRAPI_SRC', DEFAULT_EPRAPI_SRC)

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--coverage', action='store_true', default=DEFAULT_COVERAGE)
    parser.add_argument('--epr-api-src', default=DEFAULT_EPRAPI_SRC)
    extra_args, setup_argv = parser.parse_known_args(sys.argv)
    sys.argv[:] = setup_argv

    print('PYEPR_COVERAGE:', extra_args.coverage)

    setup_package(config, extra_args.epr_api_src, extra_args.coverage)
