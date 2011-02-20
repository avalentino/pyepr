cdef extern from 'Python.h':
    ctypedef struct FILE
    FILE* PyFile_AsFile(object)

cdef extern from 'epr_api.h':
    enum EPR_ErrCode:
        e_err_none = 0

    struct EPR_ProductId:
        pass

    struct EPR_DatasetId:
        pass

    struct EPR_BandId:
        pass

    struct EPR_Record:
        pass

    #struct EPR_DSD:
    #    pass

    ctypedef EPR_ErrCode   EPR_EErrCode
    ctypedef EPR_ProductId EPR_SProductId
    ctypedef EPR_DatasetId EPR_SDatasetId
    ctypedef EPR_BandId    EPR_SBandId
    ctypedef EPR_Record    EPR_SRecord
    #ctypedef EPR_DSD       EPR_SDSD

    ctypedef unsigned int uint

    enum EPR_ELogLevel:
        e_log_debug   = -1
        e_log_info    =  0
        e_log_warning =  1
        e_log_error   =  2

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
    #~ const EPR_SField* epr_get_field(const EPR_SRecord* record, const char* field_name)
    #~ const EPR_SField* epr_get_field_at(const EPR_SRecord* record, uint field_index)

    # FIELD
    #~ void epr_print_field(EPR_SField*, FILE*)
    #~ void epr_dump_field(EPR_SField*)

    #~ char* epr_get_field_unit(EPR_SField*)
    #~ char* epr_get_field_description(EPR_SField*)
    #~ uint epr_get_field_num_elems(EPR_SField*)
    #~ char* epr_get_field_name(EPR_SField*)
    #~ EPR_EDataTypeId epr_get_field_type(const EPR_SField* field)

    #~ char epr_get_field_elem_as_char(const EPR_SField* field, uint elem_index)
    #~ uchar epr_get_field_elem_as_uchar(const EPR_SField* field, uint elem_index)
    #~ short epr_get_field_elem_as_short(const EPR_SField* field, uint elem_index)
    #~ ushort epr_get_field_elem_as_ushort(const EPR_SField* field, uint elem_index)
    #~ int epr_get_field_elem_as_int(const EPR_SField* field, uint elem_index)
    #~ uint epr_get_field_elem_as_uint(const EPR_SField* field, uint elem_index)
    #~ float epr_get_field_elem_as_float(const EPR_SField* field, uint elem_index)
    #~ double epr_get_field_elem_as_double(const EPR_SField* field, uint elem_index)
    #~ const EPR_STime* epr_get_field_elem_as_mjd(const EPR_SField* field)
    #~ const char* epr_get_field_elem_as_str(const EPR_SField* field)

    #~ const char* epr_get_field_elems_char(const EPR_SField* field)
    #~ const uchar* epr_get_field_elems_uchar(const EPR_SField* field)
    #~ const short* epr_get_field_elems_short(const EPR_SField* field)
    #~ const ushort* epr_get_field_elems_ushort(const EPR_SField* field)
    #~ const int* epr_get_field_elems_int(const EPR_SField* field)
    #~ const uint* epr_get_field_elems_uint(const EPR_SField* field)
    #~ const float* epr_get_field_elems_float(const EPR_SField* field)
    #~ const double* epr_get_field_elems_double(const EPR_SField* field)

    #~ uint epr_copy_field_elems_as_ints(const EPR_SField* field, int* buffer, uint num_elems)
    #~ uint epr_copy_field_elems_as_uints(const EPR_SField* field, uint* buffer, uint num_elems)
    #~ uint epr_copy_field_elems_as_floats(const EPR_SField* field, float* buffer, uint num_elems)
    #~ uint epr_copy_field_elems_as_doubles(const EPR_SField* field, double* buffer, uint num_elems)

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

    # DATATYPE
    #~ uint epr_get_data_type_size(EPR_EDataTypeId data_type_id)
    #~ const char* epr_data_type_id_to_str(EPR_EDataTypeId data_type_id)


import sys

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

def _init_api():
    #if epr_init_api(e_log_warning, epr_log_message, NULL):
    if epr_init_api(e_log_warning, NULL, NULL):
        msg = epr_get_last_err_message()
        epr_clear_err()
        raise ImportError('unable to inizialize EPR API library: %s' % msg)


def _close_api():
    epr_close_api()
    pyepr_check_errors()


#cdef class DSD:
#    cdef EPR_SDSD* _dsd_id

cdef class Record:
    cdef EPR_SRecord* _ptr
    cdef public object _parent

    def __cinit__(self):
        self._parent = None

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

    #~ const EPR_SField* epr_get_field(const EPR_SRecord* record, const char* field_name)
    #~ const EPR_SField* epr_get_field_at(const EPR_SRecord* record, uint field_index)


cdef class Dataset:
    cdef EPR_SDatasetId* _dataset_id
    cdef public object _parent

    def get_dataset_name(self):
        if self._dataset_id:
            return epr_get_dataset_name(self._dataset_id)
        return ''

    def get_dsd_name(self):
        if self._dataset_id:
            return epr_get_dsd_name(self._dataset_id)
        return ''

    def get_num_records(self):
        if self._dataset_id:
            return epr_get_num_records(self._dataset_id)
        return 0

    #def get_dsd(self):
    #    cdef EPR_SDSD* dsd_id
    #    # cast is used to silence warnings about constness
    #    dsd_id = <EPR_SDSD*>epr_get_dsd(self._dataset_id)
    #    if dsd_id is NULL:
    #        raise EPRError('unable to get DSD')
    #
    #    dsd = DSD()
    #    (<DSD>dsd)._dsd_id = dsd_id
    #    return dsd

    def create_record(self):
        record = Record()
        (<Record>record)._ptr = epr_create_record(self._dataset_id)
        pyepr_check_errors()
        record._parent = self
        return record

    def read_record(self, uint index, record=None):
        if record is None:
            record = self.create_record()

        (<Record>record)._ptr = epr_read_record(self._dataset_id, index,
                                                (<Record>record)._ptr)
        if (<Record>record)._ptr is NULL:
            raise ValueError('unable to read record at index "%s"' % index)
        return record


cdef class Product:
    cdef EPR_SProductId* _product_id

    def __cinit__(self, filename, *args, **kargs):
        self._product_id = epr_open_product(filename)
        if not self._product_id:
            msg = epr_get_last_err_message()
            raise ValueError('unable to open %s: %s' % (filename, msg))

    def __dealloc__(self):
        if self._product_id:
            epr_close_product(self._product_id)
            pyepr_check_errors()

    def get_scene_width(self):
        return epr_get_scene_width(self._product_id)

    def get_scene_height(self):
        return epr_get_scene_height(self._product_id)

    def get_num_datasets(self):
        return epr_get_num_datasets(self._product_id)

    def get_num_dsds(self):
        return epr_get_num_dsds(self._product_id)

    def get_num_bands(self):
        return epr_get_num_bands(self._product_id)

    def get_dataset_at(self, uint index):
        cdef EPR_SDatasetId* dataset_id
        dataset_id = epr_get_dataset_id_at(self._product_id, index)
        if dataset_id is NULL:
            raise ValueError('unable to get dataset at index "%d"' % index)

        dataset = Dataset()
        (<Dataset>dataset)._dataset_id = dataset_id
        dataset._parent = self

        return dataset

    def get_dataset(self, name):
        cdef EPR_SDatasetId* dataset_id
        dataset_id = epr_get_dataset_id(self._product_id, name)
        if dataset_id is NULL:
            raise ValueError('unable to get dataset "%s"' % name)

        dataset = Dataset()
        (<Dataset>dataset)._dataset_id = dataset_id
        dataset._parent = self

        return dataset

    #def get_dsd_at(self, uint index):
    #    cdef EPR_SDSD* dsd_id
    #    dsd_id = epr_get_dsd_at(self._product_id, index)
    #    if dsd_id is NULL:
    #        raise ValueError('unable to get DSD at index "%d"' % index)
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
        #~ return epr_read_bitmask_raster(self._product_id,
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
