#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

import os
import sys
import unittest
import functools

import numpy as np

sys.path.insert(0, os.pardir)
import epr

TEST_PRODUCT = 'ASA_IMP_1PNUPA20060202_062233_000000152044_00435_20529_3110.N1'

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

def equal_products(product1, product2):
    if type(product1) != type(product2):
        return False

    for name in ('file_path', 'tot_size', 'id_string', 'meris_iodd_version'):
        if getattr(product1, name) != getattr(product2, name):
            return False

    for name in ('get_scene_width', 'get_scene_height', 'get_num_datasets',
                 'get_num_dsds', 'get_num_bands', ):
        if getattr(product1, name)() != getattr(product2, name)():
            return False

    return True


class TestOpenProduct(unittest.TestCase):
    PRODUCT_FILE = TEST_PRODUCT

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
    PRODUCT_FILE = TEST_PRODUCT
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

    def test_file_path_property(self):
        self.assertEqual(self.product.file_path, TEST_PRODUCT)

    def test_tot_size_property(self):
        self.assertEqual(self.product.tot_size, 138422957)

    def test_id_string_property(self):
        self.assertEqual(self.product.id_string,
             'ASA_IMP_1PNUPA20060202_062233_000000152044_00435')

    def test_meris_iodd_version_property(self):
        self.assertEqual(self.product.meris_iodd_version, 0)

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

    def test_get_dsd_at(self):
        self.assertTrue(isinstance(self.product.get_dsd_at(0), epr.DSD))

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
    PRODUCT_FILE = TEST_PRODUCT
    DATASET_NAME = 'MDS1'

    def setUp(self):
        self.product = epr.Product(self.PRODUCT_FILE)
        self.dataset = self.product.get_dataset(self.DATASET_NAME)

    def test_product_id_property(self):
        self.assertTrue(equal_products(self.dataset.product_id, self.product))

    def test_description_property(self):
        self.assertEqual(self.dataset.description, 'Measurement Data Set 1')

    def test_get_dataset_name(self):
        self.assertEqual(self.dataset.get_dataset_name(), self.DATASET_NAME)

    def test_get_dsd_name(self):
        self.assertEqual(self.dataset.get_dsd_name(), self.DATASET_NAME)

    def test_get_num_records(self):
        self.assertEqual(self.dataset.get_num_records(), 8192)

    def test_get_dsd(self):
        self.assertTrue(isinstance(self.dataset.get_dsd(), epr.DSD))

    def test_create_record(self):
        self.assertTrue(isinstance(self.dataset.create_record(), epr.Record))

    def test_read_record(self):
        self.assertTrue(isinstance(self.dataset.create_record(), epr.Record))

    def test_read_record_passed(self):
        created_record = self.dataset.create_record()
        read_record = self.dataset.read_record(0, created_record)
        self.assertTrue(created_record is read_record)
        # @TODO: check contents

    def test_read_record_passed_invalid(self):
        self.assertRaises(TypeError, self.dataset.read_record, 0, 0)


class TestBand(unittest.TestCase):
    PRODUCT_FILE = TEST_PRODUCT
    BAND_NAMES = (
        'slant_range_time',
        'incident_angle',
        'latitude',
        'longitude',
        'proc_data',
    )
    XOFFSET = 40
    YOFFSET = 30
    DATA_TYPE = np.float32
    TEST_DATA = np.asarray([
        [ 98.,  90.,  64.,  82.,  84.,  79.,  66.,  46.,  59.,  54.],
        [ 73., 119., 101.,  90.,  89.,  76.,  44.,  52.,  91.,  72.],
        [ 85., 106., 107.,  73.,  78.,  65.,  37.,  55., 103.,  82.],
        [118.,  77.,  97.,  70.,  87.,  67.,  45.,  51.,  65.,  83.],
        [122.,  66.,  63.,  60.,  81.,  91.,  61.,  40.,  44.,  46.],
        [ 89.,  88.,  59.,  87.,  86., 101.,  68.,  29.,  67.,  54.],
        [121., 131., 108.,  85.,  81.,  88.,  67.,  19.,  53.,  47.],
        [153., 155., 141.,  81.,  64.,  73.,  64.,  47.,  44.,  69.],
        [105., 102.,  87.,  69.,  76.,  80.,  63.,  75.,  67.,  84.],
        [ 85.,  90.,  69.,  77.,  84.,  73.,  69.,  91.,  77.,  37.],
    ])

    def setUp(self):
        self.product = epr.Product(self.PRODUCT_FILE)
        self.band = self.product.get_band_id('proc_data')

    def test_product_id_property(self):
        self.assertTrue(equal_products(self.band.product_id, self.product))

    # @TODO: check
    #def test_dataset_ref_property(self):
    #    self.assertEqual(self.band.dataset_ref, ???)

    def test_spectr_band_index_property(self):
        self.assertEqual(self.band.spectr_band_index, -1)

    def test_sample_model_property(self):
        self.assertEqual(self.band.sample_model, 0)

    def test_data_type_property(self):
        self.assertEqual(self.band.data_type, epr.E_TID_FLOAT)

    def test_scaling_method_property(self):
        self.assertEqual(self.band.scaling_method, epr.E_SMID_LIN)

    def test_scaling_offset_property(self):
        self.assertEqual(self.band.scaling_offset, 0)

    def test_scaling_factor_property(self):
        self.assertEqual(self.band.scaling_factor, 1.0)
        self.assertTrue(isinstance(self.band.scaling_factor, float))

    def test_bm_expr_property(self):
        self.assertEqual(self.band.bm_expr, None)

    def test_unit_property(self):
        self.assertEqual(self.band.unit, None)

    def test_description_property(self):
        self.assertEqual(self.band.description, 'Image Mode Precision Image')

    def test_lines_mirrored_property(self):
        self.assertTrue(isinstance(self.band.lines_mirrored, bool))
        self.assertEqual(self.band.lines_mirrored, True)

    def test_get_band_name(self):
        for index in range(len(self.BAND_NAMES)):
            b = self.product.get_band_id_at(index)
            self.assertEqual(b.get_band_name(), self.BAND_NAMES[index])

    def test_create_compatible_raster(self):
        width = self.product.get_scene_width()
        height = self.product.get_scene_height()
        raster = self.band.create_compatible_raster(width, height)
        self.assertTrue(isinstance(raster, epr.Raster))
        self.assertEqual(raster.get_raster_width(), width)
        self.assertEqual(raster.get_raster_height(), height)
        # @NOTE: data type on disk is epr.E_TID_USHORT
        self.assertEqual(raster.data_type, epr.E_TID_FLOAT)

    def test_create_compatible_raster_with_invalid_size(self):
        width = self.product.get_scene_width()
        height = self.product.get_scene_height()

        self.assertRaises((ValueError, OverflowError),
                          self.band.create_compatible_raster,
                          -1, height)
        self.assertRaises((ValueError, OverflowError),
                          self.band.create_compatible_raster,
                          width, -1)
        # @TODO: check
        #self.assertRaises(ValueError, self.band.create_compatible_raster,
        #                  self.product.get_scene_width() + 10, height)
        #self.assertRaises(ValueError, self.band.create_compatible_raster,
        #                  width, self.product.get_scene_height() + 10)

    def test_create_compatible_raster_with_step(self):
        src_width = self.product.get_scene_width()
        src_height = self.product.get_scene_height()
        xstep = 2
        ystep = 3
        width = (src_width - 1) / xstep + 1
        height = (src_height - 1) / ystep + 1
        raster = self.band.create_compatible_raster(src_width, src_height,
                                                    xstep, ystep)
        self.assertTrue(isinstance(raster, epr.Raster))
        self.assertEqual(raster.get_raster_width(), width)
        self.assertEqual(raster.get_raster_height(), height)
        # @NOTE: data type on disk is epr.E_TID_USHORT
        self.assertEqual(raster.data_type, epr.E_TID_FLOAT)

    def test_create_compatible_raster_with_invalid_step(self):
        width = self.product.get_scene_width()
        height = self.product.get_scene_height()

        self.assertRaises((ValueError, OverflowError),
                          self.band.create_compatible_raster,
                          width, height, -1, 2)
        self.assertRaises((ValueError, OverflowError),
                          self.band.create_compatible_raster,
                          width, height, 2, -1)
        self.assertRaises((ValueError, OverflowError),
                          self.band.create_compatible_raster,
                          width, height, -2, -1)

        # @TODO: check
        #self.assertRaises((ValueError, OverflowError),
        #                  self.band.create_compatible_raster,
        #                  width, height, width + 10, 2)
        #self.assertRaises((ValueError, OverflowError),
        #                  self.band.create_compatible_raster,
        #                  width, height, 2, height + 10)
        #self.assertRaises((ValueError, OverflowError),
        #                  self.band.create_compatible_raster,
        #                  width, height, width + 10, height + 10)

    def test_read_band_raster(self):
        width = 400
        height = 300
        raster = self.band.create_compatible_raster(width, height)

        self.band.read_band_raster(self.XOFFSET, self.YOFFSET, raster)

        self.assertTrue(isinstance(raster, epr.Raster))
        self.assertEqual(raster.get_raster_width(), width)
        self.assertEqual(raster.get_raster_height(), height)
        # @NOTE: data type on disk is epr.E_TID_USHORT
        self.assertEqual(raster.data_type, epr.E_TID_FLOAT)

    def test_read_band_raster_default_offset(self):
        height, width = self.TEST_DATA.shape

        raster1 = self.band.create_compatible_raster(width, height)
        raster2 = self.band.create_compatible_raster(width, height)

        self.band.read_band_raster(0, 0, raster1)
        self.band.read_band_raster(raster=raster2)

        self.assertEqual(raster1.get_pixel(0, 0), raster2.get_pixel(0, 0))
        self.assertEqual(raster1.get_pixel(width - 1, height -1),
                          raster2.get_pixel(width - 1, height -1))

    def test_read_band_raster_with_invalid_raster(self):
        self.assertRaises(TypeError, self.band.read_band_raster, 0, 0, 0)

    def test_read_band_raster_with_invalid_offset(self):
        width = 400
        height = 300
        raster = self.band.create_compatible_raster(width, height)

        # @TODO: check
        self.assertRaises(ValueError, self.band.read_band_raster,
                          -1, 0, raster)
        self.assertRaises(ValueError, self.band.read_band_raster,
                          0, -1, raster)
        self.assertRaises(ValueError, self.band.read_band_raster,
                          -1, -1, raster)
        # @TODO: check
        #self.assertRaises(ValueError, self.band.read_band_raster,
        #                  width + 10, 0, raster)
        #self.assertRaises(ValueError, self.band.read_band_raster,
        #                  0, height + 10, raster)
        #self.assertRaises(ValueError, self.band.read_band_raster,
        #                  width + 10, height + 10, raster)

    def test_read_as_array(self):
        width = 400
        height = 300

        data = self.band.read_as_array(width, height,
                                       self.XOFFSET, self.YOFFSET)

        self.assertTrue(isinstance(data, np.ndarray))
        self.assertEqual(data.shape, (height, width))
        self.assertEqual(data.dtype, self.DATA_TYPE)

        h, w = self.TEST_DATA.shape
        self.assertTrue(np.all(data[:h, :w] == self.TEST_DATA))

    # @TODO: check, it seems to be an upstream bug or a metter of data mirroring
    #def test_read_as_array_with_step(self):
    #    width = 400
    #    height = 300
    #
    #    data = self.band.read_as_array(width, height,
    #                                   self.XOFFSET, self.YOFFSET, 2, 2)
    #
    #    self.assertTrue(isinstance(data, np.ndarray))
    #    self.assertEqual(data.shape, (height/2, width/2))
    #    self.assertEqual(data.dtype, self.DATA_TYPE)
    #
    #    h, w = self.TEST_DATA.shape
    #    self.assertTrue(np.all(data[:h/2, :w/2] == self.TEST_DATA[::2, ::2]))
    #    #self.assertTrue(np.all(data[:h/2, :w/2] == self.TEST_DATA[::2, 1::2]))

    # @TODO: more read_as_array testing


class TestCreateRaster(unittest.TestCase):
    RASTER_WIDTH = 400
    RASTER_HEIGHT = 300
    RASTER_DATA_TYPE = epr.E_TID_FLOAT

    def test_create_raster(self):
        raster = epr.create_raster(self.RASTER_DATA_TYPE, self.RASTER_WIDTH,
                                   self.RASTER_HEIGHT)
        self.assertTrue(isinstance(raster, epr.Raster))
        self.assertEqual(raster.data_type, self.RASTER_DATA_TYPE)
        self.assertEqual(raster.get_raster_width(), self.RASTER_WIDTH)
        self.assertEqual(raster.get_raster_height(), self.RASTER_HEIGHT)

    def test_create_raster_with_step(self):
        src_width = 3 * self.RASTER_WIDTH
        src_height = 2 * self.RASTER_HEIGHT
        raster = epr.create_raster(self.RASTER_DATA_TYPE,
                                   src_width, src_height, 3, 2)
        self.assertTrue(isinstance(raster, epr.Raster))
        self.assertEqual(raster.data_type, self.RASTER_DATA_TYPE)
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
        self.assertEqual(raster.data_type, epr.E_TID_UCHAR)
        self.assertEqual(raster.get_raster_width(), self.RASTER_WIDTH)
        self.assertEqual(raster.get_raster_height(), self.RASTER_HEIGHT)

    def test_create_bitmask_raster_with_step(self):
        src_width = 3 * self.RASTER_WIDTH
        src_height = 2 * self.RASTER_HEIGHT
        raster = epr.create_bitmask_raster(src_width, src_height, 3, 2)
        self.assertTrue(isinstance(raster, epr.Raster))
        self.assertEqual(raster.data_type, epr.E_TID_UCHAR)
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
    TEST_DATA = np.zeros((10, 10))

    def setUp(self):
        self.raster = epr.create_raster(self.RASTER_DATA_TYPE,
                                        self.RASTER_WIDTH, self.RASTER_HEIGHT)

    def test_get_raster_width(self):
        self.assertEqual(self.raster.get_raster_width(), self.RASTER_WIDTH)

    def test_get_raster_height(self):
        self.assertEqual(self.raster.get_raster_height(), self.RASTER_HEIGHT)

    def test_get_raster_elem_size(self):
        self.assertEqual(self.raster.get_raster_elem_size(),
                         self.RASTER_ELEM_SIZE)

    def test_get_pixel(self):
        self.assertEqual(self.raster.get_pixel(0, 0), self.TEST_DATA[0, 0])

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

    def test_data_type_property(self):
        self.assertEqual(self.raster.data_type, self.RASTER_DATA_TYPE)

    def test_source_width_property(self):
        self.assertEqual(self.raster.source_width, self.RASTER_WIDTH)
        self.assertTrue(isinstance(self.raster.source_width, (int, long)))

    def test_source_height_property(self):
        self.assertEqual(self.raster.source_height, self.RASTER_HEIGHT)
        self.assertTrue(isinstance(self.raster.source_height, (int, long)))

    def test_source_step_x_property(self):
        self.assertEqual(self.raster.source_step_x, 1)
        self.assertTrue(isinstance(self.raster.source_step_x, (int, long)))

    def test_source_step_y_property(self):
        self.assertEqual(self.raster.source_step_y, 1)
        self.assertTrue(isinstance(self.raster.source_step_y, (int, long)))

    def test_data_property(self):
        height = self.raster.get_raster_height()
        width = self.raster.get_raster_width()

        data = self.raster.data

        self.assertTrue(isinstance(data, np.ndarray))
        self.assertEqual(data.ndim, 2)
        self.assertEqual(data.shape, (height, width))
        self.assertEqual(data.dtype,
                         epr.epr_to_numpy_type[self.raster.data_type])
        self.assertTrue(np.all(data[:10, :10] == self.TEST_DATA))

    def test_data_property_two_times(self):
        data1 = self.raster.data
        data2 = self.raster.data
        self.assertFalse(data1 is data2)    # @TODO: check
        self.assertTrue(np.all(data1 == data2))

    def test_data_property_shared_data_semantic(self):
        data1 = self.raster.data
        data1[0, 0] *= 2
        data2 = self.raster.data
        self.assertTrue(np.all(data1 == data2))

    def test_data_property_data_scope(self):
        data1 = self.raster.data
        self.assertTrue(isinstance(data1, np.ndarray))
        data1 = None
        data2 = self.raster.data
        self.assertTrue(isinstance(data2, np.ndarray))

    def test_data_property_raster_scope(self):
        data = self.raster.data
        self.assertTrue(isinstance(data, np.ndarray))
        self.raster = None
        self.assertTrue(isinstance(data, np.ndarray))
        self.assertTrue(np.all(data[:10, :10] == self.TEST_DATA))


class TestRasterRead(TestRaster):
    PRODUCT_FILE = TEST_PRODUCT
    BAND_NAME = 'proc_data'
    RASTER_XOFFSET = 40
    RASTER_YOFFSET = 30
    TEST_DATA = np.asarray([
        [ 98.,  90.,  64.,  82.,  84.,  79.,  66.,  46.,  59.,  54.],
        [ 73., 119., 101.,  90.,  89.,  76.,  44.,  52.,  91.,  72.],
        [ 85., 106., 107.,  73.,  78.,  65.,  37.,  55., 103.,  82.],
        [118.,  77.,  97.,  70.,  87.,  67.,  45.,  51.,  65.,  83.],
        [122.,  66.,  63.,  60.,  81.,  91.,  61.,  40.,  44.,  46.],
        [ 89.,  88.,  59.,  87.,  86., 101.,  68.,  29.,  67.,  54.],
        [121., 131., 108.,  85.,  81.,  88.,  67.,  19.,  53.,  47.],
        [153., 155., 141.,  81.,  64.,  73.,  64.,  47.,  44.,  69.],
        [105., 102.,  87.,  69.,  76.,  80.,  63.,  75.,  67.,  84.],
        [ 85.,  90.,  69.,  77.,  84.,  73.,  69.,  91.,  77.,  37.],
    ])

    def setUp(self):
        self.product = epr.Product(self.PRODUCT_FILE)
        self.band = self.product.get_band_id(self.BAND_NAME)
        self.raster = self.band.create_compatible_raster(self.RASTER_WIDTH,
                                                         self.RASTER_HEIGHT)

        self.band.read_band_raster(self.RASTER_XOFFSET, self.RASTER_YOFFSET,
                                   self.raster)

    def test_data_property_shared_semantics_readload(self):
        data1 = self.raster.data
        data1[0, 0] *= 2
        self.band.read_band_raster(self.RASTER_XOFFSET, self.RASTER_YOFFSET,
                                   self.raster)
        data2 = self.raster.data
        self.assertEqual(data1[0, 0], data2[0, 0])
        self.assertTrue(np.all(data1 == data2))



class TestRecord(unittest.TestCase):
    PRODUCT_FILE = TEST_PRODUCT
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
    #        self.assertRaises(ValueError, self.record.dump_element, field, 0)
    #
    #    def test_dump_element_element_out_of_range(self):
    #        self.assertRaises(ValueError, self.record.dump_element, 0, 150)

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
        self.assertRaises(ValueError, self.record.print_element, index, 0)

    def test_print_element_element_out_of_range(self):
        self.assertRaises(ValueError, self.record.print_element, 0, 150)

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
    PRODUCT_FILE = TEST_PRODUCT
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
        self.assertRaises(ValueError, self.field.get_field_elem, 100)

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


class TestDSD(unittest.TestCase):
    PRODUCT_FILE = TEST_PRODUCT

    def setUp(self):
        product = epr.Product(self.PRODUCT_FILE)
        self.dsd = product.get_dsd_at(0)

    def test_index(self):
        self.assertEqual(self.dsd.index, 0)
        self.assertTrue(isinstance(self.dsd.index, int))

    def test_ds_name(self):
        self.assertEqual(self.dsd.ds_name, 'MDS1 SQ ADS')
        self.assertTrue(isinstance(self.dsd.ds_name, basestring))

    def test_ds_type(self):
        self.assertEqual(self.dsd.ds_type, 'A')
        self.assertTrue(isinstance(self.dsd.ds_type, basestring))

    def test_filename(self):
        self.assertEqual(self.dsd.filename, '')
        self.assertTrue(isinstance(self.dsd.filename, basestring))

    def test_ds_offset(self):
        self.assertEqual(self.dsd.ds_offset, 7346)
        self.assertTrue(isinstance(self.dsd.ds_offset, (int, long)))

    def test_ds_size(self):
        self.assertEqual(self.dsd.ds_size, 170)
        self.assertTrue(isinstance(self.dsd.ds_size, (int, long)))

    def test_num_dsr(self):
        self.assertEqual(self.dsd.num_dsr, 1)
        self.assertTrue(isinstance(self.dsd.num_dsr, (int, long)))

    def test_dsr_size(self):
        self.assertEqual(self.dsd.dsr_size, 170)
        self.assertTrue(isinstance(self.dsd.dsr_size, (int, long)))


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

    def test_data_type_id_to_str_invalid(self):
        self.assertEqual(epr.data_type_id_to_str(500), '')

    def test_get_data_type_size(self):
        for type_id, type_size in self.TYPE_SIZES.items():
            self.assertEqual(epr.get_data_type_size(type_id), type_size)

    def test_get_data_type_size_invalid(self):
        self.assertEqual(epr.get_data_type_size(500), 0)


class TestScalingMethodFunctions(unittest.TestCase):
    METHOD_NAMES = {
        epr.E_SMID_NON: 'NONE',
        epr.E_SMID_LIN: 'LIN',
        epr.E_SMID_LOG: 'LOG',
    }

    def test_get_scaling_method_name(self):
        for id_, name in self.METHOD_NAMES.items():
            self.assertEqual(epr.get_scaling_method_name(id_), name)

    def test_get_scaling_method_name_invalid(self):
        self.assertRaises(ValueError, epr.get_scaling_method_name, 500)


class TestSampleModelFunctions(unittest.TestCase):
    MODEL_NAMES = {
        epr.E_SMOD_1OF1: '1OF1',
        epr.E_SMOD_1OF2: '1OF2',
        epr.E_SMOD_2OF2: '2OF2',
        epr.E_SMOD_3TOI: '3TOI',
        epr.E_SMOD_2TOF: '2TOF',
    }

    def test_get_scaling_method_name(self):
        for id_, name in self.MODEL_NAMES.items():
            self.assertEqual(epr.get_sample_model_name(id_), name)

    def test_get_scaling_method_name_invalid(self):
        self.assertRaises(ValueError, epr.get_sample_model_name, 500)


class TestDirectInstantiation(unittest.TestCase):
    def test_direct_dsd_instantiation(self):
        self.assertRaises(TypeError, epr.DSD)

    def test_direct_field_instantiation(self):
        self.assertRaises(TypeError, epr.Field)

    def test_direct_record_instantiation(self):
        self.assertRaises(TypeError, epr.Record)

    def test_direct_raster_instantiation(self):
        self.assertRaises(TypeError, epr.Raster)

    def test_direct_band_instantiation(self):
        self.assertRaises(TypeError, epr.Band)

    def test_direct_dataset_instantiation(self):
        self.assertRaises(TypeError, epr.Dataset)


if __name__ == '__main__':
    unittest.main()
