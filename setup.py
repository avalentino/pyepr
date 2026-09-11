#!/usr/bin/env python3

# Copyright (C) 2011-2026, Antonio Valentino <antonio.valentino@tiscali.it>
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
import warnings
import sysconfig

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


def tag_to_packed_version(tag: str) -> tuple[int, bool]:
    mobj = re.match(
        r"cp(?P<major>\d{1})(?P<minor>\d{2})(?P<free_threading>t)?", tag
    )
    if mobj is None:
        raise ValueError(f"invalid version tag: {tag!r}")
    major = int(mobj.group("major"))
    minor = int(mobj.group("minor"))
    packed_version = (major << 24) + (minor << 16)
    free_threading = bool(mobj.group("free_threading") is not None)
    return packed_version, free_threading


def setup_extension(
    eprsrcdir=None,
    *,
    coverage: bool = False,
    py_limited_api: str | None = None,
):
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

    define_macros: list[tuple[str, str | None]] = [
        ("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")
    ]
    if coverage:
        define_macros.append(("CYTHON_TRACE_NOGIL", "1"))
        if py_limited_api is not None:
            warnings.warn(
                "The use of 'limited_api` is not compatible with the "
                "'coverage': 'limited_api' will be ignored",
                stacklevel=2,
            )
    elif py_limited_api is not None:
        packed_version, free_threading = tag_to_packed_version(py_limited_api)
        macro_name = "Py_LIMITED_APIT" if free_threading else "Py_LIMITED_API"
        hex_version = f"0x{packed_version:08X}"
        print(f"{macro_name}: {hex_version} ({py_limited_api})")
        if free_threading and not sysconfig.get_config_var("Py_GIL_DISABLED"):
            warnings.warn(
                "Trying to use a free-threading stable API with a Python "
                "interpreter that has GIL enabled",
                stacklevel=1,
            )
        define_macros.append((macro_name, hex_version))

    ext = NumpyExtension(
        "epr._epr",
        sources=[os.path.join("src", "epr", "_epr.pyx"), *extra_sources],
        include_dirs=include_dirs,
        libraries=libraries,
        language="c",
        define_macros=define_macros,
        py_limited_api=bool(py_limited_api is not None),
    )

    # compiler directives
    language_level = "3"
    ext.cython_directives = {"language_level": language_level}
    print(f"CYTHON_LANGUAGE_LEVEL: {language_level}")

    if coverage:
        ext.cython_directives["linetrace"] = True

    ext.cython_directives["freethreading_compatible"] = True

    return ext


def make_config(
    eprsrcdir=None,
    *,
    coverage=False,
    py_limited_api: str | None = None,
):
    if not py_limited_api:
        py_limited_api = None
    elif py_limited_api == "AUTO":
        if not sysconfig.get_config_var("Py_GIL_DISABLED"):
            py_limited_api = "cp311"
        else:
            py_limited_api = None

    config = {
        "ext_modules": [
            setup_extension(
                eprsrcdir, coverage=coverage, py_limited_api=py_limited_api
            ),
        ]
    }

    if py_limited_api is not None:
        config["options"] = {"bdist_wheel": {"py_limited_api": py_limited_api}}

    return config


def get_parser():
    import argparse

    DEFAULT_EPRAPI_SRC = "extern/epr-api/src"
    if not os.path.exists(DEFAULT_EPRAPI_SRC):
        DEFAULT_EPRAPI_SRC = ""
    DEFAULT_EPRAPI_SRC = os.environ.get("PYEPR_EPRAPI_SRC", DEFAULT_EPRAPI_SRC)

    DEFAULT_PY_LIMITED_API = os.environ.get("PY_LIMITED_API", None)

    PYEPR_COVERAGE_STR = os.environ.get("PYEPR_COVERAGE", "").upper()
    DEFAULT_COVERAGE = bool(
        PYEPR_COVERAGE_STR in {"Y", "YES", "TRUE", "OK", "ON", "1"}
    )

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "--epr-api-src",
        default=DEFAULT_EPRAPI_SRC,
        help="set the path to the EPR-API source tree. "
        "If not set uses the system libraries for epr-api. "
        "Default: %(default)s",
    )
    parser.add_argument(
        "--use-stable-api",
        dest="py_limited_api",
        default=DEFAULT_PY_LIMITED_API,
        help=(
            "enable the use of the specified stable Python API "
            "(and limited ABI)."
            "If 'None', the use of limited API is disabled. "
            "E.g.: 'cp312' for Python 3.12. "
            f"Default: {DEFAULT_PY_LIMITED_API}."
        ),
    )
    parser.add_argument(
        "--coverage",
        action="store_true",
        default=DEFAULT_COVERAGE,
        help=(
            "build the epr module to allow cython coverage measurement "
            "(default: %(default)s)"
        ),
    )

    return parser


if __name__ == "__main__":
    parser = get_parser()
    extra_args, setup_argv = parser.parse_known_args(sys.argv)
    sys.argv[:] = setup_argv
    print("PY_LIMITED_API:", extra_args.py_limited_api)
    print("PYEPR_COVERAGE:", extra_args.coverage)

    config = make_config(
        extra_args.epr_api_src,
        coverage=extra_args.coverage,
        py_limited_api=extra_args.py_limited_api,
    )

    if "-h" in setup_argv or "--help" in setup_argv:
        msg = parser.format_help()
        msg = "\n".join(msg.splitlines()[2:])  # remove usage string
        print(msg)
        print()

    print("config:", config)
    setuptools.setup(**config)
