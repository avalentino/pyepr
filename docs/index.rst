=================================
ENVISAT Product Reader Python API
=================================

.. raw:: latex

    \listoffigures
    % \listoftables
    \clearpage


:HomePage:  https://pyepr.readthedocs.io
:Author:    Antonio Valentino
:Contact:   antonio.valentino@tiscali.it
:Copyright: 2011-2026, Antonio Valentino
:Version:   |release|


.. only:: not latex

    Overview
    ========

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
    .. _ENVISAT: https://earth.esa.int/eogateway/missions/envisat
    .. _ESA: https://earth.esa.int

    .. index:: ENVISAT, MERIS, AASTR, ASAR


    Project Links
    =============

    * HTML documentation (`stable <https://pyepr.readthedocs.io/en/stable/>`_,
      `latest <https://pyepr.readthedocs.io/en/latest/>`_)
    * PyEPR_ project page on `github <https://github.com>`_
    * `source browser`__
    * `commit history <https://github.com/avalentino/pyepr/commits>`_
    * `issue tracker <https://github.com/avalentino/pyepr/issues>`_
    * `CI status page <https://github.com/avalentino/pyepr/actions>`_
    * `PyEPR project page on PyPi <http://pypi.python.org/pypi/pyepr>`_
    * EPR-API `project page <https://github.com/bcdev/epr-api>`_
    * EPR-API `documentation
      <https://rawgithub.com/bcdev/epr-api/master/docs/epr_c_api/index.html>`_

    __ PyEPR_


    Documentation
    =============

.. toctree::
   :maxdepth: 2

   usermanual
   tutorials
   reference
   NEWS


.. only:: not latex

    Other versions
    ==============

    Online documentation for other PyEPR_ versions:

    ============ ======================================================
    PyEPR latest https://pyepr.readthedocs.io/en/latest (development)
    PyEPR 1.1.5  https://pyepr.readthedocs.io/en/v1.2.0
    PyEPR 1.1.5  https://pyepr.readthedocs.io/en/v1.1.5
    PyEPR 1.1.4  https://pyepr.readthedocs.io/en/v1.1.4
    PyEPR 1.1.3  https://pyepr.readthedocs.io/en/v1.1.3
    PyEPR 1.1.2  https://pyepr.readthedocs.io/en/v1.1.2
    PyEPR 1.1.1  https://pyepr.readthedocs.io/en/v1.1.1
    PyEPR 1.1.0  https://pyepr.readthedocs.io/en/v1.1.0
    PyEPR 1.0.1  https://pyepr.readthedocs.io/en/v1.0.1
    PyEPR 1.0.0  https://pyepr.readthedocs.io/en/v1.0.0
    ============ ======================================================


License
=======

.. index:: license

Copyright (C) 2011-2026 Antonio Valentino <antonio.valentino@tiscali.it>

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
