#!/usr/bin/env python3

# This program is a direct translation of the sample program
# "write_ndvi.c" bundled with the EPR-API distribution.
#
# Source code of the C program is available at:
# https://github.com/bcdev/epr-api/blob/master/src/examples/write_ndvi.c


'''Example for using the epr-api

Demonstrates how to open a MERIS L1b product and calculate the NDVI.

This example does not demonstrate how to write good and safe code.
It is reduced to the essentials for working with the epr-api.

Calling sequence::

    $ python write_ndvi.py <envisat-product> <output-file>

for example::

    $ python write_ndvi.py MER_RR__1P_test.N1 my_ndvi.raw

'''

import sys
import struct
import logging

import epr


def main(*argv):
    if not argv:
        argv = sys.argv

    if len(argv) != 3:
        print('Usage: write_ndvi <envisat-product> <output-file>')
        print('  where envisat-product is the input filename')
        print('  and output-file is the output filename.')
        print('Example: MER_RR__1P_TEST.N1 my_ndvi.raw')
        print
        sys.exit(1)

    # Open the product
    with epr.open(argv[1]) as product:

        # The NDVI shall be calculated using bands 6 and 8.
        band1_name = 'radiance_6'
        band2_name = 'radiance_10'

        band1 = product.get_band(band1_name)
        band2 = product.get_band(band2_name)

        # Allocate memory for the rasters
        width = product.get_scene_width()
        height = product.get_scene_height()
        subsampling_x = 1
        subsampling_y = 1
        raster1 = band1.create_compatible_raster(width, height,
                                                 subsampling_x, subsampling_y)
        raster2 = band2.create_compatible_raster(width, height,
                                                 subsampling_x, subsampling_y)

        # Read the radiance into the raster.
        offset_x = 0
        offset_y = 0

        logging.info('read "%s" data' % band1_name)
        band1.read_raster(offset_x, offset_y, raster1)

        logging.info('read "%s" data' % band2_name)
        band2.read_raster(offset_x, offset_y, raster2)

        # Open the output file
        logging.info('write ndvi to "%s"' % argv[2])
        with open(argv[2], 'wb') as out_stream:

            # Loop over all pixel and calculate the NDVI.
            #
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


if __name__ == '__main__':
    main()
