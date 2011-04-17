#!/usr/bin/env python

# This program is a direct translation of the sample program "write_ndvi.c"
# bundled with the EPR-API distribution.
#
# Source code of the C program is available at:
# https://github.com/bcdev/epr-api/blob/master/src/examples/write_ndvi.c


'''Example for using the epr-api

Demonstrates how to open a MERIS L1b product and calculate the NDVI

This example does not demonstrate how to write good and safe code.
It is reduced to the essentials for working with the epr-api.

Calling sequence: write_ndvi <ENVISAT-Product file> <output ndvi raw image file>

for example: write_ndvi MER_RR__1P_test.N1 my_ndvi.raw

'''

import sys
import struct
import logging

import epr


def main(*argv):
    if not argv:
        argv = sys.argv

    if len(argv) != 3:
        print 'Usage: write_ndvi <envisat-product> <output-file>'
        print '  where envisat-product is the input filename'
        print '  and output-file is the output filename.'
        print 'Example: MER_RR__1P_TEST.N1 my_ndvi.raw'
        print
        sys.exit(1)

    # Open the product; the name of the product is in the first argument of
    # the program call we do not check here if the product is a valid L1b
    # product to keep the code simple
    product = epr.open(argv[1])

    # The NDVI shall be calculated using bands 6 and 8.
    # The names of these bands are "radiance_6" and "radiance_10".
    # This can be found in the BEAM documentation or using VISAT.
    band1_name = 'radiance_6'
    band2_name = 'radiance_10'

    # Now we have to obtain band object for these bands.
    # This is the object which we will use in the next step to read the
    # calibrated radiances into the raster (i.e. the matrix with the radiance
    # values).
    band1 = product.get_band(band1_name)
    band2 = product.get_band(band2_name)

    # Before we can read the data into the raster, we have to allocate memory
    # for the raster, i.e. we have to create the raster.
    # We make it simple and define our raster of the same size as the whole
    # product, and don't apply subsampling.
    width = product.get_scene_width()
    height = product.get_scene_height()
    subsampling_x = 1
    subsampling_y = 1
    raster1 = band1.create_compatible_raster(width, height,
                                             subsampling_x, subsampling_y)
    raster2 = band2.create_compatible_raster(width, height,
                                             subsampling_x, subsampling_y)

    # Now we read the radiance into the raster.
    # Because our raster matches the whole product, we start reading at
    # offset (0,0)
    offset_x = 0
    offset_y = 0

    logging.info('read "%s" data' % band1_name)
    band1.read_raster(offset_x, offset_y, raster1)

    logging.info('read "%s" data' % band2_name)
    band2.read_raster(offset_x, offset_y, raster2)

    # So, now we hold the two arrays totally in memory.
    # I hope that enough memory is available.
    # The rest is easy. We loop over all pixel and calculate the NDVI.
    # We simply write each calculated pixel directly into the output image.
    # Not elegant, but simple.
    logging.info('write ndvi to "%s"' % argv[2])
    out_stream = open(argv[2], 'wb')

    # @NOTE: looping over data matrices is not the best soluton.
    #        It is done here just for demostrative purposes
    for j in range(height):
        for i in range(width):
            rad1 = raster1.get_pixel(i, j)
            rad2 = raster2.get_pixel(i, j)
            if (rad1 + rad2) != 0.0:
                ndvi = (rad2 - rad1) / (rad2 + rad1)
            else:
                ndvi = -1.0
            out_stream.write(struct.pack('f', ndvi))
    logging.info('ndvi was written success')

    # This was all.
    # Now we have to close everything, release memory and say goodbye.
    # If you want, you can open the written file an image processing program
    # and look at the result.
    out_stream.close()


if __name__ == '__main__':
    main()
