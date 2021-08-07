# -*- coding: utf-8 -*-

# PyEPR - Python bindings for ENVISAT Product Reader API
#
# Copyright (C) 2011-2021, Antonio Valentino <antonio.valentino@tiscali.it>
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


from libc.stdio cimport FILE


cdef extern from 'epr_api.h' nogil:
    char* EPR_PRODUCT_API_VERSION_STR

    ctypedef int               epr_boolean
    ctypedef unsigned char     uchar
    ctypedef unsigned short    ushort
    ctypedef unsigned int      uint
    ctypedef unsigned long     ulong

    ctypedef EPR_Time          EPR_STime
    #ctypedef EPR_FlagDef       EPR_SFlagDef
    ctypedef EPR_PtrArray      EPR_SPtrArray
    ctypedef EPR_FieldInfo     EPR_SFieldInfo
    ctypedef EPR_RecordInfo    EPR_SRecordInfo
    ctypedef EPR_Field         EPR_SField
    ctypedef EPR_Record        EPR_SRecord
    ctypedef EPR_DSD           EPR_SDSD
    ctypedef EPR_Raster        EPR_SRaster
    ctypedef EPR_BandId        EPR_SBandId
    ctypedef EPR_DatasetId     EPR_SDatasetId
    ctypedef EPR_ProductId     EPR_SProductId
    ctypedef EPR_ErrCode       EPR_EErrCode
    ctypedef EPR_LogLevel      EPR_ELogLevel
    ctypedef EPR_SampleModel   EPR_ESampleModel
    ctypedef EPR_ScalingMethod EPR_EScalingMethod
    ctypedef EPR_DataTypeId    EPR_EDataTypeId

    ctypedef int EPR_Magic

    int EPR_MAGIC_PRODUCT_ID
    int EPR_MAGIC_DATASET_ID
    int EPR_MAGIC_BAND_ID
    int EPR_MAGIC_RECORD
    int EPR_MAGIC_FIELD
    int EPR_MAGIC_RASTER
    int EPR_MAGIC_FLAG_DEF

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
        EPR_Magic magic
        char* name
        uint bit_mask
        char* description

    struct EPR_PtrArray:
        unsigned int capacity
        unsigned int length
        void** elems

    struct EPR_Field:
        EPR_Magic magic
        EPR_FieldInfo* info
        void* elems

    struct EPR_Record:
        EPR_Magic magic
        EPR_RecordInfo* info
        uint num_fields
        EPR_Field** fields

    struct EPR_DSD:
        EPR_Magic magic
        int index
        char* ds_name
        char* ds_type
        char* filename
        uint ds_offset
        uint ds_size
        uint num_dsr
        uint dsr_size

    struct EPR_Raster:
        EPR_Magic magic
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
        EPR_Magic magic
        char* file_path
        FILE* istream
        uint  tot_size
        uint  scene_width
        uint  scene_height
        char* id_string
        EPR_Record* mph_record
        EPR_Record* sph_record
        EPR_PtrArray* dsd_array
        EPR_PtrArray* record_info_cache
        EPR_PtrArray* param_table
        EPR_PtrArray* dataset_ids
        EPR_PtrArray* band_ids
        int meris_iodd_version

    struct EPR_DatasetId:
        EPR_Magic magic
        EPR_ProductId* product_id
        char* dsd_name
        EPR_DSD* dsd
        char* dataset_name
        #struct RecordDescriptor* record_descriptor
        EPR_SRecordInfo* record_info
        char* description

    struct EPR_DatasetRef:
        EPR_DatasetId* dataset_id
        int field_index             # -1 if not used
        int elem_index              # -1 if not used

    struct EPR_BandId:
        EPR_Magic magic
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
        EPR_SPtrArray* flag_coding
        char* unit
        char* description
        epr_boolean lines_mirrored

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
    const char* epr_get_last_err_message()
    void epr_clear_err()

    # API initialization/finalization
    int epr_init_api(EPR_ELogLevel, EPR_FLogHandler, EPR_FErrHandler)
    void epr_close_api()

    # DATATYPE
    uint epr_get_data_type_size(EPR_EDataTypeId)
    const char* epr_data_type_id_to_str(EPR_EDataTypeId)

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
    const char* epr_get_dataset_name(EPR_SDatasetId*)
    const char* epr_get_dsd_name(EPR_SDatasetId*)
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

    const char* epr_get_field_unit(EPR_SField*)
    const char* epr_get_field_description(EPR_SField*)
    uint epr_get_field_num_elems(EPR_SField*)
    const char* epr_get_field_name(EPR_SField*)
    EPR_EDataTypeId epr_get_field_type(EPR_SField*)

    char epr_get_field_elem_as_char(EPR_SField*, uint)
    uchar epr_get_field_elem_as_uchar(EPR_SField*, uint)
    short epr_get_field_elem_as_short(EPR_SField*, uint)
    ushort epr_get_field_elem_as_ushort(EPR_SField*, uint)
    int epr_get_field_elem_as_int(EPR_SField*, uint)
    uint epr_get_field_elem_as_uint(EPR_SField*, uint)
    float epr_get_field_elem_as_float(EPR_SField*, uint)
    double epr_get_field_elem_as_double(EPR_SField*, uint)
    const char* epr_get_field_elem_as_str(EPR_SField*)
    EPR_STime* epr_get_field_elem_as_mjd(EPR_SField*)

    const char* epr_get_field_elems_char(EPR_SField*)
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
    const char* epr_get_band_name(EPR_SBandId*)
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


# @IMPORTANT:
#
#   the following structures are not part of the public API.
#   It is not ensured that relative header files are available at build time
#   (e.g. debian does not install them), so structures are relìplicated here.
#   It is fundamental to ensure that structures defined here are kept totally
#   in sync with the one defined in EPR C API.

# epr_field.h
ctypedef struct EPR_FieldInfo:
    char* name
    EPR_EDataTypeId data_type_id
    uint num_elems
    char* unit
    char* description
    uint tot_size


# epr_record.h
ctypedef struct EPR_RecordInfo:
    char* dataset_name
    EPR_SPtrArray* field_infos
    uint tot_size
