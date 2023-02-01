===============
Overview
===============

pydsol-model provides a set of predefined model objects to construct and run a discrete event simulation model.
Discrete event simulation models are event-based, meaning that events within a simulation model are executed from event to event that can vary in time.
No fixed time for a event is scheduled; this happens for agent-based simulation models (ticks) and system dynamics. Discrete event simulation models
have a continuous simulation time. This is important for understanding the code of the model object. Each step within a model object is, therefore, scheduled using an event
instead of passing it on to the next function (which often happens in Python).

.. to do how to schedule an event!

The following model objects are provided::

    model objects
    ├── Entity
    |   └── Vehicle
    ├── Source
    ├── Server
    ├── Resource
    ├── Queue
    ├── Sink
    ├── Node
    ├── Link
    └── TimePath

**Entity**

**Vehicle**

**Source** is a station that creates entities. Depending on the interarrival time, a new batch of entities is created, and exit the source.
Source only has an output flow of entities. At least, one source is needed in a simulation model.

**Server** is a processing station where entities flow through, so it has an input and output flow of entities. Servers are multiple **Resources** combined with a **Queue**.

**Resource**

**Queue**

**Sink** is a station that destroys entities. Sink only has an input flow of entities. At least, one sink is needed in a simulation model, else the number of entities in the model becomes too large for running experiments.

**Node**

**Link** connects the various stations to ensure the flow of entities. A link has a specific distance between origin and destination. Based on the (stochastic) speed of the entity, the time from
the origin station to destination for each entity is calculated, and an event for travelling the link is scheduled.

**TimePath** also connects the various stations to ensure the flow of entities, but based on time. A time path has a specific time between
origin and destination. Based on this time, an event for travelling the path is scheduled.

