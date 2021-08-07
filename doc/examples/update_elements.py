#!/usr/bin/env python3

import numpy as np
from matplotlib import pyplot as plt
import epr


FILENAME = 'MER_LRC_2PTGMV20000620_104318_00000104X000_00000_00000_0001.N1'

# load original data
with epr.open(FILENAME) as product:
    band = product.get_band('water_vapour')
    wv_orig_histogram, orig_bins = np.histogram(band.read_as_array().flat, 50)

# plot water vapour histogram
plt.figure()
plt.bar(orig_bins[:-1], wv_orig_histogram, 0.02, label='original')
plt.grid(True)
plt.title('Water Vapour Histogram')
plt.savefig('water_vapour_histogram_01.png')

# modily scaling facotrs
with epr.open(FILENAME, 'rb+') as product:
    dataset = product.get_dataset('Scaling_Factor_GADS')
    record = dataset.read_record(0)

    field = record.get_field('sf_wvapour')
    scaling = field.get_elem()
    scaling *= 1.1
    field.set_elem(scaling)

# re-open the product and load modified data
with epr.open(FILENAME) as product:
    band = product.get_band('water_vapour')
    unit = band.unit
    new_data = band.read_as_array()
    wv_new_histogram, new_bins = np.histogram(new_data.flat, 50)

# plot histogram of modified data
plt.figure()
plt.bar(orig_bins[:-1], wv_orig_histogram, 0.02, label='original')
plt.grid(True)
plt.title('Water Vapour Histogram')
plt.hold(True)
plt.bar(new_bins[:-1], wv_new_histogram, 0.02, color='red', label='new')
plt.legend()
plt.savefig('water_vapour_histogram_02.png')

# plot the water vapour map
plt.figure(figsize=(8, 4))
plt.imshow(new_data)
plt.grid(True)
plt.title('Water Vapour')
cb = plt.colorbar()
cb.set_label('[{}]'.format(unit))
plt.savefig('modified_water_vapour.png')

# modify the "Vapour_Content" dataset
with epr.open(FILENAME, 'rb+') as product:
    dataset = product.get_dataset('Vapour_Content')
    for line in range(70, 100):
        record = dataset.read_record(line)
        field = record.get_field_at(2)
        elems = field.get_elems()
        elems[50:100] = 0
        field.set_elems(elems)

# re-open the product and load modified data
with epr.open(FILENAME) as product:
    band = product.get_band('water_vapour')
    unit = band.unit
    data = band.read_as_array()

# plot the water vapour map
plt.figure(figsize=(8, 4))
plt.imshow(data)
plt.grid(True)
plt.title('Water Vapour with box')
cb = plt.colorbar()
cb.set_label('[{}]'.format(unit))
plt.savefig('modified_water_vapour_with_box.png')
plt.show()
