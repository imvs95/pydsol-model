""" """
"""
Created on: 9-8-2021 17:02

@author: IvS
"""
import itertools

from pydsol.model.basic_logger import get_module_logger
from pydsol.model.entities import Entity

logger = get_module_logger(__name__)

__all__ = ["Resource"]


class Resource(object):
    """This class defines a basic resource for a discrete event simulation. An object (often an entity) can seize
    a resource. If the resource is seized, other objects cannot seize it anymore until it is released after the
    processing time. The remaining objects are put into a queue."""
    id_iter = itertools.count(1)

    def __init__(self, id, simulator, queue, distribution, processing_time, transfer_in_time, **kwargs):
        """

        Parameters
        ----------
        simulator: Simulator object
            simulator of the model.
        queue: Queue object
            queue where the remaining objects are places when the resource is seized.
        distribution:
            distribution from which the processing time is drawn
        processing_time: Union[int, str]
            time it takes for the resource to process an object. Default is np.random.triangular(0.1, 0.2, 0.3).
        transfer_in_time: int
            time it takes to transfer an object into the resource. Default is 0.
        kwargs:
            kwargs are the keyword arguments that are used to expand the resource class.
            *name: str
                user-specified name for the resource.

        """
        self.simulator = simulator

        self.id = id
        self.name = "{0} {1}".format(self.__class__.__name__, str(self.id))

        self.distribution = distribution
        self.processing_time = processing_time
        self.transfer_in_time = transfer_in_time
        self.kwargs = kwargs

        self.server = object

        # Create queue
        self.input_queue = queue

        self.resource_seized = False

        self.processing_entity = None

    def exit_input_node(self):
        """Schedules the event to enter the resource when the input node is exited. To ensure that the right
                resource is called, the resource key is given.

                Parameters
                ----------
                entity: Entity
                    the target on which a state change is scheduled.
                """
        logger.debug(
            "Time {0:.2f}: {1} seized {2}".format(self.simulator.simulator_time, self.processing_entity.name, self.name))

        self.simulator.schedule_event_now(self, "enter_resource")

    def enter_resource(self):
        """Schedules the event to transfer into the resource and starts processing.

        Parameters
        ----------
        entity: object
            the target on which a state change is scheduled.
        """
        self.simulator.schedule_event_rel(self.transfer_in_time, self, "processing")

    def processing(self, **kwargs):
        """Schedules the event to process the entity and exit the resource.

        Parameters
        ----------
        entity: object
            the target on which a state change is scheduled.
        kwargs:
            kwargs are the keyword arguments that are used to expand the function.

        """
        processing_time_dist = self.set_processing_time()

        if "processing_entity" in kwargs:
            self.processing_entity = kwargs["processing_entity"]

        self.simulator.schedule_event_rel(processing_time_dist, self, "exit_resource", **kwargs)

    def set_processing_time(self):
        """Draws a processing time from the distribution and parameter processing time.
        """
        if (self.distribution is None) & (isinstance(self.processing_time, (int, float))):
            processing_time_dist = self.processing_time
        elif isinstance(self.processing_time, (int, float)):
            processing_time_dist = self.distribution(self.processing_time)
        else:
            try:
                processing_time_dist = self.distribution(*self.processing_time)
            except TypeError:
                raise "Wrong types for processing time ({1}) and/or distribution ({0}) for scheduling an event".format(
                    self.processing_time, self.distribution)
        processing_time_dist = max(0, processing_time_dist)
        return processing_time_dist

    def exit_resource(self, **kwargs):
        """Exits the resource. The resource is released and the queue attached to this resource is checked.

        Parameters
        ----------
        entity:
            the target on which a state change is scheduled.
        kwargs:
            kwargs are the keyword arguments that are used to expand the function.

        """
        logger.info(
            "Time {0:.2f}: {1} is processed by {2} of {3}".format(self.simulator.simulator_time, self.processing_entity,
                                                                  self.name, self.server.name))
        self.simulator.schedule_event_now(self.server, "enter_output_node", entity=self.processing_entity)

        # Release resource and check queue
        self.simulator.schedule_event_now(self, "check_queue", priority=1)

    def check_queue(self, **kwargs):
        """Checks whether there are objects in the queue to seize the resource. If there are no objects in the queue,
        the resource stays free. If there are objects in the queue, the first object seizes the resource.

        Parameters
        ----------
        obj:
            optional
        kwargs:
            kwargs are the keyword arguments that are used to expand the function.

        """
        logger.info(
            "Time {0:.2f}: Length of queue attached to {1} is {2}".format(self.simulator.simulator_time, self.name,
                                                                          len(self.input_queue.contents)))
        if len(self.input_queue.contents) == 0:
            self.resource_seized = False
            pass
        else:
            self.resource_seized = True
            self.processing_entity = self.input_queue.contents[0]
            self.simulator.schedule_event_now(self, "exit_input_node")
            self.input_queue.contents.pop(0)


