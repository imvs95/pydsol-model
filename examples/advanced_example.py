"""
Created on: 2-2-2023 15:34

@author: IvS

Discrete event simulation model with units km and hours
"""
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


class ShoeBatch(Entity):
    def __init__(self, simulator, t, **kwargs):
        super().__init__(simulator, t, **kwargs)

        self.quantity = round(np.random.uniform(100, 150), 0)
        self.start_time = self.simulator.simulator_time
        self.time_in_system = 0

    def __repr__(self):
        return self.name


class Truck(Vehicle):
    def __init__(self, simulator, **kwargs):
        self.speed = np.random.triangular(0, 100, 120) * 24  # km/h to day
        if "vehicle_speed" in kwargs:
            self.speed = np.random.triangular(0, kwargs["vehicle_speed"], 120) * 24
        super().__init__(simulator, self.speed, **kwargs)

        self.interarrival_distribution = np.random.triangular
        self.interarrival_times = (0, 0.2, 0.5)


class ContainerShip(Vehicle):
    def __init__(self, simulator, **kwargs):
        # km/h to knots, and one knot is one nautical mile per hour
        self.speed = np.random.triangular(10 * 1.85, 18 * 1.85, 25 * 1.85)
        if "vehicle_speed" in kwargs:
            self.speed = np.random.triangular(10 * 1.85, kwargs["vehicle_speed"], 25 * 1.85)
        super().__init__(simulator, self.speed, **kwargs)

        self.interarrival_distribution = np.random.triangular
        self.interarrival_times = (0, 5, 14)


class Supplier(Source):
    def __init__(self, simulator, interarrival_time, **kwargs):
        super().__init__(simulator, interarrival_time, **kwargs)
        self.list_quantity = []

    def exit_source(self, entity: ShoeBatch, **kwargs):
        # Tally quantity
        self.list_quantity.append(entity.quantity)
        super().exit_source(entity, **kwargs)

    def exit_output_node(self, entity: Truck, **kwargs):
        # Add interarrival delay of Truck
        interarrival_delay = entity.interarrival_distribution(*entity.interarrival_times)

        self.simulator.schedule_event_rel(interarrival_delay, self, "exit_with_vehicle", entity=entity)

    def exit_with_vehicle(self, entity, **kwargs):
        super().exit_output_node(entity, **kwargs)


class Port(Server):
    def __init__(self, simulator, processing_time, capacity=1, distribution=np.random.triangular, **kwargs):
        super().__init__(simulator, capacity=capacity, distribution=distribution, processing_time=processing_time,
                         **kwargs)
        self.location = kwargs['location']
        self.name = self.name + " " + self.location

    def exit_output_node(self, entity: [Truck, ContainerShip], **kwargs):
        # Add interarrival delay
        interarrival_delay = entity.interarrival_distribution(*entity.interarrival_times)
        self.simulator.schedule_event_rel(interarrival_delay, self, "exit_with_vehicle", entity=entity)

    def exit_with_vehicle(self, entity: [Truck, ContainerShip], **kwargs):
        logging.debug(
            "Time {0:.2f}: {1} exits {2}".format(self.simulator.simulator_time, entity.name, self.name))
        super().exit_output_node(entity, **kwargs)


class Warehouse(Server):
    def __init__(self, simulator, processing_time, **kwargs):
        super().__init__(simulator, processing_time=processing_time, **kwargs)

        # Override function processing - Resource
        self.processing_function_resource = self.resources[0].processing
        for resource in self.resources:
            resource.processing = self.processing

    def enter_resource(self):
        """Schedules the event to transfer into the resource and starts processing.

        Parameters
        ----------
        entity: object
            the target on which a state change is scheduled.
        """
        self.simulator.schedule_event_rel(self.transfer_in_time, self, "processing")

    def processing(self, **kwargs):
        # This only works if you have one resource, i.e., one warehouse
        for resource in self.resources:
            entity = resource.processing_entity
        if "divide_quantity" in self.kwargs:
            batches_product = self.divide_entity(entity, self.kwargs["divide_quantity"])
            self.processing_function_resource(processing_entity=batches_product)

    @staticmethod
    def divide_entity(entity: ShoeBatch, copy_quantity: int):
        copies = []
        for i in range(copy_quantity):
            copy_entity = copy.copy(entity)
            copy_entity.quantity = entity.quantity / copy_quantity
            copy_entity.name = entity.name + "." + str(i)
            copies.append(copy_entity)
        return copies

    def enter_output_node(self, entity, **kwargs):
        # List of products due to dividing
        for batch in entity:
            super().enter_output_node(batch, **kwargs)

    def exit_output_node(self, entity: Truck, **kwargs):
        # Add interarrival delay of Truck
        interarrival_delay = entity.interarrival_distribution(*entity.interarrival_times)

        self.simulator.schedule_event_rel(interarrival_delay, self, "exit_with_vehicle", entity=entity)

    def exit_with_vehicle(self, entity, **kwargs):
        super().exit_output_node(entity, **kwargs)


class Retailer(Sink):
    def __init__(self, simulator, transfer_in_time: [float, int], **kwargs):
        super().__init__(simulator, transfer_in_time=transfer_in_time, **kwargs)

        self.location = kwargs['location']
        self.name = self.name + " " + self.location

        self.entities_of_system = []

    def destroy_entity(self, entity: Truck, **kwargs):
        for product in entity.entities_on_vehicle:
            product.time_in_system = self.simulator.simulator_time - product.start_time
            # Add value to list
            self.entities_of_system.append(product)
            super().destroy_entity(product)
        del entity


class AdvancedExampleModel(DSOLModel):
    def __init__(self, simulator, input_params, **kwargs):
        super().__init__(simulator, **kwargs)
        self.input_params = input_params
        self.seed = kwargs["seed"] if "seed" in kwargs else 1

        self.supplier = None
        self.retailers = []

    def construct_model(self):

        self.reset_model()

        np.random.seed(self.seed)

        print("\nReplication starts...")
        # Create model
        supplier = Supplier(self.simulator, interarrival_time=self.input_params["interarrival_time"],
                            entity_type=ShoeBatch, vehicle_type=Truck)
        export_port = Port(self.simulator, processing_time=(1, 2, 2), vehicle_type=ContainerShip, location="Export O")
        import_port = Port(self.simulator, processing_time=(1, 2, 3), vehicle_type=Truck, location="Import D")
        warehouse = Warehouse(self.simulator, processing_time=(0.5, 1, 2), vehicle_type=Truck, divide_quantity=3)
        retailer_1 = Retailer(self.simulator, transfer_in_time=0.2, location="City A")
        retailer_2 = Retailer(self.simulator, transfer_in_time=0.1, location="City B")
        retailer_3 = Retailer(self.simulator, transfer_in_time=0.3, location="City C")

        link_1 = Link(self.simulator, supplier, export_port, 30)
        link_2 = Link(self.simulator, export_port, import_port, 2000)
        link_3 = Link(self.simulator, import_port, warehouse, 100)
        link_4 = Link(self.simulator, warehouse, retailer_1, 55)
        link_5 = Link(self.simulator, warehouse, retailer_2, 83)
        link_6 = Link(self.simulator, warehouse, retailer_3, 22)

        # Set structure
        supplier.next = link_1
        link_1.next = export_port
        export_port.next = link_2
        link_2.next = import_port
        import_port.next = link_3
        link_3.next = warehouse
        warehouse.next = [link_4, link_5, link_6]
        link_4.next = retailer_1
        link_5.next = retailer_2
        link_6.next = retailer_3

        # For statistics
        self.supplier = supplier
        self.retailers = [retailer_1, retailer_2, retailer_3]

    def reset_model(self):
        classes = [ShoeBatch, Supplier,
                   Port, Warehouse, Retailer,
                   Link, Truck, ContainerShip]

        for i in classes:
            i.id_iter = itertools.count(1)

    def get_output_statistics(self):
        # Average Time in System
        average_product_time_in_system = []
        for retailer in self.retailers:
            average_product_time_in_system += [product.time_in_system for product in retailer.entities_of_system]

        # Average quantity of the shoe batch
        average_quantity = self.supplier.list_quantity

        outcomes = {"Time_In_System": statistics.mean(average_product_time_in_system),
                    "Quantity": statistics.mean(average_quantity)}

        return outcomes


if __name__ == "__main__":
    # Input
    NUM_REPLICATIONS = 10
    RUN_TIME = 364  # days
    INPUT_PARAMS = {"interarrival_time": 1.5}

    # Experiment
    experiment_output = {}
    for rep in range(NUM_REPLICATIONS):
        simulator = DEVSSimulatorFloat("sim")
        model = AdvancedExampleModel(simulator, INPUT_PARAMS, seed=rep)
        replication = SingleReplication("rep1", 0.0, 0.0, RUN_TIME)
        simulator.initialize(model, replication)
        simulator.start()

        while simulator.simulator_time < RUN_TIME:
            time.sleep(0.01)

        experiment_output[rep + 1] = model.get_output_statistics()

    logger.info("Experiment with {0} replications is finished".format(NUM_REPLICATIONS))
