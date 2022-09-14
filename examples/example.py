"""
Created on: 12-9-2022 14:15

@author: IvS
"""
from pydsol.core.experiment import SingleReplication
from pydsol.core.model import DSOLModel
from pydsol.core.simulator import DEVSSimulatorFloat

from entities import Entity
from source import Source
from server import Server
from sink import Sink
from link import Link
from entities import Vehicle


class ExampleModel(DSOLModel):
    def __init__(self, simulator):
        super().__init__(simulator)

    def construct_model(self):
        print("\nReplication starts...")
        # Create model
        source = Source(self.simulator, 0.5, entity_type=Entity, vehicle_type=Vehicle)
        server = Server(self.simulator, processing_time=1, distribution=None)
        sink = Sink(self.simulator)

        link_1 = Link(self.simulator, source, server, 1, name="Link 10")
        link_11 = Link(self.simulator, source, server, 1, name="Link 11")
        link_2 = Link(self.simulator, server, sink, 1, name="Link 2")

        source.next = [link_1, link_11]
        link_1.next = link_11.next = server

        server.next = link_2
        link_2.next = sink


if __name__ == "__main__":
    simulator = DEVSSimulatorFloat("sim")
    model = ExampleModel(simulator)
    replication = SingleReplication("rep1", 0.0, 0.0, 100)
    simulator.initialize(model, replication)
    simulator.start()
