# PyEPR - Python bindings for ENVISAT Product Reader API
#
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

"""Python bindings for ENVISAT Product Reader C API.

PyEPR_ provides Python_ bindings for the ENVISAT Product Reader C API
(`EPR API`_) for reading satellite data from ENVISAT_ ESA_ (European
Space Agency) mission.

PyEPR_ is fully object oriented and, as well as the `EPR API`_ for C,
supports ENVISAT_ MERIS, AATSR Level 1B and Level 2 and also ASAR data
products. It provides access to the data either on a geophysical
(decoded, ready-to-use pixel samples) or on a raw data layer.
The raw data access makes it possible to read any data field contained
in a product file.

.. _PyEPR: https://pyepr.readthedocs.io
.. _Python: https://www.python.org
.. _`EPR API`: https://github.com/bcdev/epr-api
.. _ENVISAT: http://envisat.esa.int
.. _ESA: http://earth.esa.int
"""

from ._epr import (
    Band,
    DSD,
    Dataset,
    EPRError,
    EPRTime,
    EPRValueError,
    EPR_C_API_VERSION,
    E_SMID_LIN,
    E_SMID_LOG,
    E_SMID_NON,
    E_SMOD_1OF1,
    E_SMOD_1OF2,
    E_SMOD_2OF2,
    E_SMOD_2TOF,
    E_SMOD_3TOI,
    E_TID_CHAR,
    E_TID_DOUBLE,
    E_TID_FLOAT,
    E_TID_INT,
    E_TID_SHORT,
    E_TID_SPARE,
    E_TID_STRING,
    E_TID_TIME,
    E_TID_UCHAR,
    E_TID_UINT,
    E_TID_UNKNOWN,
    E_TID_USHORT,
    EprObject,
    Field,
    MJD,
    Product,
    Raster,
    Record,
    create_bitmask_raster,
    create_raster,
    data_type_id_to_str,
    get_data_type_size,
    get_numpy_dtype,
    get_sample_model_name,
    get_scaling_method_name,
    open,
)

__version__ = "1.2.0.dev0"
