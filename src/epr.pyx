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

    struct EPR_Raster:
        EPR_DataTypeId data_type
        uint raster_width
        uint raster_height

    struct EPR_Record:
        pass

    struct EPR_Field:
        pass

    struct EPR_DSD:
        pass

    struct EPR_Time:
        int  days
        uint seconds
        uint microseconds

    ctypedef EPR_ErrCode    EPR_EErrCode
    ctypedef EPR_DataTypeId EPR_EDataTypeId
    ctypedef EPR_ProductId  EPR_SProductId
    ctypedef EPR_DatasetId  EPR_SDatasetId
    ctypedef EPR_BandId     EPR_SBandId
    ctypedef EPR_Raster     EPR_SRaster
    ctypedef EPR_Record     EPR_SRecord
    ctypedef EPR_Field      EPR_SField
    ctypedef EPR_DSD        EPR_SDSD
    ctypedef EPR_Time       EPR_STime

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


class EPRValueError(EPRError, ValueError):
    pass


cdef int pyepr_check_errors() except -1:
    cdef int code
    code = epr_get_last_err_code()
    if code != e_err_none:
        msg = epr_get_last_err_message()
        epr_clear_err()
        if 203 <= code < 220 or code in (1, 2, 5):
            raise EPRValueError(msg, epr_get_last_err_code())
        else:
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


# @TODO: complete
#cdef class DSD:
#    cdef EPR_SDSD* _ptr


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

    # @TODO: use tuples insteac od ndarrays
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


cdef class Record:
    cdef EPR_SRecord* _ptr
    cdef public object _parent
    cdef public bool _dealloc

    #def __cinit__(self, *args, **kargs):
    #    self._dealloc = True

    def __dealloc__(self):
        if not self._dealloc:
            return

        if self._ptr is not NULL:
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
        cdef EPR_SField* field_ptr
        field_ptr = <EPR_SField*>epr_get_field(self._ptr, name)
        if field_ptr is NULL:
            pyepr_null_ptr_error('unable to get field "%s"' % name)

        field = Field()
        (<Field>field)._ptr = field_ptr
        (<Field>field)._parent = self

        return field

    def get_field_at(self, uint index):
        cdef EPR_SField* field_ptr
        field_ptr = <EPR_SField*>epr_get_field_at(self._ptr, index)
        if field_ptr is NULL:
            pyepr_null_ptr_error('unable to get field at index %d' % index)

        field = Field()
        (<Field>field)._ptr = field_ptr
        (<Field>field)._parent = self

        return field


cdef class Raster:
    cdef EPR_SRaster* _ptr
    cdef public object _parent

    def __dealloc__(self):
        if self._ptr is not NULL:
            epr_free_raster(self._ptr)

    def get_raster_width(self):
        return epr_get_raster_width(self._ptr)

    def get_raster_height(self):
        return epr_get_raster_height(self._ptr)

    def get_raster_data_type(self):
        return self._ptr.data_type

    def get_raster_elem_size(self):
        return epr_get_raster_elem_size(self._ptr)

    def get_pixel(self, int x, int y):
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

    #void* epr_get_raster_elem_addr(self._ptr, uint offset)
    #void* epr_get_raster_pixel_addr(self._ptr, uint x, uint y)
    #void* epr_get_raster_line_addr(self._ptr, uint y)

    # @TODO: __getitem__ with generalized slicing


def create_raster(EPR_EDataTypeId data_type, uint src_width, uint src_height,
                  uint xstep=1, uint ystep=1):

    if xstep == 0 or ystep ==0:
        raise ValueError('invalid step: xspet=%d, ystep=%d' % (xstep, ystep))

    cdef EPR_SRaster* raster_ptr
    raster_ptr = epr_create_raster(data_type, src_width, src_height,
                                   xstep, ystep)
    if raster_ptr is NULL:
        pyepr_null_ptr_error('unable to create a new raster')

    raster = Raster()
    (<Raster>raster)._ptr = raster_ptr

    return raster

def create_bitmask_raster(uint src_width, uint src_height,
                          uint xstep=1, uint ystep=1):

    if xstep == 0 or ystep ==0:
        raise ValueError('invalid step: xspet=%d, ystep=%d' % (xstep, ystep))

    cdef EPR_SRaster* raster_ptr
    raster_ptr = epr_create_bitmask_raster(src_width, src_height, xstep, ystep)
    if raster_ptr is NULL:
        pyepr_null_ptr_error('unable to create a new raster')

    raster = Raster()
    (<Raster>raster)._ptr = raster_ptr

    return raster


cdef class Band:
    cdef EPR_SBandId* _ptr
    cdef public object _parent

    def get_band_name(self):
        return epr_get_band_name(self._ptr)

    def create_compatible_raster(self, uint width, uint height,
                                 uint xstep=1, uint ystep=1):
        cdef EPR_SRaster* raster_ptr
        raster_ptr = epr_create_compatible_raster(self._ptr, width, height,
                                                  xstep, ystep)
        if raster_ptr is NULL:
            pyepr_null_ptr_error('unable to create compatible raster with '
                                 'width=%d, height=%d xstep=%d, ystep=%d' %
                                                (width, height, xstep, ystep))

        raster = Raster()
        (<Raster>raster)._ptr = raster_ptr
        (<Raster>raster)._parent = self

        return raster

    # @TODO: make it more pythonic
    def read_band_raster(self, int xoffset, int yoffset, raster):
        if not isinstance(raster, Raster):
            raise TypeError('raster parameter is not an instance of epr.Raster')

        cdef int ret
        ret = epr_read_band_raster(self._ptr, xoffset, yoffset,
                                   (<Raster>raster)._ptr)
        if ret != 0:
            pyepr_check_errors()

        return raster


cdef class Dataset:
    cdef EPR_SDatasetId* _ptr
    cdef public object _parent

    def get_dataset_name(self):
        if self._ptr is not NULL:
            return epr_get_dataset_name(self._ptr)
        return ''

    def get_dsd_name(self):
        if self._ptr is not NULL:
            return epr_get_dsd_name(self._ptr)
        return ''

    def get_num_records(self):
        if self._ptr is not NULL:
            return epr_get_num_records(self._ptr)
        return 0

    # @TODO: complete
    #def get_dsd(self):
    #    cdef EPR_SDSD* dsd_ptr
    #    # cast is used to silence warnings about constness
    #    dsd_ptr = <EPR_SDSD*>epr_get_dsd(self._ptr)
    #    if dsd_ptr is NULL:
    #        pyepr_null_ptr_error('unable to get DSD')
    #
    #    dsd = DSD()
    #    (<DSD>dsd)._ptr = dsd_ptr
    #
    #    return dsd

    def create_record(self):
        cdef EPR_Record* record_ptr
        record_ptr = epr_create_record(self._ptr)
        if record_ptr is NULL:
            pyepr_null_ptr_error('unable to create a new record')

        record = Record()
        (<Record>record)._ptr = record_ptr
        (<Record>record)._dealloc = True
        (<Record>record)._parent = self   # None    # @TODO: check

        return record

    def read_record(self, uint index, record=None):
        cdef EPR_SRecord* record_ptr = NULL
        if record:
            if not isinstance(record, Record):
                raise TypeError('record parameter is not an instance of '
                                'epr.Record')
            record_ptr = (<Record>record)._ptr
        else:
            record = Record()
            (<Record>record)._dealloc = True

        record_ptr = epr_read_record(self._ptr, index, record_ptr)
        if record_ptr is NULL:
            pyepr_null_ptr_error('unable to read record at index %d' % index)

        # @TODO: fix
        # dealloc existing structure
        #~ if (<Record>record)._ptr is not NULL and (<Record>record)._dealloc:
            #~ epr_free_record((<Record>record)._ptr)
            #~ pyepr_check_errors()

        (<Record>record)._ptr = record_ptr
        (<Record>record)._parent = self   # None    # @TODO: check

        return record


cdef class Product:
    cdef EPR_SProductId* _ptr

    def __cinit__(self, filename, *args, **kargs):
        self._ptr = epr_open_product(filename)
        if self._ptr is NULL:
            pyepr_null_ptr_error('unable to open %s' % filename)

    def __dealloc__(self):
        if self._ptr is not NULL:
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
        (<Dataset>dataset)._parent = self

        return dataset

    def get_dataset(self, name):
        cdef EPR_SDatasetId* dataset_id
        dataset_id = epr_get_dataset_id(self._ptr, name)
        if dataset_id is NULL:
            pyepr_null_ptr_error('unable to get dataset "%s"' % name)

        dataset = Dataset()
        (<Dataset>dataset)._ptr = dataset_id
        (<Dataset>dataset)._parent = self

        return dataset

    #def get_dsd_at(self, uint index):
    #    cdef EPR_SDSD* dsd_ptr
    #    dsd_ptr = epr_get_dsd_at(self._ptr, index)
    #    if dsd_ptr is NULL:
    #        pyepr_null_ptr_error('unable to get DSD at index "%d"' % index)
    #
    #    dsd = DSD()
    #    (<DSD>dsd)._ptr = dsd_ptr
    #
    #    return dsd

    def get_mph(self):
        cdef EPR_SRecord* record_ptr
        record_ptr = epr_get_mph(self._ptr)
        if record_ptr is NULL:
            pyepr_null_ptr_error('unable to get MPH record')

        record = Record()
        (<Record>record)._ptr = record_ptr
        (<Record>record)._dealloc = False
        (<Record>record)._parent = self   # None    # @TODO: check

        return record

    def get_sph(self):
        cdef EPR_SRecord* record_ptr
        record_ptr = epr_get_sph(self._ptr)
        if record_ptr is NULL:
            pyepr_null_ptr_error('unable to get SPH record')

        record = Record()
        (<Record>record)._ptr = record_ptr
        (<Record>record)._dealloc = False
        (<Record>record)._parent = self   # None    # @TODO: check

        return record

    def get_band_id(self, name):
        cdef EPR_SBandId* band_id
        band_id = epr_get_band_id(self._ptr, name)
        if band_id is NULL:
            pyepr_null_ptr_error('unable to get band "%s"' % name)

        band = Band()
        (<Band>band)._ptr = band_id
        (<Band>band)._parent = self

        return band

    def get_band_id_at(self, uint index):
        cdef EPR_SBandId* band_id
        band_id = epr_get_band_id_at(self._ptr, index)
        if band_id is NULL:
            pyepr_null_ptr_error('unable to get band at index "%d"' % index)

        band = Band()
        (<Band>band)._ptr = band_id
        (<Band>band)._parent = self

        return band

    # @TODO: complete and make it more pythonic
    #def read_bitmask_raster(self, bm_expr, int xoffset, int yoffset, raster):
    #    cdef int ret = epr_read_bitmask_raster(self._ptr, bm_expr,
    #                                           xoffset, yoffset,
    #                                           (<Raster>raster)._ptr)
    #    if ret != 0:
    #        pyepr_check_errors()
    #
    #    return raster


def open(filename):
    return Product(filename)

# library initialization
_init_api()

import atexit
atexit.register(_close_api)
del atexit
