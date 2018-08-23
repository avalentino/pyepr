Exporting band data
-------------------

.. index:: ENVISAT, band, raster

This tutorial shows how to convert ENVISAT_ raster information from dataset
and generate flat binary rasters using PyEPR_.

The program generates as many raster as the dataset specified in input.

The example code (:download:`examples/write_bands.py`) is a direct
translation of the C sample program `write_bands.c`_ bundled with the
EPR API distribution.

The program is invoked as follows:

.. code-block:: sh

    $ python write_bands.py <envisat-product> \
    <output directory for the raster file> <dataset name 1> \
    [<dataset name 2> ... <dataset name N>]

.. _ENVISAT: https://envisat.esa.int
.. _PyEPR: https://github.com/avalentino/pyepr
.. _`write_bands.c`: https://github.com/bcdev/epr-api/blob/master/src/examples/write_bands.c


Import section
~~~~~~~~~~~~~~

To use the Python_ EPR API one have to import :mod:`epr` module.

At first import time the underlaying  C library is opportunely initialized.

.. raw:: latex

    \fvset{fontsize=\footnotesize}

.. literalinclude:: examples/write_bands.py
   :language: python
   :lines: 1-15


The main program
~~~~~~~~~~~~~~~~

The main program in quite simple (this is just an example).

.. raw:: latex

    \fvset{fontsize=\footnotesize}

.. literalinclude:: examples/write_bands.py
   :language: python
   :lines: 55-

It performs some basic command line arguments handling and then open the
input product.

.. raw:: latex

    \fvset{fontsize=\footnotesize}

.. literalinclude:: examples/write_bands.py
   :language: python
   :lines: 97-99

Finally the core function (:func:`write_raw_image`) is called on each band
specified on the command:

.. raw:: latex

    \fvset{fontsize=\footnotesize}

.. literalinclude:: examples/write_bands.py
   :language: python
   :lines: 100-101


The :func:`write_raw_image` core function
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The core function is :func:`write_raw_image`.

.. raw:: latex

    \fvset{fontsize=\footnotesize}

.. literalinclude:: examples/write_bands.py
   :language: python
   :pyobject: write_raw_image

It generates a flat binary file with data of a single band whose name is
specified as input parameter.

First the output file name is computed using the :mod:`os` module.

.. raw:: latex

    \fvset{fontsize=\footnotesize}

.. literalinclude:: examples/write_bands.py
   :language: python
   :lines: 23-25

Then the desired band is retrieved using the :meth:`epr.Product.get_band`
method and some of its parameters are loaded in to local variables:

.. raw:: latex

    \fvset{fontsize=\footnotesize}

.. literalinclude:: examples/write_bands.py
   :language: python
   :lines: 26-27

Band data are accessed by means of a :class:`epr.Raster` object.

.. seealso:: :func:`epr.Band.read_as_array`

The :meth:`epr.Band.create_compatible_raster` is a facility method that
allows to instantiate a :class:`epr.Raster` object with a data type compatible
with the band data:

.. raw:: latex

    \fvset{fontsize=\footnotesize}

.. literalinclude:: examples/write_bands.py
   :language: python
   :lines: 32-34

Then data are read using the :meth:`epr.Band.read_raster` method:

.. raw:: latex

    \fvset{fontsize=\footnotesize}

.. literalinclude:: examples/write_bands.py
   :language: python
   :lines: 36-37

Then the output file object is created (in binary mode of course)

.. raw:: latex

    \fvset{fontsize=\footnotesize}

.. literalinclude:: examples/write_bands.py
   :language: python
   :lines: 39

and data are copied to the output file one line at time

.. raw:: latex

    \fvset{fontsize=\footnotesize}

.. literalinclude:: examples/write_bands.py
   :language: python
   :lines: 41-42

Please note that it has been used :data:`epr.Raster.data` attribute of the
:class:`epr.Raster` objects that exposes :class:`epr.Raster` data with the
powerful :class:`numpy.ndarray` interface.


.. note::

    copying one line at time is not the best way to perform the task
    in Python_. It has been done just to mimic the original C code:

    .. code-block:: c

        out_stream = fopen(image_file_path, "wb");
        if (out_stream == NULL) {
            printf("Error: can't open '%s'\n", image_file_path);
            return 3;
        }

        for (y = 0; y < (uint)raster->raster_height; ++y) {
            numwritten = fwrite(epr_get_raster_line_addr(raster, y),
                                raster->elem_size,
                                raster->raster_width,
                                out_stream);

            if (numwritten != raster->raster_width) {
                printf("Error: can't write to %s\n", image_file_path);
                return 4;
            }
        }
        fclose(out_stream);

    A by far more pythonic_ solution would be::

        raster.data.tofile(out_stream)


.. _Python: https://www.python.org
.. _pythonic: http://www.cafepy.com/article/be_pythonic

.. raw:: latex

   \clearpage
