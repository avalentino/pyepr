======================================================
PyEPR - Python bindings for ENVISAT Product Reader API
======================================================

:Home Page: https://github.com/avalentino/pyepr
:Author:    Antonio Valentino
:Contact:   antonio.valentino@tiscali.it
:Date:      05/03/2011
:Copyright: 2011, Antonio Valentino <antonio.valentino@tiscali.it>
:Version:   0.1

.. contents::


Introduction
============

PyEPR_ provides Python_ bindings for the ENVISAT Product Reader C API
(`EPR API`_) for reading satellite data from ENVISAT_ ESA_ (European
Space Agency) mission.

PyEPR_, as well as the `EPR API`_ for C, supports ENVISAT_ MERIS, AATSR
Level 1B and Level 2 and also ASAR data products. It provides access to
the data either on a geophysical (decoded, ready-to-use pixel samples)
or on a raw data layer. The raw data access makes it possible to read
any data field contained in a product file.

.. _PyEPR: https://github.com/avalentino/pyepr
.. _Python: http://www.python.org
.. _`EPR API`: https://github.com/bcdev/epr-api
.. _ENVISAT: http://envisat.esa.int
.. _ESA: http://earth.esa.int


Requirements
============

In order to use PyEPR it is needed that the following software are
correctly installed and configured:

* Python_ >= 2.6
* numpy_ >= 1.3.0
* `EPR API`_ >= 2.2
* Cython_ >= 0.12.1 (build only)
* a reasonably updated C compiler [#]_ (build only)

.. [#] PyEPR_ has been developed and tested with gcc_ 4.

.. _numpy: http://www.numpy.org
.. _Cython: http://cython.org
.. _gcc: http://gcc.gnu.org


Download
========

Source code is available at

    https://github.com/avalentino/pyepr

To clone the git_ repository the following command can be used::

    $ git clone https://github.com/avalentino/pyepr.git

.. _git: http://git-scm.com


Installation
============

PyEPR_ uses the standard Python_ distutils_ so it can be installed using
the following command::

    $ python setup.py install

For a user specific installation use::

    $ python setup.py install --user

To install PyEPR_ in a non-standard path::

    $ python setup.py install --prefix=<TARGET_PATH>

just make sure that ``<TARGET_PATH>/lib/pythonX.Y/site-packages`` is in
the ``PYTHONPATH``.

.. todo: installation with easy_install

.. _distutils: http://docs.python.org/distutils


Testing
=======

PyEPR_ package comes with a complete test suite but in order to run it
the ENVISAT sample product used for testing
ASA_IMP_1PNUPA20060202_062233_000000152044_00435_20529_3110.N1__
have to be downloaded from the ESA_ website, saved in the ``tests``
directory and decompressed.

__ http://earth.esa.int/services/sample_products/asar/IMP/ASA_IMP_1PNUPA20060202_062233_000000152044_00435_20529_3110.N1.gz

On GNU Linux platforms the following shell commands can be used::

    $ cd pyepr-0.x/tests
    $ wget http://earth.esa.int/services/sample_products/asar/IMP/ASA_IMP_1PNUPA20060202_062233_000000152044_00435_20529_3110.N1.gz
    $ guinzip ASA_IMP_1PNUPA20060202_062233_000000152044_00435_20529_3110.N1

After installation the test suite can be run using the following command
in the ``tests`` directory::

    $ python test_all.py


Python vs C EPR API
===================

The Python_ EPR API is fully object oriented.
The main structures of the C API have been implemented as objects while
C function have been logically grouped and mapped onto object methods.

The entire process of defining an object oriented API for Python_ has
been quite easy and straightforward thanks to the good design of the C
API,

Of course there are also some differences.


Memory management
-----------------

Being Python_ a very high level language uses have never to worry about
memory allocation/deallocation. They simply have to instantiate objects::

    product = epr.Product('filename.N1')

and use them freely.

Objects are automatically destroyed when there are no more references to
them and memory is deallocated automatically.

Even better, each object holds a reference to other objects it depends
on so the user never have to worry about identifiers validity or about
the correct order structures have to be feed.

For example: the C `EPR_DatasetId` structure has a field (`product_id`)
that points to the *product* descriptor `EPR_productId` to which it
belongs to.

The reference to the parent product is used, for example, when one wants
to read a record using the `epr_read_record` function::

    EPR_SRecord* epr_read_record(EPR_SDatasetId* dataset_id, ...);

The function takes a `EPR_SDatasetId` as a parameter and assumes all
fields (including `dataset->product_id`) are valid.
It is responsibility of the programmer tho keep all structures valid and
free them at the right moment and in the correct order.

This is the standard way to go in C but not in Python_.

In Python_ all is by far simpler, and the user can get a *dateset*
object instance::

    dataset = product.get_dataset('MAIN_PROCESSING_PARAMS_ADS')

and then forget about the *product* instance it depends on.
Even if the *product* variable goes out of scope and is no more directly
accessible in the program the *dataset* object keeps staying valid since
it holds an internal reference to the *product* instance it depends on.

When *record* is destroyed automatically also the parent *Product*
object is destroyed (assumed there is no other reference to it).

The entire machinery is completely automatic and transparent to the user.


Arrays
------

PyEPR_ uses numpy_ in order to manage efficiently the potentially large
amount of data contained in ENVISAT_ products.

* `Field.get_field_elems()` return an 1D array containing elements of the
  field
* the `Raster.data` property is a 2D array exposes data contained in the
  *Raster* object in form of `numpy.ndarray`
  
  .. note:: `Raster.data` directly exposes *Raster* data i.e. shares the
            same memory buffer with *Raster*::
                
                >>> raster.get_pixel(i, j)
                5
                >>> raster.data[i, j]
                5
                >>> raster.data[i, j] = 3
                >>> raster.get_pixel(i, j)
                3
                
* Band.read_as_array(...) is an additional method provided by the Python
  EPR API (does not exist any correspondent function in the C API).
  It is mainly a facility method that allows users to get access to band
  data without creating an intermediate *Raster* object.
  It read a slice of data from the *Band* and returns it as a 2D
  `numpy.ndarray`.


Enumerators
-----------

Python_ does not have *enumerators* at language level.
Enumerations are simply mapped as module constants that have the same name
of the C enumerate but are spelled all in capital letters.

For example:

============ ============
    C           Pythn
============ ============
e_tid_double E_TID_DOUBLE
e_smod_1OF1  E_SMOD_1OF1
e_smid_log   E_SMID_LOG
============ ============


Error handling and logging
--------------------------


Currently error handling and logging functions of the EPR C API are not
exposed to python.

Internal library logging is completely silenced and errors are converted
to Python_ exceptions.
Where appropriate standard Python_ exception types are use in other cases
custom exception types (e.g. *EPRError*, *EPRValueError*) are used.


Library initialization
----------------------

Differently from the C API library initialization is not needed: it is
performed internally the first time the *epr* module is imported in
Python_.


How to use PyEPR
================

Full access to the Python EPR API is provided by the ``epr`` module that
have to be imported by the client program e-g- as follows::

    import epr

The following snippet open an ASAR product and dumps the "Main Processing
Parameters" record to the standard output::

    import epr

    product = epr.Product('ASA_IMP_1PNUPA20060202_062233_000000152044_00435_20529_3110.N1')
    dataset = product.get_dataset('MAIN_PROCESSING_PARAMS_ADS')
    record = dataset.read_record(0)
    record.print_record()


License
=======

Copyright (C) 2011 Antonio Valentino <antonio.valentino@tiscali.it>

PyEPR is free software: you can redistribute it and/or modify
it under the terms of the `GNU General Public License`_ as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PyEPR is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with PyEPR.  If not, see <http://www.gnu.org/licenses/>.

.. _`GNU General Public License`: http://www.gnu.org/licenses/gpl-3.0.html

