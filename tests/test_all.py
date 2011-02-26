#!/usr/bin/env python

import os
import sys
import unittest
import functools

import numpy as np

sys.path.insert(0, os.pardir)
import epr

#PRODUCT_FILE = 'SAR_IMS_1PXESA20040920_034157_00000016A098_00290_49242_0715.E2'

def quiet(func):
    @functools.wraps(func)
    def wrapper(*args, **kwds):
        sysout = sys.stdout
        syserr = sys.stderr
        try:
            with file(os.devnull) as fd:
                sys.stdout = fd
                sys.stderr = fd
                ret = func(*args, **kwds)
        finally:
            sys.stdout = sysout
            sys.stderr = syserr
        return ret

    return wrapper


class TestOpenProduct(unittest.TestCase):
    PRODUCT_FILE = 'ASA_IMP_1PNUPA20060202_062233_000000152044_00435_20529_3110.N1'

    def test_open(self):
        product = epr.open(self.PRODUCT_FILE)
        self.assertTrue(isinstance(product, epr.Product))

    def test_product_constructor(self):
        product = epr.Product(self.PRODUCT_FILE)
        self.assertTrue(isinstance(product, epr.Product))

    def test_open_failure(self):
        self.assertRaises(ValueError, epr.open, '')

    def test_product_constructor_failure(self):
        self.assertRaises(ValueError, epr.Product, '')


class TestProduct(unittest.TestCase):
    PRODUCT_FILE = 'ASA_IMP_1PNUPA20060202_062233_000000152044_00435_20529_3110.N1'
    DATASET_NAMES = [
        'MDS1_SQ_ADS',
        'MAIN_PROCESSING_PARAMS_ADS',
        'DOP_CENTROID_COEFFS_ADS',
        'SR_GR_ADS',
        'CHIRP_PARAMS_ADS',
        'GEOLOCATION_GRID_ADS',
        'MDS1'
    ]
    DATASET_WIDTH = 8439
    DATASET_HEIGHT = 8192
    DATASET_NDSDS = 18
    DATASET_NBANDS = 5

    def setUp(self):
        self.product = epr.Product(self.PRODUCT_FILE)

    def test_get_scene_width(self):
        self.assertEqual(self.product.get_scene_width(), self.DATASET_WIDTH)

    def test_get_scene_height(self):
        self.assertEqual(self.product.get_scene_height(), self.DATASET_HEIGHT)

    def test_get_num_datasets(self):
        self.assertEqual(self.product.get_num_datasets(),
                         len(self.DATASET_NAMES))

    def test_get_num_dsds(self):
        self.assertEqual(self.product.get_num_dsds(), self.DATASET_NDSDS)

    def test_get_num_bands(self):
        self.assertEqual(self.product.get_num_bands(), self.DATASET_NBANDS)

    def test_get_dataset_at(self):
        dataset = self.product.get_dataset_at(0)
        self.assertTrue(dataset)

    def test_get_dataset(self):
        dataset = self.product.get_dataset('MDS1')
        self.assertTrue(dataset)

    def test_datasets(self):
        datasets = [self.product.get_dataset_at(idx)
                        for idx in range(self.product.get_num_datasets())]
        dataset_names = [ds.get_dataset_name() for ds in datasets]
        self.assertEqual(dataset_names, self.DATASET_NAMES)

    #def test_get_dsd_at(self):
    #    self.assertTrue(isinstance(self.product.get_dsd_at(0), epr.DSD))

    def test_get_mph(self):
        record = self.product.get_mph()
        self.assertTrue(isinstance(record, epr.Record))
        self.assertEqual(record.get_field('PRODUCT').get_field_elem(),
                         self.PRODUCT_FILE)

    def test_get_sph(self):
        record = self.product.get_sph()
        self.assertTrue(isinstance(record, epr.Record))
        self.assertEqual(record.get_field('SPH_DESCRIPTOR').get_field_elem(),
                         "Image Mode Precision Image")

    def test_get_band_id(self):
        self.assertTrue(isinstance(self.product.get_band_id('proc_data'),
                                   epr.Band))

    def test_get_band_id_invalid_name(self):
        self.assertRaises(ValueError, self.product.get_band_id, '')

    def test_get_band_id_at(self):
        self.assertTrue(isinstance(self.product.get_band_id_at(0), epr.Band))

    def test_get_band_id_at_invalid_index(self):
        self.assertRaises(ValueError, self.product.get_band_id_at,
                            self.product.get_num_bands())

    #def test_read_bitmask_raster(self):
    #    bm_expr = 'l2_flags.LAND and !l2_flags.BRIGHT'
    #
    #    xoffset = self.DATASET_WIDTH / 2
    #    yoffset = self.DATASET_HEIGHT / 2
    #    width = self.DATASET_WIDTH / 2
    #    height = self.DATASET_HEIGHT / 2
    #
    #    raster = epr.create_bitmask_raster(width, height)
    #    raster = self.product.read_bitmask_raster(bm_expr, xoffset, yoffset,
    #                                              raster)
    #    self.assertTrue(isinstance(raster, epr.Raster))
    #    self.assertEqual(raster.get_raster_width(), width)
    #    self.assertEqual(raster.get_raster_height(), height)


class TestDataset(unittest.TestCase):
    PRODUCT_FILE = 'ASA_IMP_1PNUPA20060202_062233_000000152044_00435_20529_3110.N1'
    DATASET_NAME = 'MDS1'

    def setUp(self):
        product = epr.Product(self.PRODUCT_FILE)
        self.dataset = product.get_dataset(self.DATASET_NAME)

    def test_get_dataset_name(self):
        self.assertEqual(self.dataset.get_dataset_name(), self.DATASET_NAME)

    def test_get_dsd_name(self):
        self.assertEqual(self.dataset.get_dsd_name(), self.DATASET_NAME)

    def test_get_num_records(self):
        self.assertEqual(self.dataset.get_num_records(), 8192)

    #def test_get_dsd(self):
    #    self.assertTrue(isinstance(self.dataset.get_dsd(), epr.DSD))

    def test_create_record(self):
        self.assertTrue(isinstance(self.dataset.create_record(), epr.Record))

    def test_read_record(self):
        self.assertTrue(isinstance(self.dataset.create_record(), epr.Record))

    def test_read_record_passed(self):
        created_record = self.dataset.create_record()
        read_record = self.dataset.read_record(0, created_record)
        self.assertTrue(created_record is read_record)
        # @TODO: check contents


class TestUninitializedDataset(unittest.TestCase):
    def setUp(self):
        self.dataset = epr.Dataset()

    def test_get_dataset_name(self):
        self.assertEqual(self.dataset.get_dataset_name(), '')

    def test_get_dsd_name(self):
        self.assertEqual(self.dataset.get_dsd_name(), '')

    def test_get_num_records(self):
        self.assertEqual(self.dataset.get_num_records(), 0)


class TestBand(unittest.TestCase):
    PRODUCT_FILE = 'ASA_IMP_1PNUPA20060202_062233_000000152044_00435_20529_3110.N1'
    BAND_NAMES = (
        'slant_range_time',
        'incident_angle',
        'latitude',
        'longitude',
        'proc_data',
    )

    def setUp(self):
        self.product = epr.Product(self.PRODUCT_FILE)
        #self.band = self.product.get_band_id('proc_data')

    def test_get_band_name(self):
        for index in range(len(self.BAND_NAMES)):
            b = self.product.get_band_id_at(index)
            self.assertEqual(b.get_band_name(), self.BAND_NAMES[index])

class TestCreateRaster(unittest.TestCase):
    RASTER_WIDTH = 400
    RASTER_HEIGHT = 300
    RASTER_DATA_TYPE = epr.E_TID_FLOAT

    def test_create_raster(self):
        raster = epr.create_raster(self.RASTER_DATA_TYPE, self.RASTER_WIDTH,
                                   self.RASTER_HEIGHT)
        self.assertTrue(isinstance(raster, epr.Raster))
        self.assertEqual(raster.get_raster_data_type(), self.RASTER_DATA_TYPE)
        self.assertEqual(raster.get_raster_width(), self.RASTER_WIDTH)
        self.assertEqual(raster.get_raster_height(), self.RASTER_HEIGHT)

    def test_create_raster_with_step(self):
        src_width = 3 * self.RASTER_WIDTH
        src_height = 2 * self.RASTER_HEIGHT
        raster = epr.create_raster(self.RASTER_DATA_TYPE,
                                   src_width, src_height, 3, 2)
        self.assertTrue(isinstance(raster, epr.Raster))
        self.assertEqual(raster.get_raster_data_type(), self.RASTER_DATA_TYPE)
        self.assertEqual(raster.get_raster_width(), self.RASTER_WIDTH)
        self.assertEqual(raster.get_raster_height(), self.RASTER_HEIGHT)

    def test_create_raster_with_invalid_step(self):
        src_width = 3 * self.RASTER_WIDTH
        src_height = 2 * self.RASTER_HEIGHT
        self.assertRaises(ValueError, epr.create_raster,
                          self.RASTER_DATA_TYPE,  src_width, src_height, 0, 2)

    def test_create_raster_with_invalid_size(self):
        self.assertRaises((ValueError, OverflowError), epr.create_raster,
                          self.RASTER_DATA_TYPE,  -1, self.RASTER_HEIGHT)

    def test_create_bitmask_raster(self):
        raster = epr.create_bitmask_raster(self.RASTER_WIDTH,
                                           self.RASTER_HEIGHT)
        self.assertTrue(isinstance(raster, epr.Raster))
        self.assertEqual(raster.get_raster_data_type(), epr.E_TID_UCHAR)
        self.assertEqual(raster.get_raster_width(), self.RASTER_WIDTH)
        self.assertEqual(raster.get_raster_height(), self.RASTER_HEIGHT)

    def test_create_bitmask_raster_with_step(self):
        src_width = 3 * self.RASTER_WIDTH
        src_height = 2 * self.RASTER_HEIGHT
        raster = epr.create_bitmask_raster(src_width, src_height, 3, 2)
        self.assertTrue(isinstance(raster, epr.Raster))
        self.assertEqual(raster.get_raster_data_type(), epr.E_TID_UCHAR)
        self.assertEqual(raster.get_raster_width(), self.RASTER_WIDTH)
        self.assertEqual(raster.get_raster_height(), self.RASTER_HEIGHT)

    def test_create_bitmask_raster_with_invalid_step(self):
        src_width = 3 * self.RASTER_WIDTH
        src_height = 2 * self.RASTER_HEIGHT
        self.assertRaises(ValueError, epr.create_bitmask_raster,
                          src_width, src_height, 0, 2)

    def test_create_bitmask_raster_with_invalid_size(self):
        self.assertRaises((ValueError, OverflowError),
                          epr.create_bitmask_raster, -1, self.RASTER_HEIGHT)


class TestRaster(unittest.TestCase):
    RASTER_WIDTH = 400
    RASTER_HEIGHT = 300
    RASTER_DATA_TYPE = epr.E_TID_FLOAT
    RASTER_ELEM_SIZE = 4

    def setUp(self):
        self.raster = epr.create_raster(self.RASTER_DATA_TYPE,
                                        self.RASTER_WIDTH, self.RASTER_HEIGHT)

    def test_get_raster_width(self):
        self.assertEqual(self.raster.get_raster_width(), self.RASTER_WIDTH)

    def test_get_raster_height(self):
        self.assertEqual(self.raster.get_raster_height(), self.RASTER_HEIGHT)

    def test_get_raster_data_type(self):
        self.assertEqual(self.raster.get_raster_data_type(),
                         self.RASTER_DATA_TYPE)

    def test_get_raster_elem_size(self):
        self.assertEqual(self.raster.get_raster_elem_size(),
                         self.RASTER_ELEM_SIZE)

    def test_get_pixel(self):
        self.assertEqual(self.raster.get_pixel(0, 0), 0)

    def test_get_pixel_invalid_x(self):
        self.assertRaises(ValueError, self.raster.get_pixel, -1, 0)
        self.assertRaises(ValueError, self.raster.get_pixel,
                          self.RASTER_WIDTH + 1, 0)

    def test_get_pixel_invalid_y(self):
        self.assertRaises(ValueError, self.raster.get_pixel, 0, -1)
        self.assertRaises(ValueError, self.raster.get_pixel,
                          0, self.RASTER_HEIGHT + 1)

    def test_get_pixel_invalid_coor(self):
        self.assertRaises(ValueError, self.raster.get_pixel, -1, -1)
        self.assertRaises(ValueError, self.raster.get_pixel,
                          self.RASTER_WIDTH + 1, self.RASTER_HEIGHT + 1)

    def test_get_pixel_type(self):
        self.assertEqual(type(self.raster.get_pixel(0, 0)), float)


class TestRecord(unittest.TestCase):
    PRODUCT_FILE = 'ASA_IMP_1PNUPA20060202_062233_000000152044_00435_20529_3110.N1'
    DATASET_NAME = 'MAIN_PROCESSING_PARAMS_ADS'

    def setUp(self):
        product = epr.Product(self.PRODUCT_FILE)
        dataset = product.get_dataset(self.DATASET_NAME)
        self.record = dataset.read_record(0)

    def test_get_num_fields(self):
        self.assertEqual(self.record.get_num_fields(), 220)

    #if ALLOW_DUMP:
    #    def test_dump_record(self):
    #        self.record.dump_record()
    #
    #    def test_dump_element(self):
    #        self.record.dump_element(0, 0)
    #
    #    def test_dump_element_field_out_of_range(self):
    #        field = self.record.get_num_fields() + 10
    #        self.assertRaises(epr.EPRError, self.record.dump_element, field, 0)
    #
    #    def test_dump_element_element_out_of_range(self):
    #        self.assertRaises(epr.EPRError, self.record.dump_element, 0, 150)

    @quiet
    def test_print_record(self):
        self.record.print_record()

    @quiet
    def test_print_record_ostream(self):
        self.record.print_record(sys.stderr)

    def test_print_record_invalid_ostream(self):
        self.assertRaises(TypeError, self.record.print_record, 'invalid')

    @quiet
    def test_print_element(self):
        self.record.print_element(3, 0)

    @quiet
    def test_print_element_ostream(self):
        self.record.print_element(0, 0, sys.stderr)

    def test_print_element_invalid_ostream(self):
        self.assertRaises(TypeError, self.record.print_element, 0, 0, 'invalid')

    def test_print_element_field_out_of_range(self):
        index = self.record.get_num_fields() + 10
        self.assertRaises(epr.EPRError, self.record.print_element, index, 0)

    def test_print_element_element_out_of_range(self):
        self.assertRaises(epr.EPRError, self.record.print_element, 0, 150)

    def test_get_field(self):
        field = self.record.get_field('range_spacing')
        self.assertTrue(isinstance(field, epr.Field))

    def test_get_field_invlid_name(self):
        self.assertRaises(ValueError, self.record.get_field, '')

    def test_get_field_at(self):
        self.assertTrue(isinstance(self.record.get_field_at(0), epr.Field))

    def test_get_field_at_invalid_index(self):
        index = self.record.get_num_fields() + 10
        self.assertRaises(ValueError, self.record.get_field_at, index)


class TestField(unittest.TestCase):
    PRODUCT_FILE = 'ASA_IMP_1PNUPA20060202_062233_000000152044_00435_20529_3110.N1'
    DATASET_NAME = 'MAIN_PROCESSING_PARAMS_ADS'

    FIELD_NAME = 'range_spacing'
    FIELD_DESCRIPTION = 'Range sample spacing'
    FIELD_TYPE = epr.E_TID_FLOAT
    FIELD_TYPE_NAME = 'float'
    FIELD_NUM_ELEMS = 1
    FIELD_VALUES = (12.5,)
    FIELD_UNIT = 'm'

    def setUp(self):
        product = epr.Product(self.PRODUCT_FILE)
        dataset = product.get_dataset(self.DATASET_NAME)
        record = dataset.read_record(0)
        self.field = record.get_field(self.FIELD_NAME)

    @quiet
    def test_print_field(self):
        self.field.print_field()

    @quiet
    def test_print_fied_ostream(self):
        self.field.print_field(sys.stderr)

    def test_print_fied_invalid_ostream(self):
        self.assertRaises(TypeError, self.field.print_field, 'invalid')

    #if ALLOW_DUMP:
    #    def test_dump_field(self):
    #        self.field.dump_field()

    def test_get_field_unit(self):
        self.assertEqual(self.field.get_field_unit(), self.FIELD_UNIT)

    def test_get_field_description(self):
        self.assertEqual(self.field.get_field_description(),
                         self.FIELD_DESCRIPTION)

    def test_get_field_num_elems(self):
        self.assertEqual(self.field.get_field_num_elems(), self.FIELD_NUM_ELEMS)

    def test_get_field_name(self):
        self.assertEqual(self.field.get_field_name(), self.FIELD_NAME)

    def test_get_field_type(self):
        self.assertEqual(self.field.get_field_type(), self.FIELD_TYPE)

    def test_get_field_elem(self):
        self.assertEqual(self.field.get_field_elem(), self.FIELD_VALUES[0])

    def test_get_field_elem_index(self):
        self.assertEqual(self.field.get_field_elem(0), self.FIELD_VALUES[0])

    def test_get_field_elem_invalid_index(self):
        self.assertRaises(epr.EPRError, self.field.get_field_elem, 100)

    def test_get_field_elems(self):
        vect = self.field.get_field_elems()
        self.assertTrue(isinstance(vect, np.ndarray))
        self.assertEqual(vect.shape, (self.field.get_field_num_elems(),))
        self.assertEqual(vect.dtype, np.float32)
        self.assertTrue(np.allclose(vect, self.FIELD_VALUES))


class TestFieldWithMiltipleElems(TestField):
    FIELD_NAME = 'image_parameters.first_swst_value'
    FIELD_DESCRIPTION = 'Sampling Window Start time of first processed line'
    FIELD_TYPE = epr.E_TID_FLOAT
    FIELD_TYPE_NAME = 'float'
    FIELD_NUM_ELEMS = 5
    FIELD_VALUES = (6.0600759752560407e-05, 0., 0., 0., 0.)
    FIELD_UNIT = 's'


class TestDataypeFunctions(unittest.TestCase):
    TYPE_NAMES = {
        epr.E_TID_UNKNOWN: '',
        epr.E_TID_UCHAR:   'uchar',
        epr.E_TID_CHAR:    'char',
        epr.E_TID_USHORT:  'ushort',
        epr.E_TID_SHORT:   'short',
        epr.E_TID_UINT:    'uint',
        epr.E_TID_INT:     'int',
        epr.E_TID_FLOAT:   'float',
        epr.E_TID_DOUBLE:  'double',
        epr.E_TID_STRING:  'string',
        epr.E_TID_SPARE:   'spare',
        epr.E_TID_TIME:    'time',
    }

    TYPE_SIZES = {
        epr.E_TID_UNKNOWN: 0,
        epr.E_TID_UCHAR:   1,
        epr.E_TID_CHAR:    1,
        epr.E_TID_USHORT:  2,
        epr.E_TID_SHORT:   2,
        epr.E_TID_UINT:    4,
        epr.E_TID_INT:     4,
        epr.E_TID_FLOAT:   4,
        epr.E_TID_DOUBLE:  8,
        epr.E_TID_STRING:  1,
        epr.E_TID_SPARE:   1,
        epr.E_TID_TIME:    12,
    }

    def test_data_type_id_to_str(self):
        for type_id, type_name in self.TYPE_NAMES.items():
            self.assertEqual(epr.data_type_id_to_str(type_id), type_name)

    def test_get_data_type_size(self):
        for type_id, type_size in self.TYPE_SIZES.items():
            self.assertEqual(epr.get_data_type_size(type_id), type_size)


if __name__ == '__main__':
    unittest.main()
