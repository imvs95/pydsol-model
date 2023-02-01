.. pydsol-model documentation master file, created by
   sphinx-quickstart on Wed Feb  1 10:55:58 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pydsol-model documentation
========================================

**pydsol-model** is a package that includes standard model objects suitable for developing a discrete event simulation model. Standard model objects are source, server using resources, sink, node, link, entity and vehicle. This makes it easy and fast to design discrete event simulation models using queueing theory, useful for teaching, academic research, and commerical use. You can use the standard model objects as is, or use it to make your own objects for more complex simulation models.

**pydsol-model** is an additional layer on top of pydsol-core, a Python distribution discrete event simulation library. pydsol-core uses a heap queue (priority queue) as eventlist and plans events using a relative delay instead of yield, making it much faster than most discrete event simulation packages implemented in Python. Note that you need pydsol-core (https://github.com/averbraeck/pydsol-core) to use **pydsol-model**.

This repository is currently under development at Delft University of Technology. If you would like to collaborate, please open an issue/discussion or contact `Isabelle van Schilt <https://www.tudelft.nl/staff/i.m.vanschilt/?cHash=74e749835b2a89c6c76b804683ffbbcf>`_ or `Alexander Verbraeck <https://www.tudelft.nl/staff/a.verbraeck/?cHash=79d864d800b2d588772fbe7e1778ff03>`_.


Source code is available at https://github.com/imvs95/pydsol-model.

.. toctree::
   :maxdepth: 1
   :caption: Getting Started:

   ./overview.rst
   ./installation.rst

.. toctree::
   :maxdepth: 1
   :caption: Examples:

   ./basic_example.rst
   ./complex_example.rst

.. toctree::
   :maxdepth: 2
   :caption: Documentation of Code:

    ./modules.rst



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
