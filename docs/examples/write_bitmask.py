#!/usr/bin/env python3

# This program is a direct translation of the sample program
# "write_bitmask.c" bundled with the EPR-API distribution.
#
# Source code of the C program is available at:
# https://github.com/bcdev/epr-api/blob/master/src/examples/write_bitmask.c

"""Generates bit mask from ENVISAT flags information as "raw" image
for (e.g.) Photoshop.

Call::

    $ python3 write_bitmask.py <envisat-product> <bitmask-expression>
    <output-file>

Example to call the main function::

    $ python3 write_bitmask.py MER_RR__2P_TEST.N1 \
      'l2_flags.LAND and !l2_flags.BRIGHT' my_flags.raw

"""

import sys

import epr


def main(*argv):
    if not argv:
        argv = sys.argv

    if len(argv) != 4:
        print(
            """\
Usage:

  python3 write_bitmask <envisat-product> <bitmask-expression>
                        <output-file>

where envisat-product is the input filename and bitmask-expression
is a string containing the bitmask logic and output-file is the
output filename.

Example:

  MER_RR__2P_TEST.N1 'l2_flags.LAND and not l2_flags.BRIGHT'
  my_flags.raw

  """
        )
        sys.exit(1)

    product_file_path = argv[1]
    bm_expr = argv[2]
    image_file_path = argv[3]

    # Open the product; an argument is a path to product data file
    with epr.open(product_file_path) as product:
        offset_x = 0
        offset_y = 0
        source_width = product.get_scene_width()
        source_height = product.get_scene_height()
        source_step_x = 1
        source_step_y = 1

        bm_raster = epr.create_bitmask_raster(
            source_width, source_height, source_step_x, source_step_y
        )

        product.read_bitmask_raster(bm_expr, offset_x, offset_y, bm_raster)

        with open(image_file_path, "wb") as out_stream:
            bm_raster.data.tofile(out_stream)

    print(f"Raw image data successfully written to {image_file_path!r}.")
    print(
        f"Data type is 'byte', size is {source_width} x {source_height} "
        f"pixels."
    )


if __name__ == "__main__":
    main()
