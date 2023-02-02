===============
Overview
===============

pydsol-model provides a set of predefined model objects to construct and run a discrete event simulation model.
Discrete event simulation models are event-based, meaning that events within a simulation model are executed from event to event that can vary in time.
No fixed time for a event is scheduled; this happens for agent-based simulation models (ticks) and system dynamics. Discrete event simulation models
have a continuous simulation time. This is important for understanding the code of the model object. Each step within a model object is, therefore, scheduled using an event
instead of passing it on to the next function (which often happens in Python).

++++++++++++++++++++++++++++++
Model Objects
++++++++++++++++++++++++++++++

The model objects are provided in the following structure of .py files::

    pydsol
        └── model
            ├── basic_logger.py
            ├── entities.py
            |     └── Entity
            |          └── Vehicle
            ├── link.py
            |     ├── Link
            |     └── TimePath
            ├── node.py
            |     └── Node
            ├── queue_model.py
            |     └── QueueModel
            ├── resource.py
            |     └── Resource
            ├── server.py
            |     └── Server
            ├── sink.py
            |     └── Sink
            └── source.py
                  └── Source


**Entity** are the discrete items of interest flowing through the discrete event simulation model. They can pass through any model object such as
the queues, resources, servers etc. Entities can be persons, products, messages or any items of interest. Entities have attributes
that keeps data on a specific entity.

**Vehicle** is a special type of **Entity**. This is an entity that can also pass through the model, but is only used to carry
other entities over the **Link** or **TimePath**. Thus, a vehicle carries a batch of entities from origin to destination.
Vehicle has the attribute *entities_on_vehicle* to keep track of which entities the vehicle carries. At the output node of the origin
station, the entities are loaded on the vehicle. At the input node of the destination station, the entities are loaded off the vehicle.

**Link** connects the various stations/model elements to ensure the flow of entities. A link has a specific distance between origin and destination. Based on the (stochastic) speed of the entity, the time from
the origin station to destination for each entity is calculated, and an event for travelling the link is scheduled.

**TimePath** also connects the various stations/model element to ensure the flow of entities, but based on time. A time path has a specific time between
origin and destination. Based on this time, an event for travelling the path is scheduled.

**Node** is a basic travel node where entities flow through. A node has an input and output flow of entities. No processing time
is required for the node.

**QueueModel** is a basic queue attached to a specific model element or station. It keeps track of the entities in the queue
using a *contents* list attribute. This queue can be attached to any model element or station using the attribute *attached_to*.
Based on the sequence of adding and removing entities in the *contents* list, the queueing rule is defined (e.g., First-In First-Out,
Last-In First-Out etc.)

**Resource** is a processing station where entities can flow through. Resources can be seized and released by entities in the system. If the resource is seized by an entity, other
entities cannot seize it until it is released (e.g., after a certain processing time). Remaining entities are queued in a **QueueModel**.
This resource requires a processing time for each entity. Resources can represent, for example, supplies, machines, ports, stores.

**Server** is multiple **Resources** combined with a **Queue**. Server is also a processing station where entities flow through, so it has an input and output flow of entities.
It uses the resources to process the entities, based on an user-based (stochastic) processing time. The capacity of the server, i.e.,
how many resources the server has, is set by the attribute *capacity*.

**Sink** is a station that destroys entities. Sink only has an input flow of entities. At least, one sink is needed in a simulation model, else the number of entities in the model becomes too large for running experiments.

**Source** is a station that creates entities. Depending on the interarrival time, a new batch of entities is created, and exit the source.
Source only has an output flow of entities. At least, one source is needed in a simulation model.

++++++++++++++++++++++++++++++
Event Scheduling
++++++++++++++++++++++++++++++

pydsol-core is used to schedule events in the discrete event simulation models. To use pydsol-model, it is necessary to understand
how to schedule such an event on the pydsol-core simulators for understanding and developing models.

Two ways of scheduling events that are used are (1) scheduling an event **now**, and (2) scheduling an event with a **relative delay**.

To schedule an event **now**, use:
::

    simulator.schedule_event_now(target, method)

where *target* is the model object or station to schedule the event on, and *method* is the name of the event method (in string.

For example, a model has a server called *server_1* with various methods including *do_something*. Then, you have to schedule an
event as:
::

    simulator.schedule_event_now(server_1, "do_something")

This holds for every entity flowing through the model.

To schedule an event with a **relative delay**, use:
::

    simulator.schedule_event_rel(relative_delay, target, method)

where relative delay is the amount of time until the event is scheduled relative to the current simulation time. For example, event
*do_something* has to be scheduled in 1.5 minutes. The simulation time is 1.0 minute. So the event should be scheduled at 2.5 minutes, or
you can use the relative delay function as:
::

    simulator.schedule_event_rel(1.5, server_1, "do_something")

More documentation on pydsol-core can be found at `Read the Docs <https://pydsol-core.readthedocs.io/en/latest/index.html>`_ or
`Source Code <https://github.com/averbraeck/pydsol-core>`_.


