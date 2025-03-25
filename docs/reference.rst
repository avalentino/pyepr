API Reference
=============

.. module:: epr
   :synopsis: Python bindings for ENVISAT Product Reader C API

.. index:: bindings, ENVISAT, ESA, EPR-API
   pair: epr; module

PyEPR_ provides Python_ bindings for the ENVISAT Product Reader C API
(`EPR API`_) for reading satellite data from ENVISAT_ ESA_ (European
Space Agency) mission.

PyEPR_ is fully object oriented and, as well as the `EPR API`_ for C,
supports ENVISAT_ MERIS, AATSR Level 1B and Level 2 and also ASAR data
products. It provides access to the data either on a geophysical
(decoded, ready-to-use pixel samples) or on a raw data layer.
The raw data access makes it possible to read any data field contained
in a product file.

.. _PyEPR: https://github.com/avalentino/pyepr
.. _Python: https://www.python.org
.. _`EPR API`: https://github.com/bcdev/epr-api
.. _ENVISAT: https://envisat.esa.int
.. _ESA: https://earth.esa.int


.. currentmodule:: epr


Classes
-------

Product
~~~~~~~

.. class:: Product

   ENVISAT product.

   The Product class provides methods and properties to get information
   about an ENVISAT product file.

   .. seealso:: :func:`open`


   .. rubric:: Attributes

   .. attribute:: file_path

      The file's path including the file name.


   .. attribute:: mode

      String that specifies the mode in which the file is opened.

      Possible values: `rb` for read-only mode, `rb+` for read-write mode.


   .. attribute:: id_string

      The product identifier string obtained from the MPH parameter 'PRODUCT'.

      The first 10 characters of this string identify the product type,
      e.g. "MER_1P__FR" for a MERIS Level 1b full resolution product.
      The rest of the string decodes product instance properties.


   .. attribute:: meris_iodd_version

      For MERIS L1b and RR and FR to provide backward compatibility.


   .. attribute:: tot_size

      The total size in bytes of the product file.


   .. rubric:: Methods

   .. method:: get_band(name)

      Gets the band corresponding to the specified name.

      :param name:
            the name of the band
      :returns:
            the requested :class:`Band` instance, or raises a
            :exc:`EPRValueError` if not found


   .. method:: get_band_at(index)

      Gets the :class:`Band` at the specified position within the
      :class:`product`.

      :param index:
            the index identifying the position of the :class:`Band`, starting
            with 0, must not be negative
      :returns:
            the requested :class:`Band` instance, or raises a
            :exc:`EPRValueError` if not found


   .. method:: get_dataset(name)

      Gets the :class:`Dataset` corresponding to the specified dataset name.

      :param name:
            the :class:`Dataset` name
      :returns:
            the requested :class:`Dataset` instance


   .. method:: get_dataset_at(index)

      Gets the :class:`Dataset` at the specified position within the
      :class:`Product`.

      :param index:
            the index identifying the position of the :class:`Dataset`,
            starting with 0, must not be negative
      :returns:
            the requested :class:`Dataset`


   .. method:: get_dsd_at(index)

      Gets the :class:`DSD` at the specified position.

      Gets the :class:`DSD` (:class:`Dataset` descriptor) at the specified
      position within the :class:`Product`.

      :param index:
            the index identifying the position of the :class:`DSD`,
            starting with 0, must not be negative
      :returns:
            the requested :class:`DSD` instance


   .. method:: get_num_bands()

      Gets the number of all :class:`Band`\ s contained in a :class:`Product`.


   .. method:: get_num_datasets()

      Gets the number of all :class:`Dataset`\ s contained in a
      :class:`Product`.


   .. method:: get_num_dsds()

      Gets the number of all :class:`DSD`\ s (:class:`Dataset` descriptors)
      contained in the :class:`Product`.


   .. method:: get_scene_height()

      Gets the :class:`Product` scene height in pixels.


   .. method:: get_scene_width()

      Gets the :class:`Product` scene width in pixels.


   .. method:: get_mph()

      The :class:`Record` representing the main product header (MPH).


   .. method:: get_sph()

      The :class:`Record` representing the specific product header (SPH).


   .. method:: read_bitmask_raster(bm_expr, xoffset, yoffset, raster)

      Calculates a bit-mask raster.

      Calculates a bit-mask, composed of flags of the given :class:`Product`
      and combined as described in the given bit-mask expression, for
      the a certain dimension and sub-sampling as defined in the
      given raster.

      :param bm_expr:
            a string holding the logical expression for the definition
            of the bit-mask. In a bit-mask expression, any number of
            the flag-names (found in the DDDB) can be composed with
            "(", ")", "NOT", "AND", "OR". Valid bit-mask expression are
            for example ``flags.LAND OR flags.CLOUD`` or
            ``NOT flags.WATER AND flags.TURBID_S``
      :param xoffset:
            across-track co-ordinate in pixel co-ordinates (zero-based)
            of the upper right corner of the source-region
      :param yoffset:
            along-track co-ordinate in pixel co-ordinates (zero-based)
            of the upper right corner of the source-region
      :param raster:
            the raster for the bit-mask. The data type of the raster
            must be either :data:`E_TID_UCHAR` or :data:`E_TID_CHAR`
      :returns:
            zero for success, an error code otherwise

      .. seealso:: :func:`create_bitmask_raster`.


   .. method:: close

       Closes the :class:`Product` product and free the underlying
       file descriptor.

       This method has no effect if the :class:`Product` is already
       closed. Once the :class:`Product` is closed, any operation on
       it will raise a :exc:`ValueError`.

       As a convenience, it is allowed to call this method more than
       once; only the first call, however, will have an effect.


   .. method:: flush()

       Flush the file stream.


   .. rubric:: High level interface methods

   .. note::

      the following methods are part of the *high level* Python API and
      do not have any corresponding function in the C API.

   .. attribute:: closed

      True if the :class:`Product` is closed.


   .. method:: get_dataset_names()

      Return the list of names of the :class:`Dataset`\ s in the
      :class:`Product`.


   .. method:: get_band_names()

      Return the list of names of the :class:`Band`\ s in the :class:`Product`.


   .. method:: datasets()

      Return the list of :class:`Dataset`\ s in the :class:`Product`.


   .. method:: bands()

      Return the list of :class:`Band`\ s in the :class:`Product`.


   .. rubric:: Special methods

   The :class:`Product` class provides a custom implementation of the
   following *special methods*:

   * __repr__
   * __str__
   * __enter__
   * __exit__

   .. index:: __repr__, __str__, __enter__, __exit__
      pair: special; methods


Dataset
~~~~~~~

.. class:: Dataset

   ENVISAT dataset.

   The Dataset class contains information about a dataset within an
   ENVISAT product file which has been opened with the :func:`open`
   function.

   A new Dataset instance can be obtained with the
   :meth:`Product.get_dataset` or :meth:`Product.get_dataset_at` methods.


   .. rubric:: Attributes

   .. attribute:: description

      A short description of the :class:`Band` contents.


   .. attribute:: product

      The :class:`Product` instance to which this :class:`Dataset` belongs to.


   .. rubric:: Methods

   .. method:: get_name()

      Gets the name of the :class:`Dataset`.


   .. method:: get_dsd()

      Gets the :class:`Dataset` descriptor (:class:`DSD`).


   .. method:: get_dsd_name()

      Gets the name of the :class:`DSD` (:class:`Dataset` descriptor).


   .. method:: get_num_records()

      Gets the number of :class:`Record`\ s of the :class:`Dataset`.


   .. method:: create_record()

      Creates a new :class:`Record`.

      Creates a new, empty :class:`Record` with a structure compatible with
      the :class:`Dataset`. Such a :class:`Record` is typically used in
      subsequent calls to :meth:`Dataset.read_record`.

      :returns:
            the new :class:`Record` instance


   .. method:: read_record(index[, record])

      Reads specified :class:`Record` of the :class:`Dataset`.

      The :class:`Record` is identified through the given zero-based
      :class:`Record` index. In order to reduce memory reallocation, a
      :class:`Record` (pre-)created by the method
      :meth:`Dataset.create_record` can be passed to this method.
      Data is then read into this given :class:`Record`.

      If no :class:`Record` (``None``) is given, the method initiates a new
      one.

      In both cases, the :class:`Record` in which the data is read into will
      be returned.

      :param index:
            the zero-based :class:`Record` index (default: 0)
      :param record:
            a pre-created :class:`Record` to reduce memory reallocation,
            can be ``None`` (default) to let the function allocate a new
            :class:`Record`
      :returns:
            the record in which the data has been read into or raises
            an exception (:exc:`EPRValueError`) if an error occurred

      .. versionchanged:: 0.9

         The *index* parameter now defaults to zero.


   .. rubric:: High level interface methods

   .. note::

      the following methods are part of the *high level* Python API and
      do not have any corresponding function in the C API.

   .. method:: records()

      Return the list of :class:`Record`\ s contained in the :class:`Dataset`.


   .. rubric:: Special methods

   The :class:`Dataset` class provides a custom implementation of the
   following *special methods*:

   * __repr__
   * __str__
   * __iter__

   .. index:: __repr__, __str__, __iter__
      pair: special; methods


Record
~~~~~~

.. class:: Record

   Represents a record read from an ENVISAT dataset.

   A record is composed of multiple fields.

   .. seealso:: :class:`Field`


   .. rubric:: Attributes

   .. attribute::  dataset_name

      The name of the :class:`Dataset` to which this :class:`Record` belongs to.

      .. versionadded:: 0.9


   .. attribute:: tot_size

      The total size in bytes of the :class:`Record`.

      It includes all data elements of all :class:`Field`\ s of a
      :class:`Record` in a :class:`Product` file.

      *tot_size* is a derived variable, it is computed at run-time
      and not stored in the DSD-DB.

      .. versionadded:: 0.9


   .. attribute:: index

      Index of the :class:`Record` within the :class:`Dataset`.

      It is *None* for empty :class:`Record`\ s (created with
      :meth:`Dataset.create_record` but still not read) and for *MPH*
      (see :meth:`Product.get_mph`) and *SPH* (see :meth:`Product.get_sph`)
      :class:`Record`\ s.

     .. seealso:: :meth:`Dataset.read_record`

     .. versionadded:: 0.9


   .. rubric:: Methods

   .. method:: get_field(name)

      Gets a :class:`Field` specified by name.

      The :class:`Field` is here identified through the given name.
      It contains the :class:`Field` info and all corresponding values.

      :param name:
            the the name of required :class:`Field`
      :returns:
            the specified :class:`Field` or raises an exception
            (:exc:`EPRValueError`) if an error occurred


   .. method:: get_field_at(index)

      Gets a :class:`Field` at the specified position within the
      :class:`Record`.

      :param index:
            the zero-based index (position within :class:`Record`) of the
            :class:`Field`
      :returns:
            the :class:`Field` or raises and exception (:exc:`EPRValueError`)
            if an error occurred


   .. method:: get_num_fields()

      Gets the number of :class:`Field`\ s contained in the :class:`Record`.


   .. method:: print_([ostream])

      Write the :class:`Record` to specified file (default: :data:`sys.stdout`).

      This method writes formatted contents of the :class:`Record` to
      specified *ostream* text file or (default) the ASCII output
      is be printed to standard output (:data:`sys.stdout`).

      :param ostream:
            the (opened) output file object

      .. note::

         the *ostream* parameter have to be a *real* file not
         a generic stream object like :class:`StringIO.StringIO`
         instances.


   .. method:: print_element(field_index, element_index[, ostream])

      Write the specified field element to file (default: :data:`sys.stdout`).

      This method writes formatted contents of the specified :class:`Field`
      element to the *ostream* text file or (default) the ASCII output
      will be printed to standard output (:data:`sys.stdout`).

      :param field_index:
            the index of :class:`Field` in the :class:`Record`
      :param element_index:
            the index of element in the specified :class:`Field`
      :param ostream:
            the (opened) output file object

      .. note::

         the *ostream* parameter have to be a *real* file not
         a generic stream object like :class:`StringIO.StringIO`
         instances.


   .. method:: get_offset()

      :class:`Record` offset in bytes within the :class:`Dataset`.

      .. versionadded:: 0.9


   .. rubric:: High level interface methods

   .. note::

      the following methods are part of the *high level* Python API and
      do not have any corresponding function in the C API.

   .. method:: get_field_names

      Return the list of names of the :class:`Field`\ s in the :class:`Record`.


   .. method:: fields()

      Return the list of :class:`Field`\ s contained in the :class:`Record`.


   .. rubric:: Special methods

   The :class:`Record` class provides a custom implementation of the
   following *special methods*:

   * __repr__
   * __str__
   * __iter__

   .. index:: __repr__, __str__, __iter__
      pair: special; methods


Field
~~~~~

.. class:: Field

   Represents a field within a record.

   A :class:`Field` is composed of one or more data elements of one of the
   types defined in the internal ``field_info`` structure.

   .. seealso:: :class:`Record`


   .. rubric:: Attributes

   .. attribute::  tot_size

        The total size in bytes of all data elements of a :class:`Field`.

        *tot_size* is a derived variable, it is computed at run-time and
        not stored in the DSD-DB.

      .. versionadded:: 0.9


   .. method:: get_description()

      Gets the description of the :class:`Field`.


   .. method:: get_name()

      Gets the name of the :class:`Field`.


   .. method:: get_num_elems()

      Gets the number of elements of the :class:`Field`.


   .. method:: get_type()

      Gets the type of the :class:`Field`.


   .. method:: get_unit()

      Gets the unit of the :class:`Field`.


   .. method:: get_elem([index])

      :class:`Field` single element access.

      This function is for getting the elements of a :class:`Field`.

      :param index:
            the zero-based index of element to be returned, must not be
            negative. Default: 0.
      :returns:
            the typed value from given :class:`Field`


   .. method:: get_elems()

      :class:`Field` array element access.

      This function is for getting an array of field elements of the
      :class:`Field`.

      :returns:
            the data array (:class:`numpy.ndarray`) having the type of
            the :class:`Field`

      .. versionchanged:: 0.9

         the returned :class:`numpy.ndarray` shares the data buffer with
         the C :c:type:`Field` structure so any change in its contents is
         also reflected to the :class:`Filed` object


   .. method:: set_elem(elem, [index])

      Set :class:`Field` array element.

      This function is for setting an array of field element of the
      :class:`Field`.

      :param elem:
            value of the element to set
      :param index:
            the zero-based index of element to be set, must not be
            negative. Default: 0.

      .. note::

         this method does not have any corresponding function in the C API.

      .. versionadded:: 0.9


   .. method:: set_elems(elems)

      Set :class:`Field` array elements.

      This function is for setting an array of :class:`Field` elements of
      the :class:`Field`.

      :param elems:
            np.ndarray of elements to set

      .. note::

         this method does not have any corresponding function in the C API.

      .. versionadded:: 0.9


   .. method:: print_([ostream])

      Write the :class:`Field` to specified file (default: :data:`sys.stdout`).

      This method writes formatted contents of the :class:`Field` to
      specified *ostream* text file or (default) the ASCII output
      is be printed to standard output (:data:`sys.stdout`).

      :param ostream:
            the (opened) output file object

      .. note::

         the *ostream* parameter have to be a *real* file not
         a generic stream object like :class:`StringIO.StringIO`
         instances


   .. method:: get_offset()

      Field offset in bytes within the :class:`Record`.

      .. versionadded:: 0.9


   .. rubric:: Special methods

   The :class:`Field` class provides a custom implementation of the
   following *special methods*:

   * __repr__
   * __str__
   * __eq__
   * __ne__
   * __len__ [#]_

   .. index:: __repr__, __str__, __eq__, __ne__, __len__
      pair: special; methods

.. rubric:: Footnotes

.. [#] if the field is a :data:`E_TID_STRING` field then the
       :meth:`__len__` method returns the string length, otherwise the
       number of elements of the field is returned (same as
       :meth:`Field.get_num_elems`)


DSD
~~~

.. class:: DSD

   :class:`Dataset` descriptor.

   The DSD class contains information about the properties of a
   :class:`Dataset` and its location within an ENVISAT :class:`Product` file.


   .. rubric:: Attributes

   .. attribute:: ds_name

      The :class:`Dataset` name.


   .. attribute:: ds_offset

      The offset of :class:`Dataset` in the :class:`Product` file.


   .. attribute:: ds_size

      The size of :class:`Dataset` in the :class:`Product` file.


   .. attribute:: ds_type

      The :class:`Dataset` type descriptor.


   .. attribute:: dsr_size

      The size of dataset record for the given :class:`Dataset` name.


   .. attribute:: filename

      The filename in the DDDB with the description of this :class:`Dataset`.


   .. attribute:: index

      The index of this :class:`DSD` (zero-based).


   .. attribute:: num_dsr

      The number of dataset records for the given :class:`Dataset` name.


   .. rubric:: Special methods

   The :class:`DSD` class provides a custom implementation of the
   following *special methods*:

   * __repr__
   * __eq__
   * __ne__

   .. index:: __repr__, __eq__, __ne__
      pair: special; methods


Band
~~~~

.. class:: Band

   The band of an ENVISAT :class:`Product`.

   The Band class contains information about a band within an ENVISAT
   :class:`Product` file which has been opened with the :func:`open`
   function.

   A new Band instance can be obtained with the :meth:`Product.get_band`
   method.


   .. rubric:: Attributes

   .. attribute:: bm_expr

      A bit-mask expression used to filter valid pixels.

      All others are set to zero.


   .. attribute:: data_type

      The data type of the :class:`Band` pixels.

      Possible values are:

      * ``*``         --> the datatype remains unchanged.
      * ``uint8_t``   --> 8-bit unsigned integer
      * ``uint32_t``  --> 32-bit unsigned integer
      * ``Float``     --> 32-bit IEEE floating point


   .. attribute:: description

      A short description of the :class:`Band` contents.


   .. attribute:: lines_mirrored

      Mirrored lines flag.

      If true (=1) lines will be mirrored (flipped) after read into a
      raster in order to ensure a pixel ordering in raster X direction
      from WEST to EAST.


   .. attribute:: product

      The :class:`Product` instance to which this :class:`Band` belongs to.


   .. attribute:: sample_model

      The sample model operation.

      The sample model operation applied to the source :class:`Dataset` for
      getting the correct samples from the MDS (for example MERIS L2).

      Possible values are:

      * ``*``     --> no operation (direct copy)
      * ``1OF2``  --> first byte of 2-byte interleaved MDS
      * ``2OF2``  --> second byte of 2-byte interleaved MDS
      * ``0123``  --> combine 3-bytes interleaved to 4-byte integer


   .. attribute:: scaling_factor

      The scaling factor.

      Possible values are:

      * ``*`` --> no factor provided (implies scaling_method=*)
      * ``const`` --> a floating point constant
      * ``GADS.field[.field2]`` --> value is provided in global
        annotation :class:`Dataset` with name `GADS` in :class:`Field`
        `field`.
        Optionally a second element index for multiple-element fields
        can be given too


   .. attribute:: scaling_method

      The scaling method which must be applied to the raw source data
      in order to get the 'real' pixel values in geo-physical units.

      Possible values are:

      * ``*``            --> no scaling applied
      * ``Linear_Scale`` --> linear scaling applied::

            y = offset + scale * x

      * ``Log_Scale``    --> logarithmic scaling applied::

            y = log10(offset + scale * x)


   .. attribute:: scaling_offset

      Possible values are:

      * ``*`` --> no offset provided (implies scaling_method=*)
      * ``const`` --> a floating point constant
      * ``GADS.field[.field2]` --> value is provided in global
        annotation :class:`Dataset` with name ``GADS`` in :class:`Field`
        ``field``.
        Optionally a second element index for multiple-element fields
        can be given too


   .. attribute:: spectr_band_index

      The (zero-based) spectral :class:`Band` index.

      -1 if this is not a spectral :class:`Band`.


   .. attribute:: unit

      The geophysical unit for the :class:`Band` pixel values.


   .. attribute:: dataset

      The source :class:`Dataset`.

      The source :class:`Dataset` containing the raw data used to create the
      :class:`Band` pixel values.

      .. versionadded:: 0.9


   .. rubric:: Methods

   .. method:: get_name()

      Gets the name of the :class:`Band`.


   .. method:: create_compatible_raster([src_width, src_height, xstep, ystep])

      Creates a :class:`Raster` which is compatible with the data type of
      the :class:`Band`.

      The created :class:`Raster` is used to read the data in it (see
      :meth:`Band.read_raster`).

      The :class:`Raster` is defined on the grid of the :class:`Product`,
      from which the data are read. Spatial subsets and under-sampling are
      possible) through the parameter of the method.

      A :class:`Raster` is an object that allows direct access to data of a
      certain portion of the ENVISAT :class:`Product` that are read into the
      it. Such a portion is called the source. The complete ENVISAT
      :class:`Product` can be much greater than the source.
      One can move the :class:`Raster` over the complete ENVISAT
      :class:`Product` and read in turn different parts
      (always of the size of the source) of it into the :class:`Raster`.
      The source is specified by the parameters *height* and *width*.

      A typical example is a processing in blocks. Lets say, a block
      has 64x32 pixel. Then, my source has a width of 64 pixel and a
      height of 32 pixel.

      Another example is a processing of complete image lines. Then,
      my source has a widths of the complete product (for example 1121
      for a MERIS RR product), and a height of 1). One can loop over
      all blocks read into the :clasS:`Raster` and process it.

      In addition, it is possible to defined a sub-sampling step for
      a :class:`Raster`. This means, that the source is not read 1:1 into
      the :class:`Raster`, but that only every 2nd or 3rd pixel is read.
      This step can be set differently for the across track (source_step_x)
      and along track (source_step_y) directions.

      :param src_width:
            the width (across track dimension) of the source to be read
            into the :class:`Raster`. Default: scene width (see
            :attr:`Product.get_scene_width`)
      :param src_height:
            the height (along track dimension) of the source to be read
            into the :class:`Raster`. Default: scene height (see
            :attr:`Product.get_scene_height`)
      :param xstep:
            the sub-sampling step across track of the source when reading
            into the :class:`Raster`. Default: 1.
      :param ystep:
            the sub-sampling step along track of the source when reading
            into the :class:`Raster`. Default: 1.
      :returns:
            the new :class:`Raster` instance or raises an exception
            (:exc:`EPRValueError`) if an error occurred

      .. note::

         *src_width* and *src_height* are the dimantion of the of the source
         area. If one specifies a *step* parameter the resulting
         :class:`Raster` will have a size that is smaller that the specifies
         source size::

             raster_size = src_size // step


   .. method:: read_raster([xoffset, yoffset, raster])

      Reads (geo-)physical values of the :class:`Band` of the specified
      source-region.

      The source-region is a defined part of the whole ENVISAT
      :class:`Product` image, which shall be read into a :class:`Raster`.
      In this routine the co-ordinates are specified, where the
      source-region to be read starts.
      The dimension of the region and the sub-sampling are attributes
      of the :class:`Raster` into which the data are read.

      :param xoffset:
            across-track source co-ordinate in pixel co-ordinates
            (zero-based) of the upper right corner of the source-region.
            Default 0.
      :param yoffset:
            along-track source co-ordinate in pixel co-ordinates
            (zero-based) of the upper right corner of the source-region.
            Default 0.
      :param raster:
            :class:`Raster` instance set with appropriate parameters to
            read into. If not provided a new :class:`Raster` is
            instantiated
      :returns:
            the :class:`Raster` instance in which data are read

      This method raises an instance of the appropriate
      :exc:`EPRError` sub-class if case of errors

      .. seealso:: :meth:`Band.create_compatible_raster` and
                   :func:`create_raster`


   .. rubric:: High level interface methods

   .. note::

      the following methods are part of the *high level* Python API and
      do not have any corresponding function in the C API.

   .. method:: read_as_array([width, height, xoffset, yoffset, xstep, ystep])

      Reads the specified source region as an :class:`numpy.ndarray`.

      The source-region is a defined part of the whole ENVISAT
      :class:`Product` image, which shall be read into a :class:`Raster`.
      In this routine the co-ordinates are specified, where the
      source-region to be read starts.
      The dimension of the region and the sub-sampling are attributes
      of the :class:`Raster` into which the data are read.

      :param src_width:
            the width (across track dimension) of the source to be read
            into the :class:`Raster`. If not provided reads as much as
            possible
      :param src_height:
            the height (along track dimension) of the source to be read
            into the :class:`Raster`, If not provided reads as much as
            possible
      :param xoffset:
            across-track source co-ordinate in pixel co-ordinates
            (zero-based) of the upper right corner of the source-region.
            Default 0.
      :param yoffset:
            along-track source co-ordinate in pixel co-ordinates
            (zero-based) of the upper right corner of the source-region.
            Default 0.
      :param xstep:
            the sub-sampling step across track of the source when
            reading into the :class:`Raster`. Default: 1
      :param ystep:
            the sub-sampling step along track of the source when
            reading into the :class:`Raster`. Default: 1
      :returns:
            the :class:`numpy.ndarray` instance in which data are read

      This method raises an instance of the appropriate
      :exc:`EPRError` sub-class if case of errors

      .. seealso:: :meth:`Band.create_compatible_raster`,
                   :func:`create_raster` and :meth:`Band.read_raster`


   .. rubric:: Special methods

   The :class:`Band` class provides a custom implementation of the
   following *special methods*:

   * __repr__

   .. index:: __repr__
      pair: special; methods


Raster
~~~~~~

.. class:: Raster

   Represents a raster in which data will be stored.

   All 'size' parameter are in PIXEL.


   .. rubric:: Attributes

   .. attribute:: data_type

      The data type of the :class:`Band` pixels.

      All ``E_TID_*`` types are possible.


   .. attribute:: source_height

      The height of the source.


   .. attribute:: source_width

      The width of the source.


   .. attribute:: source_step_x

      The sub-sampling for the across-track direction in pixel.


   .. attribute:: source_step_y

      The sub-sampling for the along-track direction in pixel.


   .. rubric:: High level interface attributes

   .. note::

      the following attributess are part of the *high level* Python API and
      do not have a counterpart in the C API.

   .. attribute:: data

      Raster data exposed as :class:`numpy.ndarray` object.

      .. note::

         this property shares the data buffer with the :class:`Raster`
         object so any change in its contents is also reflected to
         the :class:`Raster` object

      .. note::

         the :class:`Raster` objects do not have a :class:`Field` named
         *data* in the corresponding C structure. The *EPR_SRaster* C
         structure have a :class:`Field` named *buffer* that is a raw
         pointer to the data buffer and it is not exposed as such in the
         Python API.


   .. rubric:: Methods

   .. method:: get_pixel(x, y)

      Single pixel access.

      This function is for getting the values of the elements of a
      :class:`Raster` (i.e. pixel)

      :param x:
            the (zero-based) X coordinate of the pixel
      :param y:
            the (zero-based) Y coordinate of the pixel
      :returns:
            the typed value at the given co-ordinate


   .. method:: get_elem_size()

      The size in byte of a single element (sample) of this :class:`Raster`
      buffer.


   .. method:: get_height()

      Gets the :class:`Raster` height in pixels.


   .. method:: get_width()

      Gets the :class:`Raster` width in pixels.


   .. rubric:: Special methods

   The :class:`Raster` class provides a custom implementation of the
   following *special methods*:

   * __repr__

   .. index:: __repr__
      pair: special; methods


EPRTime
~~~~~~~

.. class:: EPRTime

   Convenience class for time data exchange.

   EPRTime is a :class:`collections.namedtuple` with the following fields:

   .. attribute:: days
   .. attribute:: seconds
   .. attribute:: microseconds


.. index:: function

Functions
---------

.. function:: open(filename, mode='rb')

   Open the ENVISAT product.

   Opens the ENVISAT :class:`Product` file with the given file path,
   reads MPH, SPH and all :class:`DSD`\ s, organized the table with
   parameter of line length and tie points number.

   :param product_file_path:
        the path to the ENVISAT :class:`Product` file
   :param mode:
        string that specifies the mode in which the file is opened.
        Allowed values: `rb` for read-only mode, `rb+` for read-write
        mode. Default: mode=`rb`.
   :returns:
        the :class:`Product` instance representing the specified
        product. An exception (:exc:`exceptions.ValueError`) is raised
        if the file could not be opened.

   The :class:`Product` class supports context management so the recommended
   way to ensure that a product is actually closed as soon as a task is
   completed is to use the ``with`` statement::

       with open('ASA_IMP_1PNUPA20060202_ ... _3110.N1') as product:
           dataset = product.get_dataset('MAIN_PROCESSING_PARAMS_ADS')
           record = dataset.read_record(0)
           print(record)

   .. seealso :class:`Product`


.. function:: data_type_id_to_str(type_id)

   Gets the 'C' data type string for the given data type.


.. function:: get_data_type_size(type_id)

   Gets the size in bytes for an element of the given data type.


.. function:: get_numpy_dtype(type_id)

   Return the numpy data-type specified EPR type ID.

   .. versionadded:: 0.9


.. function:: get_sample_model_name(model)

   Return the name of the specified sample model.


.. function:: get_scaling_method_name(method)

   Return the name of the specified scaling method.


.. function:: create_raster(data_type, src_width, src_height[, xstep, ystep])

   Creates a :class:`Raster` of the specified data type.

   This function can be used to create any type of raster, e.g. for
   later use as a bit-mask.

   :param data_type:
        the type of the data to stored in the :class:`Raster`, must be one
        of E_TID_*.

        .. seealso:: `Data type Identifiers`_

   :param src_width:
        the width (across track dimension) of the source to be read
        into the :class:`Raster`.
        See description of :meth:`Band.create_compatible_raster`
   :param src_height:
        the height (along track dimension) of the source to be read
        into the :class:`Raster`.
        See description of :meth:`Band.create_compatible_raster`
   :param xstep:
        the sub-sampling step across track of the source when reading
        into the :class:`Raster`. Default: 1.
   :param ystep:
        the sub-sampling step along track of the source when reading
        into the :class:`Raster`. Default: 1.
   :returns:
        the new :class:`Raster` instance

   .. seealso:: description of :meth:`Band.create_compatible_raster`


.. function:: create_bitmask_raster(src_width, src_height[, xstep, ystep])

   Creates a :class:`Raster` to be used for reading bitmasks.

   The :class:`Raster` returned always is of type ``byte``.

   :param src_width:
        the width (across track dimension) of the source to be read
        into the :class:`Raster`
   :param src_height:
        the height (along track dimension) of the source to be read
        into the :class:`Raster`
   :param xstep:
        the sub-sampling step across track of the source when reading
        into the :class:`Raster`. Default: 1.
   :param ystep:
        the sub-sampling step along track of the source when reading
        into the :class:`Raster`. Default: 1.
   :returns:
        the new :class:`Raster` instance or raises an exception
        (:exc:`EPRValueError`) if an error occurred

   .. seealso:: the description of :meth:`Band.create_compatible_raster`


.. index:: exception, error

Exceptions
----------

EPRError
~~~~~~~~

.. exception:: EPRError

   EPR API error.

   .. attribute:: code

      EPR API error code.


   .. method:: __init__([message[, code, *args, **kwargs]])

      Initializer.

      :param message:
            error message
      :param code:
            EPR error code


EPRValueError
~~~~~~~~~~~~~

.. exception:: EPRValueError

   Inherits both :exc:`EPRError` and standard :exc:`exceptions.ValueError`.


Data
----

.. data:: __version__

   Version string of PyEPR.


.. data:: EPR_C_API_VERSION

   Version string of the wrapped `EPR API`_ C library.


Data type identifiers
~~~~~~~~~~~~~~~~~~~~~

.. data:: E_TID_UNKNOWN
.. data:: E_TID_UCHAR
.. data:: E_TID_CHAR
.. data:: E_TID_USHORT
.. data:: E_TID_SHORT
.. data:: E_TID_UINT
.. data:: E_TID_INT
.. data:: E_TID_FLOAT
.. data:: E_TID_DOUBLE
.. data:: E_TID_STRING
.. data:: E_TID_SPARE
.. data:: E_TID_TIME


.. index::
   pair: sample; model

Sample Models
~~~~~~~~~~~~~

.. data:: E_SMOD_1OF1
.. data:: E_SMOD_1OF2
.. data:: E_SMOD_2OF2
.. data:: E_SMOD_3TOI
.. data:: E_SMOD_2TOF


.. index::
   pair: scaling; method

Scaling Methods
~~~~~~~~~~~~~~~

.. data:: E_SMID_NON

   No scaling.


.. data:: E_SMID_LIN

   Linear pixel scaling.

   .. index:: linear


.. data:: E_SMID_LOG

   Logarithmic pixel scaling.

   .. index:: logarithmic
