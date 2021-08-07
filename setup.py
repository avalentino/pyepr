#!/usr/bin/env python3

# Copyright (C) 2011-2021, Antonio Valentino <antonio.valentino@tiscali.it>
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

import setuptools

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


# https://mail.python.org/pipermail/distutils-sig/2007-September/008253.html
class NumpyExtension(setuptools.Extension):
    """Extension type that adds the NumPy include directory to include_dirs."""

    @property
    def include_dirs(self):
        from numpy import get_include
        return self._include_dirs + [get_include()]

    @include_dirs.setter
    def include_dirs(self, include_dirs):
        self._include_dirs = include_dirs


def setup_extension(eprsrcdir=None, coverage=False):
    import glob

    if eprsrcdir:
        print('EPR_API: using EPR C API sources at "{}"'.format(eprsrcdir))
        extra_sources = glob.glob('{}/epr_*.c'.format(eprsrcdir))
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

    ext = NumpyExtension(
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


BASE_CONFIG = dict(
    version=get_version(os.path.join('src', 'epr.pyx')),
)


def make_config(eprsrcdir=None, coverage=False):
    config = BASE_CONFIG.copy()
    config['version'] = get_version(os.path.join('src', 'epr.pyx'))
    config['ext_modules'] = [setup_extension(eprsrcdir, coverage)]
    if not os.path.exists(os.path.join('src', 'epr.c')):
        config.setdefault('setup_requires', []).append('cython>=0.29')

    return config


def get_parser():
    PYEPR_COVERAGE_STR = os.environ.get('PYEPR_COVERAGE', '').upper()
    DEFAULT_COVERAGE = bool(
        PYEPR_COVERAGE_STR in ('Y', 'YES', 'TRUE', 'OK', 'ON', '1'))
    DEFAULT_EPRAPI_SRC = 'extern/epr-api/src'
    if not os.path.exists(DEFAULT_EPRAPI_SRC):
        DEFAULT_EPRAPI_SRC = ''
    DEFAULT_EPRAPI_SRC = os.environ.get('PYEPR_EPRAPI_SRC', DEFAULT_EPRAPI_SRC)

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--coverage', action='store_true', default=DEFAULT_COVERAGE)
    parser.add_argument('--epr-api-src', default=DEFAULT_EPRAPI_SRC)

    return parser


if __name__ == '__main__':
    parser = get_parser()
    extra_args, setup_argv = parser.parse_known_args(sys.argv)
    sys.argv[:] = setup_argv
    print('PYEPR_COVERAGE:', extra_args.coverage)

    config = make_config(extra_args.epr_api_src, extra_args.coverage)
    setuptools.setup(**config)
