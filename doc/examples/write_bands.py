#!/usr/bin/env python3

# This program is a direct translation of the sample program
# "write_bands.c" bundled with the EPR-API distribution.
#
# Source code of the C program is available at:
# https://github.com/bcdev/epr-api/blob/master/src/examples/write_bands.c

import os
import sys
import epr


def write_raw_image(output_dir, product, band_name):
    '''Generate the ENVI binary pattern image file for an actual DS.

    The first parameter is the output directory path.
    '''
    # Build ENVI file path, DS name specifically
    image_file_path = os.path.join(output_dir, band_name + '.raw')

    band = product.get_band(band_name)
    source_w = product.get_scene_width()
    source_h = product.get_scene_height()
    source_step_x = 1
    source_step_y = 1

    raster = band.create_compatible_raster(source_w, source_h,
                                           source_step_x, source_step_y)

    print('Reading band "%s"...' % band_name)
    raster = band.read_raster(0, 0, raster)

    with open(image_file_path, 'wb') as out_stream:
        for line in raster.data:
            out_stream.write(line.tostring())
        # or better: raster.data.tofile(out_stream)

    print('Raw image data successfully written to "%s".' % image_file_path)
    print('C data type is "%s", element size %u byte(s), '
          'raster size is %u x %u pixels.' % (
          epr.data_type_id_to_str(raster.data_type),
          raster.get_elem_size(),
          raster.get_width(),
          raster.get_height()))


def main(*argv):
    '''A program for converting producing ENVI raster information from
    dataset.

    It generates as many raster as there are dataset entrance parameters.

    Call::

        $ write_bands.py <envisat-product>
                         <output directory for the raster file>
                         <dataset name 1>
                         [<dataset name 2> ... <dataset name N>]

    Example::

        $ write_bands.py \
        MER_RR__1PNPDK20020415_103725_000002702005_00094_00649_1059.N1 \
        . latitude

    '''
    if not argv:
        argv = sys.argv

    if len(argv) <= 3:
        print('Usage: write_bands.py <envisat-product> <output-dir> '
              '<dataset-name-1>')
        print('                      [<dataset-name-2> ... <dataset-name-N>]')
        print('  where envisat-product is the input filename')
        print('  and output-dir is the output directory')
        print('  and dataset-name-1 is the name of the first band to be '
              'extracted (mandatory)')
        print('  and dataset-name-2 ... dataset-name-N are the names of '
              'further bands to be extracted (optional)')
        print('Example:')
        print('  write_bands MER_RR__2P_TEST.N1 . latitude')
        print()
        sys.exit(1)

    product_file_path = argv[1]
    output_dir_path = argv[2]

    # Open the product; the argument is the path to product the data file
    with epr.open(product_file_path) as product:
        for band_name in argv[3:]:
            write_raw_image(output_dir_path, product, band_name)


if __name__ == '__main__':
    main()
