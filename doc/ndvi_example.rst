NDVI computation
----------------

.. index:: NDVI, MERIS

This tutorial shows how to use PyEPR_ to open a MERIS_ L1B product, compute
the *Normalized Difference Vegetation Index* (NDVI) and store it into a flat
binary file.

The example code (:download:`examples/write_ndvi.py`) is a direct
translation of the C sample program `write_ndvi.c`_ bundled with the
EPR API distribution.

The program is invoked as follows:

.. code-block:: sh

    $ python write_ndvi.py <envisat-oroduct> <output-file>

.. _PyEPR: https://github.com/avalentino/pyepr
.. _MERIS: https://earth.esa.int/handbooks/meris/CNTR.html
.. _`write_ndvi.c`: https://github.com/bcdev/epr-api/blob/master/src/examples/write_ndvi.c

The code have been kept very simple and it consists in a single function
(:func:`main`) that also performs a minimal command line arguments handling.

.. raw:: latex

    \fvset{fontsize=\footnotesize}

.. literalinclude:: examples/write_ndvi.py

The ENVISAT_ :class:`epr.Product` is opened using the :func:`epr.open`
function.

.. raw:: latex

    \fvset{fontsize=\footnotesize}

.. literalinclude:: examples/write_ndvi.py
   :lines: 46-47

.. index:: context, open
   pair: with; statement

As usual in modern python programs the *with* statement has been used to
ensure that the product is automatically closed as soon as the program exits
the block.
Of course it is possible to use a simple assignment form::

    product = open(argv[1])

but in this case the user should take care of manually call::

    product.close()

when appropriate.

The name of the product is in the first argument passed to the program.
In order to keep the code simple no check is performed to ensure that the
product is a valid L1B product.

The NDVI is calculated using bands 6 and 8 (the names of these bands are
"radiance_6" and "radiance_10").
:class:`epr.Band` objects are retrieved using the :meth:`epr.Product.get_band`
method:

.. raw:: latex

    \fvset{fontsize=\footnotesize}

.. literalinclude:: examples/write_ndvi.py
   :lines: 49-54

*band1* and *band2* are used to read the calibrated radiances into the
:class:`epr.Raster` objects that allow to access data matrices with the
radiance values.

.. index:: raster, memory

Before reading data into the :class:`epr.Raster` objects they have to be
instantiated specifying their size and data type in order to allow the library
to allocate the correct amount of memory.

For sake of simplicity :class:`epr.Raster` object are created with the same
size of the whole product (with no sub-sampling) using the
:meth:`epr.Band.create_compatible_raster` method of the :class:`epr.Band`
class:

.. raw:: latex

    \fvset{fontsize=\footnotesize}

.. literalinclude:: examples/write_ndvi.py
   :lines: 56-64

Then data are actually loaded into memory using the
:meth:`epr.Band.read_raster` method.
Since :class:`epr.Raster` objects have been defined to match the whole
product, offset parameters are set to zero (data are read starting from
specified offset):

.. raw:: latex

    \fvset{fontsize=\footnotesize}

.. literalinclude:: examples/write_ndvi.py
   :lines: 66-74

.. note::

    in this simplified example it is assumed that there is enough system
    memory to hold the two :class:`epr.Raster` objects.

After opening (in binary mode) the stream for the output

.. raw:: latex

    \fvset{fontsize=\footnotesize}

.. literalinclude:: examples/write_ndvi.py
   :lines: 76-78

the program simply loops over all pixel and calculate the NDVI with the
following formula:

.. math:: NDVI = \frac{radiance_{10} - radiance_8}{radiance_{10} + radiance_8}

.. raw:: latex

    \fvset{fontsize=\footnotesize}

.. literalinclude:: examples/write_ndvi.py
   :lines: 80-93

This part of the code tries to mimic closely the original C code
(`write_ndvi.c`_)

.. code-block:: c

    out_stream = fopen(argv[2], "wb");
    for (j = 0; j < height; ++j) {
        for (i = 0; i < width; ++i) {
            rad1 = epr_get_pixel_as_float(raster1, i, j);
            rad2 = epr_get_pixel_as_float(raster2, i, j);
            if ((rad1 + rad2) != 0.0) {
                ndvi = (rad2 - rad1) / (rad2 + rad1);
            } else {
                ndvi = -1.0;
            }
            status = fwrite( & ndvi, sizeof(float), 1, out_stream);
        }
    }
    epr_log_message(e_log_info, "ndvi was written success");

and uses the :meth:`epr.Raster.get_pixel` method to access pixel values and
perform computation.

The Python_ :func:`struct.pack` function together with :meth:`file.write` is
used to write the NDVI of the pixel n the file in binary format.

.. raw:: latex

    \fvset{fontsize=\footnotesize}

.. literalinclude:: examples/write_ndvi.py
   :lines: 92

.. note::

    the entire solution is quite not "pythonic". As an alternative
    implementation it could be used the :class:`numpy.ndarray` interface of
    :class:`epr.Raster` objects available via the :data:`epr.Raster.data`
    property. The NDVI index is computed on all pixels altogether using
    vectorized expressions::

        # Initialize the entire matrix to -1
        ndvi = numpy.zeros((height, width), 'float32') - 1

        aux = raster2.data + raster1.data

        # indexes of pixel with non null denominator
        idx = numpy.where(aux != 0)

        # actual NDVI computation
        ndvi[idx] = (raster2.data[idx] - raster1.data[idx]) / aux[idx]

    Finally data can be saved to file simply using the
    :meth:`numpy.ndarray.tofile` method::

        ndvi.tofile(out_stream)


.. _ENVISAT: https://envisat.esa.int
.. _Python: https://www.python.org


.. raw:: latex

   \clearpage
