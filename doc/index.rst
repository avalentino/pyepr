=================================
ENVISAT Product Reader Python API
=================================

.. raw:: latex

    \listoffigures
    % \listoftables
    \clearpage


:HomePage:  https://avalentino.github.io/pyepr
:Author:    Antonio Valentino
:Contact:   antonio.valentino@tiscali.it
:Copyright: 2011-2021, Antonio Valentino
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
    .. _ENVISAT: https://envisat.esa.int
    .. _ESA: https://earth.esa.int

    .. index:: ENVISAT, MERIS, AASTR, ASAR


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

    Online documentation for other PyEpr_ versions:

    * `latest <https://pyepr.readthedocs.io/en/latest/>`_ development
    * `1.1.1 <https://pyepr.readthedocs.io/en/v1.1.1/>`_ (latest stable)
    * `1.1.0 <https://pyepr.readthedocs.io/en/v1.1.0/>`_
    * `1.0.1 <https://pyepr.readthedocs.io/en/v1.0.1/>`_
    * `1.0.0 <https://pyepr.readthedocs.io/en/v1.0.0/>`_
    * `0.9.5 <https://pyepr.readthedocs.io/en/v0.9.5/>`_
    * `0.8.2 <https://pyepr.readthedocs.io/en/v0.8.2/>`_
    * `0.7.1 <https://pyepr.readthedocs.io/en/v0.7.1/>`_
    * `0.6.1 <https://pyepr.readthedocs.io/en/v0.6.1/>`_


License
=======

.. index:: license

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
