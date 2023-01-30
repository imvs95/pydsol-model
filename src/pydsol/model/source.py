"""
Created on: 22-7-2021 10:19

@author: IvS
"""
import numpy as np
import itertools

from pydsol.model.entities import Entity
from pydsol.model.basic_logger import get_module_logger

logger = get_module_logger(__name__)


class Source(object):
    """This class defines a basic source for a discrete event simulation model. A Source is the start-station
    of each entity, meaning the entities enter the system via the source. Entities are created at a source,
    given a specific interarrival time."""
    id_iter = itertools.count(1)

    def __init__(self, simulator, interarrival_time="default", num_entities=1, entity_type=Entity, **kwargs):
        """

        Parameters
        ----------
        simulator: Simulator object
            simulator of the model.
        interarrival_time:
            time between the creation of entities. Default is np.random.exponential(0.25).
        num_entities: int
            number of entities to create at once. Default is 1.
        kwargs:
            kwargs are the keyword arguments that are used to expand the source class.
            *name: str
                user-specified source for the link
        """
        self.simulator = simulator
        self.num_entities = num_entities
        self.entity_type = entity_type

        self.next = None  # this should be the next process

        self.id = next(self.id_iter)
        self.name = "{0} {1}".format(self.__class__.__name__, str(self.id))
        if "name" in kwargs:
            self.name = kwargs["name"]

        self.interarrival_time = interarrival_time
        if "distribution" in kwargs:
            self.distribution = kwargs["distribution"]

        self.kwargs = kwargs

        self.simulator.schedule_event_now(self, "create_entities")

    def create_entities(self, **kwargs):
        """
        Create entities via SimEvent, given the interarrival time and the number of entities.

        Parameters
        ----------
        entity_type: class
            class where to make instances of, for example class Entity
        kwargs:
            kwargs are the keyword arguments that are used to invoke the method or expand the function.

        """

        # To make it work with the set seed of the simulator
        if self.interarrival_time == "default":
            self.interarrival_time = np.random.exponential(0.25)

        # Create new entity
        for _ in range(self.num_entities):
            entity = self.entity_type(self.simulator, self.simulator.simulator_time, **kwargs)
            logger.info("Time {0:.2f}: {1} is created at {2}".format(self.simulator.simulator_time, entity.name,
                                                                      self.name))
            self.exit_source(entity)

        if "distribution" in self.__dict__:
            try:
                interarrival_time = self.distribution(*self.interarrival_time)
            except TypeError:
                try:
                    interarrival_time = self.distribution(self.interarrival_time)
                except TypeError:
                    raise "Wrong types for transfer in time ({1}) and/or distribution ({0}) for scheduling an event".format(
                        self.interarrival_time, self.distribution)
        else:
            interarrival_time = self.interarrival_time

        relative_delay = interarrival_time

        # Schedule event to create next entity according to the interarrival time
        self.simulator.schedule_event_rel(relative_delay, self, "create_entities")

    def exit_source(self, entity, **kwargs):
        """Schedules the event to exit the source and enter the output node.

        Parameters
        ----------
        entity: object
            the target on which a state change is scheduled.
        kwargs:
            kwargs are the keyword arguments that are used to expand the function.

        """
        self.simulator.schedule_event_now(self, "enter_output_node", entity=entity)

    def enter_output_node(self, entity, **kwargs):
        """Combine the entity with a Vehicle if an vehicle type is given. Combined or not, it schedules an event
        for exiting the output node.

        Parameters
        ----------
        entity: object
            the target on which a state change is scheduled.
        kwargs:
            kwargs are the keyword arguments that are used to expand the function.
            *vehicle_type: Vehicle class
                subclass of Vehicle on which the entity should travel to the next destination.
            *vehicle_speed: int, optional
                speed of the vehicle.

        """
        if "vehicle_type" in self.kwargs:
            if "vehicle_speed" in self.kwargs:
                vehicle = self.kwargs["vehicle_type"](self.simulator, self.kwargs["vehicle_speed"])
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
        entity: object
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
