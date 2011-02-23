cdef extern from 'Python.h':
    ctypedef struct FILE
    FILE* PyFile_AsFile(object)

cdef extern from 'epr_api.h':
    ctypedef unsigned char  uchar
    ctypedef unsigned short ushort
    ctypedef unsigned int   uint
    #ctypedef unsigned long  ulong

    enum EPR_ErrCode:
        e_err_none = 0

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

    enum EPR_ELogLevel:
        e_log_debug   = -1
        e_log_info    =  0
        e_log_warning =  1
        e_log_error   =  2

    struct EPR_ProductId:
        pass

    struct EPR_DatasetId:
        pass

    struct EPR_BandId:
        pass

    struct EPR_Record:
        pass

    struct EPR_Field:
        pass

    #struct EPR_DSD:
    #    pass

    struct EPR_Time:
        int  days
        uint seconds
        uint microseconds

    ctypedef EPR_ErrCode    EPR_EErrCode
    ctypedef EPR_DataTypeId EPR_EDataTypeId
    ctypedef EPR_ProductId  EPR_SProductId
    ctypedef EPR_DatasetId  EPR_SDatasetId
    ctypedef EPR_BandId     EPR_SBandId
    ctypedef EPR_Record     EPR_SRecord
    ctypedef EPR_Field      EPR_SField
    #ctypedef EPR_DSD        EPR_SDSD
    ctypedef EPR_Time       EPR_STime

    # @TODO: improve logging and error management (--> custom handlers)
    # logging and error handling function pointers
    ctypedef void (*EPR_FLogHandler)(EPR_ELogLevel, char*)
    ctypedef void (*EPR_FErrHandler)(EPR_EErrCode, char*)

    # logging
    #~ int epr_set_log_level(EPR_ELogLevel log_level)
    #~ void epr_set_log_handler(EPR_FLogHandler log_handler)
    void epr_log_message(EPR_ELogLevel, char*)

    # error handling
    #~ void epr_set_err_handler(EPR_FErrHandler err_handler)
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
    #EPR_SDSD* epr_get_dsd_at(EPR_SProductId*, uint)
    EPR_SRecord* epr_get_mph(EPR_SProductId*)
    EPR_SRecord* epr_get_sph(EPR_SProductId*)

    uint epr_get_num_bands(EPR_SProductId*)
    #~ EPR_SBandId* epr_get_band_id_at(EPR_SProductId*, uint)
    #~ EPR_SBandId* epr_get_band_id(EPR_SProductId*, char*)
    #~ int epr_read_bitmask_raster(EPR_SProductId* product_id, char* bm_expr, int offset_x, int offset_y, EPR_SRaster* raster);

    # DATASET
    char* epr_get_dataset_name(EPR_SDatasetId*)
    char* epr_get_dsd_name(EPR_SDatasetId*)
    uint epr_get_num_records(EPR_SDatasetId*)
    #EPR_SDSD* epr_get_dsd(EPR_SDatasetId*)
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

    #uint epr_copy_field_elems_as_ints(EPR_SField*, int*, uint)
    #uint epr_copy_field_elems_as_uints(EPR_SField*, uint*, uint)
    #uint epr_copy_field_elems_as_floats(EPR_SField*, float*, uint)
    #uint epr_copy_field_elems_as_doubles(EPR_SField*, double*, uint)

    # BAND
    #~ EPR_SRaster* epr_create_compatible_raster(EPR_SBandId* band_id,
                                              #~ uint source_width,
                                              #~ uint source_height,
                                              #~ uint source_step_x,
                                              #~ uint source_step_y)
    #~ EPR_SRaster* epr_create_raster(EPR_EDataTypeId data_type,
                                   #~ uint source_width,
                                   #~ uint source_height,
                                   #~ uint source_step_x,
                                   #~ uint source_step_y)
    #~ EPR_SRaster* epr_create_bitmask_raster(uint source_width,
                                           #~ uint source_height,
                                           #~ uint source_step_x,
                                           #~ uint source_step_y)
    #~ int epr_read_band_raster(EPR_SBandId* band_id,
                             #~ int offset_x,
                             #~ int offset_y,
                             #~ EPR_SRaster* raster)

    #~ const char* epr_get_band_name(EPR_SBandId* band_id)

    # RASTER
    #~ uint epr_get_raster_elem_size(const EPR_SRaster* raster)
    #~ void* epr_get_raster_elem_addr(const EPR_SRaster* raster, uint offset)
    #~ void* epr_get_raster_pixel_addr(const EPR_SRaster* raster, uint x, uint y)
    #~ void* epr_get_raster_line_addr(const EPR_SRaster* raster, uint y)
    #~ uint epr_get_raster_width(EPR_SRaster* raster)
    #~ uint epr_get_raster_height(EPR_SRaster* raster)
    #~ void epr_free_raster(EPR_SRaster* raster)

    #~ uint epr_get_pixel_as_uint(const EPR_SRaster* raster, int x, int y)
    #~ int epr_get_pixel_as_int(const EPR_SRaster* raster, int x, int y)
    #~ float epr_get_pixel_as_float(const EPR_SRaster* raster, int x, int y)
    #~ double epr_get_pixel_as_double(const EPR_SRaster* raster, int x, int y)


import sys
import collections
import numpy as np
cimport numpy as np


# utils
EPRTime = collections.namedtuple('EPRTime', ('days', 'seconds', 'microseconds'))


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


class EPRError(Exception):
    def __init__(self, message='', code=None, *args, **kargs):
        super(EPRError, self).__init__(message, code, *args, **kargs)
        self.code = code


cdef int pyepr_check_errors() except -1:
    # @TODO: fine tuning of exceptions
    cdef int code
    code = epr_get_last_err_code()
    if code != e_err_none:
        msg = epr_get_last_err_message()
        epr_clear_err()
        raise EPRError(msg, epr_get_last_err_code())
        return -1
    return 0

cdef int pyepr_null_ptr_error(msg='null pointer') except -1:
    cdef char* eprmsg = <char*>epr_get_last_err_message()
    epr_clear_err()
    raise ValueError('%s: %s' % (msg, eprmsg))
    return -1


# library API initialization/finalization
def _init_api():
    #if epr_init_api(e_log_warning, epr_log_message, NULL):
    if epr_init_api(e_log_warning, NULL, NULL):
        msg = epr_get_last_err_message()
        epr_clear_err()
        raise ImportError('unable to inizialize EPR API library: %s' % msg)

def _close_api():
    epr_close_api()
    pyepr_check_errors()

def get_data_type_size(EPR_EDataTypeId type_id):
    return epr_get_data_type_size(type_id)

def data_type_id_to_str(EPR_EDataTypeId type_id):
    return epr_data_type_id_to_str(type_id)


#cdef class DSD:
#    cdef EPR_SDSD* _dsd_id


cdef class Field:
    cdef EPR_SField* _ptr
    cdef public object _parent

    def print_field(self, ostream=None):
        cdef FILE* fd

        if ostream is None:
            ostream = sys.stdout

        fd = PyFile_AsFile(ostream)
        if fd is NULL:
            raise TypeError('invalid ostream')

        epr_print_field(self._ptr, fd)
        pyepr_check_errors()

    #def dump_field(self):
    #    epr_dump_field(self._ptr)
    #    pyepr_check_errors()

    def get_field_unit(self):
        return epr_get_field_unit(self._ptr)

    def get_field_description(self):
        return epr_get_field_description(self._ptr)

    def get_field_num_elems(self):
        return epr_get_field_num_elems(self._ptr)

    def get_field_name(self):
        return epr_get_field_name(self._ptr)

    def get_field_type(self):
        return epr_get_field_type(self._ptr)

    def get_field_elem(self, uint index=0):
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

    def get_field_elems(self):
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

    #~ uint epr_copy_field_elems_as_ints(const EPR_SField* field, int* buffer, uint num_elems)
    #~ uint epr_copy_field_elems_as_uints(const EPR_SField* field, uint* buffer, uint num_elems)
    #~ uint epr_copy_field_elems_as_floats(const EPR_SField* field, float* buffer, uint num_elems)
    #~ uint epr_copy_field_elems_as_doubles(const EPR_SField* field, double* buffer, uint num_elems)


cdef class Record:
    cdef EPR_SRecord* _ptr
    cdef public object _parent

    def __dealloc__(self):
        if self._ptr:
            epr_free_record(self._ptr)
            pyepr_check_errors()

    def get_num_fields(self):
        return epr_get_num_fields(self._ptr)

    def print_record(self, ostream=None):
        cdef FILE* fd

        if ostream is None:
            ostream = sys.stdout

        fd = PyFile_AsFile(ostream)
        if fd is NULL:
            raise TypeError('invalid ostream')

        epr_print_record(self._ptr, fd)
        pyepr_check_errors()

    def print_element(self, uint field_index, uint element_index, ostream=None):
        cdef FILE* fd

        if ostream is None:
            ostream = sys.stdout

        fd = PyFile_AsFile(ostream)
        if fd is NULL:
            raise TypeError('invalid ostream')

        epr_print_element(self._ptr, field_index, element_index, fd)
        pyepr_check_errors()

    #def dump_record(self):
    #    epr_dump_record(self._ptr)
    #    pyepr_check_errors()

    #def dump_element(self, uint field_index, uint element_index):
    #    epr_dump_element(self._ptr, field_index, element_index)
    #    pyepr_check_errors()

    # @TODO: format_record, format_element --> str

    def get_field(self, name):
        cdef EPR_SField* ptr
        ptr = <EPR_SField*>epr_get_field(self._ptr, name)
        if ptr is NULL:
            pyepr_null_ptr_error('unable to get field "%s"' % name)

        field = Field()
        (<Field>field)._ptr = ptr
        field._parent = self

        return field

    def get_field_at(self, uint index):
        cdef EPR_SField* ptr
        ptr = <EPR_SField*>epr_get_field_at(self._ptr, index)
        if ptr is NULL:
            pyepr_null_ptr_error('unable to get field at index %d' % index)

        field = Field()
        (<Field>field)._ptr = ptr
        field._parent = self

        return field


cdef class Dataset:
    cdef EPR_SDatasetId* _ptr
    cdef public object _parent

    def get_dataset_name(self):
        if self._ptr:
            return epr_get_dataset_name(self._ptr)
        return ''

    def get_dsd_name(self):
        if self._ptr:
            return epr_get_dsd_name(self._ptr)
        return ''

    def get_num_records(self):
        if self._ptr:
            return epr_get_num_records(self._ptr)
        return 0

    #def get_dsd(self):
    #    cdef EPR_SDSD* dsd_id
    #    # cast is used to silence warnings about constness
    #    dsd_id = <EPR_SDSD*>epr_get_dsd(self._ptr)
    #    if dsd_id is NULL:
    #        pyepr_null_ptr_error('unable to get DSD')
    #
    #    dsd = DSD()
    #    (<DSD>dsd)._dsd_id = dsd_id
    #    return dsd

    def create_record(self):
        record = Record()
        (<Record>record)._ptr = epr_create_record(self._ptr)
        pyepr_check_errors()
        record._parent = self
        return record

    def read_record(self, uint index, record=None):
        if record is None:
            record = self.create_record()

        (<Record>record)._ptr = epr_read_record(self._ptr, index,
                                                (<Record>record)._ptr)
        if (<Record>record)._ptr is NULL:
            pyepr_null_ptr_error('unable to read record at index %d' % index)
        return record


cdef class Product:
    cdef EPR_SProductId* _ptr

    def __cinit__(self, filename, *args, **kargs):
        self._ptr = epr_open_product(filename)
        if self._ptr is NULL:
            pyepr_null_ptr_error('unable to open %s' % filename)

    def __dealloc__(self):
        if self._ptr:
            epr_close_product(self._ptr)
            pyepr_check_errors()

    def get_scene_width(self):
        return epr_get_scene_width(self._ptr)

    def get_scene_height(self):
        return epr_get_scene_height(self._ptr)

    def get_num_datasets(self):
        return epr_get_num_datasets(self._ptr)

    def get_num_dsds(self):
        return epr_get_num_dsds(self._ptr)

    def get_num_bands(self):
        return epr_get_num_bands(self._ptr)

    def get_dataset_at(self, uint index):
        cdef EPR_SDatasetId* dataset_id
        dataset_id = epr_get_dataset_id_at(self._ptr, index)
        if dataset_id is NULL:
            pyepr_null_ptr_error('unable to get dataset at index %d' % index)

        dataset = Dataset()
        (<Dataset>dataset)._ptr = dataset_id
        dataset._parent = self

        return dataset

    def get_dataset(self, name):
        cdef EPR_SDatasetId* dataset_id
        dataset_id = epr_get_dataset_id(self._ptr, name)
        if dataset_id is NULL:
            pyepr_null_ptr_error('unable to get dataset "%s"' % name)

        dataset = Dataset()
        (<Dataset>dataset)._ptr = dataset_id
        dataset._parent = self

        return dataset

    #def get_dsd_at(self, uint index):
    #    cdef EPR_SDSD* dsd_id
    #    dsd_id = epr_get_dsd_at(self._ptr, index)
    #    if dsd_id is NULL:
    #        pyepr_null_ptr_error('unable to get DSD at index "%d"' % index)
    #
    #    dsd = DSD()
    #    (<DSD>dsd)._dsd_id = dsd_id
    #
    #    return dsd


    #~ EPR_SRecord* epr_get_mph(const EPR_SProductId* product_id)
    #~ EPR_SRecord* epr_get_sph(const EPR_SProductId* product_id)
    #~ EPR_SBandId* epr_get_band_id_at(EPR_SProductId* product_id, uint index)
    #~ EPR_SBandId* epr_get_band_id(EPR_SProductId* product_id, const char* band_name)

    #~ def read_bitmask_raster(self, bm_expr, offset_x, offset_y, raster):
        #~ return epr_read_bitmask_raster(self._ptr,
                                #~ const char* bm_expr,
                                #~ int offset_x,
                                #~ int offset_y,
                                #~ EPR_SRaster* raster)



def open(filename):
    return Product(filename)

# library initialization
_init_api()

import atexit
atexit.register(_close_api)
del atexit
