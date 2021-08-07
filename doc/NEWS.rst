Change history
==============

PyEPR 1.1.1 (07/08/2021)
------------------------

* Fix a setious issue in sdist generation.


PyEPR 1.1.0 (06/08/2021)
------------------------

* Old Python versions are no longer officially supported.
  Now PyEPR require Python >= 3.5 and Cython_ >= v0.29.
* Introduced the ``pyproject.toml`` file.
* The ``setup.py`` script has been simplified and modernized,
  now it always use setuptools_ and ``setup.cfg``.
* Now the EPR C API is handled using git submodule.
* Fixed potential crash in cases in which the EPR C API fails to open the
  requested product
* Update the test suite to use the public product
  ``ASA_APM_1PNPDE20091007_025628_000000432083_00118_39751_9244.N1``.
  The previously used one is no longer available.
* Continuous Integration moved to GitHub Actions (GHA).
* Fix a leak of resources on Windows platforms.
* The ``print_()`` method of :class:`Field` and :class:`Record` classes has
  been renamed into ``print()``.
  The old ``print_()`` method is now deprecated and will be removed in
  future versions.
* Support for :mod:`pathlib`.
* Enforce type checking.


PyEPR 1.0.1 (07/03/2020)
------------------------

* Fixed a problem in the test using the :data:`epr.Product._fileno`
  (only impacting MacOS-X).
  Also some advice about the correct use of :data:`epr.Product._fileno`
  has been added to the documentation.
* Always close the product object during tests.
  Prevents errors during CI cleanup actions on Windows.


PyEPR 1.0.0 (08/09/2019)
------------------------

* Do not use deprecated numpy_ API (requires Cython_ >= 0.29)
* Minimal numpy_ version is now v1.7
* Set Cython_ 'language_level` explicitly to '3str' if Cython_ >= v0.29,
  to '2' otherwise
* Python v2.6, v3.2, v3.3 and v3.4 are now deprecated.
  Support for the deprecated Python version will be removed in future
  releases of PyEPR


PyEPR 0.9.5 (23/08/2018)
------------------------

* Fix compatibility with numpy_ >= 1.14: :func:`np.fromstring`
  is deprecated
* Update the pypi sidebar in the documentation
* Use `.rst` extension for doc source files
* Fix setup script to not use system libs if epr-api sources are available
* Do not access fields of bands after that the product has been closed
  (fix a segmentation fault on windows)
* `unittest2`_ is now required for Python < 3.4

.. _unittest2: https://pypi.org/project/unittest2


PyEPR 0.9.4 (29/04/2018)
------------------------

* Fix compatibility with Cython_ >= 0.28
* PyEPR has been successfully tested with PyPy_


.. _PyPy: https://www.pypy.org


PyEPR 0.9.3 (02/05/2015)
------------------------

* Fix PyEprExtension class in setup.py (closes :issue:`11`)
* Updated internal EPR API version


PyEPR 0.9.2 (08/03/2015)
------------------------

* Improved string representation of fields in case of :data:`E_TID_STRING`
  data type. Now bytes are decoded and represented as Python strings.
* New tutorial :doc:`gdal_export_example`
* Improved "Installation" and "Testing" sections of the user manual


PyEPR 0.9.1 (27/02/2015)
------------------------

* Fix source distribution (missing EPR API C sources)


PyEPR 0.9 (27/02/2015)
----------------------

* basic support for update mode: products can now be opened in update mode
  ('rb+') and it is possible to call :meth:`epr.Field.set_elem` and
  :meth:`epr.Field.set_elems` methods to set :class:`epr.Field` elements
  changing the contents of the :class:`epr.Product` on disk.
  This feature is not available in the EPR C API.
* new functions/methods and properties:

  - :attr:`epr.Record.index` property: returns the index of the
    :class:`epr.Record` within the :class:`epr.Dataset`
  - :attr:`epr.Band.dataset` property: returns the source
    :class:`epr.Dataset` object containing the raw data used to create
    the :class:`epr.Band`\ ’s pixel values
  - :attr:`epr.Band._field_index` and :attr:`epr.Band._elem_index`
    properties: return the :class:`epr.Field` index (within the
    :class:`epr.Record`) and the element index (within the
    :class:`epr.Field`) containing the raw data used to create the
    :class:`epr.Band`\ ’s pixel values
  - :attr:`epr.Record.dataset_name` property: returns the name of the
    :class:`epr.Dataset` from which the :class:`Record` has bee read
  - :attr:`epr.Record.tot_size` and :attr:`epr.Field.tot_size` properties:
    return the total size in bytes of the :class:`epr.Record` and
    :class:`epr.Field` respectively
  - :func:`epr.get_numpy_dtype` function: retrieves the numpy_ data type
    corresponding to the specified EPR type ID
  - added support for some low level feature: the *_magic* private attribute
    stores the identifier of EPR C stricture, the
    :meth:`epr.Record.get_offset` returns the offset in bytes of the
    :class:`epr.Record` within the file, and the :meth:`epr.Field.get_offset`
    method returns the :clasS:`epr.Field` offset within the
    :class:`epr.Record`

* improved functions/methods:

  - :meth:`epr.Field.get_elems` now also handles :data:`epr.E_TID_STRING` and
    :data:`epr.E_TID_TIME` data types
  - improved :func:`epr.get_data_type_size`, :func:`epr.data_type_id_to_str`,
    :func:`epr.get_scaling_method_name` and :func:`epr.get_sample_model_name`
    functions that are now defined using the cython `cpdef` directive
  - the :meth:`epr.Field.get_elems` method has been re-written to remove
    loops and unnecessary data copy
  - now generator expressions are used to implement `__iter__` special methods

* the *index* parameter of the :meth:`epr.Dataset.read_record` method is
  now optional (defaults to zero)
* the deprecated `__revision__` variable has been removed
* declarations of the EPR C API have been moved to the new :file:`epr.pyd`
* the `const_char` and `const_void` definitions have been dropped,
  no longer necessary with Cython_ >= 0.19
* minimum required version for Cython_ is now 0.19
* the :file:`setup.py` script has been completely rewritten to be more
  "pip_ friendly".  The new script uses setuptools_ if available and
  functions that use numpy_ are evaluated lazily so to give a chance to
  pip_ and setuptools_ to install dependencies, numpy_, before they are
  actually used.
  This should make PyEPR "pip-installable" even on system there numpy_
  is not already installed.
* the :file:`test` directory has been renamed into :file:`tests`
* the test suite now has a :func:`setUpModule` function that automatically
  downloads the ENVISAT test data required for test execution.
  The download only happens if the test dataset is not already available.
* tests can now be run using the :file:`setup.py` script::

    $ python3 setup.py test

* enable continuous integration and testing in for Windows_ using AppVeyor_
  (32bit only)
* status badges for
  `AppVeyor CI <https://ci.appveyor.com/project/avalentino/pyepr>`_ and
  PyPI_ added to the HTML doc index


.. _pip: https://pip.pypa.io
.. _setuptools: https://github.com/pypa/setuptools
.. _numpy: https://numpy.org
.. _Windows: https://windows.microsoft.com
.. _AppVeyor: https://www.appveyor.com
.. _PyPI: https://pypi.org/project/pyepr


PyEPR 0.8.2 (03/08/2014)
------------------------

* fixed segfault caused by incorrect access to :attr:`epr.Dataset.description`
  string in case of closed products
* fixed a memory leak in :class:`epr.Raster` (closes :issue:`10`)
* the size parameters (*src_width* and *src_height*) in
  :meth:`epr.Band.create_compatible_raster` are now optional. By default a
  :class:`epr.Raster` with the same size of the scene is created
* the test suite have been improved
* improved the :doc:`NDVI computation example <ndvi_example>`
* updates sphinx config
* small clarification in the :ref:`installation` section of the
  :doc:`usermanual`.
* EPR C API (version bundled with the official source tar-ball)

  - in case of error always free resources before setting the error code.
    This avoids error shadowing in some cases.
  - fixed a bug that caused reading of the incorrect portion of data in case
    of mirrored annotation datasets (closes :issue:`9`)
  - fixed a bug that caused incorrect data sub-sampling in case of mirrored
    datasets


PyEPR 0.8.1 (07/09/2013)
------------------------

* fixed an important bug in the error checking code introduced in previous
  release (closes :issue:`8`)
* fixed the NDVI example
* no more display link URL in footnotes of the PDF User Manual


PyEPR 0.8 (07/09/2013)
----------------------

* now the :class:`epr.Product` objects have a :meth:`epr.Product.close`
  method that can be used to explicitly close products without relying
  on the garbage collector behaviour (closes :issue:`7`)
* new :attr:`epr.Product.closed` (read-only) attribute that can be used to
  check if a :class:`epr.Product` has been closed
* the :class:`Product` class now supports context management so they can be
  used in ``with`` statements
* added entries for :data:`epr.__version__` and :data:`epr.__revision__` in
  the reference manual
* the :data:`epr.__revision__` module attribute is now deprecated
* some *cythonization* warnings have been fixed
* several small improvements to the documentation


PyEPR 0.7.1 (19/08/2013)
------------------------

* fixed potential issues with conversion from python strings to ``char*``
* new snapshot of the EPR C API sources (2.3dev):

  - the size of the record tables has been fixed
  - the EPR_NUM_PRODUCT_TABLES has been fixed
  - fixed a missing prototype
  - several GCC warnings has been silenced
  - additional checks on return codes
  - now and error is raised when an invalid flag name is used

* better factorization of Python 3 specific code
* use the *CLOUD* flag instead of *BRIGHT* in unit tests
* added function/method signature to all doc-strings for better interactive
  help
* several improvements to the documentation:

  - updated the :file:`README.txt` file to mention EPR C API sourced inclusion
    in the PyEPR 0.7 (and lates) source tar-ball
  - small fix in the installation instructions: the pip_ tool does not have  a
    "--prefix" parameter
  - always use the python3 syntax for the *print* function in all examples in
    the documentation
  - links to older (and dev) versions of the documentation have been added in
    the man page of the HTML doc
  - removed *date* form the doc meta-data.  The documentation build date is
    reported in the front page of the LaTeX (PDF) doc and, starting from this
    release, in the footer of the HTML doc.
  - the Ohloh_ widget has been added in the sidebar of the HTML doc
  - improved the regexp for detecting the SW version in the :file`setup.py`
    script
  - formatting

.. _Ohloh: https://www.openhub.net


PyEPR 0.7 (04/08/2013)
----------------------

* more detailed error messages in case of open failures
* new sphinx theme for the HTML documentation
* `Travis-CI`_ has been set-up for the project
* now the source tar-ball also includes a copy of the EPR C API sources
  so that no external C library is required to build PyEPR.

  This features also makes it easier to install PyEPR using pip_.

  The user can still guild PyEPR against a system version of the ERP-API
  library simply using the `--epr-api-src` option of the
  :file:`setup.py` script with "None"" as value.

  The ERP C API included in the source tar-ball is version *2.3dev-pyepr062*,
  a development and patched version that allows the following enhancements.

  - support for ERS products in ENVISAT format
  - support for ASAR products generated with the new ASAR SW version 6.02
    (ref. doc. PO-RS-MDA-GS-2009_4/C
  - fix incorrect reading of "incident_angle" bands (closes :issue:`6`).
    The issue is in the EPR C API.

.. _`Travis-CI`: https://travis-ci.org/avalentino/pyepr


PyEPR 0.6.1 (26/04/2012)
------------------------

* fix compatibility with Cython_ 0.16
* added a new option to the setup script (`--epr-api-src`) to build
  PyEPR using the EPR-API C sources


PyEPR 0.6 (12/08/2011)
----------------------

* full support for `Python 3`_
* improved code highligh in the documentation
* depend from cython >= 0.13 instead of cython >= 0.14.1.
  Cythonizing :file:`epr.pyx` with `Python 3`_ requires cython >= 0.15


PyEPR 0.5 (25/04/2011)
----------------------

* stop using :c:func:`PyFile_AsFile` that is no more available in
  `Python 3`_
* now documentation uses intersphinx_ capabilities
* code examples added to documentation
* tutorials added to documentation
* the LICENSE.txt file is now included in the source distribution
* the Cython_ construct ``with nogil`` is now used instead of calling
  :c:func:`Py_BEGIN_ALLOW_THREADS` and :c:func:`Py_END_ALLOW_THREADS`
  directly
* dropped old versions of Cython_; now Cython_ 0.14.1 or newer is required
* suppressed several constness related warnings

.. _`Python 3`: https://docs.python.org/3
.. _intersphinx: https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html
.. _Cython: https://cython.org


PyEPR 0.4 (10/04/2011)
----------------------

* fixed a bug in the :meth:`epr.Product.__str__`, :meth:`Dataset.__str__`
  and :meth:`erp.Band.__repr__` methods (bad formatting)
* fixed :meth:`epr.Field.get_elems` method for char and uchar data types
* implemented :meth:`epr.Product.read_bitmask_raster`, now the
  :class:`epr.Product` API is complete
* fixed segfault in :meth:`epr.Field.get_unit` method when the field
  has no unit
* a smaller dataset is now used for unit tests
* a new tutorial section has been added to the user documentation


PyEPR 0.3 (01/04/2011)
----------------------

* version string of the EPR C API is now exposed as module attribute
  :data:`epr.EPR_C_API_VERSION`
* implemented ``__repr__``, ``__str__``, ``__eq__``, ``__ne__`` and
  ``__iter__`` special methods
* added utility methods (not included in the C API) like:

  - :meth:`epr.Record.get_field_names`
  - :meth:`epr.Record.fields`
  - :meth:`epr.Dataset.records`
  - :meth:`epr.Product.get_dataset_names`
  - :meth:`epr.Product.get_band_names`
  - :meth:`epr.Product.datasets`
  - :meth:`epr.Product.bands`

* fixed a logic error that caused empty messages in custom EPR
  exceptions


PyEPR 0.2 (20/03/2011)
----------------------

* sphinx_ documentation added
* added docstrings to all method and classes
* renamed some method and parameter in order to avoid redundancies and
  have a more *pythonic*  API
* in case of null pointers a :exc:`epr.EPRValueError` is raised
* improved C library shutdown management
* introduced some utility methods to :class:`epr.Product` and
  :class:`epr.Record` classes

.. _sphinx: https://www.sphinx-doc.org


PyEPR 0.1 (09/03/2011)
----------------------

Initial release
