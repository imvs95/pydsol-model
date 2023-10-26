pydsol-model : Python Distributed Simulation Object Library with Predefined Model Objects
==========================================================================================================

``pydsol-model`` is a package that includes standard model objects suitable for developing a discrete event simulation model. Standard model objects are source, server using resources, sink, node, link, entity and vehicle. This makes it easy and fast to design discrete event simulation models using queueing theory, useful for teaching, academic research, and commercial use. You can use the standard model objects as is, or use it to make your own objects for more complex simulation models. 

**pydsol-model** is an additional layer on top of ``pydsol-core``, a Python distribution discrete event simulation library. pydsol-core uses a heap queue (priority queue) as eventlist and plans events using a relative delay instead of yield, making it much faster than most discrete event simulation packages implemented in Python. Note that you need pydsol-core (https://github.com/averbraeck/pydsol-core) to use **pydsol-model**.

This repository is currently under development at Delft University of Technology. If you would like to collaborate, please open an issue/discussion or contact `Isabelle van Schilt <https://www.tudelft.nl/staff/i.m.vanschilt/?cHash=74e749835b2a89c6c76b804683ffbbcf>`_ or `Alexander Verbraeck <https://www.tudelft.nl/staff/a.verbraeck/?cHash=79d864d800b2d588772fbe7e1778ff03>`_.

Documentation
=====================================================
Documentation for pydsol-model is available at `Read the Docs <https://pydsol-model.readthedocs.io/en/latest/index.html>`_. This includes the description of the theory behind each model object, and a step-by-step explanation of a basic and more advanced example. 


Installation and set-up
=====================================================

``pydsol-model`` is available using pip install.::

    pip install pydsol-model


For the latest version, please use the URL::

    pip install git+https://github.com/imvs95/pydsol-model.git


For setting up pydsol-model and ensuring that the example models can run, ``pydsol-core`` also needs to be installed. This is part of the ``requirements.txt``.
If you want to install it manually, use::

    pip install pydsol-core

The source code of that library can be found at https://github.com/averbraeck/pydsol-core.

License
=====================================================
This repository is licensed under BSD 3-Clause License. See ``LICENSE``.
