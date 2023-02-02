==============================
Advanced Examples
==============================

This is a step-by-step tutorial on how to develop a advanced discrete event simulation model using pydsol-model.
Example can be found at ``./examples/advanced_example.py``.

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Step-by-Step Tutorial
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Simulation model in km/days.


Import the following statements. Set logger level to DEBUG to inspect the entities
and model objects. For experiments, the advice is to set logger level to INFO.
::
    import copy
    import numpy as np
    import itertools
    import statistics
    import time

    from pydsol.core.experiment import SingleReplication
    from pydsol.core.model import DSOLModel
    from pydsol.core.simulator import DEVSSimulatorFloat

    from pydsol.model.entities import Entity, Vehicle
    from pydsol.model.source import Source
    from pydsol.model.server import Server
    from pydsol.model.sink import Sink
    from pydsol.model.link import Link

    import logging
    from pydsol.model.basic_logger import get_module_logger

    logger = get_module_logger(__name__, level=logging.DEBUG)

We start with creating the item of interest for this simulation, i.e., entity.
For this model, we are interested in batches of shoes - a fashion item that is regularly used
and distributed internationally. Thus, we create an child of the type ``Entity`` called ShoeBatch.
A shoe batch has the attribute *quantity*, meaning the amount of shoes that are in that batch. Also,
we want to keep track of the amount of time this batch spend in the system using the attribute
*time_in_system*.
::
    class ShoeBatch(Entity):
        def __init__(self, simulator, t, **kwargs):
            super().__init__(simulator, t, **kwargs)

            self.quantity = round(np.random.uniform(100, 150), 0)
            self.start_time = self.simulator.simulator_time
            self.time_in_system = 0

        def __repr__(self):
            return self.name

This shoe batch is transported from origin to destination over land using a truck.
::
    class Truck(Vehicle):
    def __init__(self, simulator, **kwargs):
        self.speed = np.random.triangular(0, 100, 120) * 24  # km/h to day
        if "vehicle_speed" in kwargs:
            self.speed = np.random.triangular(0, kwargs["vehicle_speed"], 120) * 24
        super().__init__(simulator, self.speed, **kwargs)

        self.interarrival_distribution = np.random.triangular
        self.interarrival_times = (0, 0.2, 0.5)

This shoe batch is transported from origin to destination over sea using a container ship.
::
    class ContainerShip(Vehicle):
    def __init__(self, simulator, **kwargs):
        # km/h to knots, and one knot is one nautical mile per hour
        self.speed = np.random.triangular(10 * 1.85, 18 * 1.85, 25 * 1.85)
        if "vehicle_speed" in kwargs:
            self.speed = np.random.triangular(10 * 1.85, kwargs["vehicle_speed"], 25 * 1.85)
        super().__init__(simulator, self.speed, **kwargs)

        self.interarrival_distribution = np.random.triangular
        self.interarrival_times = (0, 5, 14)

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Extensions
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

* Hourly statistics using a Timer
* Extensions using networkx to create a graph and automatically create a simulation model
