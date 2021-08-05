#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

import os
import re
import sys
import shutil
import numbers
import pathlib
import zipfile
import operator
import platform
import tempfile
import unittest
import functools
from urllib.request import urlopen
from distutils.version import LooseVersion

try:
    import resource
except ImportError:
    resource = None


import numpy as np
import numpy.testing as npt

import epr


EPR_TO_NUMPY_TYPE = {
    # epr.E_TID_UNKNOWN:  np.NPY_NOTYPE,
    epr.E_TID_UCHAR:    np.ubyte,
    epr.E_TID_CHAR:     np.byte,
    epr.E_TID_USHORT:   np.ushort,
    epr.E_TID_SHORT:    np.short,
    epr.E_TID_UINT:     np.uint,
    epr.E_TID_INT:      int,
    epr.E_TID_FLOAT:    np.float32,
    epr.E_TID_DOUBLE:   np.double,
    epr.E_TID_STRING:   str,
    # epr.E_TID_SPARE   = e_tid_spare,
    # epr.E_TID_TIME    = e_tid_time,
}


def has_epr_c_bug_pyepr009():
    v = LooseVersion(epr.EPR_C_API_VERSION)
    if 'pyepr' in v.version:
        return v < LooseVersion('2.3dev_pyepr082')
    else:
        return v <= LooseVersion('2.3')


EPR_C_BUG_PYEPR009 = has_epr_c_bug_pyepr009()
EPR_C_BUG_BCEPR002 = EPR_C_BUG_PYEPR009


TESTDIR = os.path.abspath(os.path.dirname(__file__))
TEST_PRODUCT = 'ASA_APM_1PNPDE20091007_025628_000000432083_00118_39751_9244.N1'
TEST_PRODUCT_BM_EXPR = None

def quiet(func):
    @functools.wraps(func)
    def wrapper(*args, **kwds):
        sysout = sys.stdout
        syserr = sys.stderr
        try:
            # using '/dev/null' doesn't work in python 3 because the file
            # object coannot be converted into a C FILE*
            # with file(os.devnull) as fd:
            with tempfile.TemporaryFile('w+') as fd:
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


def setUpModule():
    filename = os.path.join(TESTDIR, TEST_PRODUCT)
    baseurl = 'http://www.brockmann-consult.de/beam/data/products/ASAR'
    url = baseurl + '/' + os.path.splitext(TEST_PRODUCT)[0] + '.zip'
    if not os.path.exists(filename):
        with urlopen(url) as src:
            with open(filename + '.zip', 'wb') as dst:
                for data in src:
                    dst.write(data)

        with zipfile.ZipFile(filename + '.zip') as arch:
            arch.extractall(TESTDIR)

        os.remove(filename + '.zip')

    print('Test product:', filename)
    assert os.path.exists(filename)


class TestOpenProduct(unittest.TestCase):
    PRODUCT_FILE = os.path.join(TESTDIR, TEST_PRODUCT)

    def test_open(self):
        with epr.open(self.PRODUCT_FILE) as product:
            self.assertTrue(isinstance(product, epr.Product))
            self.assertEqual(product.mode, 'rb')

    def test_open_rb(self):
        with epr.open(self.PRODUCT_FILE, 'rb') as product:
            self.assertTrue(isinstance(product, epr.Product))
            self.assertEqual(product.mode, 'rb')

    def test_open_rwb_01(self):
        with epr.open(self.PRODUCT_FILE, 'r+b') as product:
            self.assertTrue(isinstance(product, epr.Product))
            self.assertTrue(product.mode in ('r+b', 'rb+'))

    def test_open_rwb_02(self):
        with epr.open(self.PRODUCT_FILE, 'rb+') as product:
            self.assertTrue(isinstance(product, epr.Product))
            self.assertTrue(product.mode in ('r+b', 'rb+'))

    def test_open_invalid_mode_01(self):
        self.assertRaises(ValueError, epr.open, self.PRODUCT_FILE, '')

    def test_open_invalid_mode_02(self):
        self.assertRaises(ValueError, epr.open, self.PRODUCT_FILE, 'rx')

    def test_open_invalid_mode_03(self):
        self.assertRaises(TypeError, epr.open, self.PRODUCT_FILE, 0)

    def test_open_bytes(self):
        filename = self.PRODUCT_FILE.encode('UTF-8')
        with epr.open(filename) as product:
            self.assertTrue(isinstance(product, epr.Product))

    def test_open_pathlib(self):
        filename = pathlib.Path(self.PRODUCT_FILE)
        with epr.open(filename) as product:
            self.assertTrue(isinstance(product, epr.Product))

    def test_product_constructor(self):
        with epr.Product(self.PRODUCT_FILE) as product:
            self.assertTrue(isinstance(product, epr.Product))

    def test_open_failure(self):
        self.assertRaises(epr.EPRError, epr.open, '')

    def test_filename_type(self):
        self.assertRaises(TypeError, epr.open, 3)

    def test_open_failure_invalid_product(self):
        self.assertRaises(ValueError, epr.open, __file__)

    def test_product_constructor_failure(self):
        self.assertRaises(epr.EPRError, epr.Product, '')

    def test_product_constructor_failure_invalid_product(self):
        self.assertRaises(ValueError, epr.Product, __file__)


class TestProduct(unittest.TestCase):
    PRODUCT_FILE = os.path.join(TESTDIR, TEST_PRODUCT)
    OPEN_MODE = 'rb'
    ID_STRING = 'ASA_APM_1PNPDE20091007_025628_000000432083_00118'
    TOT_SIZE = 22903686

    DATASET_NAMES = [
        'MDS1_SQ_ADS',
        'MDS2_SQ_ADS',
        'MAIN_PROCESSING_PARAMS_ADS',
        'DOP_CENTROID_COEFFS_ADS',
        'SR_GR_ADS',
        'CHIRP_PARAMS_ADS',
        'GEOLOCATION_GRID_ADS',
        'MDS1',
        'MDS2',
    ]
    DATASET_NAME = 'MDS1'
    DATASET_WIDTH = 1452
    DATASET_HEIGHT = 3915
    DATASET_NDSDS = 18
    DATASET_NBANDS = 6

    BAND_NAME = 'proc_data_1'
    SPH_DESCRIPTOR = 'AP Mode Medium Res. Image'
    MERIS_IODD_VERSION = 0

    def setUp(self):
        self.product = epr.Product(self.PRODUCT_FILE, self.OPEN_MODE)
        self.bm_expr = TEST_PRODUCT_BM_EXPR

    def tearDown(self):
        self.product.close()

    def test_close(self):
        self.product.close()

    def test_flush(self):
        self.product.flush()

    def test_double_close(self):
        self.product.close()
        self.product.close()

    def test_file_path_property(self):
        self.assertEqual(self.product.file_path,
                         self.PRODUCT_FILE.replace('\\', '/'))

    def test_mode_property(self):
        self.assertEqual(self.product.mode, self.OPEN_MODE)

    def test_tot_size_property(self):
        self.assertEqual(self.product.tot_size, self.TOT_SIZE)

    def test_id_string_property(self):
        self.assertEqual(self.product.id_string, self.ID_STRING)

    def test_meris_iodd_version_property(self):
        self.assertEqual(self.product.meris_iodd_version,
                         self.MERIS_IODD_VERSION)

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
        dataset = self.product.get_dataset(self.DATASET_NAME)
        self.assertTrue(dataset)

    def test_datasets(self):
        datasets = [self.product.get_dataset_at(idx)
                    for idx in range(self.product.get_num_datasets())]
        dataset_names = [ds.get_name() for ds in datasets]
        self.assertEqual(dataset_names, self.DATASET_NAMES)

    def test_get_dsd_at(self):
        self.assertTrue(isinstance(self.product.get_dsd_at(0), epr.DSD))

    def test_get_mph(self):
        record = self.product.get_mph()
        self.assertTrue(isinstance(record, epr.Record))
        product = record.get_field('PRODUCT').get_elem()
        self.assertEqual(product.decode('ascii'),
                         os.path.basename(self.PRODUCT_FILE))

    def test_get_sph(self):
        record = self.product.get_sph()
        self.assertTrue(isinstance(record, epr.Record))
        sph_desct = record.get_field('SPH_DESCRIPTOR').get_elem()
        self.assertEqual(sph_desct.decode('ascii'), self.SPH_DESCRIPTOR)

    def test_get_band_id(self):
        self.assertTrue(isinstance(self.product.get_band(self.BAND_NAME),
                                   epr.Band))

    def test_get_band_id_bytes(self):
        band_name = self.BAND_NAME.encode('UTF-8')
        self.assertTrue(isinstance(band_name, bytes))
        self.assertTrue(isinstance(self.product.get_band(self.BAND_NAME),
                                    epr.Band))

    def test_get_band_id_invalid_name(self):
        self.assertRaises(ValueError, self.product.get_band, '')

    def test_get_band_id_at(self):
        self.assertTrue(isinstance(self.product.get_band_at(0), epr.Band))

    def test_get_band_id_at_invalid_index(self):
        self.assertRaises(ValueError, self.product.get_band_at,
                          self.product.get_num_bands())

    @unittest.skipIf(TEST_PRODUCT_BM_EXPR is None, 'no flag band available')
    def test_read_bitmask_raster(self):
        bm_expr = self.bm_expr

        xoffset = self.DATASET_WIDTH // 2
        yoffset = self.DATASET_HEIGHT // 2
        width = self.DATASET_WIDTH // 2
        height = self.DATASET_HEIGHT // 2

        raster = epr.create_bitmask_raster(width, height)
        raster = self.product.read_bitmask_raster(bm_expr, xoffset, yoffset,
                                                  raster)
        self.assertTrue(isinstance(raster, epr.Raster))
        self.assertEqual(raster.get_width(), width)
        self.assertEqual(raster.get_height(), height)

    @unittest.skipIf(TEST_PRODUCT_BM_EXPR is None, 'no flag band available')
    def test_read_bitmask_raster_bytes(self):
        bm_expr = self.bm_expr.encode('UTF-8')

        self.assertTrue(isinstance(bm_expr, bytes))

        xoffset = self.DATASET_WIDTH // 2
        yoffset = self.DATASET_HEIGHT // 2
        width = self.DATASET_WIDTH // 2
        height = self.DATASET_HEIGHT // 2

        raster = epr.create_bitmask_raster(width, height)
        raster = self.product.read_bitmask_raster(bm_expr, xoffset, yoffset,
                                                  raster)
        self.assertTrue(isinstance(raster, epr.Raster))
        self.assertEqual(raster.get_width(), width)
        self.assertEqual(raster.get_height(), height)

    def test_read_bitmask_raster_with_invalid_bm_expr(self):
        bm_expr = 'l5_flags.LAND AND !l2_flags.CLOUD'

        xoffset = self.DATASET_WIDTH // 2
        yoffset = self.DATASET_HEIGHT // 2
        width = self.DATASET_WIDTH // 2
        height = self.DATASET_HEIGHT // 2

        raster = epr.create_bitmask_raster(width, height)
        self.assertRaises(epr.EPRError, self.product.read_bitmask_raster,
                          bm_expr, xoffset, yoffset, raster)
        try:
            self.product.read_bitmask_raster(bm_expr, xoffset, yoffset, raster)
        except epr.EPRError as e:
            self.assertEqual(e.code, 301)

    def test_read_bitmask_raster_with_wrong_data_type(self):
        bm_expr = 'l2_flags.LAND AND !l2_flags.CLOUD'

        xoffset = self.DATASET_WIDTH // 2
        yoffset = self.DATASET_HEIGHT // 2
        width = self.DATASET_WIDTH // 2
        height = self.DATASET_HEIGHT // 2

        raster = epr.create_raster(epr.E_TID_DOUBLE, width, height)
        self.assertRaises(epr.EPRError, self.product.read_bitmask_raster,
                          bm_expr, xoffset, yoffset, raster)
        try:
            self.product.read_bitmask_raster(bm_expr, xoffset, yoffset, raster)
        except epr.EPRError as e:
            self.assertEqual(e.code, 7)

    def test_fileno(self):
        self.assertTrue(isinstance(self.product._fileno, int))

    def test_fileno_read(self):
        pos = os.lseek(self.product._fileno, 0, os.SEEK_CUR)
        try:
            os.lseek(self.product._fileno, 0, os.SEEK_SET)
            data = os.read(self.product._fileno, 7)
            self.assertEqual(data, b'PRODUCT')
        finally:
            os.lseek(self.product._fileno, pos, os.SEEK_SET)


class TestProductRW(TestProduct):
    OPEN_MODE = 'rb+'


class TestProductHighLevelAPI(unittest.TestCase):
    PRODUCT_FILE = os.path.join(TESTDIR, TEST_PRODUCT)
    DATASET_NAMES = TestProduct.DATASET_NAMES
    BAND_NAMES = [
        'slant_range_time',
        'incident_angle',
        'latitude',
        'longitude',
        'proc_data_1',
        'proc_data_2',
    ]

    def setUp(self):
        self.product = epr.Product(self.PRODUCT_FILE)

    def tearDown(self):
        self.product.close()

    def test_closed(self):
        self.assertFalse(self.product.closed)
        self.product.close()
        self.assertTrue(self.product.closed)

    def test_readonly_closed(self):
        self.assertFalse(self.product.closed)
        self.assertRaises(AttributeError,
                          setattr, self.product, 'closed', True)

    def test_get_dataset_names(self):
        self.assertEqual(self.product.get_dataset_names(), self.DATASET_NAMES)

    def test_get_band_names(self):
        self.assertEqual(self.product.get_band_names(), self.BAND_NAMES)

    def test_datasets(self):
        datasets = self.product.datasets()
        self.assertTrue(datasets)
        self.assertEqual(len(datasets), self.product.get_num_datasets())
        for index, dataset in enumerate(datasets):
            ref_dataset = self.product.get_dataset_at(index)
            self.assertEqual(dataset.get_name(), ref_dataset.get_name())

    def test_bands(self):
        bands = self.product.bands()
        self.assertTrue(bands)
        self.assertEqual(len(bands), self.product.get_num_bands())
        for index, band in enumerate(bands):
            ref_band = self.product.get_band_at(index)
            self.assertEqual(band.get_name(), ref_band.get_name())

    # @TODO: not implemented
    # def test_iter(self):
    #     pass

    def test_repr(self):
        pattern = (r'epr\.Product\((?P<name>\w+)\) '
                   r'(?P<n_datasets>\d+) datasets, '
                   r'(?P<n_bands>\d+) bands')

        mobj = re.match(pattern, repr(self.product))
        self.assertNotEqual(mobj, None)
        self.assertEqual(mobj.group('name'), self.product.id_string)
        self.assertEqual(mobj.group('n_datasets'),
                         str(self.product.get_num_datasets()))
        self.assertEqual(mobj.group('n_bands'),
                         str(self.product.get_num_bands()))

    def test_repr_type(self):
        self.assertTrue(isinstance(repr(self.product), str))

    def test_str(self):
        lines = [repr(self.product), '']
        lines.extend(map(repr, self.product.datasets()))
        lines.append('')
        lines.extend(map(str, self.product.bands()))
        data = '\n'.join(lines)
        self.assertEqual(data, str(self.product))

    def test_str_type(self):
        self.assertTrue(isinstance(str(self.product), str))

    def test_context_manager(self):
        with epr.open(self.PRODUCT_FILE) as product:
            self.assertTrue(isinstance(product, epr.Product))
            self.assertFalse(product.closed)
            self.assertTrue(str(product))

        self.assertTrue(product.closed)


class TestProductLowLevelAPI(unittest.TestCase):
    PRODUCT_FILE = os.path.join(TESTDIR, TEST_PRODUCT)

    def setUp(self):
        self.product = epr.Product(self.PRODUCT_FILE)

    def tearDown(self):
        self.product.close()

    def test_magic(self):
        self.assertEqual(self.product._magic, epr._EPR_MAGIC_PRODUCT_ID)


class TestClosedProduct(unittest.TestCase):
    PRODUCT_FILE = os.path.join(TESTDIR, TEST_PRODUCT)
    DATASET_NAME = 'MDS1'
    BAND_NAME = 'proc_data_1'

    def setUp(self):
        self.product = epr.open(self.PRODUCT_FILE)
        self.product.close()

    def test_properties(self):
        for name in ('file_path', 'tot_size', 'id_string',
                     'meris_iodd_version'):
            self.assertRaises(ValueError, getattr, self.product, name)

    def test_get_get_scene_width(self):
        self.assertRaises(ValueError, self.product.get_scene_width)

    def test_get_get_scene_height(self):
        self.assertRaises(ValueError, self.product.get_scene_height)

    def test_get_num_datasets(self):
        self.assertRaises(ValueError, self.product.get_num_datasets)

    def test_get_num_dsds(self):
        self.assertRaises(ValueError, self.product.get_num_dsds)

    def test_get_num_bands(self):
        self.assertRaises(ValueError, self.product.get_num_bands)

    def test_get_mph(self):
        self.assertRaises(ValueError, self.product.get_mph)

    def test_get_sph(self):
        self.assertRaises(ValueError, self.product.get_sph)

    def test_get_dataset_at(self):
        self.assertRaises(ValueError, self.product.get_dataset_at, 0)

    def test_get_dataset(self):
        self.assertRaises(ValueError, self.product.get_dataset,
                          self.DATASET_NAME)

    def test_get_dsd_at(self):
        self.assertRaises(ValueError, self.product.get_dsd_at, 0)

    def test_get_band_id(self):
        self.assertRaises(ValueError, self.product.get_band, self.BAND_NAME)

    def test_get_band_id_at(self):
        self.assertRaises(ValueError, self.product.get_band_at, 0)

    def test_read_bitmask_raster(self):
        bm_expr = 'l2_flags.LAND AND !l2_flags.CLOUD'
        raster = epr.create_bitmask_raster(12, 10)
        xoffset = 0
        yoffset = 0

        self.assertRaises(ValueError, self.product.read_bitmask_raster,
                          bm_expr, xoffset, yoffset, raster)

    def test_get_dataset_names(self):
        self.assertRaises(ValueError, self.product.get_dataset_names)

    def test_get_band_names(self):
        self.assertRaises(ValueError, self.product.get_band_names)

    def test_datasets(self):
        self.assertRaises(ValueError, self.product.datasets)

    def test_bands(self):
        self.assertRaises(ValueError, self.product.bands)

    def test_repr(self):
        self.assertRaises(ValueError, repr, self.product)

    def test_str(self):
        self.assertRaises(ValueError, str, self.product)


class TestDataset(unittest.TestCase):
    PRODUCT_FILE = os.path.join(TESTDIR, TEST_PRODUCT)
    OPEN_MODE = 'rb'
    DATASET_NAME = 'MDS1'
    DATASET_DESCRIPTION = 'Measurement Data Set 1'
    NUM_RECORDS = 3915
    DSD_NAME = 'MDS1'
    RECORD_INDEX = 0

    def setUp(self):
        self.product = epr.Product(self.PRODUCT_FILE, self.OPEN_MODE)
        self.dataset = self.product.get_dataset(self.DATASET_NAME)

    def tearDown(self):
        self.product.close()

    def test_product_property(self):
        self.assertTrue(equal_products(self.dataset.product, self.product))

    def test_description_property(self):
        self.assertEqual(self.dataset.description, self.DATASET_DESCRIPTION)

    def test_get_name(self):
        self.assertEqual(self.dataset.get_name(), self.DATASET_NAME)

    def test_get_dsd_name(self):
        self.assertEqual(self.dataset.get_dsd_name(), self.DSD_NAME)

    def test_get_num_records(self):
        self.assertEqual(self.dataset.get_num_records(), self.NUM_RECORDS)

    def test_get_dsd(self):
        self.assertTrue(isinstance(self.dataset.get_dsd(), epr.DSD))

    def test_create_record(self):
        record = self.dataset.create_record()
        self.assertTrue(isinstance(record, epr.Record))

    def test_create_record_index(self):
        record = self.dataset.create_record()
        self.assertEqual(record.index, None)

    def test_read_record(self):
        record = self.dataset.read_record(self.RECORD_INDEX)
        self.assertTrue(isinstance(record, epr.Record))

    def test_read_record_index(self):
        record = self.dataset.read_record(self.RECORD_INDEX)
        self.assertEqual(record.index, self.RECORD_INDEX)

    def test_read_record_passed(self):
        created_record = self.dataset.create_record()
        read_record = self.dataset.read_record(self.RECORD_INDEX,
                                               created_record)
        self.assertTrue(created_record is read_record)

    def test_read_record_passed_index(self):
        created_record = self.dataset.create_record()
        self.assertEqual(created_record.index, None)
        read_record = self.dataset.read_record(self.RECORD_INDEX,
                                               created_record)
        self.assertEqual(read_record.index, self.RECORD_INDEX)

    def test_read_record_passed_invalid(self):
        self.assertRaises(TypeError, self.dataset.read_record, 0, 0)


class TestDatasetRW(TestDataset):
    OPEN_MODE = 'rb+'


class TestDatasetHighLevelAPI(unittest.TestCase):
    PRODUCT_FILE = os.path.join(TESTDIR, TEST_PRODUCT)
    DATASET_NAME = TestDataset.DATASET_NAME

    def setUp(self):
        self.product = epr.Product(self.PRODUCT_FILE)
        self.dataset = self.product.get_dataset(self.DATASET_NAME)

    def tearDown(self):
        self.product.close()

    def test_records(self):
        records = self.dataset.records()
        self.assertTrue(records)
        self.assertEqual(len(records), self.dataset.get_num_records())
        for index, record in enumerate(records):
            ref_record = self.dataset.read_record(index)
            self.assertEqual(record.get_field_names(),
                             ref_record.get_field_names())

    def test_iter(self):
        index = 0
        for record in self.dataset:
            ref_record = self.dataset.read_record(index)
            self.assertEqual(record.get_field_names(),
                             ref_record.get_field_names())
            index += 1
        self.assertEqual(index, self.dataset.get_num_records())

    def test_repr(self):
        pattern = r'epr\.Dataset\((?P<name>\w+)\) (?P<num>\d+) records'
        mobj = re.match(pattern, repr(self.dataset))
        self.assertNotEqual(mobj, None)
        self.assertEqual(mobj.group('name'), self.dataset.get_name())
        self.assertEqual(mobj.group('num'),
                         str(self.dataset.get_num_records()))

    def test_repr_type(self):
        self.assertTrue(isinstance(repr(self.dataset), str))

    def test_str(self):
        lines = [repr(self.dataset), '']
        lines.extend(map(str, self.dataset))
        data = '\n'.join(lines)
        self.assertEqual(data, str(self.dataset))

    def test_str_type(self):
        self.assertTrue(isinstance(str(self.dataset), str))


class TestDatasetOnClosedProduct(unittest.TestCase):
    PRODUCT_FILE = os.path.join(TESTDIR, TEST_PRODUCT)
    DATASET_NAME = 'MDS1'

    def setUp(self):
        self.product = epr.Product(self.PRODUCT_FILE)
        self.dataset = self.product.get_dataset(self.DATASET_NAME)
        self.record = self.dataset.create_record()
        self.product.close()

    def test_product_property(self):
        self.assertTrue(isinstance(self.dataset.product, epr.Product))

    def test_description_property(self):
        self.assertRaises(ValueError, getattr, self.dataset, 'description')

    def test_get_name(self):
        self.assertRaises(ValueError, self.dataset.get_name)

    def test_get_dsd_name(self):
        self.assertRaises(ValueError, self.dataset.get_dsd_name)

    def test_get_num_records(self):
        self.assertRaises(ValueError, self.dataset.get_num_records)

    def test_get_dsd(self):
        self.assertRaises(ValueError, self.dataset.get_dsd)

    def test_create_record(self):
        self.assertRaises(ValueError, self.dataset.create_record)

    def test_read_record(self):
        self.assertRaises(ValueError, self.dataset.read_record, 0)

    def test_read_record_passed(self):
        self.assertRaises(ValueError, self.dataset.read_record, 0, self.record)

    def test_records(self):
        self.assertRaises(ValueError, self.dataset.records)

    def test_iter(self):
        self.assertRaises(ValueError, iter, self.dataset)

    def test_repr(self):
        self.assertRaises(ValueError, repr, self.dataset)

    def test_str(self):
        self.assertRaises(ValueError, str, self.dataset)


class TestBand(unittest.TestCase):
    PRODUCT_FILE = os.path.join(TESTDIR, TEST_PRODUCT)
    OPEN_MODE = 'rb+'
    DATASET_NAME = 'MDS1'
    BAND_NAMES = (
        'slant_range_time',
        'incident_angle',
        'latitude',
        'longitude',
        'proc_data_1',
        'proc_data_2',
     )
    BAND_NAME = 'proc_data_1'
    BAND_DESCTIPTION = 'Alternating Polarization Medium Resolution Image'
    XOFFSET = 90
    YOFFSET = 80
    WIDTH = 200
    HEIGHT = 100
    SCALING_FACTOR = 1.0
    SCALING_OFFSET = 0.0
    UNIT = None
    RTOL = 1e-7
    DATA_TYPE = np.float32
    TEST_DATA = np.asarray([
        [228., 213., 235., 256., 239., 260., 210., 197., 233., 213.],
        [246., 248., 333., 317., 272., 247., 247., 221., 221., 205.],
        [239., 297., 412., 381., 301., 226., 262., 256., 229., 214.],
        [212., 279., 328., 318., 279., 231., 253., 274., 240., 242.],
        [199., 236., 245., 262., 282., 265., 261., 255., 255., 239.],
        [214., 218., 284., 300., 269., 266., 272., 224., 292., 238.],
        [240., 241., 300., 308., 248., 254., 269., 230., 276., 256.],
        [256., 261., 265., 269., 263., 262., 279., 279., 300., 367.],
        [273., 262., 262., 239., 270., 284., 344., 380., 416., 447.],
        [292., 286., 303., 261., 284., 374., 445., 431., 422., 416.],
    ])

    def setUp(self):
        self.product = epr.Product(self.PRODUCT_FILE, self.OPEN_MODE)
        self.band = self.product.get_band(self.BAND_NAME)

    def tearDown(self):
        self.product.close()

    def test_product_property(self):
        self.assertTrue(equal_products(self.band.product, self.product))

    def test_spectr_band_index_property(self):
        self.assertEqual(self.band.spectr_band_index, -1)

    def test_sample_model_property(self):
        self.assertEqual(self.band.sample_model, 0)

    def test_data_type_property(self):
        self.assertEqual(self.band.data_type, epr.E_TID_FLOAT)

    def test_scaling_method_property(self):
        self.assertEqual(self.band.scaling_method, epr.E_SMID_LIN)

    def test_scaling_offset_property(self):
        self.assertEqual(self.band.scaling_offset, self.SCALING_OFFSET)

    def test_scaling_factor_property(self):
        self.assertEqual(self.band.scaling_factor, self.SCALING_FACTOR)
        self.assertTrue(isinstance(self.band.scaling_factor, float))

    def test_bm_expr_property(self):
        self.assertEqual(self.band.bm_expr, None)

    def test_unit_property(self):
        self.assertEqual(self.band.unit, self.UNIT)

    def test_description_property(self):
        self.assertEqual(self.band.description, self.BAND_DESCTIPTION)

    def test_lines_mirrored_property(self):
        self.assertTrue(isinstance(self.band.lines_mirrored, bool))
        self.assertEqual(self.band.lines_mirrored, True)

    def test_dataset_property(self):
        dataset = self.band.dataset
        self.assertTrue(isinstance(dataset, epr.Dataset))
        self.assertEqual(dataset.get_name(), self.DATASET_NAME)

    def test_get_name(self):
        for index in range(len(self.BAND_NAMES)):
            b = self.product.get_band_at(index)
            self.assertEqual(b.get_name(), self.BAND_NAMES[index])

    def test_create_compatible_raster(self):
        width = self.product.get_scene_width()
        height = self.product.get_scene_height()
        raster = self.band.create_compatible_raster(width, height)
        self.assertTrue(isinstance(raster, epr.Raster))
        self.assertEqual(raster.get_width(), width)
        self.assertEqual(raster.get_height(), height)
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

        self.assertRaises(ValueError, self.band.create_compatible_raster,
                          self.product.get_scene_width() + 10, height)
        self.assertRaises(ValueError, self.band.create_compatible_raster,
                          width, self.product.get_scene_height() + 10)

    def test_create_compatible_raster_with_step(self):
        src_width = self.product.get_scene_width()
        src_height = self.product.get_scene_height()
        xstep = 2
        ystep = 3
        width = (src_width - 1) // xstep + 1
        height = (src_height - 1) // ystep + 1
        raster = self.band.create_compatible_raster(src_width, src_height,
                                                    xstep, ystep)
        self.assertTrue(isinstance(raster, epr.Raster))
        self.assertEqual(raster.get_width(), width)
        self.assertEqual(raster.get_height(), height)
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

        self.assertRaises((ValueError, ValueError),
                          self.band.create_compatible_raster,
                          width, height, width + 10, 2)
        self.assertRaises((ValueError, ValueError),
                          self.band.create_compatible_raster,
                          width, height, 2, height + 10)
        self.assertRaises((ValueError, ValueError),
                          self.band.create_compatible_raster,
                          width, height, width + 10, height + 10)

    def test_create_compatible_raster_with_default_size(self):
        src_width = self.product.get_scene_width()
        src_height = self.product.get_scene_height()
        raster = self.band.create_compatible_raster()
        self.assertTrue(isinstance(raster, epr.Raster))
        self.assertEqual(raster.get_width(), src_width)
        self.assertEqual(raster.get_height(), src_height)
        # @NOTE: data type on disk is epr.E_TID_USHORT
        self.assertEqual(raster.data_type, epr.E_TID_FLOAT)

    def test_read_raster(self):
        rasterin = self.band.create_compatible_raster(self.WIDTH, self.HEIGHT)

        raster = self.band.read_raster(self.XOFFSET, self.YOFFSET, rasterin)

        self.assertTrue(isinstance(raster, epr.Raster))
        self.assertTrue(raster is rasterin)
        self.assertEqual(raster.get_width(), self.WIDTH)
        self.assertEqual(raster.get_height(), self.HEIGHT)
        # @NOTE: data type on disk is epr.E_TID_USHORT
        self.assertEqual(raster.data_type, epr.E_TID_FLOAT)

        h, w = self.TEST_DATA.shape
        npt.assert_allclose(raster.get_pixel(0, 0),
                            self.TEST_DATA[0, 0],
                            rtol=self.RTOL)
        npt.assert_allclose(raster.get_pixel(w - 1, h - 1),
                            self.TEST_DATA[h - 1, w - 1],
                            rtol=self.RTOL)

    def test_read_raster_none(self):
        raster = self.band.read_raster()

        self.assertTrue(isinstance(raster, epr.Raster))
        self.assertEqual(raster.get_width(), self.product.get_scene_width())
        self.assertEqual(raster.get_height(), self.product.get_scene_height())
        # @NOTE: data type on disk is epr.E_TID_USHORT
        self.assertEqual(raster.data_type, epr.E_TID_FLOAT)

        h, w = self.TEST_DATA.shape
        npt.assert_allclose(
            raster.get_pixel(self.XOFFSET, self.YOFFSET),
            self.TEST_DATA[0, 0],
            rtol=self.RTOL)
        npt.assert_allclose(
            raster.get_pixel(self.XOFFSET + w - 1, self.YOFFSET + h - 1),
            self.TEST_DATA[h - 1, w - 1],
            rtol=self.RTOL)

    def test_read_raster_default_offset(self):
        height = self.HEIGHT
        width = self.WIDTH

        raster1 = self.band.create_compatible_raster(width, height)
        raster2 = self.band.create_compatible_raster(width, height)

        r1 = self.band.read_raster(0, 0, raster1)
        r2 = self.band.read_raster(raster=raster2)

        self.assertTrue(r1 is raster1)
        self.assertTrue(r2 is raster2)
        self.assertEqual(raster1.get_pixel(0, 0), raster2.get_pixel(0, 0))
        self.assertEqual(raster1.get_pixel(width - 1, height - 1),
                         raster2.get_pixel(width - 1, height - 1))

        h, w = self.TEST_DATA.shape
        npt.assert_allclose(
            raster1.get_pixel(self.XOFFSET, self.YOFFSET),
            self.TEST_DATA[0, 0],
            rtol=self.RTOL)
        npt.assert_allclose(
            raster1.get_pixel(self.XOFFSET + w - 1, self.YOFFSET + h - 1),
            self.TEST_DATA[h - 1, w - 1],
            rtol=self.RTOL)

    def test_read_raster_with_invalid_raster(self):
        self.assertRaises(TypeError, self.band.read_raster, 0, 0, 0)

    def test_read_raster_with_invalid_offset(self):
        raster = self.band.create_compatible_raster(self.WIDTH, self.HEIGHT)

        self.assertRaises(ValueError, self.band.read_raster, -1, 0, raster)
        self.assertRaises(ValueError, self.band.read_raster, 0, -1, raster)
        self.assertRaises(ValueError, self.band.read_raster, -1, -1, raster)

        invalid_xoffset = 2 * self.product.get_scene_width()
        invalid_yoffset = 2 * self.product.get_scene_height()
        self.assertRaises(ValueError, self.band.read_raster,
                          invalid_xoffset, 0, raster)
        self.assertRaises(ValueError, self.band.read_raster,
                          0, invalid_yoffset, raster)
        self.assertRaises(ValueError, self.band.read_raster,
                          invalid_xoffset, invalid_yoffset, raster)

    def test_read_as_array_ref(self):
        data = self.band.read_as_array(self.WIDTH, self.HEIGHT,
                                       self.XOFFSET, self.YOFFSET)

        self.assertTrue(isinstance(data, np.ndarray))
        self.assertEqual(data.shape, (self.HEIGHT, self.WIDTH))
        self.assertEqual(data.dtype, self.DATA_TYPE)

        h, w = self.TEST_DATA.shape
        npt.assert_allclose(data[:h, :w], self.TEST_DATA, rtol=self.RTOL)

    def test_read_as_array_cross(self):
        data = self.band.read_as_array()
        box = self.band.read_as_array(self.WIDTH, self.HEIGHT,
                                      self.XOFFSET, self.YOFFSET)

        npt.assert_array_equal(
            data[self.YOFFSET:self.YOFFSET + self.HEIGHT,
                 self.XOFFSET:self.XOFFSET + self.WIDTH],
            box)

    def test_read_as_array_default(self):
        data = self.band.read_as_array()

        self.assertTrue(isinstance(data, np.ndarray))
        self.assertEqual(
            data.shape,
            (self.product.get_scene_height(), self.product.get_scene_width()))
        self.assertEqual(data.dtype, self.DATA_TYPE)

        h, w = self.TEST_DATA.shape
        npt.assert_allclose(
            data[self.YOFFSET:self.YOFFSET + h, self.XOFFSET:self.XOFFSET + w],
            self.TEST_DATA,
            rtol=self.RTOL)

    # @SEEALSO: https://www.brockmann-consult.de/beam-jira/browse/EPR-2
    @unittest.skipIf(EPR_C_BUG_BCEPR002, 'buggy EPR_C_API detected')
    def test_read_as_array_with_step_2(self):
        step = 2
        band = self.band

        data = band.read_as_array()
        box = band.read_as_array(self.WIDTH, self.HEIGHT,
                                 self.XOFFSET, self.YOFFSET, step, step)

        self.assertTrue(isinstance(box, np.ndarray))
        self.assertEqual(
            box.shape,
            ((self.HEIGHT - 1) // step + 1, (self.WIDTH - 1) // step + 1))
        self.assertEqual(box.dtype, self.DATA_TYPE)

        npt.assert_allclose(
            data[self.YOFFSET:self.YOFFSET + self.HEIGHT:step,
                 self.XOFFSET:self.XOFFSET + self.WIDTH:step],
            box)

        h, w = self.TEST_DATA.shape
        npt.assert_allclose(
            box[:(h-1)//step+1, :(w-1)//step+1],
            self.TEST_DATA[::step, ::step],
            rtol=self.RTOL)

    @unittest.skipIf(EPR_C_BUG_BCEPR002, 'buggy EPR_C_API detected')
    def test_read_as_array_with_step_3(self):
        step = 3
        band = self.band

        data = band.read_as_array()
        box = band.read_as_array(self.WIDTH, self.HEIGHT,
                                 self.XOFFSET, self.YOFFSET, step, step)

        self.assertTrue(isinstance(box, np.ndarray))
        self.assertEqual(
            box.shape,
            ((self.HEIGHT - 1) // step + 1, (self.WIDTH - 1) // step + 1))
        self.assertEqual(box.dtype, self.DATA_TYPE)

        npt.assert_allclose(
            data[self.YOFFSET:self.YOFFSET + self.HEIGHT:step,
                 self.XOFFSET:self.XOFFSET + self.WIDTH:step],
            box)

        h, w = self.TEST_DATA.shape
        npt.assert_allclose(
            box[:(h-1)//step+1, :(w-1)//step+1],
            self.TEST_DATA[::step, ::step],
            rtol=self.RTOL)

    @unittest.skipIf(EPR_C_BUG_BCEPR002, 'buggy EPR_C_API detected')
    def test_read_as_array_with_step_4(self):
        step = 4
        band = self.band

        data = band.read_as_array()
        box = band.read_as_array(self.WIDTH, self.HEIGHT,
                                 self.XOFFSET, self.YOFFSET, step, step)

        self.assertTrue(isinstance(box, np.ndarray))
        self.assertEqual(
            box.shape,
            ((self.HEIGHT - 1) // step + 1, (self.WIDTH - 1) // step + 1))
        self.assertEqual(box.dtype, self.DATA_TYPE)

        npt.assert_allclose(
            data[self.YOFFSET:self.YOFFSET + self.HEIGHT:step,
                 self.XOFFSET:self.XOFFSET + self.WIDTH:step],
            box)

        h, w = self.TEST_DATA.shape
        npt.assert_allclose(
            box[:(h-1)//step+1, :(w-1)//step+1],
            self.TEST_DATA[::step, ::step])

    @unittest.skipIf(EPR_C_BUG_BCEPR002, 'buggy EPR_C_API detected')
    def test_read_as_array_with_step_5(self):
        step = 5
        band = self.band

        data = band.read_as_array()
        box = band.read_as_array(self.WIDTH, self.HEIGHT,
                                 self.XOFFSET, self.YOFFSET, step, step)

        self.assertTrue(isinstance(box, np.ndarray))
        self.assertEqual(
            box.shape,
            ((self.HEIGHT - 1) // step + 1, (self.WIDTH - 1) // step + 1))
        self.assertEqual(box.dtype, self.DATA_TYPE)

        npt.assert_allclose(
            data[self.YOFFSET:self.YOFFSET + self.HEIGHT:step,
                 self.XOFFSET:self.XOFFSET + self.WIDTH:step],
            box)

        h, w = self.TEST_DATA.shape
        npt.assert_allclose(
            box[:(h-1)//step+1, :(w-1)//step+1],
            self.TEST_DATA[::step, ::step],
            rtol=self.RTOL)


class TestBandRW(TestBand):
    OPEN_MODE = 'rb+'


class TestAnnotationBand(TestBand):
    DATASET_NAME = 'GEOLOCATION_GRID_ADS'
    BAND_NAME = 'incident_angle'
    BAND_DESCTIPTION = 'Incident angle'
    SCALING_FACTOR = 1.0
    SCALING_OFFSET = 0.0
    UNIT = 'deg'
    RTOL = 1e-7
    TEST_DATA = np.asarray([
        [21.86950111, 21.86438370, 21.85926437, 21.85414696, 21.84902954,
         21.84391022, 21.83879280, 21.83367538, 21.82855606, 21.82343864],
        [21.86950302, 21.86438560, 21.85926628, 21.85414886, 21.84903145,
         21.84391212, 21.83879471, 21.83367729, 21.82855797, 21.82344055],
        [21.86950302, 21.86438560, 21.85926628, 21.85414886, 21.84903145,
         21.84391212, 21.83879471, 21.83367729, 21.82855797, 21.82344055],
        [21.86950302, 21.86438560, 21.85926628, 21.85414886, 21.84903145,
         21.84391212, 21.83879471, 21.83367729, 21.82855797, 21.82344055],
        [21.86950493, 21.86438751, 21.85926819, 21.85415077, 21.84903335,
         21.84391403, 21.83879662, 21.83367920, 21.82855987, 21.82344246],
        [21.86950493, 21.86438751, 21.85926819, 21.85415077, 21.84903335,
         21.84391403, 21.83879661, 21.83367920, 21.82855987, 21.82344246],
        [21.86950493, 21.86438751, 21.85926819, 21.85415077, 21.84903335,
         21.84391403, 21.83879661, 21.83367912, 21.82855987, 21.82344246],
        [21.86950683, 21.86438942, 21.85927009, 21.85415268, 21.84903526,
         21.84391594, 21.83879852, 21.83368111, 21.82856178, 21.82344437],
        [21.86950683, 21.86438942, 21.85927009, 21.85415268, 21.84903526,
         21.84391594, 21.83879852, 21.83368111, 21.82856178, 21.82344437],
        [21.86950683, 21.86438942, 21.85927009, 21.85415268, 21.84903526,
         21.84391594, 21.83879852, 21.83368111, 21.82856178, 21.82344437],
    ])

    @unittest.skipIf(EPR_C_BUG_PYEPR009, 'buggy EPR_C_API detected')
    def test_read_raster(self):
        super(TestAnnotationBand, self).test_read_raster()

    @unittest.skipIf(EPR_C_BUG_PYEPR009, 'buggy EPR_C_API detected')
    def test_read_raster_default_offset(self):
        super(TestAnnotationBand, self).test_read_raster_default_offset()

    @unittest.skipIf(EPR_C_BUG_PYEPR009, 'buggy EPR_C_API detected')
    def test_read_as_array_ref(self):
        super(TestAnnotationBand, self).test_read_as_array_ref()

    @unittest.skipIf(EPR_C_BUG_PYEPR009, 'buggy EPR_C_API detected')
    def test_read_as_array_cross(self):
        super(TestAnnotationBand, self).test_read_as_array_cross()


class TestBandHighLevelAPI(unittest.TestCase):
    PRODUCT_FILE = os.path.join(TESTDIR, TEST_PRODUCT)

    def setUp(self):
        self.product = epr.Product(self.PRODUCT_FILE)

    def tearDown(self):
        self.product.close()

    def test_repr(self):
        pattern = (r'epr.Band\((?P<name>\w+)\) of '
                   r'epr.Product\((?P<product_id>\w+)\)')
        for band in self.product.bands():
            mobj = re.match(pattern, repr(band))
            self.assertNotEqual(mobj, None)
            self.assertEqual(mobj.group('name'), band.get_name())
            self.assertEqual(mobj.group('product_id'), self.product.id_string)

    def test_repr_type(self):
        band = self.product.get_band_at(0)
        self.assertTrue(isinstance(repr(band), str))

    def test_str_type(self):
        band = self.product.get_band_at(0)
        self.assertTrue(isinstance(str(band), str))


class TestBandLowLevelAPI(unittest.TestCase):
    PRODUCT_FILE = os.path.join(TESTDIR, TEST_PRODUCT)
    FIELD_INDEX = 7
    ELEM_INDEX = -1

    def setUp(self):
        self.product = epr.Product(self.PRODUCT_FILE)
        self.band = self.product.get_band_at(0)

    def tearDown(self):
        self.product.close()

    def test_magic(self):
        self.assertEqual(self.band._magic, epr._EPR_MAGIC_BAND_ID)

    def test_field_index(self):
        self.assertEqual(self.band._field_index, self.FIELD_INDEX)

    def test_elem_index(self):
        self.assertEqual(self.band._elem_index, self.ELEM_INDEX)


class TestBandOnClosedProduct(unittest.TestCase):
    PRODUCT_FILE = os.path.join(TESTDIR, TEST_PRODUCT)
    WIDTH = 12
    HEIGHT = 10

    def setUp(self):
        self.product = epr.Product(self.PRODUCT_FILE)
        self.band = self.product.get_band_at(0)
        self.raster = self.band.create_compatible_raster(self.WIDTH,
                                                         self.HEIGHT)
        self.product.close()

    def test_product_property(self):
        self.assertTrue(isinstance(self.band.product, epr.Product))

    def test_properties(self):
        fields = (
            'spectr_band_index',
            'sample_model',
            'data_type',
            'scaling_method',
            'scaling_offset',
            'scaling_factor',
            'bm_expr',
            'unit',
            'description',
            'lines_mirrored',
        )
        for name in fields:
            with self.subTest(field=name):
                self.assertRaises(ValueError, getattr, self.band, name)

    def test_get_name(self):
        self.assertRaises(ValueError, self.product.get_band_at, 0)

    def test_create_compatible_raster(self):
        self.assertRaises(ValueError, self.band.create_compatible_raster,
                          self.WIDTH, self.HEIGHT)

    def test_read_raster(self):
        self.assertRaises(ValueError, self.band.read_raster)

    def test_read_as_array(self):
        self.assertRaises(ValueError, self.band.read_as_array,
                          self.WIDTH, self.HEIGHT)

    def test_str(self):
        self.assertRaises(ValueError, str, self.band)

    def test_repr(self):
        self.assertRaises(ValueError, repr, self.band)


class TestCreateRaster(unittest.TestCase):
    RASTER_WIDTH = 400
    RASTER_HEIGHT = 300
    RASTER_DATA_TYPE = epr.E_TID_FLOAT

    def test_create_raster(self):
        raster = epr.create_raster(self.RASTER_DATA_TYPE, self.RASTER_WIDTH,
                                   self.RASTER_HEIGHT)
        self.assertTrue(isinstance(raster, epr.Raster))
        self.assertEqual(raster.data_type, self.RASTER_DATA_TYPE)
        self.assertEqual(raster.get_width(), self.RASTER_WIDTH)
        self.assertEqual(raster.get_height(), self.RASTER_HEIGHT)

    def test_create_raster_with_step(self):
        src_width = 3 * self.RASTER_WIDTH
        src_height = 2 * self.RASTER_HEIGHT
        raster = epr.create_raster(self.RASTER_DATA_TYPE,
                                   src_width, src_height, 3, 2)
        self.assertTrue(isinstance(raster, epr.Raster))
        self.assertEqual(raster.data_type, self.RASTER_DATA_TYPE)
        self.assertEqual(raster.get_width(), self.RASTER_WIDTH)
        self.assertEqual(raster.get_height(), self.RASTER_HEIGHT)

    def test_create_raster_with_invalid_step(self):
        src_width = 3 * self.RASTER_WIDTH
        src_height = 2 * self.RASTER_HEIGHT
        self.assertRaises(ValueError, epr.create_raster,
                          self.RASTER_DATA_TYPE,  src_width, src_height, 0, 2)

    def test_create_raster_with_invalid_size(self):
        self.assertRaises((ValueError, OverflowError), epr.create_raster,
                          self.RASTER_DATA_TYPE, -1, self.RASTER_HEIGHT)

    def test_create_bitmask_raster(self):
        raster = epr.create_bitmask_raster(self.RASTER_WIDTH,
                                           self.RASTER_HEIGHT)
        self.assertTrue(isinstance(raster, epr.Raster))
        self.assertEqual(raster.data_type, epr.E_TID_UCHAR)
        self.assertEqual(raster.get_width(), self.RASTER_WIDTH)
        self.assertEqual(raster.get_height(), self.RASTER_HEIGHT)

    def test_create_bitmask_raster_with_step(self):
        src_width = 3 * self.RASTER_WIDTH
        src_height = 2 * self.RASTER_HEIGHT
        raster = epr.create_bitmask_raster(src_width, src_height, 3, 2)
        self.assertTrue(isinstance(raster, epr.Raster))
        self.assertEqual(raster.data_type, epr.E_TID_UCHAR)
        self.assertEqual(raster.get_width(), self.RASTER_WIDTH)
        self.assertEqual(raster.get_height(), self.RASTER_HEIGHT)

    def test_create_bitmask_raster_with_invalid_step(self):
        src_width = 3 * self.RASTER_WIDTH
        src_height = 2 * self.RASTER_HEIGHT
        self.assertRaises(ValueError, epr.create_bitmask_raster,
                          src_width, src_height, 0, 2)

    def test_create_bitmask_raster_with_invalid_size(self):
        self.assertRaises((ValueError, OverflowError),
                          epr.create_bitmask_raster, -1, self.RASTER_HEIGHT)


class TestRaster(unittest.TestCase):
    RASTER_WIDTH = TestBand.WIDTH
    RASTER_HEIGHT = TestBand.HEIGHT
    RASTER_DATA_TYPE = epr.E_TID_FLOAT
    RASTER_ELEM_SIZE = 4
    RTOL = 1e-7
    TEST_DATA = np.zeros((10, 10))

    def setUp(self):
        self.raster = epr.create_raster(self.RASTER_DATA_TYPE,
                                        self.RASTER_WIDTH, self.RASTER_HEIGHT)

    def test_get_width(self):
        self.assertEqual(self.raster.get_width(), self.RASTER_WIDTH)

    def test_get_height(self):
        self.assertEqual(self.raster.get_height(), self.RASTER_HEIGHT)

    def test_get_elem_size(self):
        self.assertEqual(self.raster.get_elem_size(), self.RASTER_ELEM_SIZE)

    def test_get_pixel(self):
        self.assertAlmostEqual(self.raster.get_pixel(0, 0),
                               self.TEST_DATA[0, 0])

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
        self.assertTrue(isinstance(self.raster.source_width, numbers.Integral))

    def test_source_height_property(self):
        self.assertEqual(self.raster.source_height, self.RASTER_HEIGHT)
        self.assertTrue(isinstance(self.raster.source_height,
                                   numbers.Integral))

    def test_source_step_x_property(self):
        self.assertEqual(self.raster.source_step_x, 1)
        self.assertTrue(isinstance(self.raster.source_step_x,
                                   numbers.Integral))

    def test_source_step_y_property(self):
        self.assertEqual(self.raster.source_step_y, 1)
        self.assertTrue(isinstance(self.raster.source_step_y,
                                   numbers.Integral))

    def test_data_property(self):
        height = self.raster.get_height()
        width = self.raster.get_width()

        data = self.raster.data

        self.assertTrue(isinstance(data, np.ndarray))
        self.assertEqual(data.ndim, 2)
        self.assertEqual(data.shape, (height, width))
        self.assertEqual(data.dtype, EPR_TO_NUMPY_TYPE[self.raster.data_type])

        ny, nx = self.TEST_DATA.shape
        npt.assert_allclose(data[:ny, :nx], self.TEST_DATA, rtol=self.RTOL)

    def test_data_property_two_times(self):
        data1 = self.raster.data
        data2 = self.raster.data
        self.assertTrue(data1 is data2)
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

        ny, nx = self.TEST_DATA.shape
        npt.assert_allclose(data[:ny, :nx], self.TEST_DATA, rtol=self.RTOL)


class TestRasterRead(TestRaster):
    PRODUCT_FILE = os.path.join(TESTDIR, TEST_PRODUCT)
    BAND_NAME = TestBand.BAND_NAME
    RASTER_XOFFSET = TestBand.XOFFSET
    RASTER_YOFFSET = TestBand.YOFFSET
    TEST_DATA = TestBand.TEST_DATA

    def setUp(self):
        self.product = epr.Product(self.PRODUCT_FILE)
        self.band = self.product.get_band(self.BAND_NAME)
        self.raster = self.band.create_compatible_raster(self.RASTER_WIDTH,
                                                         self.RASTER_HEIGHT)

        self.band.read_raster(self.RASTER_XOFFSET, self.RASTER_YOFFSET,
                              self.raster)

    def tearDown(self):
        self.product.close()

    def test_data_property_shared_semantics_readload(self):
        data1 = self.raster.data
        data1[0, 0] *= 2
        self.band.read_raster(self.RASTER_XOFFSET, self.RASTER_YOFFSET,
                              self.raster)
        data2 = self.raster.data
        self.assertEqual(data1[0, 0], data2[0, 0])
        self.assertTrue(np.all(data1 == data2))


class TestAnnotatedRasterRead(TestRasterRead):
    PRODUCT_FILE = os.path.join(TESTDIR, TEST_PRODUCT)
    BAND_NAME = TestAnnotationBand.BAND_NAME
    RASTER_XOFFSET = TestAnnotationBand.XOFFSET
    RASTER_YOFFSET = TestAnnotationBand.YOFFSET
    TEST_DATA = TestAnnotationBand.TEST_DATA
    RTOL = 1e-6

    @unittest.skipIf(EPR_C_BUG_PYEPR009, 'buggy EPR_C_API detected')
    def test_get_pixel(self):
        super(TestAnnotatedRasterRead, self).test_get_pixel()

    @unittest.skipIf(EPR_C_BUG_PYEPR009, 'buggy EPR_C_API detected')
    def test_data_property(self):
        super(TestAnnotatedRasterRead, self).test_data_property()

    @unittest.skipIf(EPR_C_BUG_PYEPR009, 'buggy EPR_C_API detected')
    def test_data_property_raster_scope(self):
        super(TestAnnotatedRasterRead, self).test_data_property_raster_scope()


class TestRasterHighLevelAPI(unittest.TestCase):
    RASTER_WIDTH = 400
    RASTER_HEIGHT = 300
    RASTER_DATA_TYPE = epr.E_TID_FLOAT

    def setUp(self):
        self.raster = epr.create_raster(self.RASTER_DATA_TYPE,
                                        self.RASTER_WIDTH, self.RASTER_HEIGHT)

    def test_repr(self):
        pattern = (r'<epr.Raster object at 0x\w+> (?P<data_type>\w+) '
                   r'\((?P<lines>\d+)L x (?P<pixels>\d+)P\)')
        mobj = re.match(pattern, repr(self.raster))
        self.assertNotEqual(mobj, None)
        self.assertEqual(mobj.group('data_type'),
                         epr.data_type_id_to_str(self.raster.data_type))
        self.assertEqual(mobj.group('lines'), str(self.raster.get_height()))
        self.assertEqual(mobj.group('pixels'), str(self.raster.get_width()))

    def test_repr_type(self):
        self.assertTrue(isinstance(repr(self.raster), str))

    def test_str_type(self):
        self.assertTrue(isinstance(str(self.raster), str))


class TestRasterLowLevelAPI(unittest.TestCase):
    RASTER_WIDTH = 400
    RASTER_HEIGHT = 300
    RASTER_DATA_TYPE = epr.E_TID_FLOAT

    def setUp(self):
        self.raster = epr.create_raster(self.RASTER_DATA_TYPE,
                                        self.RASTER_WIDTH, self.RASTER_HEIGHT)

    def test_magic(self):
        self.assertEqual(self.raster._magic, epr._EPR_MAGIC_RASTER)


class TestRecord(unittest.TestCase):
    PRODUCT_FILE = os.path.join(TESTDIR, TEST_PRODUCT)
    OPEN_MODE = 'rb'
    DATASET_NAME = 'MDS1_SQ_ADS'
    NUM_FIELD = 39
    FIELD_NAME = 'input_missing_lines_flag'
    TOT_SIZE = 170
    RECORD_INDEX = 0

    def setUp(self):
        self.product = epr.Product(self.PRODUCT_FILE, self.OPEN_MODE)
        self.dataset = self.product.get_dataset(self.DATASET_NAME)
        self.record = self.dataset.read_record(self.RECORD_INDEX)

    def tearDown(self):
        self.product.close()

    def test_get_num_fields(self):
        self.assertEqual(self.record.get_num_fields(), self.NUM_FIELD)

    @quiet
    def test_print(self):
        self.record.print()

    @quiet
    def test_print_ostream(self):
        self.record.print(sys.stderr)

    def test_print_invalid_ostream(self):
        self.assertRaises(TypeError, self.record.print, 'invalid')

    @quiet
    def test_print_element(self):
        self.record.print_element(3, 0)

    @quiet
    def test_print_element_ostream(self):
        self.record.print_element(0, 0, sys.stderr)

    def test_print_element_invalid_ostream(self):
        self.assertRaises(TypeError, self.record.print_element, 0, 0,
                          'invalid')

    @quiet  # quiet avoids errors when sys.stderr does not have fileno
    def test_print_element_field_out_of_range(self):
        index = self.record.get_num_fields() + 10
        self.assertRaises(ValueError, self.record.print_element, index, 0)

    @quiet  # quiet avoids errors when sys.stderr does not have fileno
    def test_print_element_element_out_of_range(self):
        self.assertRaises(ValueError, self.record.print_element, 0, 150)

    def test_get_field(self):
        field = self.record.get_field(self.FIELD_NAME)
        self.assertTrue(isinstance(field, epr.Field))

    def test_get_field_bytes(self):
        field_name = self.FIELD_NAME.encode('UTF-8')
        field = self.record.get_field(self.FIELD_NAME)
        self.assertTrue(isinstance(field_name, bytes))
        self.assertTrue(isinstance(field, epr.Field))

    def test_get_field_invlid_name(self):
        self.assertRaises(ValueError, self.record.get_field, '')

    def test_get_field_at(self):
        self.assertTrue(isinstance(self.record.get_field_at(0), epr.Field))

    def test_get_field_at_invalid_index(self):
        index = self.record.get_num_fields() + 10
        self.assertRaises(ValueError, self.record.get_field_at, index)

    def test_dataset_name(self):
        self.assertEqual(self.record.dataset_name, self.DATASET_NAME)

    def test_dataset_name_new(self):
        record = self.dataset.create_record()
        self.assertEqual(record.dataset_name, self.DATASET_NAME)

    def test_tot_size(self):
        self.assertEqual(self.record.tot_size, self.TOT_SIZE)

    def test_index(self):
        self.assertEqual(self.record.index, self.RECORD_INDEX)


class TestRecordRW(TestRecord):
    OPEN_MODE = 'rb+'


class TestRecordHighLevelAPI(unittest.TestCase):
    PRODUCT_FILE = os.path.join(TESTDIR, TEST_PRODUCT)
    DATASET_NAME = TestRecord.DATASET_NAME
    FIELD_NAMES = [
        'zero_doppler_time',
        'attach_flag',
        'input_mean_flag',
        'input_std_dev_flag',
        'input_gaps_flag',
        'input_missing_lines_flag',
        'dop_cen_flag',
        'dop_amb_flag',
        'output_mean_flag',
        'output_std_dev_flag',
        'chirp_flag',
        'missing_data_sets_flag',
        'invalid_downlink_flag',
        'spare_1',
        'thresh_chirp_broadening',
        'thresh_chirp_sidelobe',
        'thresh_chirp_islr',
        'thresh_input_mean',
        'exp_input_mean',
        'thresh_input_std_dev',
        'exp_input_std_dev',
        'thresh_dop_cen',
        'thresh_dop_amb',
        'thresh_output_mean',
        'exp_output_mean',
        'thresh_output_std_dev',
        'exp_output_std_dev',
        'thresh_input_missing_lines',
        'thresh_input_gaps',
        'lines_per_gaps',
        'spare_2',
        'input_mean',
        'input_std_dev',
        'num_gaps',
        'num_missing_lines',
        'output_mean',
        'output_std_dev',
        'tot_errors',
        'Spare_3',
    ]

    def setUp(self):
        self.product = epr.Product(self.PRODUCT_FILE)
        self.dataset = self.product.get_dataset(self.DATASET_NAME)
        self.record = self.dataset.read_record(0)

    def tearDown(self):
        self.product.close()

    def test_get_field_names_number(self):
        self.assertEqual(len(self.record.get_field_names()),
                         self.record.get_num_fields())

    def test_get_field_names(self):
        self.assertEqual(self.record.get_field_names()[:len(self.FIELD_NAMES)],
                         self.FIELD_NAMES)

    def test_fields(self):
        fields = self.record.fields()
        self.assertTrue(fields)
        self.assertEqual(len(fields), self.record.get_num_fields())
        names = [field.get_name() for field in fields]
        self.assertEqual(self.record.get_field_names(), names)

    def test_iter(self):
        index = 0
        for field in self.record:
            ref_field = self.record.get_field_at(index)
            self.assertEqual(field.get_name(), ref_field.get_name())
            index += 1
        self.assertEqual(index, self.record.get_num_fields())

    def test_repr_type(self):
        self.assertTrue(isinstance(repr(self.record), str))

    def test_str_type(self):
        self.assertTrue(isinstance(str(self.record), str))


class TestRecordLowLevelAPI(unittest.TestCase):
    PRODUCT_FILE = os.path.join(TESTDIR, TEST_PRODUCT)
    RECORD_INDEX = 0
    RECORD_SIZE = 170
    RECORD_OFFSET = RECORD_INDEX * RECORD_SIZE

    def setUp(self):
        self.product = epr.Product(self.PRODUCT_FILE)
        dataset = self.product.get_dataset_at(0)
        self.record = dataset.read_record(self.RECORD_INDEX)

    def tearDown(self):
        self.product.close()

    def test_magic(self):
        self.assertEqual(self.record._magic, epr._EPR_MAGIC_RECORD)

    def test_get_offset(self):
        self.assertEqual(self.record.get_offset(), self.RECORD_OFFSET)


class TestMultipleRecordsHighLevelAPI(unittest.TestCase):
    PRODUCT_FILE = os.path.join(TESTDIR, TEST_PRODUCT)
    DATASET_NAME = TestProduct.DATASET_NAME

    def setUp(self):
        self.product = epr.Product(self.PRODUCT_FILE)
        self.dataset = self.product.get_dataset(self.DATASET_NAME)

    def tearDown(self):
        self.product.close()

    def test_repr(self):
        pattern = r'<epr\.Record object at 0x\w+> (?P<num>\d+) fields'
        for record in self.dataset:
            mobj = re.match(pattern, repr(record))
            self.assertNotEqual(mobj, None)
            self.assertEqual(mobj.group('num'), str(record.get_num_fields()))

    def test_str_vs_print(self):
        for record in self.dataset:
            with tempfile.TemporaryFile('w+') as fd:
                record.print(fd)
                fd.flush()
                fd.seek(0)
                data = fd.read()
                if data.endswith('\n'):
                    data = data[:-1]
                self.assertEqual(data, str(record))


class TestMphRecordHighLevelAPI(TestRecordHighLevelAPI):
    PRODUCT_FILE = os.path.join(TESTDIR, TEST_PRODUCT)
    DATASET_NAME = 'MPH'
    FIELD_NAMES = [
        'PRODUCT',
        'PROC_STAGE',
        'REF_DOC',
        'ACQUISITION_STATION',
        'PROC_CENTER',
        'PROC_TIME',
        'SOFTWARE_VER',
        'SENSING_START',
        'SENSING_STOP',
        'PHASE',
        'CYCLE',
        'REL_ORBIT',
    ]

    def setUp(self):
        self.product = epr.Product(self.PRODUCT_FILE)
        self.record = self.product.get_mph()

    def tearDown(self):
        self.product.close()

    def test_index(self):
        self.assertEqual(self.record.index, None)


class TestRecordOnClosedProduct(unittest.TestCase):
    PRODUCT_FILE = os.path.join(TESTDIR, TEST_PRODUCT)
    DATASET_NAME = 'MDS1_SQ_ADS'
    NUM_FIELD = 39
    FIELD_NAME = 'input_missing_lines_flag'
    FIELD_NAMES = TestRecordHighLevelAPI.FIELD_NAMES

    def setUp(self):
        product = epr.Product(self.PRODUCT_FILE)
        dataset = product.get_dataset(self.DATASET_NAME)
        self.record = dataset.read_record(0)
        # self.mph = product.get_mph()
        product.close()

    def test_get_num_fields(self):
        self.assertEqual(self.record.get_num_fields(), self.NUM_FIELD)

    # def test_get_num_fields_mph(self):
    #     self.assertEqual(self.mph.get_num_fields(), 34)

    def test_print(self):
        self.assertRaises(ValueError, self.record.print)

    def test_print_element(self):
        self.assertRaises(ValueError, self.record.print_element, 3, 0)

    def test_get_field(self):
        self.assertRaises(ValueError, self.record.get_field, self.FIELD_NAME)

    def test_get_field_at(self):
        self.assertRaises(ValueError, self.record.get_field_at, 0)

    def test_get_field_names(self):
        self.assertRaises(ValueError, self.record.get_field_names)

    def test_fields(self):
        self.assertRaises(ValueError, self.record.fields)

    def test_iter(self):
        self.assertRaises(ValueError, iter, self.record)

    def test_repr(self):
        self.assertRaises(ValueError, repr, self.record)

    def test_str(self):
        self.assertRaises(ValueError, str, self.record)


class TestField(unittest.TestCase):
    PRODUCT_FILE = os.path.join(TESTDIR, TEST_PRODUCT)
    OPEN_MODE = 'rb'
    DATASET_NAME = 'MDS1_SQ_ADS'
    RECORD_INDEX = 0

    FIELD_NAME = 'input_missing_lines_flag'
    FIELD_DESCRIPTION = (
        'Missing lines significant flag. '
        '0 = percentage of missing lines &lt;= threshold value '
        '1 = percentage of missing lines &gt; threshold value. '
        'The number of missing lines is the number of lines missing from '
        'the input data excluding data gaps.'
    )
    FIELD_TYPE = epr.E_TID_UCHAR
    # FIELD_TYPE_NAME = 'uchar'
    FIELD_NUM_ELEMS = 1
    FIELD_VALUES = (0,)
    FIELD_UNIT = 'flag'
    FIELD_OFFSET = 16

    def setUp(self):
        self.product = epr.Product(self.PRODUCT_FILE, self.OPEN_MODE)
        dataset = self.product.get_dataset(self.DATASET_NAME)
        record = dataset.read_record(self.RECORD_INDEX)
        self.field = record.get_field(self.FIELD_NAME)

    def tearDown(self):
        self.product.close()

    @quiet
    def test_print_field(self):
        self.field.print()

    @quiet
    def test_print_field_ostream(self):
        self.field.print(sys.stderr)

    def test_print_fied_invalid_ostream(self):
        self.assertRaises(TypeError, self.field.print, 'invalid')

    def test_get_unit(self):
        self.assertEqual(self.field.get_unit(), self.FIELD_UNIT)

    def test_get_description(self):
        self.assertEqual(self.field.get_description(), self.FIELD_DESCRIPTION)

    def test_get_num_elems(self):
        self.assertEqual(self.field.get_num_elems(), self.FIELD_NUM_ELEMS)

    def test_get_name(self):
        self.assertEqual(self.field.get_name(), self.FIELD_NAME)

    def test_get_type(self):
        self.assertEqual(self.field.get_type(), self.FIELD_TYPE)

    def test_get_offset(self):
        self.assertEqual(self.field.get_offset(), self.FIELD_OFFSET)

    def test_get_elem(self):
        self.assertEqual(self.field.get_elem(), self.FIELD_VALUES[0])

    def test_get_elem_index(self):
        self.assertEqual(self.field.get_elem(0), self.FIELD_VALUES[0])

    def test_get_elem_invalid_index(self):
        self.assertRaises(ValueError, self.field.get_elem,
                          self.FIELD_NUM_ELEMS + 10)

    def test_get_elems(self):
        vect = self.field.get_elems()
        self.assertTrue(isinstance(vect, np.ndarray))
        self.assertEqual(vect.shape, (self.field.get_num_elems(),))
        self.assertEqual(vect.dtype, epr.get_numpy_dtype(self.FIELD_TYPE))
        npt.assert_allclose(vect[:len(self.FIELD_VALUES)], self.FIELD_VALUES)

    def test_tot_size(self):
        elem_size = epr.get_data_type_size(self.FIELD_TYPE)
        tot_size = elem_size * self.FIELD_NUM_ELEMS
        self.assertEqual(self.field.tot_size, tot_size)


class TestFieldRW(TestField):
    OPEN_MODE = 'rb+'


class TestFieldWriteOnReadOnly(unittest.TestCase):
    PRODUCT_FILE = os.path.join(TESTDIR, TEST_PRODUCT)
    OPEN_MODE = 'rb'
    DATASET_NAME = 'MDS1'
    RECORD_INDEX = 10

    FIELD_NAME = 'proc_data'
    FIELD_DESCRIPTION = 'SAR Processed Data. Real samples (detected products)'
    FIELD_TYPE = epr.E_TID_USHORT
    FIELD_TYPE_NAME = 'ushort'
    FIELD_UNIT = ''
    FIELD_NUM_ELEMS = 1452

    def setUp(self):
        self.filename = self.PRODUCT_FILE + '_'
        shutil.copy(self.PRODUCT_FILE, self.filename)
        self.product = epr.Product(self.filename, self.OPEN_MODE)
        dataset = self.product.get_dataset(self.DATASET_NAME)
        record = dataset.read_record(self.RECORD_INDEX)
        self.field = record.get_field(self.FIELD_NAME)

    def tearDown(self):
        self.product.close()
        os.unlink(self.filename)

    def test_write_on_read_only_product(self):
        value = self.field.get_elem() + 10
        self.assertRaises(TypeError, self.field.set_elem, value)


class TestFieldWrite(unittest.TestCase):
    PRODUCT_FILE = os.path.join(TESTDIR, TEST_PRODUCT)
    OPEN_MODE = 'rb+'
    REOPEN = False
    DATASET_NAME = 'MDS1'
    RECORD_INDEX = 100

    FIELD_NAME = 'proc_data'
    FIELD_DESCRIPTION = 'SAR Processed Data. Real samples (detected products)'
    FIELD_TYPE = epr.E_TID_USHORT
    FIELD_TYPE_NAME = 'ushort'
    FIELD_UNIT = ''
    FIELD_INDEX = 3
    FIELD_NUM_ELEMS = 1452
    FIELD_VALUES = (
           0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
           0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
           0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
           0,    0,    0,    0,    0, 2417, 2282, 2280, 2393, 2440,
        2697, 3119, 3577, 3853, 3688, 3784, 4201, 3846, 2821, 2186,
    )

    def setUp(self):
        self.filename = self.PRODUCT_FILE + '_'
        shutil.copy(self.PRODUCT_FILE, self.filename)
        self.product = None
        self.dataset = None
        self.record = None
        self.field = None
        self.reopen(self.OPEN_MODE)
        self.offset = self._get_offset()

    def _get_offset(self):
        offset = self.dataset.get_dsd().ds_offset
        offset += self.record.index * self.record.tot_size
        for i in range(self.FIELD_INDEX):
            offset += self.record.get_field_at(i).tot_size

        return offset

    def tearDown(self):
        self.product.close()
        os.unlink(self.filename)

    def reopen(self, mode='rb'):
        if self.product is not None:
            self.product.close()
        self.product = epr.Product(self.filename, mode)
        self.dataset = self.product.get_dataset(self.DATASET_NAME)
        self.record = self.dataset.read_record(self.RECORD_INDEX)
        self.field = self.record.get_field(self.FIELD_NAME)

    def read(self, offset=0, size=None):
        if size is None:
            size = self.field.tot_size

        os.lseek(self.product._fileno, self.offset + offset, os.SEEK_SET)

        return os.read(self.product._fileno, size)

    def test_set_elem_metadata(self):
        self.assertEqual(self.field.get_description(), self.FIELD_DESCRIPTION)
        self.assertEqual(self.field.get_num_elems(), self.FIELD_NUM_ELEMS)
        self.assertEqual(self.field.get_type(), self.FIELD_TYPE)
        self.assertEqual(epr.data_type_id_to_str(self.field.get_type()),
                         self.FIELD_TYPE_NAME)
        self.assertEqual(self.field.get_unit(), self.FIELD_UNIT)

        value = self.field.get_elem() + 10
        self.field.set_elem(value)

        if self.REOPEN:
            self.reopen()
        else:
            self.product.flush()

        self.assertEqual(self.field.get_description(), self.FIELD_DESCRIPTION)
        self.assertEqual(self.field.get_num_elems(), self.FIELD_NUM_ELEMS)
        self.assertEqual(self.field.get_type(), self.FIELD_TYPE)
        self.assertEqual(epr.data_type_id_to_str(self.field.get_type()),
                         self.FIELD_TYPE_NAME)
        self.assertEqual(self.field.get_unit(), self.FIELD_UNIT)

    def test_set_elem_data(self):
        npt.assert_array_equal(
            self.field.get_elems()[:len(self.FIELD_VALUES)],
            self.FIELD_VALUES)
        self.assertEqual(self.field.get_elem(), self.FIELD_VALUES[0])

        value = self.field.get_elem() + 10
        self.field.set_elem(value)

        if self.REOPEN:
            self.reopen()
        else:
            self.product.flush()

        self.assertEqual(self.field.get_elem(), value)

        values = np.array(self.FIELD_VALUES)
        values[0] = value
        npt.assert_array_equal(
            self.field.get_elems()[:len(self.FIELD_VALUES)], values)

    def test_set_elem_rawdata(self):
        orig_data = self.read()

        value = self.field.get_elem() + 10
        self.field.set_elem(value)

        if self.REOPEN:
            self.reopen()
        else:
            self.product.flush()

        data = self.read()
        self.assertNotEqual(data, orig_data)

        dtype = np.dtype(epr.get_numpy_dtype(self.FIELD_TYPE))
        if dtype.byteorder != '>':
            dtype = dtype.newbyteorder()

        data = np.frombuffer(data, dtype)
        orig_data = np.frombuffer(orig_data, dtype).copy()
        orig_data[0] = value
        npt.assert_array_equal(data, orig_data)

    def test_set_elem0_metadata(self):
        self.assertEqual(self.field.get_description(), self.FIELD_DESCRIPTION)
        self.assertEqual(self.field.get_num_elems(), self.FIELD_NUM_ELEMS)
        self.assertEqual(self.field.get_type(), self.FIELD_TYPE)
        self.assertEqual(epr.data_type_id_to_str(self.field.get_type()),
                         self.FIELD_TYPE_NAME)
        self.assertEqual(self.field.get_unit(), self.FIELD_UNIT)

        value = self.field.get_elem(0) + 10
        self.field.set_elem(value)

        if self.REOPEN:
            self.reopen()
        else:
            self.product.flush()

        self.assertEqual(self.field.get_description(), self.FIELD_DESCRIPTION)
        self.assertEqual(self.field.get_num_elems(), self.FIELD_NUM_ELEMS)
        self.assertEqual(self.field.get_type(), self.FIELD_TYPE)
        self.assertEqual(epr.data_type_id_to_str(self.field.get_type()),
                         self.FIELD_TYPE_NAME)
        self.assertEqual(self.field.get_unit(), self.FIELD_UNIT)

    def test_set_elem0_data(self):
        npt.assert_array_equal(
            self.field.get_elems()[:len(self.FIELD_VALUES)],
            self.FIELD_VALUES)
        self.assertEqual(self.field.get_elem(0), self.FIELD_VALUES[0])

        value = self.field.get_elem(0) + 10
        self.field.set_elem(value)

        if self.REOPEN:
            self.reopen()
        else:
            self.product.flush()

        self.assertEqual(self.field.get_elem(0), value)

        values = np.array(self.FIELD_VALUES)
        values[0] = value
        npt.assert_array_equal(
            self.field.get_elems()[:len(self.FIELD_VALUES)], values)

    def test_set_elem0_rawdata(self):
        orig_data = self.read()

        value = self.field.get_elem(0) + 10
        self.field.set_elem(value)

        if self.REOPEN:
            self.reopen()
        else:
            self.product.flush()

        data = self.read()
        self.assertNotEqual(data, orig_data)

        dtype = np.dtype(epr.get_numpy_dtype(self.FIELD_TYPE))
        if dtype.byteorder != '>':
            dtype = dtype.newbyteorder()

        data = np.frombuffer(data, dtype)
        orig_data = np.frombuffer(orig_data, dtype).copy()
        orig_data[0] = value
        npt.assert_array_equal(data, orig_data)

    def test_set_elem20_metadata(self):
        self.assertEqual(self.field.get_description(), self.FIELD_DESCRIPTION)
        self.assertEqual(self.field.get_num_elems(), self.FIELD_NUM_ELEMS)
        self.assertEqual(self.field.get_type(), self.FIELD_TYPE)
        self.assertEqual(epr.data_type_id_to_str(self.field.get_type()),
                         self.FIELD_TYPE_NAME)
        self.assertEqual(self.field.get_unit(), self.FIELD_UNIT)

        value = self.field.get_elem(20) + 1
        self.field.set_elem(value, 20)

        if self.REOPEN:
            self.reopen()
        else:
            self.product.flush()

        self.assertEqual(self.field.get_description(), self.FIELD_DESCRIPTION)
        self.assertEqual(self.field.get_num_elems(), self.FIELD_NUM_ELEMS)
        self.assertEqual(self.field.get_type(), self.FIELD_TYPE)
        self.assertEqual(epr.data_type_id_to_str(self.field.get_type()),
                         self.FIELD_TYPE_NAME)
        self.assertEqual(self.field.get_unit(), self.FIELD_UNIT)

    def test_set_elem20_data(self):
        npt.assert_array_equal(
            self.field.get_elems()[:len(self.FIELD_VALUES)],
            self.FIELD_VALUES)
        self.assertEqual(self.field.get_elem(20), self.FIELD_VALUES[20])

        value = self.field.get_elem(20) + 1
        self.field.set_elem(value, 20)

        if self.REOPEN:
            self.reopen()
        else:
            self.product.flush()

        self.assertEqual(self.field.get_elem(20), value)

        values = np.array(self.FIELD_VALUES)
        values[20] = value
        npt.assert_array_equal(
            self.field.get_elems()[:len(self.FIELD_VALUES)], values)

    def test_set_elem20_rawdata(self):
        orig_data = self.read()

        value = self.field.get_elem(20) + 1
        self.field.set_elem(value, 20)

        if self.REOPEN:
            self.reopen()
        else:
            self.product.flush()

        data = self.read()
        self.assertNotEqual(data, orig_data)

        dtype = np.dtype(epr.get_numpy_dtype(self.FIELD_TYPE))
        if dtype.byteorder != '>':
            dtype = dtype.newbyteorder()

        data = np.frombuffer(data, dtype)
        orig_data = np.frombuffer(orig_data, dtype).copy()
        orig_data[20] = value
        npt.assert_array_equal(data, orig_data)

    def test_set_elems_metadata(self):
        self.assertEqual(self.field.get_description(), self.FIELD_DESCRIPTION)
        self.assertEqual(self.field.get_num_elems(), self.FIELD_NUM_ELEMS)
        self.assertEqual(self.field.get_type(), self.FIELD_TYPE)
        self.assertEqual(epr.data_type_id_to_str(self.field.get_type()),
                         self.FIELD_TYPE_NAME)
        self.assertEqual(self.field.get_unit(), self.FIELD_UNIT)

        values = self.field.get_elems() + 1
        self.field.set_elems(values)

        if self.REOPEN:
            self.reopen()
        else:
            self.product.flush()

        self.assertEqual(self.field.get_description(), self.FIELD_DESCRIPTION)
        self.assertEqual(self.field.get_num_elems(), self.FIELD_NUM_ELEMS)
        self.assertEqual(self.field.get_type(), self.FIELD_TYPE)
        self.assertEqual(epr.data_type_id_to_str(self.field.get_type()),
                         self.FIELD_TYPE_NAME)
        self.assertEqual(self.field.get_unit(), self.FIELD_UNIT)

    def test_set_elems_data(self):
        npt.assert_array_equal(
            self.field.get_elems()[:len(self.FIELD_VALUES)],
            self.FIELD_VALUES)

        values = self.field.get_elems() + 1
        self.field.set_elems(values)

        if self.REOPEN:
            self.reopen()
        else:
            self.product.flush()

        npt.assert_array_equal(self.field.get_elems(), values)

    def test_set_elems_rawdata(self):
        orig_data = self.read()

        values = self.field.get_elems() + 1
        self.field.set_elems(values)

        if self.REOPEN:
            self.reopen()
        else:
            self.product.flush()

        data = self.read()
        self.assertNotEqual(data, orig_data)

        dtype = np.dtype(epr.get_numpy_dtype(self.FIELD_TYPE))
        if dtype.byteorder != '>':
            dtype = dtype.newbyteorder()

        data = np.frombuffer(data, dtype)
        orig_data = np.frombuffer(orig_data, dtype).copy()
        orig_data += 1
        npt.assert_array_equal(data, orig_data)

    def test_set_mph_elem(self):
        mph = self.product.get_mph()
        field = mph.get_field_at(3)
        self.assertRaises(NotImplementedError, field.set_elem, 5)


class TestFieldWriteReopen(TestFieldWrite):
    REOPEN = True


class TestTimeField(TestField):
    PRODUCT_FILE = os.path.join(TESTDIR, TEST_PRODUCT)
    DATASET_NAME = 'MDS1_SQ_ADS'

    FIELD_NAME = 'zero_doppler_time'
    FIELD_DESCRIPTION = 'Zero doppler time at which SQ information applies'
    FIELD_TYPE = epr.E_TID_TIME
    FIELD_TYPE_NAME = 'time'
    FIELD_NUM_ELEMS = 1
    FIELD_VALUES = (
        epr.EPRTime(days=3567, seconds=10588, microseconds=239091),
    )
    FIELD_UNIT = 'MJD'
    FIELD_OFFSET = 0

    def test_get_elems(self):
        vect = self.field.get_elems()
        self.assertTrue(isinstance(vect, np.ndarray))
        self.assertEqual(vect.shape, (self.field.get_num_elems(),))
        self.assertEqual(vect.dtype, epr.MJD)
        value = self.FIELD_VALUES[0]
        self.assertEqual(vect[0]['days'], value.days)
        self.assertEqual(vect[0]['seconds'], value.seconds)
        self.assertEqual(vect[0]['microseconds'], value.microseconds)


class TestFieldWithMiltipleElems(TestField):
    DATASET_NAME = TestProduct.DATASET_NAME
    RECORD_INDEX = TestFieldWrite.RECORD_INDEX
    FIELD_NAME = 'proc_data'
    FIELD_DESCRIPTION = 'SAR Processed Data. Real samples (detected products)'
    FIELD_TYPE = epr.E_TID_USHORT
    FIELD_TYPE_NAME = 'ushort'
    FIELD_NUM_ELEMS = 1452
    FIELD_VALUES = TestFieldWrite.FIELD_VALUES
    FIELD_UNIT = ''
    FIELD_OFFSET = 17


class TestFieldHighLevelAPI(unittest.TestCase):
    PRODUCT_FILE = os.path.join(TESTDIR, TEST_PRODUCT)
    DATASET_NAME = TestProduct.DATASET_NAME

    def setUp(self):
        self.product = epr.Product(self.PRODUCT_FILE)
        dataset = self.product.get_dataset(self.DATASET_NAME)
        self.record = dataset.read_record(0)

    def tearDown(self):
        self.product.close()

    def test_repr(self):
        pattern = (r'epr\.Field\("(?P<name>.+)"\) (?P<num>\d+) '
                   r'(?P<type>\w+) elements')
        for field in self.record:
            mobj = re.match(pattern, repr(field))
            self.assertNotEqual(mobj, None)
            self.assertEqual(mobj.group('name'), field.get_name())
            self.assertEqual(mobj.group('num'), str(field.get_num_elems()))
            self.assertEqual(mobj.group('type'),
                             epr.data_type_id_to_str(field.get_type()))

    def test_repr_type(self):
        field = self.record.get_field_at(0)
        self.assertTrue(isinstance(repr(field), str))

    def test_str_type(self):
        field = self.record.get_field_at(0)
        self.assertTrue(isinstance(str(field), str))

    def test_str_vs_print(self):
        for field in self.record:
            with tempfile.TemporaryFile('w+') as fd:
                field.print(fd)
                fd.flush()
                fd.seek(0)
                data = fd.read()
                if data.endswith('\n'):
                    data = data[:-1]
                self.assertEqual(data, str(field))

    def test_eq_field1_field1(self):
        field = self.record.get_field_at(0)
        self.assertEqual(field, field)

    def test_eq_field1_field2(self):
        field1 = self.record.get_field_at(1)
        field2 = self.record.get_field_at(2)
        self.assertFalse(field1 == field2)

    def test_eq_field_record(self):
        field = self.record.get_field_at(0)
        self.assertFalse(field == self.record)

    def test_ne_field1_field1(self):
        field = self.record.get_field_at(0)
        self.assertFalse(field != field)

    def test_ne_field1_field2(self):
        field1 = self.record.get_field_at(1)
        field2 = self.record.get_field_at(2)
        self.assertNotEqual(field1, field2)

    def test_ne_field_record(self):
        field = self.record.get_field_at(0)
        self.assertNotEqual(field, self.record)


class TestFieldHighLevelAPI2(unittest.TestCase):
    PRODUCT_FILE = os.path.join(TESTDIR, TEST_PRODUCT)
    DATASET_NAME = 'MAIN_PROCESSING_PARAMS_ADS'
    RECORD_INDEX = 0

    def setUp(self):
        self.product = epr.Product(self.PRODUCT_FILE)

    def tearDown(self):
        self.product.close()

    def test_len_1(self):
        dataset = self.product.get_dataset(self.DATASET_NAME)
        record = dataset.read_record(self.RECORD_INDEX)
        field = record.get_field('range_spacing')
        self.assertEqual(len(field), field.get_num_elems())

    def test_len_x(self):
        dataset = self.product.get_dataset(self.DATASET_NAME)
        record = dataset.read_record(self.RECORD_INDEX)
        field = record.get_field('image_parameters.prf_value')
        self.assertEqual(len(field), field.get_num_elems())

    def test_len_e_tid_unknown(self):
        dataset = self.product.get_dataset(self.DATASET_NAME)
        record = dataset.read_record(self.RECORD_INDEX)
        field = record.get_field('spare_1')
        self.assertEqual(len(field), field.get_num_elems())

    def test_len_e_tid_string(self):
        dataset = self.product.get_dataset(self.DATASET_NAME)
        record = dataset.read_record(self.RECORD_INDEX)
        field = record.get_field('swath_id')
        self.assertEqual(len(field), len(field.get_elem()))


class TestFieldLowLevelAPI(unittest.TestCase):
    PRODUCT_FILE = os.path.join(TESTDIR, TEST_PRODUCT)
    DATASET_INDEX = 0
    RECORD_INDEX = 0
    FIELD_NAME = 'invalid_downlink_flag'
    FIELD_OFFSET = 23

    def setUp(self):
        self.product = epr.Product(self.PRODUCT_FILE)
        dataset = self.product.get_dataset_at(self.DATASET_INDEX)
        record = dataset.read_record(self.RECORD_INDEX)
        self.field = record.get_field(self.FIELD_NAME)

    def tearDown(self):
        self.product.close()

    def test_magic(self):
        self.assertEqual(self.field._magic, epr._EPR_MAGIC_FIELD)

    def test_get_offset(self):
        self.assertEqual(self.field.get_offset(), self.FIELD_OFFSET)


class TestFieldOnClosedProduct(unittest.TestCase):
    PRODUCT_FILE = os.path.join(TESTDIR, TEST_PRODUCT)
    DATASET_NAME = 'MDS1_SQ_ADS'
    RECOSR_INDEX = 0
    FIELD_NAME = 'invalid_downlink_flag'
    FIELD_NAME2 = 'zero_doppler_time'

    def setUp(self):
        product = epr.Product(self.PRODUCT_FILE)
        dataset = product.get_dataset(self.DATASET_NAME)
        self.record = dataset.read_record(self.RECOSR_INDEX)
        self.field = self.record.get_field(self.FIELD_NAME)
        self.field2 = self.record.get_field(self.FIELD_NAME2)
        product.close()

    def test_print_field(self):
        self.assertRaises(ValueError, self.field.print)

    def test_get_unit(self):
        self.assertRaises(ValueError, self.field.get_unit)

    def test_get_description(self):
        self.assertRaises(ValueError, self.field.get_description)

    def test_get_num_elems(self):
        self.assertRaises(ValueError, self.field.get_num_elems)

    def test_get_name(self):
        self.assertRaises(ValueError, self.field.get_name)

    def test_get_type(self):
        self.assertRaises(ValueError, self.field.get_type)

    def test_get_elem(self):
        self.assertRaises(ValueError, self.field.get_elem)

    def test_get_elems(self):
        self.assertRaises(ValueError, self.field.get_elems)

    def test_repr(self):
        self.assertRaises(ValueError, repr, self.field)

    def test_str(self):
        self.assertRaises(ValueError, str, self.field)

    def test_eq(self):
        self.assertRaises(ValueError, operator.eq, self.field, self.field2)

    def test_ne(self):
        self.assertRaises(ValueError, operator.ne, self.field, self.field2)

    def test_len(self):
        self.assertRaises(ValueError, len, self.field)


class TestDSD(unittest.TestCase):
    PRODUCT_FILE = os.path.join(TESTDIR, TEST_PRODUCT)
    OPEN_MODE = 'rb'
    DSD_INDEX = 0
    DS_NAME = 'MDS1 SQ ADS'
    DS_OFFSET = 7346
    DS_TYPE = 'A'
    DS_SIZE = 170
    DSR_SIZE = 170
    NUM_DSR = 1

    def setUp(self):
        self.product = epr.Product(self.PRODUCT_FILE, self.OPEN_MODE)
        self.dsd = self.product.get_dsd_at(self.DSD_INDEX)

    def tearDown(self):
        self.product.close()

    def test_index(self):
        self.assertEqual(self.dsd.index, self.DSD_INDEX)
        self.assertTrue(isinstance(self.dsd.index, int))

    def test_ds_name(self):
        self.assertEqual(self.dsd.ds_name, self.DS_NAME)
        self.assertTrue(isinstance(self.dsd.ds_name, str))

    def test_ds_type(self):
        self.assertEqual(self.dsd.ds_type, self.DS_TYPE)
        self.assertTrue(isinstance(self.dsd.ds_type, str))

    def test_filename(self):
        self.assertEqual(self.dsd.filename, '')
        self.assertTrue(isinstance(self.dsd.filename, str))

    def test_ds_offset(self):
        self.assertEqual(self.dsd.ds_offset, self.DS_OFFSET)
        self.assertTrue(isinstance(self.dsd.ds_offset, numbers.Integral))

    def test_ds_size(self):
        self.assertEqual(self.dsd.ds_size, self.DS_SIZE)
        self.assertTrue(isinstance(self.dsd.ds_size, numbers.Integral))

    def test_num_dsr(self):
        self.assertEqual(self.dsd.num_dsr, self.NUM_DSR)
        self.assertTrue(isinstance(self.dsd.num_dsr, numbers.Integral))

    def test_dsr_size(self):
        self.assertEqual(self.dsd.dsr_size, self.DSR_SIZE)
        self.assertTrue(isinstance(self.dsd.dsr_size, numbers.Integral))

    def test_eq_dsd1_dsd1(self):
        self.assertEqual(self.dsd, self.dsd)

    def test_eq_dsd1_dsd2(self):
        dsd1 = self.product.get_dsd_at(1)
        dsd2 = self.product.get_dsd_at(2)
        self.assertFalse(dsd1 == dsd2)

    def test_eq_dsd_product(self):
        self.assertFalse(self.dsd == self.product)

    def test_ne_dsd1_dsd1(self):
        self.assertFalse(self.dsd != self.dsd)

    def test_ne_dsd1_dsd2(self):
        dsd1 = self.product.get_dsd_at(1)
        dsd2 = self.product.get_dsd_at(2)
        self.assertNotEqual(dsd1, dsd2)

    def test_ne_dsd_record(self):
        self.assertTrue(self.dsd != self.product)


class TestDSDRW(TestDSD):
    OPEN_MODE = 'rb+'


class TestDsdHighLevelAPI(unittest.TestCase):
    PRODUCT_FILE = os.path.join(TESTDIR, TEST_PRODUCT)

    def setUp(self):
        self.product = epr.Product(self.PRODUCT_FILE)
        self.dsd = self.product.get_dsd_at(0)

    def tearDown(self):
        self.product.close()

    def test_repr(self):
        pattern = r'epr\.DSD\("(?P<name>.+)"\)'
        mobj = re.match(pattern, repr(self.dsd))
        self.assertNotEqual(mobj, None)
        self.assertEqual(mobj.group('name'), self.dsd.ds_name)

    def test_repr_type(self):
        self.assertTrue(isinstance(repr(self.dsd), str))

    def test_str_type(self):
        self.assertTrue(isinstance(str(self.dsd), str))


class TestDsdLowLevelAPI(unittest.TestCase):
    PRODUCT_FILE = os.path.join(TESTDIR, TEST_PRODUCT)

    def setUp(self):
        self.product = epr.Product(self.PRODUCT_FILE)
        self.dsd = self.product.get_dsd_at(0)

    def tearDown(self):
        self.product.close()

    def test_magic(self):
        # self.assertEqual(self.dsd._magic, epr._EPR_MAGIC_DSD_ID)
        self.assertTrue(isinstance(self.dsd._magic, int))


class TestDSDOnCloserProduct(unittest.TestCase):
    PRODUCT_FILE = os.path.join(TESTDIR, TEST_PRODUCT)
    DSD_INDEX = 0

    def setUp(self):
        self.product = epr.Product(self.PRODUCT_FILE)
        self.dsd = self.product.get_dsd_at(self.DSD_INDEX)
        self.dsd2 = self.product.get_dsd_at(self.DSD_INDEX + 1)
        self.product.close()

    def test_index(self):
        self.assertRaises(ValueError, getattr, self.dsd, 'index')

    def test_ds_name(self):
        self.assertRaises(ValueError, getattr, self.dsd, 'ds_name')

    def test_ds_type(self):
        self.assertRaises(ValueError, getattr, self.dsd, 'ds_type')

    def test_filename(self):
        self.assertRaises(ValueError, getattr, self.dsd, 'filename')

    def test_ds_offset(self):
        self.assertRaises(ValueError, getattr, self.dsd, 'ds_offset')

    def test_ds_size(self):
        self.assertRaises(ValueError, getattr, self.dsd, 'ds_size')

    def test_num_dsr(self):
        self.assertRaises(ValueError, getattr, self.dsd, 'num_dsr')

    def test_dsr_size(self):
        self.assertRaises(ValueError, getattr, self.dsd, 'dsr_size')

    def test_eq(self):
        self.assertRaises(ValueError, operator.eq, self.dsd, self.dsd2)

    def test_ne(self):
        self.assertRaises(ValueError, operator.ne, self.dsd, self.dsd2)

    def test_repr(self):
        self.assertRaises(ValueError, repr, self.dsd)

    def test_str(self):
        self.assertRaises(ValueError, str, self.dsd)


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

    TYPE_MAP = {
        epr.E_TID_UNKNOWN: None,
        epr.E_TID_UCHAR:   np.uint8,
        epr.E_TID_CHAR:    np.int8,
        epr.E_TID_USHORT:  np.uint16,
        epr.E_TID_SHORT:   np.int16,
        epr.E_TID_UINT:    np.uint32,
        epr.E_TID_INT:     np.int32,
        epr.E_TID_FLOAT:   np.float32,
        epr.E_TID_DOUBLE:  np.float64,
        epr.E_TID_STRING:  np.bytes_,
        epr.E_TID_SPARE:   None,
        epr.E_TID_TIME:    epr.MJD,
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

    def test_epr_to_numpy_dtype(self):
        for epr_type in self.TYPE_MAP:
            with self.subTest(epr_type=epr_type):
                self.assertEqual(
                    epr.get_numpy_dtype(epr_type), self.TYPE_MAP[epr_type])


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
    MSG_PATTERN = '"%s" class cannot be instantiated from Python'

    def test_direct_dsd_instantiation(self):
        pattern = self.MSG_PATTERN % epr.DSD.__name__
        self.assertRaisesRegex(TypeError, pattern, epr.DSD)

    def test_direct_field_instantiation(self):
        pattern = self.MSG_PATTERN % epr.Field.__name__
        self.assertRaisesRegex(TypeError, pattern, epr.Field)

    def test_direct_record_instantiation(self):
        pattern = self.MSG_PATTERN % epr.Record.__name__
        self.assertRaisesRegex(TypeError, pattern, epr.Record)

    def test_direct_raster_instantiation(self):
        pattern = self.MSG_PATTERN % epr.Raster.__name__
        self.assertRaisesRegex(TypeError, pattern, epr.Raster)

    def test_direct_band_instantiation(self):
        pattern = self.MSG_PATTERN % epr.Band.__name__
        self.assertRaisesRegex(TypeError, pattern, epr.Band)

    def test_direct_dataset_instantiation(self):
        pattern = self.MSG_PATTERN % epr.Dataset.__name__
        self.assertRaisesRegex(TypeError, pattern, epr.Dataset)

    def test_direct_Product_instantiation(self):
        self.assertRaises(epr.EPRError, epr.Product, 'filename')


class TestLibVersion(unittest.TestCase):
    def test_c_api_version(self):
        self.assertTrue(isinstance(epr.EPR_C_API_VERSION, str))


# only PyPy 3 seems to be affected
@unittest.skipIf(platform.python_implementation() == 'PyPy',
                 'skip memory leak check on PyPy')
@unittest.skipIf(resource is None, '"resource" module not available')
class TestMemoryLeaks(unittest.TestCase):
    # See gh-10 (https://github.com/avalentino/pyepr/issues/10)

    PRODUCT_FILE = os.path.join(TESTDIR, TEST_PRODUCT)
    BAND_NAME = 'incident_angle'

    def test_memory_leacks_on_read_as_array(self):
        N = 10

        for n in range(N):
            with epr.open(self.PRODUCT_FILE) as p:
                p.get_band(self.BAND_NAME).read_as_array()
            if n <= 1:
                m1 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            m2 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        self.assertLessEqual(m2 - m1, 8)


if __name__ == '__main__':
    print('PyEPR: %s' % epr.__version__)
    print('EPR API: %s' % epr.EPR_C_API_VERSION)
    print('Numpy: %s' % np.__version__)
    print('Python: %s' % sys.version)
    unittest.main()
