"""
Created on: 22-7-2021 10:22

@author: IvS
"""
import itertools
from pydsol.model.basic_logger import get_module_logger
logger = get_module_logger(__name__)

__all__ = ["Entity", "Vehicle"]

class Entity(object):
    """This class defines a basic entity for a discrete event simulation model."""
    id_iter = itertools.count(1)

    def __init__(self, simulator, t, speed=1.4, **kwargs):
        """

        Parameters
        ----------
        simulator: Simulator object
            simulator of the model.
        speed:
            speed of the entity. Default is 1.4 m/s.
        kwargs:
             kwargs are the keyword arguments that are used to expand the entity class.
             * source_entity: object
                source of which the entity should exit after creation. If keyword is not existing, the entity has no
                source to exit from.
        """
        self.simulator = simulator
        self.time_creations = t
        self.id = next(self.id_iter)
        self.name = "{0} {1}".format(self.__class__.__name__, str(self.id))
        self.speed = speed
        self.kwargs = kwargs


class Vehicle(Entity):
    """This class defines a vehicle in a discrete event simulation model, and is a subclass of Entity. A vehicle is an
    entity of which other entities can be transported. The entities on the vehicle are tracked by a list."""
    def __init__(self, simulator, speed=10, **kwargs):
        """

        Parameters
        ----------
        simulator: Simulator object
            simulator of the model.
        speed:
            speed of the vehicle.
        kwargs:
             kwargs are the keyword arguments that are used to expand the vehicle class.
        """
        super().__init__(simulator, t=simulator.simulator_time, speed=speed, **kwargs)
        self.entities_on_vehicle = []
