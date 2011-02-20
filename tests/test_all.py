#!/usr/bin/env python

import os
import sys
import unittest


#~ PRODUCT_FILE = 'SAR_IMS_1PXESA20040920_034157_00000016A098_00290_49242_0715.E2'
PRODUCT_FILE = 'ASA_IMP_1PNUPA20060202_062233_000000152044_00435_20529_3110.N1'
if not os.path.exists(PRODUCT_FILE):
    raise RuntimeError('no test product available')

sys.path.insert(0, os.pardir)

import epr

class TestOpenProduct(unittest.TestCase):
    def test_open(self):
        product = epr.Product(PRODUCT_FILE)
        self.assertTrue(product)

class TestProduct(unittest.TestCase):
    def setUp(self):
        self.product = epr.Product(PRODUCT_FILE)

    def test_get_scene_width(self):
        self.assertEqual(self.product.get_scene_width(), 8439)

    def test_get_scene_height(self):
        self.assertEqual(self.product.get_scene_height(), 8192)

    def test_get_num_datasets(self):
        self.assertEqual(self.product.get_num_datasets(), 7)

    def test_get_num_dsds(self):
        self.assertEqual(self.product.get_num_dsds(), 18)

    def test_get_num_bands(self):
        self.assertEqual(self.product.get_num_bands(), 5)

    def test_get_dataset_at(self):
        dataset = self.product.get_dataset_at(0)
        self.assertTrue(dataset)

    def test_get_dataset(self):
        dataset = self.product.get_dataset('MDS1')
        self.assertTrue(dataset)


class TestDataset(unittest.TestCase):
    DATASET_NAME = 'MDS1'

    def setUp(self):
        self.product = epr.Product(PRODUCT_FILE)
        self.dataset = self.product.get_dataset(self.DATASET_NAME)

    def test_get_dataset_name(self):
        self.assertEqual(self.dataset.get_dataset_name(), self.DATASET_NAME)

    def test_get_dsd_name(self):
        self.assertEqual(self.dataset.get_dsd_name(), self.DATASET_NAME)

    def test_get_num_records(self):
        self.assertEqual(self.dataset.get_num_records(), 8192)


class TestUninitializedDataset(unittest.TestCase):
    DATASET_NAME = ''

    def setUp(self):
        self.product = epr.Product(PRODUCT_FILE)
        self.dataset = epr.Dataset()

    def test_get_dataset_name(self):
        self.assertEqual(self.dataset.get_dataset_name(), '')

    def test_get_dsd_name(self):
        self.assertEqual(self.dataset.get_dsd_name(), '')

    def test_get_num_records(self):
        self.assertEqual(self.dataset.get_num_records(), 0)


if __name__ == '__main__':
    unittest.main()
