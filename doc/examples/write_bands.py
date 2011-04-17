#!/usr/bin/env python

# This program is a direct translation of the sample program "write_bands.c"
# bundled with the EPR-API distribution.
#
# Source code of the C program is available at:
# https://github.com/bcdev/epr-api/blob/master/src/examples/write_bands.c


import os
import sys
import epr

def write_raw_image(output_dir, product, band_name):
    '''Generate the ENVI binary pattern image file for an actual DS.

    The first parameter is the output directory path.

    The function returns 1, if the file is generated, 0 otherwise.

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

    print 'Reading band "%s"...' % band_name
    raster = band.read_raster(0, 0, raster)

    out_stream = open(image_file_path, 'wb')

    for line in raster.data:
        out_stream.write(line.tostring())
    # or better: raster.data.tofile(out_stream)

    out_stream.close()

    print 'Raw image data successfully written to "%s".' % image_file_path
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

    Call: write_bands.py <ENVISAT-Product file path>
                         <Output directory for the raster file>
                         <Dataset name 1>
                         [<Dataset name 2> ... <Dataset name N>]

    Example::

        $ write_bands.py
            "d:/ENVISAT/data/MERIS/L1b/MER_RR__1PNPDK20020415_103725_000002702005_00094_00649_1059.N1"
            "./"
            "latitude"
            ["longitude" "dem_alt" "dem_rough" "lat_corr" "lon_corr"
             "sun_zenith" "sun_azimuth" "view_zenith" "view_azimuth"
             "zonal_wind" "merid_wind" "atm_press" "ozone" "rel_hum"
             "radiance_1" "radiance_2" "radiance_3" "radiance_4" "radiance_5"
             "radiance_6" "radiance_7" "radiance_8" "radiance_9" "radiance_10"
             "radiance_11" "radiance_12" "radiance_13" "radiance_14"
             "radiance_15"]

    OR::

        $ write_bands.py
            /data/AATSR/L1b/ATS_TOA_1PTRAL19950510_071649_00000000X000_00000_00000_0000.N1"
            .
            latitude
            [longitude lat_corr_nadir lon_corr_nadir lat_corr_fward
             lon_corr_fward altitude sun_elev_nadir view_elev_nadir
             sun_azimuth_nadir view_azimuth_nadir sun_elev_fward
             view_elev_fward sun_azimuth_fward view_azimuth_fward
             btemp_nadir_1200 btemp_nadir_1100 btemp_nadir_0370
             reflec_nadir_1600 reflec_nadir_0870 reflec_nadir_0670
             reflec_nadir_0550 btemp_fward_1200 btemp_fward_1100
             btemp_fward_0370 reflec_fward_1600 reflec_fward_0870
             reflec_fward_0670 reflec_fward_0550 confid_flags_nadir
             confid_flags_fward cloud_flags_nadir cloud_flags_fward]

    '''

    if not argv:
        argv = sys.argv

    if len(argv) <= 3:
        print 'Usage: write_bands.py <envisat-product> <output-dir> <dataset-name-1>'
        print '                      [<dataset-name-2> ... <dataset-name-N>]'
        print '  where envisat-product is the input filename'
        print '  and output-dir is the output directory'
        print '  and dataset-name-1 is the name of the first band to be extracted (mandatory)'
        print '  and dataset-name-2 ... dataset-name-N are the names of further bands to be extracted (optional)'
        print 'Example:'
        print '  write_bands MER_RR__2P_TEST.N1 . latitude'
        print
        sys.exit(1)

    product_file_path = argv[1]
    output_dir_path = argv[2]

    # Open the product; an argument is a path to product data file
    product = epr.open(product_file_path)

    for band_name in argv[3:]:
        write_raw_image(output_dir_path, product, band_name)

if __name__ == '__main__':
    main()
