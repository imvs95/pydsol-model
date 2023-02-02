""" """
"""
Created on: 23-7-2021 16:00

@author: IvS
"""
import math
import numpy as np
import itertools

from pydsol.model.basic_logger import get_module_logger
from pydsol.model.entities import Entity

logger = get_module_logger(__name__)

__all__ = ["Node"]


class Node(object):
    """This class defines a basic node for travelling in a discrete event simulation model. Input and output links
    are assigned by the link."""
    id_iter = itertools.count(1)

    def __init__(self, simulator, capacity=math.inf, **kwargs):
        """

        Parameters
        ----------
        simulator: Simulator object
            simulator of the model.
        capacity: int
            number of travellers that are simultaneously allowed on the node. Default is infinity.
        kwargs:
            kwargs are the keyword arguments that are used to expand the node class.
            *name: str
                user-specified name for the node.
        """
        self.simulator = simulator
        self.capacity = capacity

        self.next = None

        self.id = next(self.id_iter)
        self.name = "{0} {1}".format(self.__class__.__name__, str(self.id))
        if "name" in kwargs:
            self.name = kwargs["name"]
        self.kwargs = kwargs

    def enter_input_node(self, entity: Entity, **kwargs):
        self.simulator.schedule_event_now(self, "exit_output_node", entity=entity)

    def exit_output_node(self, entity: Entity, **kwargs):
        """Exit the resource by selecting a link on which the entity should travel to the next destination by
        weighted choice.

        Parameters
        ----------
        entity: Entity
            the target on which a state change is scheduled.
        kwargs:
            kwargs are the keyword arguments that are used to expand the function.

        """
        # If there is a vehicle
        if "vehicle_type" in self.kwargs:
            if "vehicle_speed" in self.kwargs:
                vehicle = self.kwargs["vehicle_type"](self.simulator, vehicle_speed=self.kwargs["vehicle_speed"])
            else:
                vehicle = self.kwargs["vehicle_type"](self.simulator)
            vehicle.entities_on_vehicle.append(entity)
            logger.info("Time {0:.2f}: {1} loaded on {2} at {3}".format(self.simulator.simulator_time, entity.name,
                                                                        vehicle.name, self.name))
            entity = vehicle

        try:
            # Selection based on weights in links
            next_list = self.next if isinstance(self.next, list) else [self.next]
            weights = [link.selection_weight for link in next_list]
            link_by_weight = np.random.choice(np.array(next_list), p=weights / np.sum(weights))
            link_by_weight.enter_input_node(entity)
        except AttributeError:
            try:
                if len(next_list) > 1:
                    next_process = np.random.choice(np.array(next_list))
                    next_process.enter_input_node(entity)
                if len(next_list) == 1:
                    self.next.enter_input_node(entity)
            except AttributeError:
                raise AttributeError("{0} has no next process assigned".format(self.name))
