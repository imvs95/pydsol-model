""" """
"""
Created on: 5-8-2021 15:10

@author: IvS
"""
import numpy as np
import itertools

from pydsol.model.queue_model import QueueModel
from pydsol.model.resource import Resource
from pydsol.model.entities import Vehicle

from pydsol.model.basic_logger import get_module_logger

logger = get_module_logger(__name__)

__all__ = ["Server"]


class Server(object):
    """This class defines a basic server for a discrete event simulation. It includes input nodes, input queue,
    multiple resource processes (so seize-and-release principle) based on the capacity, and output node. Since each
    resource process in the server has the same characteristics, the capacity is regulated via a dictionary that
    keeps track of the state of each resource."""
    id_iter = itertools.count(1)

    def __init__(self, simulator, capacity=1, distribution=np.random.triangular, processing_time=(0.1, 0.2, 0.3),
                 transfer_in_time=0, **kwargs):
        """

        Parameters
        ----------
        simulator: Simulator object
            simulator of the model.
        capacity: int
            capacity of the server, i.e., the number of objects that can be handled simultaneously.
        distribution:
            distribution for which the processing time is drawn. Default is np.random.triangular.
        processing_time: int or tuple
            time it takes for the resource to process an object. Default is (0.1, 0.2, 0.3).
        transfer_in_time: int
            time it takes to transfer an object into the resource. Default is 0.
        kwargs:
            kwargs are the keyword arguments that are used to expand the server class.
            *name: str
                user-specified name for the server.

        """
        self.simulator = simulator
        self.next = None

        self.id = next(self.id_iter)
        self.name = "{0} {1}".format(self.__class__.__name__, str(self.id))
        if "name" in kwargs:
            self.name = kwargs["name"]

        self.processing_time = processing_time
        self.distribution = distribution

        self.capacity = capacity
        self.transfer_in_time = transfer_in_time
        self.kwargs = kwargs

        # Queue
        self.input_queue = QueueModel(self)
        self.resources = []
        for i in range(1, self.capacity + 1):
            # TODO make distribution and processing time for multiple resources (in list)
            resource = Resource(i, self.simulator, self.input_queue, self.distribution, self.processing_time,
                                self.transfer_in_time, **kwargs)
            resource.server = self

            self.resources.append(resource)

    def enter_input_node(self, entity, **kwargs):
        """Schedules the event to seize the resource when an object (often an entity) enters the input node.
        If the entity is Vehicle, there are entities on the vehicle and therefore, the vehicle will be separated from
        the entity. The individual entities will try to seize a resource (capacity) in the server.

        Parameters
        ----------
        entity: object
            the target on which a state change is scheduled.
        kwargs:
            kwargs are the keyword arguments that are used to expand the function.

        """
        if isinstance(entity, Vehicle):
            vehicle = entity
            for entity in vehicle.entities_on_vehicle:
                logger.info("Time {0:.2f}: {1} loaded off {2}".format(self.simulator.simulator_time, entity.name,
                                                                      vehicle.name))
                self.simulator.schedule_event_now(self, "seize_resource", entity=entity)
                # To reduce number of objects in model
            del vehicle
        else:
            self.simulator.schedule_event_now(self, "seize_resource", entity=entity)


    def seize_resource(self, entity, **kwargs):
        """Process to seize a resource by the entity. If the resource is free and there is no queue, the entity
        can directly seize the resource. If the resource is free and there is a queue, the first entity of the queue
        seizes the resource and this entity is added to the queue. If the resource is occupied, the entity is directly
        added to the queue.

        Parameters
        ----------
        entity: Entity
            the target on which a state change is scheduled.
        kwargs:
            kwargs are the keyword arguments that are used to expand the function.

        """
        not_seized = [resource for resource in self.resources if not resource.resource_seized]

        if len(not_seized) == 0:
            self.input_queue.contents.append(entity)
            logger.debug(
                "Time {0:.2f}: {1} added to the queue".format(self.simulator.simulator_time, entity.name))
        else:
            resource_to_seize = not_seized[0]
            if len(self.input_queue.contents) == 0:
                resource_to_seize.resource_seized = True
                resource_to_seize.processing_entity = entity
                self.simulator.schedule_event_now(resource_to_seize, "exit_input_node")
                logger.debug(
                    "Time {0:.2f}: {1} seized {2}".format(self.simulator.simulator_time, entity.name,
                                                          resource_to_seize.name))
            else:
                resource_to_seize.resource_seized = True
                resource_to_seize.processing_entity = self.input_queue.contents[0]
                self.simulator.schedule_event_now(resource_to_seize, "exit_input_node")
                logger.debug(
                    "Time {0:.2f}: {1} seized {2}".format(self.simulator.simulator_time,
                                                          resource_to_seize.processing_entity.name, resource_to_seize.name))
                self.input_queue.contents.pop(0)
                self.input_queue.contents.append(entity)

    def enter_output_node(self, entity, **kwargs):
        """Combine the entity with a Vehicle if an vehicle type is given. Combined or not, it schedules an event
        for exiting the output node.

        Parameters
        ----------
        entity: Entity
            the target on which a state change is scheduled.
        kwargs:
            kwargs are the keyword arguments that are used to expand the function.
            *vehicle_type: Vehicle class
                subclass of Vehicle on which the entity should travel to the next destination.
            *vehicle_speed: int, optional
                speed of the vehicle.

        """
        # If there is a vehicle
        if "vehicle_type" in self.kwargs:
            if "vehicle_speed" in self.kwargs:
                vehicle = self.kwargs["vehicle_type"](self.simulator, vehicle_speed=self.kwargs["vehicle_speed"])
            else:
                vehicle = self.kwargs["vehicle_type"](self.simulator)
            vehicle.entities_on_vehicle.append(entity)
            logger.info("Time {0:.2f}: {1} loaded on {2}".format(self.simulator.simulator_time, entity.name,
                                                                 vehicle.name))
            entity = vehicle

        self.simulator.schedule_event_now(self, "exit_output_node", entity=entity)

    def exit_output_node(self, entity, **kwargs):
        """Exit the resource by selecting a link on which the entity should travel to the next destination by
        weighted choice.

        Parameters
        ----------
        entity: Entity
            the target on which a state change is scheduled.
        kwargs:
            kwargs are the keyword arguments that are used to expand the function.

        """
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
