# -*- coding: utf-8 -*-

# PyEPR - Python bindings for ENVISAT Product Reader API
#
# Copyright (C) 2011, Antonio Valentino <antonio.valentino@tiscali.it>
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

__revision__ = '$Id$'
__version__  = '0.2a'


cdef extern from 'Python.h':
    ctypedef struct FILE
    FILE* PyFile_AsFile(object)

    # To release global interpreter lock (GIL) for threading
    void Py_BEGIN_ALLOW_THREADS()
    void Py_END_ALLOW_THREADS()


cdef extern from 'epr_api.h':
    ctypedef int            epr_boolean
    ctypedef unsigned char  uchar
    ctypedef unsigned short ushort
    ctypedef unsigned int   uint
    ctypedef unsigned long  ulong

    enum EPR_ErrCode:
        e_err_none                 =    0
        e_err_null_pointer         =    1
        e_err_illegal_arg          =    2
        e_err_illegal_state        =    3
        e_err_out_of_memory        =    4
        e_err_index_out_of_range   =    5
        e_err_illegal_conversion   =    6
        e_err_illegal_data_type	   =    7
        e_err_file_not_found       =  101
        e_err_file_access_denied   =  102
        e_err_file_read_error      =  103
        e_err_file_write_error     =  104
        e_err_file_open_failed     =  105
        e_err_file_close_failed    =  106
        e_err_api_not_initialized  =  201
        e_err_invalid_product_id   =  203
        e_err_invalid_record       =  204
        e_err_invalid_band         =  205
        e_err_invalid_raster       =  206
        e_err_invalid_dataset_name =  207
        e_err_invalid_field_name   =  208
        e_err_invalid_record_name  =  209
        e_err_invalid_product_name =  210
        e_err_invalid_band_name    =  211
        e_err_invalid_data_format  =  212
        e_err_invalid_value        =  213
        e_err_invalid_keyword_name =  214
        e_err_unknown_endian_order =  216
        e_err_flag_not_found       =  301
        e_err_invalid_ddbb_format  =  402

    enum EPR_DataTypeId:
        e_tid_unknown = 0
        e_tid_uchar   = 1
        e_tid_char    = 2
        e_tid_ushort  = 3
        e_tid_short   = 4
        e_tid_uint    = 5
        e_tid_int     = 6
        e_tid_float   = 7
        e_tid_double  = 8
        e_tid_string  = 11
        e_tid_spare   = 13
        e_tid_time    = 21

    enum EPR_LogLevel:
        e_log_debug   = -1
        e_log_info    =  0
        e_log_warning =  1
        e_log_error   =  2

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
        #void* elems
        pass


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
    char* epr_get_last_err_message()
    void epr_clear_err()

    # API initialization/finalization
    int epr_init_api(EPR_ELogLevel, EPR_FLogHandler, EPR_FErrHandler)
    void epr_close_api()

    # DATATYPE
    uint epr_get_data_type_size(EPR_EDataTypeId)
    char* epr_data_type_id_to_str(EPR_EDataTypeId)

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
    char* epr_get_dataset_name(EPR_SDatasetId*)
    char* epr_get_dsd_name(EPR_SDatasetId*)
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

    char* epr_get_field_unit(EPR_SField*)
    char* epr_get_field_description(EPR_SField*)
    uint epr_get_field_num_elems(EPR_SField*)
    char* epr_get_field_name(EPR_SField*)
    EPR_EDataTypeId epr_get_field_type(EPR_SField*)

    char epr_get_field_elem_as_char(EPR_SField*, uint)
    uchar epr_get_field_elem_as_uchar(EPR_SField*, uint)
    short epr_get_field_elem_as_short(EPR_SField*, uint)
    ushort epr_get_field_elem_as_ushort(EPR_SField*, uint)
    int epr_get_field_elem_as_int(EPR_SField*, uint)
    uint epr_get_field_elem_as_uint(EPR_SField*, uint)
    float epr_get_field_elem_as_float(EPR_SField*, uint)
    double epr_get_field_elem_as_double(EPR_SField*, uint)
    char* epr_get_field_elem_as_str(EPR_SField*)
    EPR_STime* epr_get_field_elem_as_mjd(EPR_SField*)

    char* epr_get_field_elems_char(EPR_SField*)
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
    char* epr_get_band_name(EPR_SBandId*)
    EPR_SRaster* epr_create_compatible_raster(EPR_SBandId*, uint, uint, uint, uint)
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


import sys
import collections
import numpy as np
cimport numpy as np
np.import_array()


# utils
EPRTime = collections.namedtuple('EPRTime', ('days', 'seconds', 'microseconds'))

# EPR_DataTypeId
E_TID_UNKNOWN = e_tid_unknown
E_TID_UCHAR   = e_tid_uchar
E_TID_CHAR    = e_tid_char
E_TID_USHORT  = e_tid_ushort
E_TID_SHORT   = e_tid_short
E_TID_UINT    = e_tid_uint
E_TID_INT     = e_tid_int
E_TID_FLOAT   = e_tid_float
E_TID_DOUBLE  = e_tid_double
E_TID_STRING  = e_tid_string
E_TID_SPARE   = e_tid_spare
E_TID_TIME    = e_tid_time

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
    cdef np.NPY_TYPES result = np.NPY_NOTYPE

    if epr_type == E_TID_UCHAR:
        result = np.NPY_UBYTE
    if epr_type == E_TID_CHAR:
        result = np.NPY_BYTE
    if epr_type == E_TID_USHORT:
        result = np.NPY_USHORT
    if epr_type == E_TID_SHORT:
        result = np.NPY_SHORT
    if epr_type == E_TID_UINT:
        result = np.NPY_UINT
    if epr_type == E_TID_INT:
        result = np.NPY_INT
    if epr_type == E_TID_FLOAT:
        result = np.NPY_FLOAT
    if epr_type == E_TID_DOUBLE:
        result = np.NPY_DOUBLE
    if epr_type == E_TID_STRING:
        result = np.NPY_STRING

    return result


class EPRError(Exception):
    '''Error in the EPR C API'''

    def __init__(self, message='', code=None, *args, **kargs):
        super(EPRError, self).__init__(message, code, *args, **kargs)

        #: error code of the generated in the C library
        self.code = code


class EPRValueError(EPRError, ValueError):
    pass


cdef int pyepr_check_errors() except -1:
    cdef int code
    cdef char* msg
    code = epr_get_last_err_code()
    if code != e_err_none:
        msg = <char*>epr_get_last_err_message()
        epr_clear_err()
        if (e_err_invalid_product_id <= code <= e_err_invalid_keyword_name or
            code in (e_err_null_pointer,
                     e_err_illegal_arg,
                     e_err_index_out_of_range)):
            raise EPRValueError(msg, code)
        else:
            raise EPRError(msg, code)
        return -1
    return 0

cdef int pyepr_null_ptr_error(msg='null pointer') except -1:
    cdef int code
    cdef char* eprmsg = <char*>epr_get_last_err_message()

    code = epr_get_last_err_code()
    if not code:
        code = None

    epr_clear_err()
    raise EPRValueError('%s: %s' % (msg, eprmsg), code=code)
    return -1


# library API initialization/finalization
def _init_api():
    cdef char* msg
    #if epr_init_api(e_log_warning, epr_log_message, NULL):
    if epr_init_api(e_log_warning, NULL, NULL):
        msg = <char*>epr_get_last_err_message()
        epr_clear_err()
        raise ImportError('unable to inizialize EPR API library: %s' % msg)

def _close_api():
    epr_close_api()
    pyepr_check_errors()

def get_data_type_size(EPR_EDataTypeId type_id):
    '''Gets the size in bytes for an element of the given data type'''

    return epr_get_data_type_size(type_id)

def data_type_id_to_str(EPR_EDataTypeId type_id):
    '''Gets the 'C' data type string for the given data type'''

    return epr_data_type_id_to_str(type_id)

def get_scaling_method_name(method):
    '''Return the name of the specified scaling method'''

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
    '''Return the name of the specified sample model'''

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


cdef class DSD:
    '''Dataset descriptor

    The DSD class contains information about the properties of a
    dataset and its location within an ENVISAT product file

    '''

    cdef EPR_SDSD* _ptr
    cdef object _parent

    def __init__(self):
        raise TypeError('"%s" class cannot be instantiated from Python' %
                                                    self.__class__.__name__)

    property index:
        '''The index of this DSD (zero-based)'''

        def __get__(self):
            return self._ptr.index

    property ds_name:
        '''The dataset name'''

        def __get__(self):
            return self._ptr.ds_name

    property ds_type:
        '''The dataset type descriptor'''

        def __get__(self):
            return self._ptr.ds_type

    property filename:
        '''The filename in the DDDB with the description of this dataset'''

        def __get__(self):
            return self._ptr.filename

    property ds_offset:
        '''The offset of dataset-information the product file'''

        def __get__(self):
            return self._ptr.ds_offset

    property ds_size:
        '''The size of dataset-information in dataset product file'''

        def __get__(self):
            return self._ptr.ds_size

    property num_dsr:
        '''The number of dataset records for the given dataset name'''

        def __get__(self):
            return self._ptr.num_dsr

    property dsr_size:
        '''The size of dataset record for the given dataset name'''

        def __get__(self):
            return self._ptr.dsr_size


cdef new_dsd(EPR_SDSD* ptr, object parent=None):
    if ptr is NULL:
        pyepr_null_ptr_error()

    cdef DSD instance = DSD.__new__(DSD)

    instance._ptr = ptr
    instance._parent = parent

    return instance


cdef class Field:
    '''Represents a field within a record

    A field is composed of one or more data elements of one of the
    types defined in the internal ``field_info`` structure.

    .. seealso:: :class:`Record`

    '''

    cdef EPR_SField* _ptr
    cdef object _parent

    def __init__(self):
        raise TypeError('"%s" class cannot be instantiated from Python' %
                                                    self.__class__.__name__)

    def print_(self, ostream=None):
        '''Write the field to specified file (default: sys.stdout)

        This method writes formatted contents of the field to
        specified *ostream* text file or (default) the ASCII output
        is be printed to standard output (sys.stdout)

        :param ostream:
            the (opened) output file object

        .. note:: the *ostream* parameter have to be a *real* file not
                  a generic stream object like *StringIO* instances

        '''

        cdef FILE* fd

        if ostream is None:
            ostream = sys.stdout

        fd = PyFile_AsFile(ostream)
        if fd is NULL:
            raise TypeError('invalid ostream')

        Py_BEGIN_ALLOW_THREADS
        epr_print_field(self._ptr, fd)
        Py_END_ALLOW_THREADS

        pyepr_check_errors()

    #def dump_field(self):
    #    epr_dump_field(self._ptr)
    #    pyepr_check_errors()

    def get_unit(self):
        '''Gets the unit of the field'''

        return epr_get_field_unit(self._ptr)

    def get_description(self):
        '''Gets the description of the field'''

        return epr_get_field_description(self._ptr)

    def get_num_elems(self):
        '''Gets the number of elements of the field'''

        return epr_get_field_num_elems(self._ptr)

    def get_name(self):
        '''Gets the name of the field'''

        return epr_get_field_name(self._ptr)

    def get_type(self):
        '''Gets the type of the field'''

        return epr_get_field_type(self._ptr)

    def get_elem(self, uint index=0):
        '''Field single element access

        This function is for getting the elements of a field.

        :param index:
            the zero-based index of element to be returned, must not be
            negative
        :returns:
            the typed value from given field

        '''

        cdef EPR_STime* eprtime
        etype = epr_get_field_type(self._ptr)

        if etype == e_tid_uchar:
            val = epr_get_field_elem_as_char(self._ptr, index)
        elif etype == e_tid_char:
            val = epr_get_field_elem_as_uchar(self._ptr, index)
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
            val = epr_get_field_elem_as_str(self._ptr)
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
        '''Field array element access

        This function is for getting an array of field elements of the
        field.

        :returns:
            the data array (numpy.ndarray) having the type of the field

        '''

        # @NOTE: internal C const pointer is not shared with numpy
        cdef void* buf
        cdef size_t num_elems
        cdef size_t i
        cdef np.ndarray out

        num_elems = epr_get_field_num_elems(self._ptr)
        etype = epr_get_field_type(self._ptr)

        if etype == e_tid_uchar:
            buf = <uchar*>epr_get_field_elems_char(self._ptr)
            if buf is NULL:
                pyepr_null_ptr_error()
            out = np.ndarray(num_elems, np.uchar)
            #memcpy(out.data, buf, num_elems*sizeof(uchar)) # @TODO: check
            for i in range(num_elems):
                out[i] = (<uchar*>buf)[i]
        elif etype == e_tid_char:
            buf = <char*>epr_get_field_elems_uchar(self._ptr)
            if buf is NULL:
                pyepr_null_ptr_error()
            out = np.ndarray(num_elems, np.char)
            for i in range(num_elems):
                out[i] = (<char*>buf)[i]
        elif etype == e_tid_ushort:
            buf = <ushort*>epr_get_field_elems_ushort(self._ptr)
            if buf is NULL:
                pyepr_null_ptr_error()
            out = np.ndarray(num_elems, np.ushort)
            for i in range(num_elems):
                out[i] = (<ushort*>buf)[i]
        elif etype == e_tid_short:
            buf = <short*>epr_get_field_elems_short(self._ptr)
            if buf is NULL:
                pyepr_null_ptr_error()
            out = np.ndarray(num_elems, np.short)
            for i in range(num_elems):
                out[i] = (<short*>buf)[i]
        elif etype == e_tid_uint:
            buf = <uint*>epr_get_field_elems_uint(self._ptr)
            if buf is NULL:
                pyepr_null_ptr_error()
            out = np.ndarray(num_elems, np.uint)
            for i in range(num_elems):
                out[i] = (<uint*>buf)[i]
        elif etype == e_tid_int:
            buf = <int*>epr_get_field_elems_int(self._ptr)
            if buf is NULL:
                pyepr_null_ptr_error()
            out = np.ndarray(num_elems, np.int)
            for i in range(num_elems):
                out[i] = (<int*>buf)[i]
        elif etype == e_tid_float:
            buf = <float*>epr_get_field_elems_float(self._ptr)
            if buf is NULL:
                pyepr_null_ptr_error()
            out = np.ndarray(num_elems, np.float32)
            for i in range(num_elems):
                out[i] = (<float*>buf)[i]
        elif etype == e_tid_double:
            buf = <double*>epr_get_field_elems_double(self._ptr)
            if buf is NULL:
                pyepr_null_ptr_error()
            out = np.ndarray(num_elems, np.double)
            for i in range(num_elems):
                out[i] = (<double*>buf)[i]
        else:
            raise ValueError('invalid field type')

        return out


cdef new_field(EPR_SField* ptr, object parent=None):
    if ptr is NULL:
        pyepr_null_ptr_error()

    cdef Field instance = Field.__new__(Field)

    instance._ptr = ptr
    instance._parent = parent

    return instance


cdef class Record:
    '''Represents a record read from an ENVISAT dataset

    A record is composed of multiple fields.

    .. seealso:: :class:`Field`

    '''

    cdef EPR_SRecord* _ptr
    cdef object _parent
    cdef bint _dealloc

    def __dealloc__(self):
        if not self._dealloc:
            return

        if self._ptr is not NULL:
            epr_free_record(self._ptr)
            pyepr_check_errors()

    def __init__(self):
        raise TypeError('"%s" class cannot be instantiated from Python' %
                                                    self.__class__.__name__)

    def get_num_fields(self):
        '''Gets the number of fields contained in the record'''

        return epr_get_num_fields(self._ptr)

    def print_(self, ostream=None):
        '''Write the record to specified file (default: sys.stdout)

        This method writes formatted contents of the record to
        specified *ostream* text file or (default) the ASCII output
        is be printed to standard output (sys.stdout)

        :param ostream:
            the (opened) output file object

        .. note:: the *ostream* parameter have to be a *real* file not
                  a generic stream object like *StringIO* instances

        '''

        cdef FILE* fd

        if ostream is None:
            ostream = sys.stdout

        fd = PyFile_AsFile(ostream)
        if fd is NULL:
            raise TypeError('invalid ostream')

        Py_BEGIN_ALLOW_THREADS
        epr_print_record(self._ptr, fd)
        Py_END_ALLOW_THREADS

        pyepr_check_errors()

    def print_element(self, uint field_index, uint element_index, ostream=None):
        '''Write the specified field element to file (default: sys.stdout)

        This method writes formatted contents of the specified field
        element to the *ostream* text file or (default) the ASCII output
        will be printed to standard output (sys.stdout)

        :param field_index:
            the index of field in the record
        :param element_index:
            the index of element in the specified field
        :param ostream:
            the (opened) output file object

        .. note:: the *ostream* parameter have to be a *real* file not
                  a generic stream object like *StringIO* instances

        '''

        cdef FILE* fd

        if ostream is None:
            ostream = sys.stdout

        fd = PyFile_AsFile(ostream)
        if fd is NULL:
            raise TypeError('invalid ostream')

        Py_BEGIN_ALLOW_THREADS
        epr_print_element(self._ptr, field_index, element_index, fd)
        Py_END_ALLOW_THREADS

        pyepr_check_errors()

    #def dump_record(self):
    #    epr_dump_record(self._ptr)
    #    pyepr_check_errors()

    #def dump_element(self, uint field_index, uint element_index):
    #    epr_dump_element(self._ptr, field_index, element_index)
    #    pyepr_check_errors()

    # @TODO: format_record, format_element --> str

    def get_field(self, name):
        '''Gets a field specified by name

        The field is here identified through the given name.
        It contains the field info and all corresponding values.

        :param name:
            the the name of required field
        :returns:
            the specified :class:`Field` or raises an exception
            (:class:`EPRValueError`) if an error occured

        '''

        cdef EPR_SField* field_ptr
        field_ptr = <EPR_SField*>epr_get_field(self._ptr, name)
        if field_ptr is NULL:
            pyepr_null_ptr_error('unable to get field "%s"' % name)

        return new_field(field_ptr, self)

    def get_field_at(self, uint index):
        '''Gets a field at the specified position within the record

        :param index:
            the zero-based index (position within record) of the field
        :returns:
            the field or raises and exception (:class:`EPRValueError`)
            if an error occured

        '''

        cdef EPR_SField* field_ptr
        field_ptr = <EPR_SField*>epr_get_field_at(self._ptr, index)
        if field_ptr is NULL:
            pyepr_null_ptr_error('unable to get field at index %d' % index)

        return new_field(field_ptr, self)


cdef new_record(EPR_SRecord* ptr, object parent=None, bint dealloc=False):
    if ptr is NULL:
        pyepr_null_ptr_error()

    cdef Record instance = Record.__new__(Record)

    instance._ptr = ptr
    instance._parent = parent
    instance._dealloc = dealloc

    return instance


cdef class Raster:
    '''Represents a raster in which data will be stored

    All 'size' parameter are in PIXEL.

    '''

    cdef EPR_SRaster* _ptr
    cdef object _parent

    def __dealloc__(self):
        if self._ptr is not NULL:
            epr_free_raster(self._ptr)

    def __init__(self):
        raise TypeError('"%s" class cannot be instantiated from Python' %
                                                    self.__class__.__name__)

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
        '''Gets the raster's width in pixels'''

        return epr_get_raster_width(self._ptr)

    def get_height(self):
        '''Gets the raster's height in pixels'''

        return epr_get_raster_height(self._ptr)

    def get_elem_size(self):
        '''The size in byte of a single element (sample) of this raster's
        buffer'''

        return epr_get_raster_elem_size(self._ptr)

    def get_pixel(self, int x, int y):
        '''Single pixel access

        This function is for getting the values of the elements of a
        raster (i.e. pixel)

        :param x:
            the (zero-based) X co-ordinate of the pixel
        :param y:
            the (zero-based) Y co-ordinate of the pixel
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
                                                epr_data_type_id_to_str(dtype))

        pyepr_check_errors()    # @TODO: check

        return val

    cdef np.ndarray toarray(self):
        cdef np.NPY_TYPES dtype = _epr_to_numpy_type_id(self._ptr.data_type)
        if dtype == np.NPY_NOTYPE:
            raise TypeError('invalid data type')

        cdef np.npy_intp shape[2]
        shape[0] = self._ptr.raster_height
        shape[1] = self._ptr.raster_width

        cdef np.ndarray result
        result = np.PyArray_SimpleNewFromData(2, shape, dtype,
                                              self._ptr.buffer)

        # Make the ndarray keep a reference to this object
        np.set_array_base(result, self)

        return result

    property data:
        '''Raster data exposed as ``numpy.ndarray`` object

        .. note:: this property shares the data buffer with the
                  :class:`Raster` object so any change in its contents
                  is also reflected to the :class:`Raster` object

        '''

        def __get__(self):
            if self._ptr.buffer is NULL:
                return np.ndarray(())

            return self.toarray()


cdef new_raster(EPR_SRaster* ptr, object parent=None):
    if ptr is NULL:
        pyepr_null_ptr_error()

    cdef Raster instance = Raster.__new__(Raster)

    instance._ptr = ptr
    instance._parent = parent

    return instance


def create_raster(EPR_EDataTypeId data_type, uint src_width, uint src_height,
                  uint xstep=1, uint ystep=1):
    '''Creates a raster of the specified data type

    This function can be used to create any type of raster, e.g. for
    later use as a bit-mask.

    :param data_type:
        the type of the data to stored in the raster, must be one of
        E_TID_*
    :param src_width:
        the width (across track dimension) of the source to be read into
        the raster. See description of epr_create_compatible_raster
    :param src_height:
        the height (along track dimension) of the source to be read into
        the raster. See description of epr_create_compatible_raster
    :param xstep:
        the subsampling step across track of the source when reading
        into the raster
    :param ystep:
        the subsampling step along track of the source when reading
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
    '''Creates a raster to be used for reading bitmasks

    The raster returned always is of type ``byte``.

    :param src_width:
        the width (across track dimension) of the source to be read
        into the raster
    :param src_height:
        the height (along track dimension) of the source to be read
        into the raster
    :param xstep:
        the subsampling step across track of the source when reading
        into the raster
    :param ystep:
        the subsampling step along track of the source when reading
        into the raster
    :returns:
        the new raster instance or raises an exception
        (:class:`EPRValueError`) if an error occured

    .. seealso:: the description of :meth:`Band.create_compatible_raster`

    '''

    if xstep == 0 or ystep == 0:
        raise ValueError('invalid step: xspet=%d, ystep=%d' % (xstep, ystep))

    cdef EPR_SRaster* raster_ptr
    raster_ptr = epr_create_bitmask_raster(src_width, src_height, xstep, ystep)
    if raster_ptr is NULL:
        pyepr_null_ptr_error('unable to create a new raster')

    return new_raster(raster_ptr)


cdef class Band:
    '''The aand of an ENVISAT product

    The Band class contains information about a band within an ENVISAT
    product file which has been opened with the :func:`open` function.

    A new Band instance can be obtained with the :meth:`Product.get_band`
    method.

    '''

    cdef EPR_SBandId* _ptr
    cdef object _parent

    def __init__(self):
        raise TypeError('"%s" class cannot be instantiated from Python' %
                                                    self.__class__.__name__)

    property product_id:
        '''The :class:`Product` instance to which this band belongs to'''

        def __get__(self):
            return self._parent

    # @TODO: complete
    #property dataset_ref:
    #    def __get__(self):
    #        return self._ptr.dataset_ref

    property spectr_band_index:
        '''The (zero-based) spectral band index

        -1 if this is not a spectral band

        '''

        def __get__(self):
            return self._ptr.spectr_band_index

    property sample_model:
        '''The sample model operation

        The sample model operation applied to the source dataset for
        getting the correct samples from the MDS (for example MERIS L2).

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
                return self._ptr.bm_expr

    property unit:
        '''The geophysical unit for the band's pixel values'''

        def __get__(self):
            if self._ptr.unit is NULL:
                return None
            else:
                return self._ptr.unit

    property description:
        '''A short description of the band's contents'''

        def __get__(self):
            if self._ptr.description is NULL:
                return None
            else:
                return self._ptr.description

    property lines_mirrored:
        '''Mirrored lined flag

        If true (=1) lines will be mirrored (flipped) after read into a
        raster in order to ensure a pixel ordering in raster X direction
        from WEST to EAST.

        '''

        def __get__(self):
            return <bint>self._ptr.lines_mirrored

    def get_name(self):
        '''Gets the name of the band'''

        return epr_get_band_name(self._ptr)

    def create_compatible_raster(self, uint src_width, uint src_height,
                                 uint xstep=1, uint ystep=1):
        '''Creates a raster which is compatible with the data type of the band

        The created raster is used to read the data in it (see
        :meth:`Band.read_band_raster`).

        The raster is defined on the grid of the product, from which the
        data are read. Spatial subsets and undersampling are possible)
        through the parameter of the method.

        A raster is an object that allows direct acces to data of a
        certain portion of the ENVISAT product that are read into the it.
        Such a portion is called the source. The complete ENVISAT product
        can be much greater than the source. One can move the raster over
        the complete ENVISAT product and read in turn different parts
        (always of the size of the source) of it into the raster.
        The source is specified by the parameters *height* and *width*.

        A typical example is a processing in blocks. Lets say, a block
        has 64x32 pixel. Then, my source has a width of 64 pixel and a
        height of 32 pixel.

        Another example is a processing of complete image lines. Then,
        my source has a widths of the complete product (for example 1121
        for a MERIS RR product), and a height of 1). One can loop over
        all blocks read into the raster and process it.

        In addition, it is possible to defined a subsampling step for a
        raster. This means, that the source is not read 1:1 into the
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
            the subsampling step across track of the source when reading
            into the raster
        :param ystep:
            the subsampling step along track of the source when reading
            into the raster
        :returns:
            the new raster instance or raises an exception
            (:class:`EPRValueError`) if an error occured

        '''

        # @TODO: improve
        #if width is None:
        #    width = self.product_id.get_scene_width()
        #
        #if height is None:
        #    height = self.product_id.get_scene_height()

        cdef EPR_SRaster* raster_ptr
        raster_ptr = epr_create_compatible_raster(self._ptr,
                                                  src_width, src_height,
                                                  xstep, ystep)
        if raster_ptr is NULL:
            pyepr_null_ptr_error('unable to create compatible raster with '
                                 'width=%d, height=%d xstep=%d, ystep=%d' %
                                        (src_width, src_height, xstep, ystep))

        return new_raster(raster_ptr, self)

    cpdef read_raster(self, int xoffset=0, int yoffset=0, Raster raster=None):
        '''Reads (geo-)physical values of the band of the specified
        source-region

        The source-region is a defined part of the whole ENVISAT product
        image, which shall be read into a raster.
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
            (optional) :class:`Raster` instance set with appropriate
            parameters
        :returns:
            the :class:`Raster` instance in which dara are read

        This method raises an instance of the appropriete :class:`EPRError`
        sub-class if case of errors

        .. seealso:: :meth:`Band.create_compatible_raster` and
                     :func:`create_rater`

        '''

        cdef int ret

        if raster is None:
            raster = self.create_compatible_raster()

        Py_BEGIN_ALLOW_THREADS
        ret = epr_read_band_raster(self._ptr, xoffset, yoffset, raster._ptr)
        Py_END_ALLOW_THREADS

        if ret != 0:
            pyepr_check_errors()

        return raster

    def read_as_array(self, width=None, height=None,
                      uint xoffset=0, uint yoffset=0,
                      uint xstep=1, uint ystep=1):
        '''Rads the specified source region as an numpy.ndarray

        The source-region is a defined part of the whole ENVISAT product
        image, which shall be read into a raster.
        In this routine the co-ordinates are specified, where the
        source-region to be read starts.
        The dimension of the region and the sub-sampling are attributes
        of the raster into which the data are read.

        :param src_width:
            the width (across track dimension) of the source to be read
            into the raster
        :param src_height:
            the height (along track dimension) of the source to be read
            into the raster
        :param xoffset:
            across-track source co-ordinate in pixel co-ordinates
            (zero-based) of the upper right corner of the source-region
        :param yoffset:
            along-track source co-ordinate in pixel co-ordinates
            (zero-based) of the upper right corner of the source-region
        :param xstep:
            the subsampling step across track of the source when reading
            into the raster
        :param ystep:
            the subsampling step along track of the source when reading
            into the raster
        :returns:
            the numpy.ndarray instance in which dara are read

        This method raises an instance of the appropriete :class:`EPRError`
        sub-class if case of errors

        .. seealso:: :meth:`Band.create_compatible_raster`,
                     :func:`create_rater` and :meth:`Band.read_band_raster`

        '''

        if width is None:
            w = self.product_id.get_scene_width()
            if w > xoffset:
                width = w - xoffset
            else:
                raise ValueError('xoffset os larger that he scene width')

        if height is None:
            h = self.product_id.get_scene_height()
            if h > yoffset:
                height = h - yoffset
            else:
                raise ValueError('yoffset os larger that he scene height')

        raster = self.create_compatible_raster(width, height, xstep, ystep)
        self.read_raster(xoffset, yoffset, raster)

        return raster.data


cdef new_band(EPR_SBandId* ptr, object parent=None):
    if ptr is NULL:
        pyepr_null_ptr_error()

    cdef Band instance = Band.__new__(Band)

    instance._ptr = ptr
    instance._parent = parent

    return instance


cdef class Dataset:
    '''ENVISAT dataset

    The Dataset class contains information about a dataset within an
    ENVISAT product file which has been opened with the :func:`open`
    function.

    A new Dataset instance can be obtained with the
    :meth:`Product.get_dataset` or :meth:`Product.get_dataset_at` methods.

    '''

    cdef EPR_SDatasetId* _ptr
    cdef object _parent

    def __init__(self):
        raise TypeError('"%s" class cannot be instantiated from Python' %
                                                    self.__class__.__name__)

    property product_id:
        '''The ID of the product to which this dataset belongs to'''

        def __get__(self):
            return self._parent

    property description:
        '''A short description of the band's contents'''

        def __get__(self):
            if self._ptr.description is NULL:
                return ''
            else:
                return self._ptr.description

    def get_name(self):
        '''Gets the name of the dataset'''

        if self._ptr is not NULL:
            return epr_get_dataset_name(self._ptr)
        return ''

    def get_dsd_name(self):
        '''Gets the name of the DSD (dataset descriptor)'''

        if self._ptr is not NULL:
            return epr_get_dsd_name(self._ptr)
        return ''

    def get_num_records(self):
        '''Gets the number of records of the dataset'''

        if self._ptr is not NULL:
            return epr_get_num_records(self._ptr)
        return 0

    def get_dsd(self):
        '''Gets the dataset descriptor (DSD)'''

        return new_dsd(<EPR_SDSD*>epr_get_dsd(self._ptr), self)

    def create_record(self):
        '''Creates a new record

        Creates a new, empty record with a structure compatible with
        the dataset. Such a record is typically used in subsequent
        calls to :meth:`Dataset.read_record`.

        :returns:
            the new record instance

        '''

        return new_record(epr_create_record(self._ptr), self, True)

    def read_record(self, uint index, Record record=None):
        '''Reads specified record of the dataset

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
            an exception (:class:`EPRValueError`) if an error occured

        '''

        cdef EPR_SRecord* record_ptr = NULL
        if record:
            record_ptr = (<Record>record)._ptr

        Py_BEGIN_ALLOW_THREADS
        record_ptr = epr_read_record(self._ptr, index, record_ptr)
        Py_END_ALLOW_THREADS

        if record_ptr is NULL:
            pyepr_null_ptr_error('unable to read record at index %d' % index)

        if not record:
            record = new_record(record_ptr, self, True)

        return record


cdef new_dataset(EPR_SDatasetId* ptr, object parent=None):
    if ptr is NULL:
        pyepr_null_ptr_error()

    cdef Dataset instance = Dataset.__new__(Dataset)

    instance._ptr = ptr
    instance._parent = parent

    return instance


cdef class Product:
    '''ENVISAT product

    The Product class provides methos and properties to get information
    about an ENVISAT product files.

    .. seealso:: :func:`open`

    '''

    cdef EPR_SProductId* _ptr

    def __cinit__(self, filename, *args, **kargs):

        Py_BEGIN_ALLOW_THREADS
        self._ptr = epr_open_product(filename)
        Py_END_ALLOW_THREADS

        if self._ptr is NULL:
            pyepr_null_ptr_error('unable to open %s' % filename)

    def __dealloc__(self):
        if self._ptr is not NULL:
            epr_close_product(self._ptr)
            pyepr_check_errors()

    property file_path:
        '''The file's path including the file name'''

        def __get__(self):
            if self._ptr.file_path is NULL:
                return None
            else:
                return self._ptr.file_path

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
            return self._ptr.tot_size

    property id_string:
        '''The product identifier string obtained from the MPH parameter
        'PRODUCT'

        The first 10 characters of this string identify the product type,
        e.g. "MER_1P__FR" for a MERIS Level 1b full resolution product.
        The rest of the string decodes product instance properties.

        '''

        def __get__(self):
            if self._ptr.id_string is NULL:
                return None
            else:
                return self._ptr.id_string

    property meris_iodd_version:
        '''For MERIS L1b and RR and FR to provide backward compatibility'''

        def __get__(self):
            return self._ptr.meris_iodd_version

    def get_scene_width(self):
        '''Gets the product's scene width in pixels'''

        return epr_get_scene_width(self._ptr)

    def get_scene_height(self):
        '''Gets the product's scene height in pixels'''

        return epr_get_scene_height(self._ptr)

    def get_num_datasets(self):
        '''Gets the number of all datasets contained in a product'''

        return epr_get_num_datasets(self._ptr)

    def get_num_dsds(self):
        '''Gets the number of all DSDs (dataset descriptors) contained
        in the product'''

        return epr_get_num_dsds(self._ptr)

    def get_num_bands(self):
        '''Gets the number of all bands contained in a product'''

        return epr_get_num_bands(self._ptr)

    def get_dataset_at(self, uint index):
        '''Gets the dataset at the specified position within the product

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
        '''Gets the dataset coresponding to the specified dataset name

        :param name:
            the dataset name
        :returns:
            the requested :class:`Dataset` instance

        '''

        cdef EPR_SDatasetId* dataset_id
        dataset_id = epr_get_dataset_id(self._ptr, name)
        if dataset_id is NULL:
            pyepr_null_ptr_error('unable to get dataset "%s"' % name)

        return new_dataset(dataset_id, self)

    def get_dsd_at(self, uint index):
        '''Gets the DSD at the specified position

        Gets the DSD (dataset descriptor) at the specified position
        within the product.

        :param index:
            the index identifying the position of the DSD, starting
            with 0, must not be negative
        :returns:
            the requested :class:`DSD` instance

        '''

        cdef EPR_SDSD* dsd_ptr
        dsd_ptr = epr_get_dsd_at(self._ptr, index)
        if dsd_ptr is NULL:
            pyepr_null_ptr_error('unable to get DSD at index "%d"' % index)

        return new_dsd(dsd_ptr, self)

    def get_mph(self):
        '''The :class:`Record` representing the main product header (MPH)'''

        cdef EPR_SRecord* record_ptr
        record_ptr = epr_get_mph(self._ptr)
        if record_ptr is NULL:
            pyepr_null_ptr_error('unable to get MPH record')

        return new_record(record_ptr, self, False)

    def get_sph(self):
        '''The :class:`Record` representing the specific product header (SPH)'''

        cdef EPR_SRecord* record_ptr
        record_ptr = epr_get_sph(self._ptr)
        if record_ptr is NULL:
            pyepr_null_ptr_error('unable to get SPH record')

        return new_record(record_ptr, self, False)

    def get_band(self, name):
        '''Gets the band corresponding to the specified name.

        :param name:
            the name of the band, must not be <code>NULL</code>
        :returns:
            the requested :class:`Band` instance, or taises a
            :class:`EPRValueError` if not found

        '''

        cdef EPR_SBandId* band_id
        band_id = epr_get_band_id(self._ptr, name)
        if band_id is NULL:
            pyepr_null_ptr_error('unable to get band "%s"' % name)

        return new_band(band_id, self)

    def get_band_at(self, uint index):
        '''Gets the band at the specified position within the product

        :param index:
            the index identifying the position of the band, starting
            with 0, must not be negative
        :returns:
            the requested :class:`Band` instance, or raises a
            :class:`EPRValueError` if not found

        '''

        cdef EPR_SBandId* band_id
        band_id = epr_get_band_id_at(self._ptr, index)
        if band_id is NULL:
            pyepr_null_ptr_error('unable to get band at index "%d"' % index)

        return new_band(band_id, self)

    # @TODO: add to high evel interface
    #def get_band_ids(self):
    #    cdef EPR_SBandId band_ptr
    #    cder int idx
    #    names = []
    #    for idx in range(self.get_num_bands()):
    #        band_ptr = epr_get_band_id(self._ptr, idx)
    #        names.apped(epr_get_band_name(band_ptr))
    #    return names

    # @TODO: complete and make it more pythonic
    #def read_bitmask_raster(self, bm_expr, int xoffset, int yoffset,
    #                        Raster raster not Null):
    #    '''Calculates a bit-mask raster
    #
    #    Calculates a bit-mask, composed of flags of the given product
    #    and combined as described in the given bit-mask expression, for
    #    the a certain dimension and sub-sampling as defined in the
    #    given raster.
    #
    #    :param bm_expr:
    #        a string holding the logical expression for the defintion
    #        of the bit-mask. In a bit-mask expression, any number of
    #        the flag-names (found in the DDDB) can be composed with
    #        "(", ")", "NOT", "AND", "OR". Valid bit-mask expression are
    #        for example::
    #
    #            flags.LAND OR flags.CLOUD
    #
    #       or::
    #
    #           NOT flags.WATER AND flags.TURBID_S
    #
    #   :param xoffset:
    #       across-track co-ordinate in pixel co-ordinates (zero-based)
    #       of the upper right corner of the source-region
    #   :param yoffset:
    #       along-track co-ordinate in pixel co-ordinates (zero-based)
    #       of the upper right corner of the source-region
    #   :param raster:
    #       the raster for the bit-mask. The data type of the raster
    #       must be either e_tid_uchar or e_tid_char
    #   :returns:
    #       zero for success, an error code otherwise
    #
    #   .. seealso: :func:`create_band_raster`
    #
    #   '''
    #
    #    cdef int ret = epr_read_bitmask_raster(self._ptr, bm_expr,
    #                                           xoffset, yoffset,
    #                                           (<Raster>raster)._ptr)
    #    if ret != 0:
    #        pyepr_check_errors()
    #
    #    return raster


def open(filename):
    '''Opens the ENVISAT product

    Opens the ENVISAT product file with the given file path, reads MPH,
    SPH and all DSDs, organized the table with parameter of line length
    and tie points number.

    :param product_file_path:
        the path to the ENVISAT product file
    :returns:
        the :class:`Product` instance representing the specified
        product. An exception (:class:`ValueError`) is raised if the
        file could not be opened.

    '''

    return Product(filename)

# library initialization
_init_api()

import atexit
atexit.register(_close_api)
del atexit
