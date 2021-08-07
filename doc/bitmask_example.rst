Exporting bitmasks
-------------------

.. index:: bitmask, ENVISAT

This tutorial shows how to generate bit masks from ENVISAT_ flags information
as "raw" image using PyEPR_.

The example code (:download:`examples/write_bitmask.py`) is a direct
translation of the C sample program `write_bitmask.c`_ bundled with the
EPR API distribution.

The program is invoked as follows:

.. code-block:: sh

    $ python write_bitmask.py <envisat-product> <bitmask-expression> \
    <output-file>

.. _ENVISAT: https://envisat.esa.int
.. _PyEPR: https://github.com/avalentino/pyepr
.. _`write_bitmask.c`: https://github.com/bcdev/epr-api/blob/master/src/examples/write_bitmask.c

The :download:`examples/write_bitmask.py` code consists in a single function
that also includes command line arguments handling:

.. raw:: latex

    \fvset{fontsize=\footnotesize}

.. literalinclude:: examples/write_bitmask.py
   :language: python

.. index:: EPR-API, module
   pair: epr; module

In order to use the Python_ EPR API the :mod:`epr` module is imported:

.. raw:: latex

    \fvset{fontsize=\footnotesize}

.. literalinclude:: examples/write_bitmask.py
   :lines: 25

.. index:: product, open
   pair: with; statement

As usual the ENVISAT_ product is opened using the :func:`epr.open` function
that returns an :class:`epr.Product` instance.
In this case the :func:`epr.open` is used together with a ``with`` statement
so that the :class:`epr.Product` instance is closed automatically when the
program exits the ``with`` block.

.. raw:: latex

    \fvset{fontsize=\footnotesize}

.. literalinclude:: examples/write_bitmask.py
   :language: python
   :lines: 49-50

.. index:: product

Scene size parameters are retrieved form the :class:`epr.Product` object
using the :meth:`epr.Product.get_scene_width` and
:meth:`epr.Product.get_scene_height` methods:

.. raw:: latex

    \fvset{fontsize=\footnotesize}

.. literalinclude:: examples/write_bitmask.py
   :language: python
   :lines: 53-54

The EPR API allows to manage data by means of :class:`epr.Raster` objects, so
the function :func:`epr.create_bitmask_raster`, specific for bitmasks, is used
to create a :class:`epr.Raster` instance.

.. seealso:: :func:`epr.create_raster`

Data are actually read using the :meth:`epr.Product.read_bitmask_raster`
method of the :class:`epr.Product` class:

.. raw:: latex

    \fvset{fontsize=\footnotesize}

.. literalinclude:: examples/write_bitmask.py
   :language: python
   :lines: 61

The :meth:`epr.Product.read_bitmask_raster` method receives in input the
*bm_expr* parameter that is set via command line:

.. raw:: latex

    \fvset{fontsize=\footnotesize}

.. literalinclude:: examples/write_bitmask.py
   :language: python
   :lines: 46

*bm_expr* is a string that define the logical expression for the definition
of the bit-mask. In a bit-mask expression, any number of the flag-names
(found in the DDDB) can be composed with “(”, ”)”, “NOT”, “AND”, “OR”.

.. index:: AND, OR, NOT, DDDB

Valid bit-mask expression are for example::

    flags.LAND OR flags.CLOUD

or::

    NOT flags.WATER AND flags.TURBID_S

Finally data are written to disk as a flat binary file using the
:meth:`numpy.ndarray.tofile` method of the :data:`epr.Raster.data` attribute
of the :class:`epr.Raster` objects that exposes data via the
:class:`numpy.ndarray` interface:

.. raw:: latex

    \fvset{fontsize=\footnotesize}

.. literalinclude:: examples/write_bitmask.py
   :language: python
   :lines: 63-64


.. _Python: https://www.python.org
.. _ENVISAT: https://envisat.esa.int


.. raw:: latex

   \clearpage
