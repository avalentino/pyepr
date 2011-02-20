#!/usr/bin/env python

import os
import sys
import unittest

sys.path.insert(0, os.pardir)
import epr

#PRODUCT_FILE = 'SAR_IMS_1PXESA20040920_034157_00000016A098_00290_49242_0715.E2'


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
    WIDTH = 8439
    HEIGHT = 8192
    NDSDS = 18
    NBANDS = 5

    def setUp(self):
        self.product = epr.Product(self.PRODUCT_FILE)

    def test_get_scene_width(self):
        self.assertEqual(self.product.get_scene_width(), self.WIDTH)

    def test_get_scene_height(self):
        self.assertEqual(self.product.get_scene_height(), self.HEIGHT)

    def test_get_num_datasets(self):
        self.assertEqual(self.product.get_num_datasets(),
                         len(self.DATASET_NAMES))

    def test_get_num_dsds(self):
        self.assertEqual(self.product.get_num_dsds(), self.NDSDS)

    def test_get_num_bands(self):
        self.assertEqual(self.product.get_num_bands(), self.NBANDS)

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


class TestUninitializedDataset(unittest.TestCase):
    def setUp(self):
        self.dataset = epr.Dataset()

    def test_get_dataset_name(self):
        self.assertEqual(self.dataset.get_dataset_name(), '')

    def test_get_dsd_name(self):
        self.assertEqual(self.dataset.get_dsd_name(), '')

    def test_get_num_records(self):
        self.assertEqual(self.dataset.get_num_records(), 0)


if __name__ == '__main__':
    unittest.main()
