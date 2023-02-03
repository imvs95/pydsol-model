========================
Basic Examples
========================

This is a step-by-step tutorial on how to develop a basic discrete event simulation model using pydsol-model.
Example can be found at ``./examples/basic_example.py``.

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Step-by-Step Tutorial
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

We want to create a basic discrete event simulation model with one source, one server, one sink with entities passing
through the model, using links with distance of 1. See conceptualization of the simulation model in the figure below.

.. image:: ./images/figure_1_basic_example.jpg
    :width: 550px
    :align: center
    :height: 200px
    :alt: alternate text


Start with creating a new ``DSOLModel`` class for this basic example.
::
    from pydsol.core.model import DSOLModel

    class BasicExampleModel(DSOLModel):
        def __init__(self, simulator):
            super().__init__(simulator)

        def construct_model(self):
           # add model objects

Then, add the model objects that we want in our simulation model as following:
::
    from pydsol.core.model import DSOLModel

    from pydsol.model.source import Source
    from pydsol.model.server import Server
    from pydsol.model.sink import Sink
    from pydsol.model.link import Link

    class BasicExampleModel(DSOLModel):
        def __init__(self, simulator):
            super().__init__(simulator)

        def construct_model(self):
            # Create model
            source = Source(self.simulator)
            server = Server(self.simulator)
            sink = Sink(self.simulator)

            link_1 = Link(self.simulator, source, server, 1)
            link_2 = Link(self.simulator, server, sink, 1)

For all the model objects, the default values are used. Note that Source creates entities of type ``Entity`` by default.

Next, the structure of the model components needs to be set - so how are the entities flowing through the model? This is done
using the attribute *next*. This attribute defines what the next model object is. A *next* needs to be defined for each model object
expect for the Sink.
::
    from pydsol.core.model import DSOLModel

    from pydsol.model.source import Source
    from pydsol.model.server import Server
    from pydsol.model.sink import Sink
    from pydsol.model.link import Link

    class BasicExampleModel(DSOLModel):
        def __init__(self, simulator):
            super().__init__(simulator)

        def construct_model(self):
            # Create model
            source = Source(self.simulator)
            server = Server(self.simulator)
            sink = Sink(self.simulator)

            link_1 = Link(self.simulator, source, server, 1)
            link_2 = Link(self.simulator, server, sink, 1)

            # Set structure
            source.next = link_1
            link_1.next = server
            server.next = link_2
            link_2.next = sink

The simulation model is now finished and ready to run. For running, ``pydsol-core`` is used. Running the model for one
replication with a start time of 0, no warm-up time, and a run time of 100. This results in the following code:
::
    from pydsol.core.experiment import SingleReplication
    from pydsol.core.model import DSOLModel
    from pydsol.core.simulator import DEVSSimulatorFloat

    from pydsol.model.source import Source
    from pydsol.model.server import Server
    from pydsol.model.sink import Sink
    from pydsol.model.link import Link


    class BasicExampleModel(DSOLModel):
        def __init__(self, simulator):
            super().__init__(simulator)

        def construct_model(self):
            print("\nReplication starts...")
            # Create model
            source = Source(self.simulator)
            server = Server(self.simulator)
            sink = Sink(self.simulator)

            link_1 = Link(self.simulator, source, server, 1)
            link_2 = Link(self.simulator, server, sink, 1)

            # Set structure
            source.next = link_1
            link_1.next = server
            server.next = link_2
            link_2.next = sink

    if __name__ == "__main__":
        simulator = DEVSSimulatorFloat("sim")
        model = BasicExampleModel(simulator)
        replication = SingleReplication("rep1", 0.0, 0.0, 100)
        simulator.initialize(model, replication)
        simulator.start()

+++++++++++++++++++++
Extensions
+++++++++++++++++++++

An example for extending or modifying a basic discrete event simulation models (in ``def construct_model``) is to give
your own input to the interarrival times, processing times, and distribution to each model station. For example:
::
            def construct_model(self):
                print("\nReplication starts...")
                # Create model
                source = Source(self.simulator, interarrival_time=0.5)
                server = Server(self.simulator, processing_time=1, distribution=None)
                sink = Sink(self.simulator)

                link_1 = Link(self.simulator, source, server, 1)
                link_2 = Link(self.simulator, server, sink, 1)

                # Set structure
                source.next = link_1
                link_1.next = server
                server.next = link_2
                link_2.next = sink

Also, you can customize the names of each model objects. For example, naming the links:
::
            def construct_model(self):
                print("\nReplication starts...")
                # Create model
                source = Source(self.simulator, interarrival_time=0.5)
                server = Server(self.simulator, processing_time=1, distribution=None)
                sink = Sink(self.simulator)

                link_1 = Link(self.simulator, source, server, 1, name="Link 1.0")
                link_2 = Link(self.simulator, server, sink, 1, name="Link 2.0")

                # Set structure
                source.next = link_1
                link_1.next = server
                server.next = link_2
                link_2.next = sink

If entities should be carried by a ``Vehicle`` from, for example, the source to the server, add the vehicle type to the
Source object. Also, to make sure that the Source actually uses ``Entity`` as entity type, we add this attribute
to the Source object like:
::
    from pydsol.model.entities import Entity, Vehicle

                def construct_model(self):
                    print("\nReplication starts...")
                    # Create model
                    source = Source(self.simulator, interarrival_time=0.5, vehicle_type=Vehicle,
                                    entity_type = Entity)
                    server = Server(self.simulator, processing_time=1, distribution=None)
                    sink = Sink(self.simulator)

                    link_1 = Link(self.simulator, source, server, 1, name="Link 1.0")
                    link_2 = Link(self.simulator, server, sink, 1, name="Link 2.0")

                    # Set structure
                    source.next = link_1
                    link_1.next = server
                    server.next = link_2
                    link_2.next = sink

Another example to extend the basic simulation model is to add another link from the source to the server.
This is combined with all the other customizations and extensions, and gives the code as below. This code is  also available at ``./examples/basic_example_extended.py``.
::
    from pydsol.core.experiment import SingleReplication
    from pydsol.core.model import DSOLModel
    from pydsol.core.simulator import DEVSSimulatorFloat

    from pydsol.model.entities import Entity, Vehicle
    from pydsol.model.source import Source
    from pydsol.model.server import Server
    from pydsol.model.sink import Sink
    from pydsol.model.link import Link


    class BasicExampleModel(DSOLModel):
        def __init__(self, simulator):
            super().__init__(simulator)

        def construct_model(self):
            print("\nReplication starts...")
            # Create model
            source = Source(self.simulator, 0.5, entity_type=Entity, vehicle_type=Vehicle)
            server = Server(self.simulator, processing_time=1, distribution=None)
            sink = Sink(self.simulator)

            link_1 = Link(self.simulator, source, server, 1, name="Link 1.0")
            link_11 = Link(self.simulator, source, server, 1, name="Link 1.1")
            link_2 = Link(self.simulator, server, sink, 1, name="Link 2.0")

            # Set structure
            source.next = [link_1, link_11]
            link_1.next = link_11.next = server

            server.next = link_2
            link_2.next = sink


    if __name__ == "__main__":
        simulator = DEVSSimulatorFloat("sim")
        model = BasicExampleModel(simulator)
        replication = SingleReplication("rep1", 0.0, 0.0, 100)
        simulator.initialize(model, replication)
        simulator.start()