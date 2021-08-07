Update :class:`Field` elements
------------------------------

.. highlight:: ipython

.. index:: update, field, read-only, EPR-API, MERIS
   pair: open; mode

The EPR C API has been designed to provide read-only features.

PyEPR_ provides and extra capability consisting in the possibility to
modify (*update*) an existing ENVISAT_ :class:`Product`.

Lets consider a MERIS Level 2 low resolution product (
`MER_LRC_2PTGMV20000620_104318_00000104X000_00000_00000_0001.N1`).
It has a :class:`Band` named `water_vapour` containing the water vapour
content at a specific position.

One can load water vapour and compute an histogram using the following
instructions:

.. raw:: latex

    \fvset{fontsize=\footnotesize}

.. literalinclude:: examples/update_elements.py
   :language: python
   :lines: 8-13

.. index:: matplotlib

The resulting histogram can be plot using Matplotlib_:

.. raw:: latex

    \fvset{fontsize=\footnotesize}

.. literalinclude:: examples/update_elements.py
   :language: python
   :lines: 15-19

.. figure:: images/water_vapour_histogram_01.*
   :width: 60%

   Histogram of the original water vapour content

The actual values of the water vapour content :class:`Band` are computed
starting form data stored in the `Vapour_Content` :class:`Dataset` using
scaling factors contained in the `Scaling_Factor_GADS` :class:`Dataset`.
In particular :class:`Field`\ s `sf_wvapour` and  `off_wvapour` are used::

    In [21]: dataset = product.get_dataset('Scaling_Factor_GADS')

    In [22]: print(dataset)
    epr.Dataset(Scaling_Factor_GADS) 1 records

    sf_cl_opt_thick = 1.000000
    sf_cloud_top_press = 4.027559
    sf_wvapour = 0.100000
    off_cl_opt_thick = -1.000000
    off_cloud_top_press = -4.027559
    off_wvapour = -0.100000
    spare_1 = <<unknown data type>>

.. index:: band
   pair: scaling; factor

Now suppose that for some reason one needs to update the `sf_wvapour` scaling
factor for the water vapour content.
Changing the scaling factor, of course, will change all values in the
`water_vapour` :class:`Band`.

The change can be performed using the :meth:`Field.set_elem` and
:meth:`Field.set_elems` methods of :class:`Field` objects:

.. raw:: latex

    \fvset{fontsize=\footnotesize}

.. literalinclude:: examples/update_elements.py
   :language: python
   :lines: 22-30

Now the `sf_wvapour` scaling factor has been changed and it is possible to
compute and display the histogram of modified data in the `water_vapour`
:class:`Band`:

.. raw:: latex

    \fvset{fontsize=\footnotesize}

.. literalinclude:: examples/update_elements.py
   :language: python
   :lines: 32-46

.. figure:: images/water_vapour_histogram_02.*
   :width: 60%

   Histogram of the water vapour content (original and modified)

Figure above shows the two different histograms, original data in blue and
modified data in red, demonstrating the effect of the change of the scaling
factor.

The new map of water vapour is showed in the following picture:

.. figure:: images/modified_water_vapour.*

   Modified water vapour content map

.. important::

   it is important to stress that it is necessary to close and re-open the
   :class:`Product` in order to see changes in the scaling factors applied
   to the `water_vapour`:class:`Band` data.

   This is a limitation of the current implementation that could be removed
   in future versions of the PyEPR_ package.

It has been showed that changing the `sf_wvapour` scaling factor modifies
all values of the `water_vapour` :class:`Band`.

Now suppose that one needs to modify only a specific area.
It can be done changing the contents of the `Vapour_Content` :class:`Dataset`.

The :class:`Dataset` size can be read form the :class:`Product`::

    In [44]: product.get_scene_height(), product.get_scene_width()
    Out[44]: (149, 281)

while information about the fields in each record can be retrieved
introspecting the :class:`Record` object::

    In [49]: record = dataset.read_record(0)

    In [50]: record.get_field_names()
    Out[50]: ['dsr_time', 'quality_flag', 'wvapour_cont_pix']

    In [51]: record.get_field('wvapour_cont_pix')
    Out[51]: epr.Field("wvapour_cont_pix") 281 uchar elements

So the name of the :class:`Field` we need to change is the `wvapour_cont_pix`,
and its index is `2`.

It is possible to change a small box inside the :class:`Dataset` as follows:

.. raw:: latex

    \fvset{fontsize=\footnotesize}

.. literalinclude:: examples/update_elements.py
   :language: python
   :lines: 58-66

Please note that when one modifies the content of a :class:`Dataset` he/she
should also take into account id the corresponding band has lines mirrored
or not::

    In [59]: band = p.get_band('water_vapour')

    In [60]: band.lines_mirrored
    Out[60]: True

Finally the :class:`Product` can be re-opened to load and display the
modified :class:`Band`:

.. raw:: latex

    \fvset{fontsize=\footnotesize}

.. literalinclude:: examples/update_elements.py
   :language: python
   :lines: 69-80

.. figure:: images/modified_water_vapour_with_box.*

   Modified water vapour content map with zeroed box

Of course values in the box that has been set to zero in the :class:`Dataset`
are transformed according to the scaling factor and offset parameters
associated to `water_vapour` :class:`Band`.

The complete code of the example can be found at
:download:`examples/update_elements.py`.


.. _PyEPR: https://github.com/avalentino/pyepr
.. _ENVISAT: https://envisat.esa.int
.. _Matplotlib: https://matplotlib.org


.. raw:: latex

   \clearpage
