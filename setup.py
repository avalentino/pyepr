#!/usr/bin/env python3

# Copyright (C) 2011-2025, Antonio Valentino <antonio.valentino@tiscali.it>
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

    print(f"CYTHON_VERSION: {Cython.__version__}")
    del Cython
except ImportError:
    print("CYTHON not installed")


# https://mail.python.org/pipermail/distutils-sig/2007-September/008253.html
class NumpyExtension(setuptools.Extension):
    """Extension type that adds the NumPy include directory to include_dirs."""

    @property
    def include_dirs(self):
        from numpy import get_include

        return [*self._include_dirs, get_include()]

    @include_dirs.setter
    def include_dirs(self, include_dirs):
        self._include_dirs = include_dirs


def setup_extension(eprsrcdir=None, *, coverage: bool = False):
    import glob

    if eprsrcdir:
        print(f'EPR_API: using EPR C API sources at "{eprsrcdir}"')
        extra_sources = glob.glob(f"{eprsrcdir}/epr_*.c")
        include_dirs = [eprsrcdir]
        libraries = []
    else:
        print("EPR_API: using pre-built dynamic library for EPR C API")
        extra_sources = []
        include_dirs = []
        libraries = ["epr_api"]

    define_macros = [("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")]
    if coverage:
        define_macros.extend([("CYTHON_TRACE_NOGIL", "1")])

    ext = NumpyExtension(
        "epr._epr",
        sources=[os.path.join("src", "epr", "epr.pyx"), *extra_sources],
        include_dirs=include_dirs,
        libraries=libraries,
        language="c",
        define_macros=define_macros,
    )

    # compiler directives
    language_level = "3"
    ext.cython_directives = {"language_level": language_level}
    print(f"CYTHON_LANGUAGE_LEVEL: {language_level}")

    if coverage:
        ext.cython_directives["linetrace"] = True

    return ext


def make_config(eprsrcdir=None, *, coverage=False):
    return {
        "ext_modules": [setup_extension(eprsrcdir, coverage=coverage)],
    }


def get_parser():
    import argparse

    PYEPR_COVERAGE_STR = os.environ.get("PYEPR_COVERAGE", "").upper()
    DEFAULT_COVERAGE = bool(
        PYEPR_COVERAGE_STR in {"Y", "YES", "TRUE", "OK", "ON", "1"}
    )
    DEFAULT_EPRAPI_SRC = "extern/epr-api/src"
    if not os.path.exists(DEFAULT_EPRAPI_SRC):
        DEFAULT_EPRAPI_SRC = ""
    DEFAULT_EPRAPI_SRC = os.environ.get("PYEPR_EPRAPI_SRC", DEFAULT_EPRAPI_SRC)

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "--coverage",
        action="store_true",
        default=DEFAULT_COVERAGE,
        help="build the epr module to allow cython coverage measurement "
        "(default: %(default)s)",
    )
    parser.add_argument(
        "--epr-api-src",
        default=DEFAULT_EPRAPI_SRC,
        help="set the path to the EPR-API source tree. "
        "If not set uses the system libraries for epr-api. "
        "Default: %(default)s",
    )

    return parser


if __name__ == "__main__":
    parser = get_parser()
    extra_args, setup_argv = parser.parse_known_args(sys.argv)
    sys.argv[:] = setup_argv
    print("PYEPR_COVERAGE:", extra_args.coverage)

    config = make_config(extra_args.epr_api_src, coverage=extra_args.coverage)

    if "-h" in setup_argv or "--help" in setup_argv:
        msg = parser.format_help()
        msg = "\n".join(msg.splitlines()[2:])  # remove usage string
        print(msg)
        print()

    print("config:", config)
    setuptools.setup(**config)
