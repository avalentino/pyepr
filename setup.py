#!/usr/bin/env python
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
import re
import sys
import glob

from setuptools import setup, Extension


PYEPR_COVERAGE = False


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


try:
    from Cython.Build import cythonize
    from Cython import __version__ as CYTHON_VERSION
    HAVE_CYTHON = True
except ImportError:
    HAVE_CYTHON = False
    CYTHON_VERSION = None
print('HAVE_CYTHON: {0}'.format(HAVE_CYTHON))
if HAVE_CYTHON:
    print('CYTHON_VERSION: {0}'.format(CYTHON_VERSION))


# @COMPATIBILITY: Extension is an old style class in Python 2
class PyEprExtension(Extension, object):
    def __init__(self, *args, **kwargs):
        self._include_dirs = []
        eprsrcdir = kwargs.pop('eprsrcdir', None)

        Extension.__init__(self, *args, **kwargs)

        if not any('epr_' in src for src in self.sources):
            self.sources.extend(self._extra_sources(eprsrcdir))

        self.setup_requires_cython = False

    def _extra_sources(self, eprsrcdir=None):
        sources = []

        # check for local epr-api sources
        if eprsrcdir is None:
            default_eprapisrc = 'epr-api-src'
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

    define_macros = []

    # @NOTE: uses the CYTHON_VERSION global variable
    if HAVE_CYTHON and CYTHON_VERSION >= '0.29':
        define_macros.append(
            ('NPY_NO_DEPRECATED_API', 'NPY_1_7_API_VERSION'),
        )

    ext = PyEprExtension(
        'epr',
        sources=[os.path.join('src', 'epr.pyx')],
        # libraries=['m'],
        define_macros=define_macros,
        eprsrcdir=eprsrcdir,
    )

    # @NOTE: uses the HAVE_CYTHON and CYTHON_VERSION global variables
    if HAVE_CYTHON:
        if CYTHON_VERSION >= '0.29':
            language_level = '3str'
        else:
            language_level = '2'
        print('CYTHON_LANGUAGE_LEVEL: {0}'.format(language_level))

        compiler_directives = dict(
            language_level=language_level,
        )

        if PYEPR_COVERAGE:
            compiler_directives['linetrace'] = True

        extlist = cythonize([ext], compiler_directives=compiler_directives)
        ext = extlist[0]

        if PYEPR_COVERAGE:
            ext.define_macros.extend([
                ('CYTHON_TRACE_NOGIL', '1'),
            ])
    else:
        ext.convert_pyx_sources_to_lang()

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
    ext_modules=[get_extension()],
    setup_requires=['numpy>=1.7'],
    install_requires=['numpy>=1.7'],
    python_requires='>=3.5, <4',
    zip_safe=False,
)


def setup_package():
    ext = config['ext_modules'][0]
    if ext.setup_requires_cython:
        config.setdefault('setup_requires', []).append('cython>=0.19')

    setup(**config)


if __name__ == '__main__':
    if '--coverage' in sys.argv or 'PYEPR_COVERAGE' in os.environ:
        PYEPR_COVERAGE = True
        if '--coverage' in sys.argv:
            sys.argv.remove('--coverage')

    print('PYEPR_COVERAGE:', PYEPR_COVERAGE)

    setup_package()
