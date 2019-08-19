GDAL_ export example
--------------------

.. index:: GDAL, export, VRT, ENVISAT, offset

This tutorial explains how to use PyEPR_ to generate a file in GDAL Virtual
Format (VRT) that can be used to access data with the powerful and popular
GDAL_ library.
GDAL_ already has support for ENVISAT_ products but this example is
interesting for two reasons:

* it exploits some low level feature (like e.g. offset management) that are
  rarely used but that can be very useful in some cases
* the generated VRT file uses raw raster access and it can be opened in
  update mode to modify the ENVISAT_ product data.
  This feature is not supported by the native ENVISAT_ driver of the GDAL_
  library


export_gdalvrt module
~~~~~~~~~~~~~~~~~~~~~

The complete code of the example is available in the
:download:`examples/export_gdalvrt.py` file.
It is organized so that it can also be imported as a module in any program.

The :mod:`export_gdalvrt` module provides two functions:

.. module:: export_gdalvrt


.. function:: epr2gdal_band(band, vrt)

   Takes in input an :class:`epr.Band` object and a VRT dataset
   and add a GDAL_ band to the VRT dataset


.. function:: epr2gdal(product, vrt, overwrite_existing=False)

   Takes in input a PyEPR_ :class:`Product` (or a filename) and the
   file name of the output VRT file and generates the VRT file itself
   containing a band for each :class:`epr.Band` present in the original
   :class:`epr.Product` and also associated metadata.


The :func:`epr2gdal` function first creates the VRT dataset

.. raw:: latex

    \fvset{fontsize=\footnotesize}

.. literalinclude:: examples/export_gdalvrt.py
   :language: python
   :lines: 101-117

and then loops on all :class:`epr.Band`\ s of the PyEPR_ :class:`epr.Product`
calling the :func:`epr2gdal_band` function on each of them:

.. raw:: latex

    \fvset{fontsize=\footnotesize}

.. literalinclude:: examples/export_gdalvrt.py
   :language: python
   :lines: 136-137

The :mod:`export_gdalvrt` module also provides a :data:`epr_to_gdal_type`
mapping between EPR and GDAL data type identifiers.


.. index:: VRTRawRasterBand

Generating *VRTRawRasterBand*\ s
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The core of the example is the part of the code in the :func:`epr2gdal_band`
function that generates the GDAL_ *VRTRawRasterBand*.
It is a description of a raster file that the GDAL_ library uses for low level
data access.
Of course the entire machinery works because data in :class:`epr.Band`\s and
:class:`epr.Dataset`\ s of ENVISAT_ products are stored as contiguous
rasters.

.. raw:: latex

    \fvset{fontsize=\footnotesize}

.. literalinclude:: examples/export_gdalvrt.py
   :language: python
   :lines: 54-78

.. index:: offset

The fundamental part is the computation of the:

**ImageOffset**:

    the offset in bytes to the beginning of the first pixel of data with
    respect to the beginning of the file.

    In the example it is computed using

    * the :data:`epr.DSD.ds_offset` attribute, that represents the offset
      in bytes of the :class:`epr.Dataset` from the beginning of the file,
      and
    * the :meth:`epr.Field.get_offset` method that returns the offset in
      bytes of the :class:`epr.Field` containing :class:`epr.Band` data from
      the beginning of the :class:`epr.Record`

     ::

        offset = dataset.get_dsd().ds_offset + field.get_offset()

**LineOffset**:

    the offset in bytes from the beginning of one *scanline* of data and the
    next scanline of data.
    In the example it is set to the :class:`epr.Record` size in bytes using
    the :attr:`epr.Record.tot_size` attribute::

        line_offset = record.tot_size

**PixelOffset**:

    the offset in bytes from the beginning of one pixel and the next on
    the same line. Usually it corresponds to the size in bytes of the
    elementary data type.
    It is set using the :meth:`epr.Field.get_type` method and the
    :func:`epr.get_data_type_size` function::

        pixel_offset = epr.get_data_type_size(field.get_type())

The band size in lines and columns of the GDAL_ bands is fixed at GDAL_
dataset level when it is created:

.. raw:: latex

    \fvset{fontsize=\footnotesize}

.. literalinclude:: examples/export_gdalvrt.py
   :language: python
   :lines: 50-52

.. index:: dataset, band

Please note that in case of :class:`epr.Dataset`\ s storing complex values,
like in `MDS1` :class:`epr.Dataset` of ASAR IMS :class:`epr.Product`\ s,
pixels of real and imaginary parts are interleaved, so to represent
:class:`epr.Band`\ s of the two components the pixel offset have to be
doubled and an additional offset (one pixel) must be added to the
*ImageOffset* of the :class:`epr.Band` representing the imaginary part:

.. raw:: latex

    \fvset{fontsize=\footnotesize}

.. literalinclude:: examples/export_gdalvrt.py
   :language: python
   :lines: 59-63

.. note::

   the PyEPR_ API does not supports complex :class:`Band`\ s.
   :class:`epr.Dataset`\s containing complex data, like the `MDS1`
   :class:`epr.Dataset` of ASAR IMS :class:`epr.Product`\ s, are associated
   to two distinct :class:`epr.Band`\s containing the real (I) and the
   imaginary (Q) component respectively.

   GDAL_, instead, supports complex data types, so it is possible to map a
   complex ENVISAT_ :class:`epr.Dataset` onto a single GDAL_ bands with
   complex data type.

   This case is not handled in the example.


.. index:: metadata

Metadata
~~~~~~~~

The :func:`epr2gdal_band` function also stores a small set of metadata for
each :class:`epr.Band`:

.. raw:: latex

    \fvset{fontsize=\footnotesize}

.. literalinclude:: examples/export_gdalvrt.py
   :language: python
   :lines: 80-95

Metadata are also stored at GDAL_ dataset level by the :func:`epr2gdal`
function:

.. raw:: latex

    \fvset{fontsize=\footnotesize}

.. literalinclude:: examples/export_gdalvrt.py
   :language: python
   :lines: 119-126

.. index:: MPH, SPH

The  :func:`epr2gdal` function also stores the contents of the *MPH* and the
*SPH* records as GDAL_ dataset matadata in custom domains:

.. raw:: latex

    \fvset{fontsize=\footnotesize}

.. literalinclude:: examples/export_gdalvrt.py
   :language: python
   :lines: 128-134


Complete listing
~~~~~~~~~~~~~~~~

.. raw:: latex

    \fvset{fontsize=\footnotesize}

.. literalinclude:: examples/export_gdalvrt.py
   :language: python


.. _GDAL: https://gdal.org
.. _PyEPR: https://github.com/avalentino/pyepr
.. _ENVISAT: https://envisat.esa.int


.. raw:: latex

   \clearpage
