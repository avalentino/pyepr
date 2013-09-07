# -*- coding: utf-8 -*-

# PyEPR - Python bindings for ENVISAT Product Reader API
#
# Copyright (C) 2011-2013, Antonio Valentino <antonio.valentino@tiscali.it>
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


'''Python bindings for ENVISAT Product Reader C API

PyEPR_ provides Python_ bindings for the ENVISAT Product Reader C API
(`EPR API`_) for reading satellite data from ENVISAT_ ESA_ (European
Space Agency) mission.

PyEPR_ is fully object oriented and, as well as the `EPR API`_ for C,
supports ENVISAT_ MERIS, AATSR Level 1B and Level 2 and also ASAR data
products. It provides access to the data either on a geophysical
(decoded, ready-to-use pixel samples) or on a raw data layer.
The raw data access makes it possible to read any data field contained
in a product file.

.. _PyEPR: http://avalentino.github.com/pyepr
.. _Python: http://www.python.org
.. _`EPR API`: https://github.com/bcdev/epr-api
.. _ENVISAT: http://envisat.esa.int
.. _ESA: http://earth.esa.int

'''

__version__ = '0.8.1'
__revision__ = __version__  # deprecated


cdef extern from *:
    ctypedef char const_char 'const char'
    ctypedef void const_void 'const void'


from libc cimport string as cstring
from libc cimport stdio
from libc.stdio cimport FILE


cdef extern from 'stdio.h' nogil:
    FILE* fdopen(int, char *mode)


cdef extern from 'epr_api.h' nogil:
    char* EPR_PRODUCT_API_VERSION_STR

    ctypedef int            epr_boolean
    ctypedef unsigned char  uchar
    ctypedef unsigned short ushort
    ctypedef unsigned int   uint
    ctypedef unsigned long  ulong

    enum EPR_ErrCode:
        e_err_none = 0
        e_err_null_pointer = 1
        e_err_illegal_arg = 2
        e_err_illegal_state = 3
        e_err_out_of_memory = 4
        e_err_index_out_of_range = 5
        e_err_illegal_conversion = 6
        e_err_illegal_data_type = 7
        e_err_file_not_found = 101
        e_err_file_access_denied = 102
        e_err_file_read_error = 103
        e_err_file_write_error = 104
        e_err_file_open_failed = 105
        e_err_file_close_failed = 106
        e_err_api_not_initialized = 201
        e_err_invalid_product_id = 203
        e_err_invalid_record = 204
        e_err_invalid_band = 205
        e_err_invalid_raster = 206
        e_err_invalid_dataset_name = 207
        e_err_invalid_field_name = 208
        e_err_invalid_record_name = 209
        e_err_invalid_product_name = 210
        e_err_invalid_band_name = 211
        e_err_invalid_data_format = 212
        e_err_invalid_value = 213
        e_err_invalid_keyword_name = 214
        e_err_unknown_endian_order = 216
        e_err_flag_not_found = 301
        e_err_invalid_ddbb_format = 402

    enum EPR_DataTypeId:
        e_tid_unknown = 0
        e_tid_uchar = 1
        e_tid_char = 2
        e_tid_ushort = 3
        e_tid_short = 4
        e_tid_uint = 5
        e_tid_int = 6
        e_tid_float = 7
        e_tid_double = 8
        e_tid_string = 11
        e_tid_spare = 13
        e_tid_time = 21

    enum EPR_LogLevel:
        e_log_debug = -1
        e_log_info = 0
        e_log_warning = 1
        e_log_error = 2

    enum EPR_SampleModel:
        e_smod_1OF1 = 0
        e_smod_1OF2 = 1
        e_smod_2OF2 = 2
        e_smod_3TOI = 3
        e_smod_2TOF = 4

    enum EPR_ScalingMethod:
        e_smid_non = 0
        e_smid_lin = 1
        e_smid_log = 2

    struct EPR_Time:
        int  days
        uint seconds
        uint microseconds

    struct EPR_FlagDef:
        #EPR_Magic magic
        char* name
        uint bit_mask
        char* description

    struct EPR_Field:
        #EPR_Magic magic
        #EPR_FieldInfo* info
        void* elems

    struct EPR_Record:
        #EPR_Magic magic
        #EPR_RecordInfo* info
        uint num_fields
        EPR_Field** fields

    struct EPR_DSD:
        #EPR_Magic magic
        int index
        char* ds_name
        char* ds_type
        char* filename
        uint ds_offset
        uint ds_size
        uint num_dsr
        uint dsr_size

    struct EPR_Raster:
        #EPR_Magic magic
        EPR_DataTypeId data_type
        uint elem_size
        uint source_width
        uint source_height
        uint source_step_x
        uint source_step_y
        uint raster_width
        uint raster_height
        void* buffer

    struct EPR_ProductId:
        #EPR_Magic magic
        char* file_path
        FILE* istream
        uint  tot_size
        uint  scene_width
        uint  scene_height
        char* id_string
        EPR_Record* mph_record
        EPR_Record* sph_record
        #EPR_PtrArray* dsd_array
        #EPR_PtrArray* record_info_cache
        #EPR_PtrArray* param_table
        #EPR_PtrArray* dataset_ids
        #EPR_PtrArray* band_ids
        int meris_iodd_version

    struct EPR_DatasetId:
        #EPR_Magic magic
        EPR_ProductId* product_id
        char* dsd_name
        EPR_DSD* dsd
        char* dataset_name
        #struct RecordDescriptor* record_descriptor
        #EPR_SRecordInfo* record_info
        char* description

    struct EPR_DatasetRef:
        EPR_DatasetId* dataset_id
        int field_index             # -1 if not used
        int elem_index              # -1 if not used

    struct EPR_BandId:
        #EPR_Magic magic
        EPR_ProductId* product_id
        char* band_name
        int spectr_band_index
        EPR_DatasetRef dataset_ref
        EPR_SampleModel sample_model
        EPR_DataTypeId data_type
        EPR_ScalingMethod scaling_method
        float scaling_offset
        float scaling_factor
        char* bm_expr
        #EPR_SPtrArray* flag_coding
        char* unit
        char* description
        epr_boolean lines_mirrored

    ctypedef EPR_ErrCode       EPR_EErrCode
    ctypedef EPR_LogLevel      EPR_ELogLevel
    ctypedef EPR_SampleModel   EPR_ESampleModel
    ctypedef EPR_ScalingMethod EPR_EScalingMethod
    ctypedef EPR_DataTypeId    EPR_EDataTypeId
    ctypedef EPR_ProductId     EPR_SProductId
    ctypedef EPR_DatasetId     EPR_SDatasetId
    ctypedef EPR_BandId        EPR_SBandId
    ctypedef EPR_Raster        EPR_SRaster
    ctypedef EPR_Record        EPR_SRecord
    ctypedef EPR_Field         EPR_SField
    ctypedef EPR_DSD           EPR_SDSD
    ctypedef EPR_Time          EPR_STime

    # @TODO: improve logging and error management (--> custom handlers)
    # logging and error handling function pointers
    ctypedef void (*EPR_FLogHandler)(EPR_ELogLevel, char*)
    ctypedef void (*EPR_FErrHandler)(EPR_EErrCode, char*)

    # logging
    int epr_set_log_level(EPR_ELogLevel)
    void epr_set_log_handler(EPR_FLogHandler)
    void epr_log_message(EPR_ELogLevel, char*)

    # error handling
    void epr_set_err_handler(EPR_FErrHandler)
    EPR_EErrCode epr_get_last_err_code()
    const_char* epr_get_last_err_message()
    void epr_clear_err()

    # API initialization/finalization
    int epr_init_api(EPR_ELogLevel, EPR_FLogHandler, EPR_FErrHandler)
    void epr_close_api()

    # DATATYPE
    uint epr_get_data_type_size(EPR_EDataTypeId)
    const_char* epr_data_type_id_to_str(EPR_EDataTypeId)

    # open products
    EPR_SProductId* epr_open_product(char*)

    # PRODUCT
    int epr_close_product(EPR_SProductId*)
    uint epr_get_scene_width(EPR_SProductId*)
    uint epr_get_scene_height(EPR_SProductId*)
    uint epr_get_num_datasets(EPR_SProductId*)
    EPR_SDatasetId* epr_get_dataset_id_at(EPR_SProductId*, uint)
    EPR_SDatasetId* epr_get_dataset_id(EPR_SProductId*, char*)
    uint epr_get_num_dsds(EPR_SProductId*)
    EPR_SDSD* epr_get_dsd_at(EPR_SProductId*, uint)
    EPR_SRecord* epr_get_mph(EPR_SProductId*)
    EPR_SRecord* epr_get_sph(EPR_SProductId*)

    uint epr_get_num_bands(EPR_SProductId*)
    EPR_SBandId* epr_get_band_id_at(EPR_SProductId*, uint)
    EPR_SBandId* epr_get_band_id(EPR_SProductId*, char*)
    int epr_read_bitmask_raster(EPR_SProductId*, char*, int, int, EPR_SRaster*)

    # DATASET
    const_char* epr_get_dataset_name(EPR_SDatasetId*)
    const_char* epr_get_dsd_name(EPR_SDatasetId*)
    uint epr_get_num_records(EPR_SDatasetId*)
    EPR_SDSD* epr_get_dsd(EPR_SDatasetId*)
    EPR_SRecord* epr_create_record(EPR_SDatasetId*)
    EPR_SRecord* epr_read_record(EPR_SDatasetId*, uint, EPR_SRecord*)

    # RECORD
    void epr_free_record(EPR_SRecord*)
    uint epr_get_num_fields(EPR_SRecord*)
    void epr_print_record(EPR_SRecord*, FILE*)
    void epr_print_element(EPR_SRecord*, uint, uint, FILE*)
    void epr_dump_record(EPR_SRecord*)
    void epr_dump_element(EPR_SRecord*, uint, uint)
    EPR_SField* epr_get_field(EPR_SRecord*, char*)
    EPR_SField* epr_get_field_at(EPR_SRecord*, uint)

    # FIELD
    void epr_print_field(EPR_SField*, FILE*)
    void epr_dump_field(EPR_SField*)

    const_char* epr_get_field_unit(EPR_SField*)
    const_char* epr_get_field_description(EPR_SField*)
    uint epr_get_field_num_elems(EPR_SField*)
    const_char* epr_get_field_name(EPR_SField*)
    EPR_EDataTypeId epr_get_field_type(EPR_SField*)

    char epr_get_field_elem_as_char(EPR_SField*, uint)
    uchar epr_get_field_elem_as_uchar(EPR_SField*, uint)
    short epr_get_field_elem_as_short(EPR_SField*, uint)
    ushort epr_get_field_elem_as_ushort(EPR_SField*, uint)
    int epr_get_field_elem_as_int(EPR_SField*, uint)
    uint epr_get_field_elem_as_uint(EPR_SField*, uint)
    float epr_get_field_elem_as_float(EPR_SField*, uint)
    double epr_get_field_elem_as_double(EPR_SField*, uint)
    const_char* epr_get_field_elem_as_str(EPR_SField*)
    EPR_STime* epr_get_field_elem_as_mjd(EPR_SField*)

    const_char* epr_get_field_elems_char(EPR_SField*)
    uchar* epr_get_field_elems_uchar(EPR_SField*)
    short* epr_get_field_elems_short(EPR_SField*)
    ushort* epr_get_field_elems_ushort(EPR_SField*)
    int* epr_get_field_elems_int(EPR_SField*)
    uint* epr_get_field_elems_uint(EPR_SField*)
    float* epr_get_field_elems_float(EPR_SField*)
    double* epr_get_field_elems_double(EPR_SField*)

    uint epr_copy_field_elems_as_ints(EPR_SField*, int*, uint)
    uint epr_copy_field_elems_as_uints(EPR_SField*, uint*, uint)
    uint epr_copy_field_elems_as_floats(EPR_SField*, float*, uint)
    uint epr_copy_field_elems_as_doubles(EPR_SField*, double*, uint)

    # BAND
    const_char* epr_get_band_name(EPR_SBandId*)
    EPR_SRaster* epr_create_compatible_raster(EPR_SBandId*, uint, uint, uint,
                                              uint)
    int epr_read_band_raster(EPR_SBandId*, int, int, EPR_SRaster*)

    # RASTER
    void epr_free_raster(EPR_SRaster*)
    uint epr_get_raster_width(EPR_SRaster*)
    uint epr_get_raster_height(EPR_SRaster*)
    uint epr_get_raster_elem_size(EPR_SRaster*)

    uint epr_get_pixel_as_uint(EPR_SRaster*, int, int)
    int epr_get_pixel_as_int(EPR_SRaster*, int, int)
    float epr_get_pixel_as_float(EPR_SRaster*, int, int)
    double epr_get_pixel_as_double(EPR_SRaster*, int, int)

    void* epr_get_raster_elem_addr(EPR_SRaster*, uint)
    void* epr_get_raster_pixel_addr(EPR_SRaster*, uint, uint)
    void* epr_get_raster_line_addr(EPR_SRaster*, uint)

    EPR_SRaster* epr_create_raster(EPR_EDataTypeId, uint, uint, uint, uint)
    EPR_SRaster* epr_create_bitmask_raster(uint, uint, uint, uint)


from cpython.version cimport PY_MAJOR_VERSION
from cpython.object cimport PyObject_AsFileDescriptor
cimport numpy as np
np.import_array()

import sys
from collections import namedtuple

import numpy as np

cdef int PY3 = (PY_MAJOR_VERSION >= 3)

# internal utils
_DEFAULT_FS_ENCODING = sys.getfilesystemencoding()


cdef inline bytes _to_bytes(s, encoding='UTF-8'):
    if hasattr(s, 'encode'):
        return s.encode(encoding)
    else:
        return s


cdef inline str _to_str(b, encoding='UTF-8'):
    if PY3:
        return b.decode(encoding)
    else:
        return b


# utils
EPRTime = namedtuple('EPRTime', ('days', 'seconds', 'microseconds'))

EPR_C_API_VERSION = _to_str(EPR_PRODUCT_API_VERSION_STR, 'ascii')

# EPR_DataTypeId
E_TID_UNKNOWN = e_tid_unknown
E_TID_UCHAR = e_tid_uchar
E_TID_CHAR = e_tid_char
E_TID_USHORT = e_tid_ushort
E_TID_SHORT = e_tid_short
E_TID_UINT = e_tid_uint
E_TID_INT = e_tid_int
E_TID_FLOAT = e_tid_float
E_TID_DOUBLE = e_tid_double
E_TID_STRING = e_tid_string
E_TID_SPARE = e_tid_spare
E_TID_TIME = e_tid_time

# EPR_SampleModel
E_SMOD_1OF1 = e_smod_1OF1
E_SMOD_1OF2 = e_smod_1OF2
E_SMOD_2OF2 = e_smod_2OF2
E_SMOD_3TOI = e_smod_3TOI
E_SMOD_2TOF = e_smod_2TOF

# EPR_ScalingMethod
E_SMID_NON = e_smid_non
E_SMID_LIN = e_smid_lin
E_SMID_LOG = e_smid_log


cdef np.NPY_TYPES _epr_to_numpy_type_id(EPR_DataTypeId epr_type):
    if epr_type == E_TID_UCHAR:
        return np.NPY_UBYTE
    if epr_type == E_TID_CHAR:
        return np.NPY_BYTE
    if epr_type == E_TID_USHORT:
        return np.NPY_USHORT
    if epr_type == E_TID_SHORT:
        return np.NPY_SHORT
    if epr_type == E_TID_UINT:
        return np.NPY_UINT
    if epr_type == E_TID_INT:
        return np.NPY_INT
    if epr_type == E_TID_FLOAT:
        return np.NPY_FLOAT
    if epr_type == E_TID_DOUBLE:
        return np.NPY_DOUBLE
    if epr_type == E_TID_STRING:
        return np.NPY_STRING

    return np.NPY_NOTYPE


class EPRError(Exception):
    '''EPR API error'''

    def __init__(self, message='', code=None, *args, **kargs):
        '''__init__(self, message='', code=None, *args, **kargs)'''

        super(EPRError, self).__init__(message, code, *args, **kargs)

        #: EPR API error code
        self.code = code


class EPRValueError(EPRError, ValueError):
    pass


cdef pyepr_check_errors():
    cdef int code
    cdef str msg
    code = epr_get_last_err_code()
    if code != e_err_none:
        msg = _to_str(<char*>epr_get_last_err_message(), 'ascii')
        epr_clear_err()

        # @TODO: if not msg: msg = EPR_ERR_MSG[code]
        if (e_err_invalid_product_id <= code <= e_err_invalid_keyword_name or
            code in (e_err_null_pointer,
                     e_err_illegal_arg,
                     e_err_index_out_of_range)):
            raise EPRValueError(msg, code)
        else:
            raise EPRError(msg, code)


cdef pyepr_null_ptr_error(msg='null pointer'):
    cdef int code
    cdef str eprmsg = _to_str(<char*>epr_get_last_err_message(), 'ascii')

    code = epr_get_last_err_code()
    if not code:
        code = None

    epr_clear_err()

    raise EPRValueError('%s: %s' % (msg, eprmsg), code=code)


cdef FILE* pyepr_get_file_stream(object ostream) except NULL:
    cdef FILE* fstream = NULL
    cdef int fileno

    if ostream is None:
        ostream = sys.stdout

    try:
        ostream.flush()
    except AttributeError, e:
        raise TypeError(str(e))
    else:
        fileno = PyObject_AsFileDescriptor(ostream)
        if fileno == -1:
            raise TypeError('bad output stream')
        else:
            fstream = fdopen(fileno, 'w')
            if fstream is NULL:
                raise TypeError('invalid ostream')

    return fstream


cdef class _CLib:
    '''Library object to handle C API initialization/finalization

    .. warning:: this is meant for internal use only. **Do not use it**.

    '''

    def __cinit__(self, *args, **kwargs):
        cdef bytes msg

        # @TODO:check
        #if EPR_C_API_VERSION != '2.2':
        #    raise ImportError('C library version not supported: "%s"' %
        #                                                    EPR_C_API_VERSION)

        #if epr_init_api(e_log_warning, epr_log_message, NULL):
        if epr_init_api(e_log_warning, NULL, NULL):
            msg = <char*>epr_get_last_err_message()
            epr_clear_err()
            raise ImportError('unable to inizialize EPR API library: '
                              '%s' % _to_str(msg, 'ascii'))

    def __dealloc__(self):
        epr_close_api()

    def __init__(self):
        raise TypeError('"%s" class cannot be instantiated from Python' %
                                                    self.__class__.__name__)


# global _CLib instance
cdef _CLib _EPR_C_LIB = None


cdef class EprObject:
    cdef object epr_c_lib

    def __cinit__(self, *ars, **kargs):
        self.epr_c_lib = _EPR_C_LIB

    def __dealloc__(self):
        self.epr_c_lib = None

    def __init__(self):
        raise TypeError('"%s" class cannot be instantiated from Python' %
                                                    self.__class__.__name__)


def get_data_type_size(EPR_EDataTypeId type_id):
    '''get_data_type_size(type_id)

    Gets the size in bytes for an element of the given data type

    '''

    return epr_get_data_type_size(type_id)


def data_type_id_to_str(EPR_EDataTypeId type_id):
    '''data_type_id_to_str(type_id)

    Gets the 'C' data type string for the given data type

    '''

    cdef char* type_id_str = <char*>epr_data_type_id_to_str(type_id)

    return _to_str(type_id_str, 'ascii')


def get_scaling_method_name(method):
    '''get_scaling_method_name(method)

    Return the name of the specified scaling method

    '''

    mmap = {
        E_SMID_NON: 'NONE',
        E_SMID_LIN: 'LIN',
        E_SMID_LOG: 'LOG',
    }

    try:
        return mmap[method]
    except KeyError:
        raise ValueError('invalid scaling method: "%s"' % method)


def get_sample_model_name(model):
    '''get_sample_model_name(model)

    Return the name of the specified sample model

    '''

    mmap = {
        E_SMOD_1OF1: '1OF1',
        E_SMOD_1OF2: '1OF2',
        E_SMOD_2OF2: '2OF2',
        E_SMOD_3TOI: '3TOI',
        E_SMOD_2TOF: '2TOF',
    }

    try:
        return mmap[model]
    except KeyError:
        raise ValueError('invalid sample model: "%s"' % model)


cdef class DSD(EprObject):
    '''Dataset descriptor

    The DSD class contains information about the properties of a
    dataset and its location within an ENVISAT product file

    '''

    cdef EPR_SDSD* _ptr
    cdef object _parent     # Dataset or Product

    cdef inline check_closed_product(self):
        if isinstance(self, Dataset):
            (<Dataset>self._parent).check_closed_product()
        else:
            #elif isinstance(self, Product):
            (<Product>self._parent).check_closed_product()

    property index:
        '''The index of this DSD (zero-based)'''

        def __get__(self):
            self.check_closed_product()
            return self._ptr.index

    property ds_name:
        '''The dataset name'''

        def __get__(self):
            self.check_closed_product()
            return _to_str(self._ptr.ds_name, 'ascii')

    property ds_type:
        '''The dataset type descriptor'''

        def __get__(self):
            self.check_closed_product()
            return _to_str(self._ptr.ds_type, 'ascii')

    property filename:
        '''The filename in the DDDB with the description of this dataset'''

        def __get__(self):
            self.check_closed_product()
            return _to_str(self._ptr.filename, 'ascii')

    property ds_offset:
        '''The offset of dataset-information the product file'''

        def __get__(self):
            self.check_closed_product()
            return self._ptr.ds_offset

    property ds_size:
        '''The size of dataset-information in dataset product file'''

        def __get__(self):
            self.check_closed_product()
            return self._ptr.ds_size

    property num_dsr:
        '''The number of dataset records for the given dataset name'''

        def __get__(self):
            self.check_closed_product()
            return self._ptr.num_dsr

    property dsr_size:
        '''The size of dataset record for the given dataset name'''

        def __get__(self):
            self.check_closed_product()
            return self._ptr.dsr_size

    # --- high level interface ------------------------------------------------
    def __repr__(self):
        return 'epr.DSD("%s")' % self.ds_name

    def __richcmp__(self, other, int op):
        cdef EPR_SDSD* p1 = (<DSD>self)._ptr
        cdef EPR_SDSD* p2 = (<DSD>other)._ptr

        if isinstance(self, DSD) and isinstance(other, DSD):
            if op == 2:         # eq
                if p1 == p2:
                    return True

                (<DSD>self).check_closed_product()

                return ((p1.index == p2.index) and
                        (p1.ds_offset == p2.ds_offset) and
                        (p1.ds_size == p2.ds_size) and
                        (p1.num_dsr == p2.num_dsr) and
                        (p1.dsr_size == p2.dsr_size)and
                        (cstring.strcmp(p1.ds_name, p2.ds_name) == 0) and
                        (cstring.strcmp(p1.ds_type, p2.ds_type) == 0) and
                        (cstring.strcmp(p1.filename, p2.filename) == 0))

            elif op == 3:       # ne
                if p1 == p2:
                    return False

                (<DSD>self).check_closed_product()

                return ((p1.index != p2.index) or
                        (p1.ds_offset != p2.ds_offset) or
                        (p1.ds_size != p2.ds_size) or
                        (p1.num_dsr != p2.num_dsr) or
                        (p1.dsr_size != p2.dsr_size) or
                        (cstring.strcmp(p1.ds_name, p2.ds_name) != 0) or
                        (cstring.strcmp(p1.ds_type, p2.ds_type) != 0) or
                        (cstring.strcmp(p1.filename, p2.filename) != 0))

            else:
                raise TypeError('DSD only implements "==" and "!=" operators')
        else:
            return NotImplemented


cdef new_dsd(EPR_SDSD* ptr, object parent=None):
    if ptr is NULL:
        pyepr_null_ptr_error()

    cdef DSD instance = DSD.__new__(DSD)

    instance._ptr = ptr
    instance._parent = parent   # Dataset or Product

    return instance


cdef class Field(EprObject):
    '''Represents a field within a record

    A field is composed of one or more data elements of one of the
    types defined in the internal ``field_info`` structure.

    .. seealso:: :class:`Record`

    '''

    cdef EPR_SField* _ptr
    cdef Record _parent

    cdef inline check_closed_product(self):
        self._parent.check_closed_product()

    def print_(self, ostream=None):
        '''print_(self, ostream=None)

        Write the field to specified file (default: :data:`sys.stdout`)

        This method writes formatted contents of the field to
        specified *ostream* text file or (default) the ASCII output
        is be printed to standard output (:data:`sys.stdout`)

        :param ostream:
            the (opened) output file object

        .. note:: the *ostream* parameter have to be a *real* file not
                  a generic stream object like
                  :class:`StringIO.StringIO` instances

        '''

        cdef FILE* fstream = pyepr_get_file_stream(ostream)

        self.check_closed_product()

        with nogil:
            epr_print_field(self._ptr, fstream)
            stdio.fflush(fstream)

        pyepr_check_errors()

    #def dump_field(self):
    #    epr_dump_field(self._ptr)
    #    pyepr_check_errors()

    def get_unit(self):
        '''get_unit(self)

        Gets the unit of the field

        '''

        cdef const_char* unit = NULL

        self.check_closed_product()

        unit = epr_get_field_unit(self._ptr)

        if unit is NULL:
            return ''
        else:
            return _to_str(<char*>unit, 'ascii')

    def get_description(self):
        '''get_description(self)

        Gets the description of the field

        '''

        cdef char* description = NULL

        self.check_closed_product()

        description = <char*>epr_get_field_description(self._ptr)

        return _to_str(description, 'ascii')

    def get_num_elems(self):
        '''get_num_elems(self)

        Gets the number of elements of the field

        '''

        self.check_closed_product()

        return epr_get_field_num_elems(self._ptr)

    def get_name(self):
        '''get_name(self)

        Gets the name of the field

        '''

        cdef char* name = NULL

        self.check_closed_product()

        name = <char*>epr_get_field_name(self._ptr)

        return _to_str(name, 'ascii')

    def get_type(self):
        '''get_type(self)

        Gets the type of the field

        '''

        self.check_closed_product()

        return epr_get_field_type(self._ptr)

    def get_elem(self, uint index=0):
        '''get_elem(self, index=0)

        Field single element access

        This function is for getting the elements of a field.

        :param index:
            the zero-based index of element to be returned, must not be
            negative
        :returns:
            the typed value from given field

        '''

        cdef EPR_STime* eprtime

        self.check_closed_product()

        etype = epr_get_field_type(self._ptr)

        if etype == e_tid_uchar:
            val = epr_get_field_elem_as_uchar(self._ptr, index)
        elif etype == e_tid_char:
            val = epr_get_field_elem_as_char(self._ptr, index)
        elif etype == e_tid_ushort:
            val = epr_get_field_elem_as_ushort(self._ptr, index)
        elif etype == e_tid_short:
            val = epr_get_field_elem_as_short(self._ptr, index)
        elif etype == e_tid_uint:
            val = epr_get_field_elem_as_uint(self._ptr, index)
        elif etype == e_tid_int:
            val = epr_get_field_elem_as_int(self._ptr, index)
        elif etype == e_tid_float:
            val = epr_get_field_elem_as_float(self._ptr, index)
        elif etype == e_tid_double:
            val = epr_get_field_elem_as_double(self._ptr, index)
        elif etype == e_tid_string:
            if index != 0:
                raise ValueError('invalid index: %d' % index)
            val = <char*>epr_get_field_elem_as_str(self._ptr)
        #elif etype == e_tid_spare:
        #    val = epr_get_field_elem_as_str(self._ptr)
        elif etype == e_tid_time:
            if index != 0:
                raise ValueError('invalid index: %d' % index)

            # use casting to silence warnings
            eprtime = <EPR_STime*>epr_get_field_elem_as_mjd(self._ptr)
            val = EPRTime(eprtime.days, eprtime.seconds, eprtime.microseconds)
        else:
            raise ValueError('invalid field type')

        pyepr_check_errors()
        return val

    def get_elems(self):
        '''get_elems(self)

        Field array element access

        This function is for getting an array of field elements of the
        field.

        :returns:
            the data array (:class:`numpy.ndarray`) having the type of
            the field

        '''

        # @NOTE: internal C const pointer is not shared with numpy
        cdef const_void* buf
        cdef size_t num_elems
        cdef size_t i
        cdef np.ndarray out

        self.check_closed_product()

        num_elems = epr_get_field_num_elems(self._ptr)
        etype = epr_get_field_type(self._ptr)
        msg = 'Filed("%s") elems pointer is null' % self.get_name()

        if etype == e_tid_uchar:
            buf = <uchar*>epr_get_field_elems_uchar(self._ptr)
            if buf is NULL:
                pyepr_null_ptr_error(msg)
            out = np.ndarray(num_elems, np.byte)
            for i in range(num_elems):
                out[i] = (<uchar*>buf)[i]
        elif etype == e_tid_char:
            buf = <char*>epr_get_field_elems_char(self._ptr)
            if buf is NULL:
                pyepr_null_ptr_error(msg)
            out = np.ndarray(num_elems, np.byte)
            for i in range(num_elems):
                out[i] = (<char*>buf)[i]
        elif etype == e_tid_ushort:
            buf = <ushort*>epr_get_field_elems_ushort(self._ptr)
            if buf is NULL:
                pyepr_null_ptr_error(msg)
            out = np.ndarray(num_elems, np.ushort)
            for i in range(num_elems):
                out[i] = (<ushort*>buf)[i]
        elif etype == e_tid_short:
            buf = <short*>epr_get_field_elems_short(self._ptr)
            if buf is NULL:
                pyepr_null_ptr_error(msg)
            out = np.ndarray(num_elems, np.short)
            for i in range(num_elems):
                out[i] = (<short*>buf)[i]
        elif etype == e_tid_uint:
            buf = <uint*>epr_get_field_elems_uint(self._ptr)
            if buf is NULL:
                pyepr_null_ptr_error(msg)
            out = np.ndarray(num_elems, np.uint)
            for i in range(num_elems):
                out[i] = (<uint*>buf)[i]
        elif etype == e_tid_int:
            buf = <int*>epr_get_field_elems_int(self._ptr)
            if buf is NULL:
                pyepr_null_ptr_error(msg)
            out = np.ndarray(num_elems, np.int)
            for i in range(num_elems):
                out[i] = (<int*>buf)[i]
        elif etype == e_tid_float:
            buf = <float*>epr_get_field_elems_float(self._ptr)
            if buf is NULL:
                pyepr_null_ptr_error(msg)
            out = np.ndarray(num_elems, np.float32)
            for i in range(num_elems):
                out[i] = (<float*>buf)[i]
        elif etype == e_tid_double:
            buf = <double*>epr_get_field_elems_double(self._ptr)
            if buf is NULL:
                pyepr_null_ptr_error(msg)
            out = np.ndarray(num_elems, np.double)
            for i in range(num_elems):
                out[i] = (<double*>buf)[i]
        else:
            raise ValueError('invalid field type')

        return out

    # --- high level interface ------------------------------------------------
    def __repr__(self):
        return 'epr.Field("%s") %d %s elements' % (self.get_name(),
                    self.get_num_elems(), data_type_id_to_str(self.get_type()))

    def __str__(self):
        cdef EPR_DataTypeId type_ = self.get_type()
        if type_ == e_tid_string:
            return '%s = "%s"' % (self.get_name(), self.get_elem())
        elif type_ == e_tid_time:
            days, seconds, microseconds = self.get_elem()
            return '%s = {d=%d, j=%d, m=%d}' % (self.get_name(),
                                                days, seconds, microseconds)
        else:
            if type_ == e_tid_uchar:
                fmt = '%u'
            elif type_ == e_tid_char:
                fmt = '%d'
            elif type_ == e_tid_ushort:
                fmt = '%u'
            elif type_ == e_tid_short:
                fmt = '%d'
            elif type_ == e_tid_uint:
                fmt = '%u'
            elif type_ == e_tid_int:
                fmt = '%d'
            elif type_ == e_tid_float:
                fmt = '%f'
            elif type_ == e_tid_double:
                fmt = '%f'
            else:
                if self.get_num_elems() > 1:
                    data = ['<<unknown data type>>'] * self.get_elems()
                    data = ', '.join(data)
                    return '%s = {%s}' % (self.get_name(), data)
                else:
                    return '%s = <<unknown data type>>' % (self.get_name())

            if self.get_num_elems() > 1:
                data = ', '.join([fmt % item for item in self.get_elems()])
                return '%s = {%s}' % (self.get_name(), data)
            else:
                return '%s = %s' % (self.get_name(), fmt % self.get_elem())

    def __richcmp__(self, other, int op):
        cdef int ret
        cdef size_t n
        cdef EPR_SField* p1 = (<Field>self)._ptr
        cdef EPR_SField* p2 = (<Field>other)._ptr

        if isinstance(self, Field) and isinstance(other, Field):
            if op == 2:         # eq
                if p1 == p2:
                    return True

                (<Field>self).check_closed_product()

                if ((epr_get_field_num_elems(p1) !=
                            epr_get_field_num_elems(p2)) or

                    (epr_get_field_type(p1) != epr_get_field_type(p2)) or

                    (cstring.strcmp(epr_get_field_unit(p1),
                                    epr_get_field_unit(p2)) != 0) or

                    (cstring.strcmp(epr_get_field_description(p1),
                                    epr_get_field_description(p2)) != 0) or

                    (cstring.strcmp(epr_get_field_name(p1),
                                    epr_get_field_name(p2)) != 0)):

                    return False

                n = epr_get_data_type_size(epr_get_field_type(p1))
                if n != 0:
                    n *= epr_get_field_num_elems(p1)
                #pyepr_check_errors()
                if n <= 0:
                    # @TODO: check
                    return True

                return (cstring.memcmp(p1.elems, p2.elems, n) == 0)

            elif op == 3:       # ne
                if p1 == p2:
                    return False

                (<Field>self).check_closed_product()

                if ((epr_get_field_num_elems(p1) !=
                            epr_get_field_num_elems(p2)) or

                    (epr_get_field_type(p1) != epr_get_field_type(p2)) or

                    (cstring.strcmp(epr_get_field_unit(p1),
                                    epr_get_field_unit(p2)) != 0) or

                    (cstring.strcmp(epr_get_field_description(p1),
                                    epr_get_field_description(p2)) != 0) or

                    (cstring.strcmp(epr_get_field_name(p1),
                                    epr_get_field_name(p2)) != 0)):

                    return True

                n = epr_get_data_type_size(epr_get_field_type(p1))
                if n != 0:
                    n *= epr_get_field_num_elems(p1)
                #pyepr_check_errors()
                if n <= 0:
                    # @TODO: check
                    return False

                return (cstring.memcmp(p1.elems, p2.elems, n) != 0)

            else:
                raise TypeError('Field only implements "==" and '
                                '"!=" operators')
        else:
            return NotImplemented

    def __len__(self):
        self.check_closed_product()

        if epr_get_field_type(self._ptr) == e_tid_string:
            return cstring.strlen(epr_get_field_elem_as_str(self._ptr))
        else:
            return epr_get_field_num_elems(self._ptr)


cdef new_field(EPR_SField* ptr, Record parent=None):
    if ptr is NULL:
        pyepr_null_ptr_error()

    cdef Field instance = Field.__new__(Field)

    instance._ptr = ptr
    instance._parent = parent

    return instance


cdef class Record(EprObject):
    '''Represents a record read from an ENVISAT dataset

    A record is composed of multiple fields.

    .. seealso:: :class:`Field`

    '''

    cdef EPR_SRecord* _ptr
    cdef object _parent     # Dataset or Product
    cdef bint _dealloc

    def __dealloc__(self):
        if not self._dealloc:
            return

        if self._ptr is not NULL:
            epr_free_record(self._ptr)
            pyepr_check_errors()

    cdef inline check_closed_product(self):
        if isinstance(self._parent, Dataset):
            (<Dataset>self._parent).check_closed_product()
        else:
            #elif isinstance(self._parent, Product):
            (<Product>self._parent).check_closed_product()

    def get_num_fields(self):
        '''get_num_fields(self)

        Gets the number of fields contained in the record

        '''

        return epr_get_num_fields(self._ptr)

    def print_(self, ostream=None):
        '''print_(self, ostream=None)

        Write the record to specified file

        This method writes formatted contents of the record to
        specified *ostream* text file or (default) the ASCII output
        is be printed to standard output (:data:`sys.stdout`)

        :param ostream:
            the (opened) output file object

        .. note:: the *ostream* parameter have to be a *real* file not
                  a generic stream object like
                  :class:`StringIO.StringIO` instances

        '''

        cdef FILE* fstream = pyepr_get_file_stream(ostream)

        self.check_closed_product()

        with nogil:
            epr_print_record(self._ptr, fstream)
            stdio.fflush(fstream)

        pyepr_check_errors()

    def print_element(self, uint field_index, uint element_index,
                      ostream=None):
        '''print_element(self, field_index, element_index, ostream=None)

        Write the specified field element to file

        This method writes formatted contents of the specified field
        element to the *ostream* text file or (default) the ASCII output
        will be printed to standard output (:data:`sys.stdout`)

        :param field_index:
            the index of field in the record
        :param element_index:
            the index of element in the specified field
        :param ostream:
            the (opened) output file object

        .. note:: the *ostream* parameter have to be a *real* file not
                  a generic stream object like
                  :class:`StringIO.StringIO` instances

        '''

        cdef FILE* fstream = pyepr_get_file_stream(ostream)

        self.check_closed_product()

        with nogil:
            epr_print_element(self._ptr, field_index, element_index, fstream)
            stdio.fflush(fstream)

        pyepr_check_errors()

    def get_field(self, name):
        '''get_field(self, name)

        Gets a field specified by name

        The field is here identified through the given name.
        It contains the field info and all corresponding values.

        :param name:
            the the name of required field
        :returns:
            the specified :class:`Field` or raises an exception
            (:exc:`EPRValueError`) if an error occurred

        '''

        cdef EPR_SField* field_ptr
        cdef bytes cname = _to_bytes(name)

        self.check_closed_product()

        field_ptr = <EPR_SField*>epr_get_field(self._ptr, cname)
        if field_ptr is NULL:
            pyepr_null_ptr_error('unable to get field "%s"' % name)

        return new_field(field_ptr, self)

    def get_field_at(self, uint index):
        '''get_field_at(self, index)

        Gets a field at the specified position within the record

        :param index:
            the zero-based index (position within record) of the field
        :returns:
            the field or raises and exception (:exc:`EPRValueError`)
            if an error occurred

        '''

        cdef EPR_SField* field_ptr

        self.check_closed_product()

        field_ptr = <EPR_SField*>epr_get_field_at(self._ptr, index)
        if field_ptr is NULL:
            pyepr_null_ptr_error('unable to get field at index %d' % index)

        return new_field(field_ptr, self)

    # --- high level interface ------------------------------------------------
    def get_field_names(self):
        '''get_field_names(self)

        Return the list of names of the fields in the product

        .. note:: this method has no correspondent in the C API

        '''

        cdef EPR_SField* field_ptr
        cdef int idx
        cdef char* name

        self.check_closed_product()

        names = []
        for idx in range(self.get_num_fields()):
            field_ptr = <EPR_SField*>epr_get_field_at(self._ptr, idx)
            name = <char*>epr_get_field_name(field_ptr)
            names.append(_to_str(name, 'ascii'))

        return names

    # @NOTE: generator and generator expressions are not yet implemented in
    #        cython. As a workaround a list is used
    def fields(self):
        '''fields(self)

        Return the list of fields contained in the record

        '''

        # @TODO: use __iter__ when generator expressions will be available
        #return list(self)
        cdef int idx
        self.check_closed_product()
        return [self.get_field_at(idx)
                            for idx in range(epr_get_num_fields(self._ptr))]

    def __iter__(self):
        # @TODO: use generator expression when it will be available
        #return (self.get_field_at(idx)
        #                    for idx in range(epr_get_num_elems(self._ptr)))
        return iter(self.fields())

    def __str__(self):
        self.check_closed_product()
        return '\n'.join(map(str, self))

    def __repr__(self):
        self.check_closed_product()
        return '%s %d fields' % (super(Record, self).__repr__(),
                                 self.get_num_fields())


cdef new_record(EPR_SRecord* ptr, object parent=None, bint dealloc=False):
    if ptr is NULL:
        pyepr_null_ptr_error()

    cdef Record instance = Record.__new__(Record)

    instance._ptr = ptr
    instance._parent = parent       # Dataset or Product
    instance._dealloc = dealloc

    return instance


cdef class Raster(EprObject):
    '''Represents a raster in which data will be stored

    All 'size' parameter are in PIXEL.

    '''

    cdef EPR_SRaster* _ptr
    cdef Band _parent
    cdef np.ndarray _data

    def __dealloc__(self):
        if self._ptr is not NULL:
            epr_free_raster(self._ptr)

    property data_type:
        '''The data type of the band's pixels

        All ``E_TID_*`` types are possible

        '''

        def __get__(self):
            return self._ptr.data_type

    property source_width:
        '''The width of the source'''

        def __get__(self):
            return self._ptr.source_width

    property source_height:
        '''The height of the source'''

        def __get__(self):
            return self._ptr.source_height

    property source_step_x:
        '''The sub-sampling for the across-track direction in pixel'''

        def __get__(self):
            return self._ptr.source_step_x

    property source_step_y:
        '''The sub-sampling for the along-track direction in pixel'''

        def __get__(self):
            return self._ptr.source_step_y

    def get_width(self):
        '''get_width(self)

        Gets the raster's width in pixels

        '''

        return epr_get_raster_width(self._ptr)

    def get_height(self):
        '''get_height(self)

        Gets the raster's height in pixels

        '''

        return epr_get_raster_height(self._ptr)

    def get_elem_size(self):
        '''get_elem_size(self)

        The size in byte of a single element (sample) of this
        raster's buffer

        '''

        return epr_get_raster_elem_size(self._ptr)

    def get_pixel(self, int x, int y):
        '''get_pixel(x, y)

        Single pixel access

        This function is for getting the values of the elements of a
        raster (i.e. pixel)

        :param x:
            the (zero-based) X coordinate of the pixel
        :param y:
            the (zero-based) Y coordinate of the pixel
        :returns:
            the typed value at the given co-ordinate

        '''

        if (x < 0 or x >= self._ptr.raster_width or
            y < 0  or y >= self._ptr.raster_height):
            raise ValueError('index out of range: x=%d, y=%d' % (x, y))

        cdef EPR_EDataTypeId dtype = self._ptr.data_type

        if dtype == e_tid_uint:
            val = epr_get_pixel_as_uint(self._ptr, x, y)
        elif dtype == e_tid_int:
            val = epr_get_pixel_as_int(self._ptr, x, y)
        elif dtype == e_tid_float:
            val = epr_get_pixel_as_float(self._ptr, x, y)
        elif dtype == e_tid_double:
            val = epr_get_pixel_as_double(self._ptr, x, y)
        else:
            raise ValueError('invalid data type: "%s"' %
                                        <char*>epr_data_type_id_to_str(dtype))

        pyepr_check_errors()    # @TODO: check

        return val

    # --- high level interface ------------------------------------------------
    cdef np.ndarray toarray(self):
        cdef np.NPY_TYPES dtype = _epr_to_numpy_type_id(self._ptr.data_type)
        cdef np.npy_intp shape[2]
        cdef np.ndarray result

        if dtype == np.NPY_NOTYPE:
            raise TypeError('invalid data type')
        else:
            shape[0] = self._ptr.raster_height
            shape[1] = self._ptr.raster_width

            result = np.PyArray_SimpleNewFromData(2, shape, dtype,
                                                  self._ptr.buffer)

            # Make the ndarray keep a reference to this object
            np.set_array_base(result, self)

        return result

    property data:
        '''Raster data exposed as :class:`numpy.ndarray` object

        .. note:: this property shares the data buffer with the
                  :class:`Raster` object so any change in its contents
                  is also reflected to the :class:`Raster` object

        '''

        def __get__(self):
            if self._data is not None:
                return self._data

            if self._ptr.buffer is NULL:
                return np.ndarray(())

            self._data = self.toarray()

            return self._data

    def __repr__(self):
        return '%s %s (%dL x %dP)' % (super(Raster, self).__repr__(),
                                      data_type_id_to_str(self.data_type),
                                      self.get_height(), self.get_width())


cdef new_raster(EPR_SRaster* ptr, Band parent=None):
    if ptr is NULL:
        pyepr_null_ptr_error()

    cdef Raster instance = Raster.__new__(Raster)

    instance._ptr = ptr
    instance._parent = parent       # Band or None
    instance._data = None

    return instance


def create_raster(EPR_EDataTypeId data_type, uint src_width, uint src_height,
                  uint xstep=1, uint ystep=1):
    '''create_raster(data_type, src_width, src_height, xstep=1, ystep=1)

    Creates a raster of the specified data type

    This function can be used to create any type of raster, e.g. for
    later use as a bit-mask.

    :param data_type:
        the type of the data to stored in the raster, must be one of
        E_TID_*
    :param src_width:
        the width (across track dimension) of the source to be read
        into the raster.
        See description of :meth:`Band.create_compatible_raster`
    :param src_height:
        the height (along track dimension) of the source to be read
        into the raster.
        See description of :meth:`Band.create_compatible_raster`
    :param xstep:
        the sub-sampling step across track of the source when reading
        into the raster
    :param ystep:
        the sub-sampling step along track of the source when reading
        into the raster
    :returns:
        the new :class:`Raster` instance

    .. seealso:: description of :meth:`Band.create_compatible_raster`

    '''

    if xstep == 0 or ystep == 0:
        raise ValueError('invalid step: xspet=%d, ystep=%d' % (xstep, ystep))

    cdef EPR_SRaster* raster_ptr
    raster_ptr = epr_create_raster(data_type, src_width, src_height,
                                   xstep, ystep)
    if raster_ptr is NULL:
        pyepr_null_ptr_error('unable to create a new raster')

    return new_raster(raster_ptr)


def create_bitmask_raster(uint src_width, uint src_height,
                          uint xstep=1, uint ystep=1):
    '''create_bitmask_raster(src_width, src_height, xstep=1, ystep=1)

    Creates a raster to be used for reading bitmasks

    The raster returned always is of type ``byte``.

    :param src_width:
        the width (across track dimension) of the source to be read
        into the raster
    :param src_height:
        the height (along track dimension) of the source to be read
        into the raster
    :param xstep:
        the sub-sampling step across track of the source when reading
        into the raster
    :param ystep:
        the sub-sampling step along track of the source when reading
        into the raster
    :returns:
        the new raster instance or raises an exception
        (:exc:`EPRValueError`) if an error occurred

    .. seealso:: the description of
                 :meth:`Band.create_compatible_raster`

    '''

    if xstep == 0 or ystep == 0:
        raise ValueError('invalid step: xspet=%d, ystep=%d' % (xstep, ystep))

    cdef EPR_SRaster* raster_ptr
    raster_ptr = epr_create_bitmask_raster(src_width, src_height, xstep, ystep)
    if raster_ptr is NULL:
        pyepr_null_ptr_error('unable to create a new raster')

    return new_raster(raster_ptr)


cdef class Band(EprObject):
    '''The band of an ENVISAT product

    The Band class contains information about a band within an ENVISAT
    product file which has been opened with the :func:`open` function.

    A new Band instance can be obtained with the
    :meth:`Product.get_band` method.

    '''

    cdef EPR_SBandId* _ptr
    cdef Product _parent

    cdef inline check_closed_product(self):
        self._parent.check_closed_product()

    property product:
        '''The :class:`Product` instance to which this band belongs to'''

        def __get__(self):
            return self._parent

    property spectr_band_index:
        '''The (zero-based) spectral band index

        -1 if this is not a spectral band

        '''

        def __get__(self):
            self.check_closed_product()
            return self._ptr.spectr_band_index

    property sample_model:
        '''The sample model operation

        The sample model operation applied to the source dataset for
        getting the correct samples from the MDS (for example MERIS
        L2).

        Possible values are:

        * ``*``     --> no operation (direct copy)
        * ``1OF2``  --> first byte of 2-byte interleaved MDS
        * ``2OF2``  --> second byte of 2-byte interleaved MDS
        * ``0123``  --> combine 3-bytes interleaved to 4-byte integer

        '''

        def __get__(self):
            return self._ptr.sample_model

    property data_type:
        '''The data type of the band's pixels

        Possible values are:

        * ``*``         --> the datatype remains unchanged.
        * ``uint8_t``   --> 8-bit unsigned integer
        * ``uint32_t``  --> 32-bit unsigned integer
        * ``Float``     --> 32-bit IEEE floating point

        '''

        def __get__(self):
            return self._ptr.data_type

    property scaling_method:
        '''Scaling method

        The scaling method which must be applied to the raw source data
        in order to get the 'real' pixel values in geo-physical units.

        Possible values are:

        * ``*``            --> no scaling applied
        * ``Linear_Scale`` --> linear scaling applied::

            y = offset + scale * x

        * ``Log_Scale``    --> logarithmic scaling applied::

            y = log10(offset + scale * x)

        '''

        def __get__(self):
            return self._ptr.scaling_method

    property scaling_offset:
        '''The scaling offset

        Possible values are:

        * ``*`` --> no offset provided (implies scaling_method=*)
        * ``const`` --> a floating point constant
        * ``GADS.field[.field2]` --> value is provided in global
          annotation dataset with name ``GADS`` in field ``field``.
          Optionally a second element index for multiple-element fields
          can be given too

        '''

        def __get__(self):
            return self._ptr.scaling_offset

    property scaling_factor:
        '''The scaling factor

        Possible values are:

        * ``*`` --> no factor provided (implies scaling_method=*)
        * ``const`` --> a floating point constant
        * ``GADS.field[.field2]`` --> value is provided in global
          annotation dataset with name `GADS` in field `field``.
          Optionally a second element index for multiple-element fields
          can be given too

        '''

        def __get__(self):
            return self._ptr.scaling_factor

    property bm_expr:
        '''A bit-mask expression used to filter valid pixels

        All others are set to zero

        '''

        def __get__(self):
            if self._ptr.bm_expr is NULL:
                return None
            else:
                return _to_str(self._ptr.bm_expr, 'ascii')

    property unit:
        '''The geophysical unit for the band's pixel values'''

        def __get__(self):
            if self._ptr.unit is NULL:
                return None
            else:
                return _to_str(self._ptr.unit, 'ascii')

    property description:
        '''A short description of the band's contents'''

        def __get__(self):
            if self._ptr.description is NULL:
                return None
            else:
                return _to_str(self._ptr.description, 'ascii')

    property lines_mirrored:
        '''Mirrored lines flag

        If true (=1) lines will be mirrored (flipped) after read into a
        raster in order to ensure a pixel ordering in raster X
        direction from WEST to EAST.

        '''

        def __get__(self):
            return <bint>self._ptr.lines_mirrored

    def get_name(self):
        '''get_name(self)

        Gets the name of the band

        '''

        cdef char* name = NULL

        self.check_closed_product()

        name = <char*>epr_get_band_name(self._ptr)

        return _to_str(name, 'ascii')

    # @TODO: default values for src_width and src_height
    def create_compatible_raster(self, uint src_width, uint src_height,
                                 uint xstep=1, uint ystep=1):
        '''create_compatible_raster(self, src_width, src_height, xstep=1, ystep=1)

        Creates a raster which is compatible with the data type of
        the band

        The created raster is used to read the data in it (see
        :meth:`Band.read_raster`).

        The raster is defined on the grid of the product, from which
        the data are read. Spatial subsets and under-sampling are
        possible) through the parameter of the method.

        A raster is an object that allows direct access to data of a
        certain portion of the ENVISAT product that are read into the
        it.
        Such a portion is called the source. The complete ENVISAT
        product can be much greater than the source.
        One can move the raster over the complete ENVISAT product and
        read in turn different parts (always of the size of the source)
        of it into the raster.
        The source is specified by the parameters *height* and *width*.

        A typical example is a processing in blocks. Lets say, a block
        has 64x32 pixel. Then, my source has a width of 64 pixel and a
        height of 32 pixel.

        Another example is a processing of complete image lines. Then,
        my source has a widths of the complete product (for example
        1121 for a MERIS RR product), and a height of 1).
        One can loop over all blocks read into the raster and process
        it.

        In addition, it is possible to defined a sub-sampling step for
        a raster. This means, that the source is not read 1:1 into the
        raster, but that only every 2nd or 3rd pixel is read. This step
        can be set differently for the across track (source_step_x) and
        along track (source_step_y) directions.

        :param src_width:
            the width (across track dimension) of the source to be read
            into the raster
        :param src_height:
            the height (along track dimension) of the source to be read
            into the raster
        :param xstep:
            the sub-sampling step across track of the source when
            reading into the raster
        :param ystep:
            the sub-sampling step along track of the source when
            reading into the raster
        :returns:
            the new raster instance or raises an exception
            (:exc:`EPRValueError`) if an error occurred

        '''

        # @TODO: improve
        #if width is None:
        #    width = self._parent.get_scene_width()
        #
        #if height is None:
        #    height = self._parent.get_scene_height()

        cdef EPR_SRaster* raster_ptr

        self.check_closed_product()

        raster_ptr = epr_create_compatible_raster(self._ptr,
                                                  src_width, src_height,
                                                  xstep, ystep)
        if raster_ptr is NULL:
            pyepr_null_ptr_error('unable to create compatible raster with '
                                 'width=%d, height=%d xstep=%d, ystep=%d' %
                                        (src_width, src_height, xstep, ystep))

        return new_raster(raster_ptr, self)

    cpdef read_raster(self, int xoffset=0, int yoffset=0, Raster raster=None):
        '''read_raster(self, xoffset=0, yoffset=0, Raster raster=None)

        Reads (geo-)physical values of the band of the specified
        source-region

        The source-region is a defined part of the whole ENVISAT
        product image, which shall be read into a raster.
        In this routine the co-ordinates are specified, where the
        source-region to be read starts.
        The dimension of the region and the sub-sampling are attributes
        of the raster into which the data are read.

        :param xoffset:
            across-track source co-ordinate in pixel co-ordinates
            (zero-based) of the upper right corner of the source-region
        :param yoffset:
            along-track source co-ordinate in pixel co-ordinates
            (zero-based) of the upper right corner of the source-region
        :param raster:
            :class:`Raster` instance set with appropriate parameters to
            read into. If not provided a new :class:`Raster` is
            instantiated
        :returns:
            the :class:`Raster` instance in which data are read

        This method raises an instance of the appropriate
        :exc:`EPRError` sub-class if case of errors

        .. seealso:: :meth:`Band.create_compatible_raster` and
                     :func:`create_raster`

        '''

        cdef int ret

        self.check_closed_product()

        if raster is None:
            raster = self.create_compatible_raster()

        with nogil:
            ret = epr_read_band_raster(self._ptr, xoffset, yoffset,
                                       raster._ptr)

        if ret != 0:
            pyepr_check_errors()

        raster._data = None

        return raster

    # --- high level interface ------------------------------------------------
    def read_as_array(self, width=None, height=None,
                      uint xoffset=0, uint yoffset=0,
                      uint xstep=1, uint ystep=1):
        '''read_as_array(self, width=None, height=None, xoffset=0, yoffset=0, xstep=1, ystep=1):

        Reads the specified source region as an :class:`numpy.ndarray`

        The source-region is a defined part of the whole ENVISAT
        product image, which shall be read into a raster.
        In this routine the co-ordinates are specified, where the
        source-region to be read starts.
        The dimension of the region and the sub-sampling are attributes
        of the raster into which the data are read.

        :param src_width:
            the width (across track dimension) of the source to be read
            into the raster. If not provided reads as much as possible
        :param src_height:
            the height (along track dimension) of the source to be read
            into the raster. If not provided reads as much as possible
        :param xoffset:
            across-track source co-ordinate in pixel co-ordinates
            (zero-based) of the upper right corner of the source-region
        :param yoffset:
            along-track source co-ordinate in pixel co-ordinates
            (zero-based) of the upper right corner of the source-region
        :param xstep:
            the sub-sampling step across track of the source when
            reading into the raster
        :param ystep:
            the sub-sampling step along track of the source when
            reading into the raster
        :returns:
            the :class:`numpy.ndarray` instance in which data are read

        This method raises an instance of the appropriate
        :exc:`EPRError` sub-class if case of errors

        .. seealso:: :meth:`Band.create_compatible_raster`,
                     :func:`create_raster` and :meth:`Band.read_raster`

        '''

        if width is None:
            w = self.product.get_scene_width()
            if w > xoffset:
                width = w - xoffset
            else:
                raise ValueError('xoffset os larger that he scene width')

        if height is None:
            h = self.product.get_scene_height()
            if h > yoffset:
                height = h - yoffset
            else:
                raise ValueError('yoffset os larger that he scene height')

        raster = self.create_compatible_raster(width, height, xstep, ystep)
        self.read_raster(xoffset, yoffset, raster)

        return raster.data

    def __repr__(self):
        return 'epr.Band(%s) of epr.Product(%s)' % (self.get_name(),
                                                    self.product.id_string)


cdef new_band(EPR_SBandId* ptr, Product parent=None):
    if ptr is NULL:
        pyepr_null_ptr_error()

    cdef Band instance = Band.__new__(Band)

    instance._ptr = ptr
    instance._parent = parent

    return instance


cdef class Dataset(EprObject):
    '''ENVISAT dataset

    The Dataset class contains information about a dataset within an
    ENVISAT product file which has been opened with the :func:`open`
    function.

    A new Dataset instance can be obtained with the
    :meth:`Product.get_dataset` or :meth:`Product.get_dataset_at`
    methods.

    '''

    cdef EPR_SDatasetId* _ptr
    cdef Product _parent

    cdef inline check_closed_product(self):
        self._parent.check_closed_product()

    property product:
        '''The :class:`Product` instance to which this dataset belongs to'''

        def __get__(self):
            return self._parent

    property description:
        '''A short description of the band's contents'''

        def __get__(self):
            if self._ptr.description is NULL:
                return ''
            else:
                return _to_str(self._ptr.description, 'ascii')

    def get_name(self):
        '''get_name(self)

        Gets the name of the dataset

        '''

        cdef char* name

        if self._ptr is not NULL:
            self.check_closed_product()
            name = <char*>epr_get_dataset_name(self._ptr)
            return _to_str(name, 'ascii')
        return ''

    def get_dsd_name(self):
        '''get_dsd_name(self)

        Gets the name of the DSD (dataset descriptor)

        '''

        cdef char* name

        if self._ptr is not NULL:
            self.check_closed_product()
            name = <char*>epr_get_dsd_name(self._ptr)
            return _to_str(name, 'ascii')
        return ''

    def get_num_records(self):
        '''get_num_records(self)

        Gets the number of records of the dataset

        '''

        if self._ptr is not NULL:
            self.check_closed_product()
            return epr_get_num_records(self._ptr)
        return 0

    def get_dsd(self):
        '''get_dsd(self)

        Gets the dataset descriptor (DSD)

        '''

        self.check_closed_product()

        return new_dsd(<EPR_SDSD*>epr_get_dsd(self._ptr), self)

    def create_record(self):
        '''create_record(self)

        Creates a new record

        Creates a new, empty record with a structure compatible with
        the dataset. Such a record is typically used in subsequent
        calls to :meth:`Dataset.read_record`.

        :returns:
            the new record instance

        '''

        self.check_closed_product()

        return new_record(epr_create_record(self._ptr), self, True)

    # @TODO: default: index=0
    def read_record(self, uint index, Record record=None):
        '''read_record(self, index, record=None)

        Reads specified record of the dataset

        The record is identified through the given zero-based record
        index. In order to reduce memory reallocation, a record
        (pre-)created by the method :meth:`Dataset.create_record` can
        be passed to this method.
        Data is then read into this given record.

        If no record (``None``) is given, the method initiates a new
        one.

        In both cases, the record in which the data is read into will
        be  returned.

        :param index:
            the zero-based record index
        :param record:
            a pre-created record to reduce memory reallocation, can be
            ``None`` (default) to let the function allocate a new
            record
        :returns:
            the record in which the data has been read into or raises
            an exception (:exc:`EPRValueError`) if an error occurred

        '''

        cdef EPR_SRecord* record_ptr = NULL

        self.check_closed_product()

        if record:
            record_ptr = (<Record>record)._ptr

        with nogil:
            record_ptr = epr_read_record(self._ptr, index, record_ptr)

        if record_ptr is NULL:
            pyepr_null_ptr_error('unable to read record at index %d' % index)

        if not record:
            record = new_record(record_ptr, self, True)

        return record

    # --- high level interface ------------------------------------------------
    # @NOTE: generator and generator expressions are not yet implemented in
    #        cython. As a workaround a list is used
    def records(self):
        '''records(self)

        Return the list of records contained in the dataset

        '''

        # @TODO: use __iter__ when generator expressions will be available
        #return list(self)
        cdef int idx

        self.check_closed_product()

        return [self.read_record(idx)
                            for idx in range(epr_get_num_records(self._ptr))]

    def __iter__(self):
        # @TODO: use generator expression when it will be available
        #return (self.get_field_at(idx)
        #                    for idx in range(epr_get_num_elems(self._ptr)))
        return iter(self.records())

    def __str__(self):
        lines = [repr(self), '']
        lines.extend(map(str, self))
        return '\n'.join(lines)

    def __repr__(self):
        return 'epr.Dataset(%s) %d records' % (self.get_name(),
                                               self.get_num_records())


cdef new_dataset(EPR_SDatasetId* ptr, Product parent=None):
    if ptr is NULL:
        pyepr_null_ptr_error()

    cdef Dataset instance = Dataset.__new__(Dataset)

    instance._ptr = ptr
    instance._parent = parent

    return instance


cdef class Product(EprObject):
    '''ENVISAT product

    The Product class provides methods and properties to get
    information about an ENVISAT product file.

    .. seealso:: :func:`open`

    '''

    cdef EPR_SProductId* _ptr

    def __cinit__(self, filename, *args, **kargs):
        cdef bytes bfilename = _to_bytes(filename, _DEFAULT_FS_ENCODING)
        cdef char* cfilename = bfilename

        with nogil:
            self._ptr = epr_open_product(cfilename)

        if self._ptr is NULL:
            # try to get error info from the lib
            pyepr_check_errors()

            raise ValueError('unable to open "%s"' % filename)

    def __dealloc__(self):
        if self._ptr is not NULL:
            epr_close_product(self._ptr)
            pyepr_check_errors()
            self._ptr = NULL

    cdef inline check_closed_product(self):
        if self._ptr is NULL:
            raise ValueError('I/O operation on closed file')

    def __init__(self, filename):
        # @NOTE: this method suppresses the default behavior of EprObject
        #        that is raising an exception when it is instantiated by
        #        the user.
        pass

    def close(self):
        '''close(self)

        Closes the ENVISAT :class:`epr.Product` product

        Closes the :class:`epr.Product` product and free the underlying
        file descriptor.

        This method has no effect if the :class:`Product` is already
        closed. Once the :class:`Product` is closed, any operation on
        it will raise a ValueError.

        As a convenience, it is allowed to call this method more than
        once; only the first call, however, will have an effect.

        '''

        if self._ptr is not NULL:
            epr_close_product(self._ptr)
            pyepr_check_errors()
            self._ptr = NULL

    property file_path:
        '''The file's path including the file name'''

        def __get__(self):
            self.check_closed_product()
            if self._ptr.file_path is NULL:
                return None
            else:
                return _to_str(self._ptr.file_path, 'ascii')

    # @TODO: check
    #property istream:
    #    '''The input stream as returned by the ANSI C :c:func:`fopen`
    #       function for the given file path
    #
    #    '''
    #
    #    def __get__(self):
    #        if self._ptr.istream is NULL:
    #            return None
    #        else:
    #            return os.fdopen(self._ptr.istream)

    property tot_size:
        '''The total size in bytes of the product file'''

        def __get__(self):
            self.check_closed_product()
            return self._ptr.tot_size

    property id_string:
        '''The product identifier string obtained from the MPH
        parameter 'PRODUCT'

        The first 10 characters of this string identify the product
        type, e.g. "MER_1P__FR" for a MERIS Level 1b full resolution
        product.
        The rest of the string decodes product instance properties.

        '''

        def __get__(self):
            self.check_closed_product()
            if self._ptr.id_string is NULL:
                return None
            else:
                return _to_str(self._ptr.id_string, 'ascii')

    property meris_iodd_version:
        '''For MERIS L1b and RR and FR to provide backward compatibility'''

        def __get__(self):
            self.check_closed_product()
            return self._ptr.meris_iodd_version

    def get_scene_width(self):
        '''get_scene_width(self)

        Gets the product's scene width in pixels

        '''

        self.check_closed_product()
        return epr_get_scene_width(self._ptr)

    def get_scene_height(self):
        '''get_scene_height(self)

        Gets the product's scene height in pixels

        '''

        self.check_closed_product()
        return epr_get_scene_height(self._ptr)

    def get_num_datasets(self):
        '''get_num_datasets(self)

        Gets the number of all datasets contained in a product

        '''

        self.check_closed_product()
        return epr_get_num_datasets(self._ptr)

    def get_num_dsds(self):
        '''get_num_dsds(self)

        Gets the number of all :class:`DSD`\ s

        Gets the number of all :class:`DSD`\ s (dataset descriptors)
        contained in the product

        '''

        self.check_closed_product()
        return epr_get_num_dsds(self._ptr)

    def get_num_bands(self):
        '''get_num_bands(self)

        Gets the number of all bands contained in a product

        '''

        self.check_closed_product()
        return epr_get_num_bands(self._ptr)

    def get_dataset_at(self, uint index):
        '''get_dataset_at(self, index)

        Gets the dataset at the specified position within the product

        :param index:
            the index identifying the position of the dataset, starting
            with 0, must not be negative
        :returns:
            the requested :class:`Dataset`

        '''

        cdef EPR_SDatasetId* dataset_id
        dataset_id = epr_get_dataset_id_at(self._ptr, index)
        if dataset_id is NULL:
            pyepr_null_ptr_error('unable to get dataset at index %d' % index)

        return new_dataset(dataset_id, self)

    def get_dataset(self, name):
        '''get_dataset(self, name)

        Gets the dataset corresponding to the specified dataset name

        :param name:
            the dataset name
        :returns:
            the requested :class:`Dataset` instance

        '''

        cdef EPR_SDatasetId* dataset_id
        cdef bytes cname = _to_bytes(name)
        dataset_id = epr_get_dataset_id(self._ptr, cname)
        if dataset_id is NULL:
            pyepr_null_ptr_error(r'unable to get dataset "%s"' % name)

        return new_dataset(dataset_id, self)

    def get_dsd_at(self, uint index):
        '''get_dsd_at(self, index)

        Gets the :class:`DSD` at the specified position

        Gets the :class:`DSD` (dataset descriptor) at the specified
        position within the product.

        :param index:
            the index identifying the position of the :class:`DSD`,
            starting with 0, must not be negative
        :returns:
            the requested :class:`DSD` instance

        '''

        cdef EPR_SDSD* dsd_ptr

        self.check_closed_product()

        dsd_ptr = epr_get_dsd_at(self._ptr, index)
        if dsd_ptr is NULL:
            pyepr_null_ptr_error('unable to get DSD at index "%d"' % index)

        return new_dsd(dsd_ptr, self)

    def get_mph(self):
        '''get_mph(self)

        The main product header (MPH) :class:`Record`

        '''

        cdef EPR_SRecord* record_ptr
        record_ptr = epr_get_mph(self._ptr)
        if record_ptr is NULL:
            pyepr_null_ptr_error('unable to get MPH record')

        return new_record(record_ptr, self, False)

    def get_sph(self):
        '''get_sph(self)

        The specific product header (SPH) :class:`Record`

        '''

        cdef EPR_SRecord* record_ptr
        record_ptr = epr_get_sph(self._ptr)
        if record_ptr is NULL:
            pyepr_null_ptr_error('unable to get SPH record')

        return new_record(record_ptr, self, False)

    def get_band(self, name):
        '''get_band(self, name)

        Gets the band corresponding to the specified name.

        :param name:
            the name of the band
        :returns:
            the requested :class:`Band` instance, or raises a
            :exc:`EPRValueError` if not found

        '''

        cdef EPR_SBandId* band_id
        cdef bytes cname = _to_bytes(name)
        band_id = epr_get_band_id(self._ptr, cname)
        if band_id is NULL:
            pyepr_null_ptr_error('unable to get band "%s"' % name)

        return new_band(band_id, self)

    def get_band_at(self, uint index):
        '''get_band_at(self, index)

        Gets the band at the specified position within the product

        :param index:
            the index identifying the position of the band, starting
            with 0, must not be negative
        :returns:
            the requested :class:`Band` instance, or raises a
            :exc:`EPRValueError` if not found

        '''

        cdef EPR_SBandId* band_id
        band_id = epr_get_band_id_at(self._ptr, index)
        if band_id is NULL:
            pyepr_null_ptr_error('unable to get band at index "%d"' % index)

        return new_band(band_id, self)

    def read_bitmask_raster(self, bm_expr, int xoffset, int yoffset,
                            Raster raster not None):
        '''read_bitmask_raster(self, bm_expr, xoffset, yoffset, raster)

        Calculates a bit-mask raster

        Calculates a bit-mask, composed of flags of the given product
        and combined as described in the given bit-mask expression, for
        the a certain dimension and sub-sampling as defined in the
        given raster.

        :param bm_expr:
            a string holding the logical expression for the definition
            of the bit-mask. In a bit-mask expression, any number of
            the flag-names (found in the DDDB) can be composed with
            "(", ")", "NOT", "AND", "OR". Valid bit-mask expression are
            for example ``flags.LAND OR flags.CLOUD`` or
            ``NOT flags.WATER AND flags.TURBID_S``

       :param xoffset:
            across-track co-ordinate in pixel co-ordinates (zero-based)
            of the upper right corner of the source-region
       :param yoffset:
            along-track co-ordinate in pixel co-ordinates (zero-based)
            of the upper right corner of the source-region
       :param raster:
            the raster for the bit-mask. The data type of the raster
            must be either e_tid_uchar or e_tid_char
        :returns:
            zero for success, an error code otherwise

        .. seealso: :func:`create_bitmask_raster`

        '''

        cdef bytes c_bm_expr = _to_bytes(bm_expr)
        cdef int ret = 0

        self.check_closed_product()

        ret = epr_read_bitmask_raster(self._ptr, c_bm_expr,
                                      xoffset, yoffset,
                                      (<Raster>raster)._ptr)
        if ret != 0:
            pyepr_check_errors()

        return raster

    # --- high level interface ------------------------------------------------
    property closed:
        '''True if the :class:`epr.Product` is closed.'''

        def __get__(self):
            return self._ptr is NULL

    def get_dataset_names(self):
        '''get_dataset_names(self)

        Return the list of names of the datasets in the product

        .. note:: this method has no correspondent in the C API

        '''

        cdef EPR_SDatasetId* dataset_ptr
        cdef int idx
        cdef char* name

        names = []
        for idx in range(self.get_num_datasets()):
            dataset_ptr = epr_get_dataset_id_at(self._ptr, idx)
            name = <char*>epr_get_dataset_name(dataset_ptr)
            names.append(_to_str(name, 'ascii'))

        return names

    def get_band_names(self):
        '''get_band_names(self)

        Return the list of names of the bands in the product

        .. note:: this method has no correspondent in the C API

        '''

        cdef EPR_SBandId* band_ptr
        cdef int idx
        cdef char* name

        names = []
        for idx in range(self.get_num_bands()):
            band_ptr = epr_get_band_id_at(self._ptr, idx)
            name = <char*>epr_get_band_name(band_ptr)
            names.append(_to_str(name, 'ascii'))

        return names

    # @NOTE: generator and generator expressions are not yet implemented in
    #        cython. As a workaround a list is used
    def datasets(self):
        '''datasets(self)

        Return the list of dataset in the product

        '''

        cdef int idx
        return [self.get_dataset_at(idx)
                            for idx in range(epr_get_num_datasets(self._ptr))]

    def bands(self):
        '''bands(self)

        Return the list of bands in the product

        '''

        return [self.get_band_at(idx)
                            for idx in range(epr_get_num_bands(self._ptr))]

    # @TODO: iter on both datasets and bands (??)
    #def __iter__(self):
    #    return itertools.chain((self.datasets(), self.bands()))

    def __repr__(self):
        return 'epr.Product(%s) %d datasets, %d bands' % (self.id_string,
                                self.get_num_datasets(), self.get_num_bands())

    def __str__(self):
        lines = [repr(self), '']
        lines.extend(map(repr, self.datasets()))
        lines.append('')
        lines.extend(map(repr, self.bands()))
        return '\n'.join(lines)

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.close()


def open(filename):
    '''open(filename)

    Opens the ENVISAT product

    Opens the ENVISAT product file with the given file path, reads MPH,
    SPH and all DSDs, organized the table with parameter of line length
    and tie points number.

    :param product_file_path:
        the path to the ENVISAT product file
    :returns:
        the :class:`Product` instance representing the specified
        product. An exception (:exc:`exceptions.ValueError`) is raised
        if the file could not be opened.

    .. seealso :class:`Product`

    '''

    return Product(filename)


# library initialization/finalization
_EPR_C_LIB = _CLib.__new__(_CLib)


import atexit


@atexit.register
def _close_api():
    # ensure that all EprObject(s) are collected before removing the last
    # reference to _EPR_C_LIB
    import gc
    gc.collect()

    global _EPR_C_LIB
    _EPR_C_LIB = None


# clean namespace
del atexit, namedtuple
