"""
Created on: 22-7-2021 10:20

@author: IvS
"""
import itertools
import logging

from node import Node

from basic_logger import get_module_logger
logger = get_module_logger(__name__)


class Sink(object):
    """This class defines a sink for a discrete event simulation model. A Sink is the end-station of an entity,
    meaning the system will end here for the entity. The entity will be destroyed to reduce the number
    of objects in the model."""
    id_iter = itertools.count(1)

    def __init__(self, simulator, transfer_in_time=0, **kwargs):
        """

        Parameters
        ----------
        simulator: Simulator object
            simulator of the model.
        transfer_in_time: [float, int]
            time it takes to transfer an object into the sink. Default is 0.
        kwargs:
            kwargs are the keyword arguments that are used to expand the sink class.
            *name: str
                user-specified name for the sink.
        """
        self.simulator = simulator
        self.transfer_in_time = transfer_in_time
        if "distribution" in kwargs:
            self.distribution = kwargs["distribution"]

        self.id = next(self.id_iter)
        self.name = "{0} {1}".format(self.__class__.__name__, str(self.id))
        if "name" in kwargs:
            self.name = kwargs["name"]

        self.kwargs = kwargs

        self.processing_entity = None

    def enter_input_node(self, entity):
        """Schedules the event to transfer into the sink and exit the input node.

        Parameters
        ----------
        entity: object
            the target on which a state change is scheduled.

        """
        self.processing_entity = entity

        transfer_in_time_dist = self.distribution(
            self.transfer_in_time) if "distribution" in self.__dict__ else self.transfer_in_time

        self.simulator.schedule_event_rel(transfer_in_time_dist, self, "exit_input_node")

    def exit_input_node(self):
        """Schedules the event to exit the input node and to destroy the entity.

        Parameters
        ----------
        entity: object
            the target on which a state change is scheduled.

        """
        self.simulator.schedule_event_now(self, "destroy_entity")

    def destroy_entity(self):
        """Destroys the entity.

        Parameters
        ----------
        entity: object
            the target on which a state change is scheduled.

        """
        logger.info("Time {0:.2f}: {1} is destroyed".format(self.simulator.simulator_time, self.processing_entity.name))
        # To reduce number of objects in model
        del self.processing_entity
