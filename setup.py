#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011-2018, Antonio Valentino <antonio.valentino@tiscali.it>
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
print('HAVE_SETUPTOOLS: {0}'.format(HAVE_SETUPTOOLS))


try:
    from Cython.Build import cythonize
    HAVE_CYTHON = True
except ImportError:
    HAVE_CYTHON = False
print('HAVE_CYTHON: {0}'.format(HAVE_CYTHON))


# @COMPATIBILITY: Extension is an old style class in Python 2
class PyEprExtension(Extension, object):
    def __init__(self, *args, **kwargs):
        self._include_dirs = []
        eprsrcdir = kwargs.pop('eprsrcdir', None)

        super(PyEprExtension, self).__init__(*args, **kwargs)

        self.sources.extend(self._extra_sources(eprsrcdir))
        self.setup_requires_cython = False

    def _extra_sources(self, eprsrcdir=None):
        sources = []

        # check for local epr-api sources
        if eprsrcdir is None:
            default_eprapisrc = os.path.join('epr-api-src')
            if os.path.isdir(default_eprapisrc):
                eprsrcdir = default_eprapisrc

        if eprsrcdir:
            print('using EPR C API sources at "{0}"'.format(eprsrcdir))
            self._include_dirs.append(eprsrcdir)
            sources.extend(glob.glob(os.path.join(eprsrcdir, 'epr_*.c')))

        else:
            print('using pre-built dynamic libraray for EPR C API')
            if 'epr_api' not in self.libraries:
                self.libraries.append('epr_api')

        sources = sorted(set(sources).difference(self.sources))

        return sources

    @property
    def include_dirs(self):
        from numpy.distutils.misc_util import get_numpy_include_dirs
        includes = set(get_numpy_include_dirs()).difference(self._include_dirs)
        return self._include_dirs + sorted(includes)

    @include_dirs.setter
    def include_dirs(self, value):
        self._include_dirs = value

    # disable setuptools automatic conversion
    def _convert_pyx_sources_to_lang(self):
        pass

    def convert_pyx_sources_to_lang(self):
        lang = self.language or ''
        target_ext = '.cpp' if lang.lower() == 'c++' else '.c'

        sources = []
        for src in self.sources:
            if src.endswith('.pyx'):
                csrc = re.sub('.pyx$', target_ext, src)
                if os.path.exists(csrc):
                    sources.append(csrc)
                else:
                    self.setup_requires_cython = True
                    sources.append(src)
            else:
                sources.append(src)

        if not self.setup_requires_cython:
            self.sources = sources

        return self.setup_requires_cython


def get_extension():
    # command line arguments management
    eprsrcdir = None
    for arg in list(sys.argv):
        if arg.startswith('--epr-api-src='):
            eprsrcdir = os.path.expanduser(arg.split('=')[1])
            if eprsrcdir.lower() == 'none':
                eprsrcdir = False
            sys.argv.remove(arg)
            break

    ext = PyEprExtension(
        'epr',
        sources=[os.path.join('src', 'epr.pyx')],
        # libraries=['m'],
        # define_macros=[('NPY_NO_DEPRECATED_API', 'NPY_1_7_API_VERSION'),],
        eprsrcdir=eprsrcdir,
    )

    # @NOTE: uses the HAVE_CYTHON global variable
    if HAVE_CYTHON:
        extlist = cythonize([ext])
        ext = extlist[0]
    else:
        ext.convert_pyx_sources_to_lang()

    return ext


config = dict(
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

.. _Python: https://www.python.org
.. _`EPR API`: https://github.com/bcdev/epr-api
.. _ENVISAT: https://envisat.esa.int
.. _ESA: https://earth.esa.int
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
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Cython',
        'Topic :: Software Development :: Libraries',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: GIS',
    ],
    platforms=['any'],
    license='GPL3',
    requires=['numpy'],     # XXX: check
)


def setup_package():
    ext = get_extension()
    config['ext_modules'] = [ext]

    if HAVE_SETUPTOOLS:
        config['test_suite'] = 'tests'
        config.setdefault('setup_requires', []).append('numpy>=1.5')
        config.setdefault('install_requires', []).append('numpy>=1.5')
        if ext.setup_requires_cython:
            config['setup_requires'].append('cython>=0.19')

    setup(**config)


if __name__ == '__main__':
    setup_package()
