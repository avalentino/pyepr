=================================
ENVISAT Product Reader Python API
=================================

:HomePage:  https://avalentino.github.io/pyepr
:Author:    Antonio Valentino
:Contact:   antonio.valentino@tiscali.it
:Copyright: 2011-2021, Antonio Valentino <antonio.valentino@tiscali.it>
:Version:   1.1.0

.. image:: https://github.com/avalentino/pyepr/actions/workflows/python-package.yml/badge.svg?branch=master
    :alt: CI status page
    :target: https://github.com/avalentino/pyepr/actions

.. image:: https://img.shields.io/pypi/v/pyepr
    :alt: Latest Version
    :target: https://pypi.org/project/pyepr

.. image:: https://img.shields.io/pypi/pyversions/pyepr
    :alt: Supported Python versions
    :target: https://pypi.org/project/pyepr

.. image:: https://img.shields.io/pypi/l/pyepr
    :alt: License
    :target: https://pypi.org/project/pyepr

.. image:: https://img.shields.io/pypi/wheel/pyepr
    :alt: Wheel Status
    :target: https://pypi.org/project/pyepr

.. image:: https://readthedocs.org/projects/pyepr/badge
    :alt: Documentation Status
    :target: https://pyepr.readthedocs.io/en/latest

.. image:: https://codecov.io/gh/avalentino/pyepr/branch/master/graph/badge.svg
    :alt: Coverage Status
    :target: https://codecov.io/gh/avalentino/pyepr


Introduction
============

PyEPR_ provides Python_ bindings for the ENVISAT Product Reader C API
(`EPR API`_) for reading satellite data from ENVISAT_ ESA_ (European
Space Agency) mission.

PyEPR_, as well as the `EPR API`_ for C, supports ENVISAT_ MERIS, AATSR
Level 1B and Level 2 and also ASAR data products. It provides access to
the data either on a geophysical (decoded, ready-to-use pixel samples)
or on a raw data layer. The raw data access makes it possible to read
any data field contained in a product file.

.. _PyEPR: https://github.com/avalentino/pyepr
.. _Python: https://www.python.org
.. _`EPR API`: https://github.com/bcdev/epr-api
.. _ENVISAT: https://envisat.esa.int
.. _ESA: https://earth.esa.int


Requirements
============

In order to use PyEPR it is needed that the following software are
correctly installed and configured:

* Python3_ >= 3.5 (including PyPy3_)
* numpy_ >= 1.7.0
* `EPR API`_ >= 2.2 (optional, since PyEPR 0.7 the source tar-ball comes
  with a copy of the EPR C API sources)
* a reasonably updated C compiler (build only)
* Cython_ >= 0.29 (build only)

.. _Python3: Python_
.. _PyPy3: https://www.pypy.org
.. _numpy: https://numpy.org
.. _gcc: https://gcc.gnu.org
.. _Cython: https://cython.org


Download
========

Official source tar-balls can be downloaded form PyPi_:

    https://pypi.org/project/pyepr

The source code of the development versions is available on the GitHub_
project page

    https://github.com/avalentino/pyepr

To clone the git_ repository the following command can be used::

    $ git clone https://github.com/avalentino/pyepr.git

To get also the EPR C API source code, the following commands are necessary::

    $ cd pyepr
    $ git submodule init
    Submodule 'extern/epr-api' (https://github.com/avalentino/epr-api.git) registered for path 'extern/epr-api'
    $ git submodule update
    Cloning into '/Users/antonio valentino/projects/av/pyepr/extern/epr-api'...
    Submodule path 'extern/epr-api': checked out '93c1f1efce26c64d508fe882d5c72a898a068f29'

.. _PyPi: https://pypi.org
.. _GitHub: https://github.com
.. _git: https://git-scm.com


Installation
============

The easier way to install PyEPR_ is using tools like pip_::

    $ python3 -m pip install pyepr

or::

    $ python3 -m pip install -U --prefix=<TARGET DIRECTORY>

PyEPR_ can be installed from the source tar-ball using the following
command::

    $ python3 setup.py install

To install PyEPR_ in a non-standard path::

    $ python3 setup.py install --prefix=<TARGET_PATH>

.. _pip: https://pypi.python.org/pypi/pip


License
=======

Copyright (C) 2011-2021 Antonio Valentino <antonio.valentino@tiscali.it>

PyEPR is free software: you can redistribute it and/or modify
it under the terms of the `GNU General Public License`_ as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PyEPR is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with PyEPR.  If not, see <http://www.gnu.org/licenses/>.

.. _`GNU General Public License`: http://www.gnu.org/licenses/gpl-3.0.html
