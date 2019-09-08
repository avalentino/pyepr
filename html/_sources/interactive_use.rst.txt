Interactive use of PyEPR_
-------------------------

.. highlight:: ipython

.. index:: jupyter, ipython, interactive, ENVISAT, ASAR, ESA, pylab, matplotlib
   pair: interactive; shell
   pair: sample; dataset

In this tutorial it is showed an example of how to use PyEPR_ interactively
to open, browse and display data of an ENVISAT_ ASAR_ product.

For the interactive session it is used the Jupyter_ console started
with the `--pylab` option to enable the interactive plotting features provided
by the matplotlib_ package.

The ASAR_ product used in this example is a `free sample`_ available at the
ESA_ web site.

.. _PyEPR: https://github.com/avalentino/pyepr
.. _ENVISAT: https://envisat.esa.int
.. _ASAR: https://earth.esa.int/handbooks/asar/CNTR.html
.. _Jupyter: https://jupyter.org/
.. _matplotlib: https://matplotlib.org
.. _`free sample`: https://earth.esa.int/services/sample_products/asar/IMP/ASA_IMP_1PNUPA20060202_062233_000000152044_00435_20529_3110.N1.gz
.. _ESA: https://earth.esa.int


.. index:: module
   pair: epr; module

:mod:`epr` module and classes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After starting the jupyter console with the following command:

.. code-block:: sh

    $ jupyter console -- --pylab

one can import the :mod:`epr` module and start start taking confidence with
available classes and functions::

    Jupyter console 5.2.0

    Python 3.6.5 (default, Apr  1 2018, 05:46:30)
    Type "copyright", "credits" or "license" for more information.

    IPython 5.5.0 -- An enhanced Interactive Python.
    ?         -> Introduction and overview of IPython's features.
    %quickref -> Quick reference.
    help      -> Python's own help system.
    object?   -> Details about 'object', use 'object??' for extra details.

    In [1]: import epr

    In [2]: epr?

    Base Class:       <type 'module'>
    String Form:      <module 'epr' from 'epr.so'>
    Namespace:        Interactive
    File:             /home/antonio/projects/pyepr/epr.so
    Docstring:
        Python bindings for ENVISAT Product Reader C API

        PyEPR_ provides Python_ bindings for the ENVISAT Product Reader C API
        (`EPR API`_) for reading satellite data from ENVISAT_ ESA_ (European
        Space Agency) mission.

        PyEPR_ is fully object oriented and, as well as the `EPR API`_ for C,
        supports ENVISAT_ MERIS, AATSR Level 1B and Level 2 and also ASAR data
        products. It provides access to the data either on a geophysical
        (decoded, ready-to-use pixel samples) or on a raw data layer.
        The raw data access makes it possible to read any data field contained
        in a product file.

        .. _PyEPR: http://avalentino.github.io/pyepr
        .. _Python: https://www.python.org
        .. _`EPR API`: https://github.com/bcdev/epr-api
        .. _ENVISAT: https://envisat.esa.int
        .. _ESA: https://earth.esa.int

    In [3]: epr.__version__, epr.EPR_C_API_VERSION
    Out[3]: ('1.0.0', '2.3dev')

.. index:: __version__

Docstrings are available for almost all classes, methods and functions in
the :mod:`epr` and they can be displayed using the :func:`help` python_
command or the ``?`` Jupyter_ shortcut as showed above.

.. _python: https://www.python.org

Also Jupyter_ provides a handy tab completion mechanism to automatically
complete commands or to display available functions and classes::

    In [4]: product = epr. [TAB]
    epr.Band                     epr.E_TID_STRING
    epr.DSD                      epr.E_TID_TIME
    epr.Dataset                  epr.E_TID_UCHAR
    epr.EPRError                 epr.E_TID_UINT
    epr.EPRTime                  epr.E_TID_UNKNOWN
    epr.EPRValueError            epr.E_TID_USHORT
    epr.EPR_C_API_VERSION        epr.EprObject
    epr.E_SMID_LIN               epr.Field
    epr.E_SMID_LOG               epr.Product
    epr.E_SMID_NON               epr.Raster
    epr.E_SMOD_1OF1              epr.Record
    epr.E_SMOD_1OF2              epr.create_bitmask_raster
    epr.E_SMOD_2OF2              epr.create_raster
    epr.E_SMOD_2TOF              epr.data_type_id_to_str
    epr.E_SMOD_3TOI              epr.get_data_type_size
    epr.E_TID_CHAR               epr.get_sample_model_name
    epr.E_TID_DOUBLE             epr.get_scaling_method_name
    epr.E_TID_FLOAT              epr.np
    epr.E_TID_INT                epr.open
    epr.E_TID_SHORT              epr.so
    epr.E_TID_SPARE              epr.sys


.. index:: product

:class:`epr.Product` navigation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The first thing to do is to use the :func:`epr.open` function to get an
instance of the desired ENVISAT_ :class:`epr.Product`::

    In [4]: product = epr.open(\
    'ASA_IMP_1PNUPA20060202_062233_000000152044_00435_20529_3110.N1')

    In [4]: product.
    product.bands                product.get_mph
    product.close                product.get_num_bands
    product.closed               product.get_num_datasets
    product.datasets             product.get_num_dsds
    product.file_path            product.get_scene_height
    product.get_band             product.get_scene_width
    product.get_band_at          product.get_sph
    product.get_band_names       product.id_string
    product.get_dataset          product.meris_iodd_version
    product.get_dataset_at       product.read_bitmask_raster
    product.get_dataset_names    product.tot_size
    product.get_dsd_at

    In [5]: product.tot_size / 1024.**2
    Out[5]: 132.01041889190674

    In [6]: print(product)
    epr.Product(ASA_IMP_1PNUPA20060202_ ...) 7 datasets, 5 bands

    epr.Dataset(MDS1_SQ_ADS) 1 records
    epr.Dataset(MAIN_PROCESSING_PARAMS_ADS) 1 records
    epr.Dataset(DOP_CENTROID_COEFFS_ADS) 1 records
    epr.Dataset(SR_GR_ADS) 1 records
    epr.Dataset(CHIRP_PARAMS_ADS) 1 records
    epr.Dataset(GEOLOCATION_GRID_ADS) 11 records
    epr.Dataset(MDS1) 8192 records

    epr.Band(slant_range_time) of epr.Product(ASA_IMP_1PNUPA20060202_ ...)
    epr.Band(incident_angle) of epr.Product(ASA_IMP_1PNUPA20060202_ ...)
    epr.Band(latitude) of epr.Product(ASA_IMP_1PNUPA20060202 ...)
    epr.Band(longitude) of epr.Product(ASA_IMP_1PNUPA20060202 ...)
    epr.Band(proc_data) of epr.Product(ASA_IMP_1PNUPA20060202 ...)

A short summary of product contents can be displayed simply printing the
:class:`epr.Product` object as showed above.
Being able to display contents of each object it is easy to keep browsing and
get all desired information from the product::

    In [7]: dataset = product.get_dataset('MAIN_PROCESSING_PARAMS_ADS')

    In [8]: dataset
    Out[8]: epr.Dataset(MAIN_PROCESSING_PARAMS_ADS) 1 records

    In [9]: record = dataset.[TAB]
    dataset.create_record    dataset.get_dsd_name     dataset.product
    dataset.description      dataset.get_name         dataset.read_record
    dataset.get_dsd          dataset.get_num_records  dataset.records

    In [9]: record = dataset.read_record(0)

    In [10]: record
    Out[10]: <epr.Record object at 0x33570f0> 220 fields

    In [11]: record.get_field_names()[:20]
    Out[11]:
    ['first_zero_doppler_time',
     'attach_flag',
     'last_zero_doppler_time',
     'work_order_id',
     'time_diff',
     'swath_id',
     'range_spacing',
     'azimuth_spacing',
     'line_time_interval',
     'num_output_lines',
     'num_samples_per_line',
     'data_type',
     'spare_1',
     'data_analysis_flag',
     'ant_elev_corr_flag',
     'chirp_extract_flag',
     'srgr_flag',
     'dop_cen_flag',
     'dop_amb_flag',
     'range_spread_comp_flag']

    In [12]: field = record.get_field('range_spacing')

    In [13]: field.get [TAB]
    field.get_description  field.get_name         field.get_unit
    field.get_elem         field.get_num_elems
    field.get_elems        field.get_type

    In [13]: field.get_description()
    Out[13]: 'Range sample spacing'

    In [14]: epr.data_type_id_to_str(field.get_type())
    Out[14]: 'float'

    In [15]: field.get_num_elems()
    Out[15]: 1

    In [16]: field.get_unit()
    Out[16]: 'm'

    In [17]: print(field)
    range_spacing = 12.500000


.. index:: iteration, iterable, record

Iterating over :mod:`epr` objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:class:`epr.Record` objects are also iterable_ so one can write code like
the following::

    In [18]: for field in record:
                 if field.get_num_elems() == 4:
                     print('%s: %d elements' % (field.get_name(), len(field)))

            ....:
    nominal_chirp.1.nom_chirp_amp: 4 elements
    nominal_chirp.1.nom_chirp_phs: 4 elements
    nominal_chirp.2.nom_chirp_amp: 4 elements
    nominal_chirp.2.nom_chirp_phs: 4 elements
    nominal_chirp.3.nom_chirp_amp: 4 elements
    nominal_chirp.3.nom_chirp_phs: 4 elements
    nominal_chirp.4.nom_chirp_amp: 4 elements
    nominal_chirp.4.nom_chirp_phs: 4 elements
    nominal_chirp.5.nom_chirp_amp: 4 elements
    nominal_chirp.5.nom_chirp_phs: 4 elements
    beam_merge_sl_range: 4 elements
    beam_merge_alg_param: 4 elements


.. index:: data, image

Image data
~~~~~~~~~~

Dealing with image data is simple as well::

    In [19]: product.get_band_names()
    Out[19]: ['slant_range_time',
              'incident_angle',
              'latitude',
              'longitude',
              'proc_data']

    In [19]: band = product.get_band('proc_data')

    In [20]: data = band. [TAB]
    band.bm_expr                   band.read_raster
    band.create_compatible_raster  band.sample_model
    band.data_type                 band.scaling_factor
    band.description               band.scaling_method
    band.get_name                  band.scaling_offset
    band.lines_mirrored            band.spectr_band_index
    band.product                   band.unit
    band.read_as_array

    In [20]: data = band.read_as_array(1000, 1000, xoffset=100, \
    yoffset=6500, xstep=2, ystep=2)

    In [21]: data
    Out[21]:
    array([[ 146.,  153.,  134., ...,   51.,   55.,   72.],
           [ 198.,  163.,  146., ...,   26.,   54.,   57.],
           [ 127.,  205.,  105., ...,   64.,   76.,   61.],
           ...,
           [  64.,   78.,   52., ...,   96.,  176.,  159.],
           [  66.,   41.,   45., ...,  200.,  153.,  203.],
           [  64.,   71.,   88., ...,  289.,  182.,  123.]], dtype=float32)

    In [22]: data.shape
    Out[22]: (500, 500)

    In [23]: imshow(data, cmap=cm.gray, vmin=0, vmax=1000)
    Out[23]: <matplotlib.image.AxesImage object at 0x60dcf10>

    In [24]: title(band.description)
    Out[24]: <matplotlib.text.Text object at 0x67e9950>

    In [25]: colorbar()
    Out[25]: <matplotlib.colorbar.Colorbar instance at 0x6b18cb0>

.. figure:: images/ASA_IMP_crop.*
   :width: 100%

   Image data read from the "proc_data" band


.. _iterable: https://docs.python.org/3/glossary.html#term-iterable


.. index:: close, product

Closing the epr.Product
~~~~~~~~~~~~~~~~~~~~~~~

Finally the :class:`epr.Product` can be closed using the
:meth:`epr.Product.close` method::

    In [26]: product.close()

After a product is closed no more I/O operations can be performed on it.
Any attempt to do it will raise a :exc:`ValueError`::

    In [27]: product.tot_size / 1024.**2
    -------------------------------------------------------------------------
    ValueError                              Traceback (most recent call last)
    <ipython-input-13-6420c80534dc> in <module>()
    ----> 1 product.tot_size / 1024.**2

    epr.so in epr.Product.tot_size.__get__ (src/epr.c:16534)()

    epr.so in epr.Product.check_closed_product (src/epr.c:16230)()

    ValueError: I/O operation on closed file


At any time the user can check whenever a :class:`epr.Product` is closed or
not using the :attr:`epr.Product.closed` property::

    In [28]: product.closed
    Out[28]: True

.. raw:: latex

   \clearpage
