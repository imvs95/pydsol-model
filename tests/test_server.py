"""
Created on: 30-1-2023 13:01

@author: IvS
"""
import pytest
import numpy as np

from pydsol.model.server import Server
from pydsol.model.entities import Vehicle


def test_server_class(mocker):
    mock_simulator = mocker.Mock()

    server = Server(mock_simulator)

    assert server.simulator == mock_simulator
    assert isinstance(server.capacity, int)
    assert server.id == 1
    assert isinstance(server.id, int)
    assert server.name == "Server 1"
    assert isinstance(server.name, str)
    assert len(server.resources) == server.capacity
    assert any(isinstance(resource, object) for resource in server.resources)
    assert isinstance(server.input_queue.contents, list)

    server_2 = Server(mock_simulator, capacity=2, distribution=np.random.normal, processing_time=1, transfer_in_time=1,
                      name="test")

    assert server_2.id == 2
    assert server_2.capacity == 2
    assert server_2.distribution == np.random.normal
    assert server_2.processing_time == 1
    assert server_2.transfer_in_time == 1
    assert server_2.name == "test"
    assert isinstance(server_2.name, str)
    assert len(server_2.resources) == server_2.capacity
    assert any(isinstance(resource, object) for resource in server_2.resources)


def test_enter_input_node(mocker):
    mock_simulator = mocker.Mock()
    mock_simulator.simulator_time = 1

    mock_entity = mocker.Mock()
    mock_entity.name = "entity"

    mock_vehicle = Vehicle(mock_simulator)

    server = Server(mock_simulator)

    # Entity is not vehicle
    server.enter_input_node(mock_entity)

    # Entity is vehicle but wrong entities on vehicle
    with pytest.raises(AttributeError):
        mock_vehicle.entities_on_vehicle = ["1", "2", "3"]
        server.enter_input_node(mock_vehicle)

    # Entity is vehicle with right entites on vehicle
    mock_entity_1 = mocker.Mock(name="entity1")
    mock_entity_2 = mocker.Mock(name="entity2")
    mock_vehicle.entities_on_vehicle = [mock_entity, mock_entity_1, mock_entity_2]
    server.enter_input_node(mock_vehicle)

    # #Entity is vehicle with other data format
    mock_vehicle.entities_on_vehicle = (mock_entity, mock_entity_1, mock_entity_2)
    server.enter_input_node(mock_vehicle)


def test_seize_resource(mocker):
    mock_simulator = mocker.Mock(simulator_time=1)
    mock_entity = mocker.Mock(name="entity")

    server = Server(mock_simulator)

    mock_resource_1 = mocker.Mock(resource_seized=True, name="resource 1")
    mock_resource_2 = mocker.Mock(resource_seized=True, name="resource 2")
    mock_resource_3 = mocker.Mock(resource_seized=True, name="resource 3")

    # Test when all are taken that entity goes to queue
    server.resources = [mock_resource_1, mock_resource_2, mock_resource_3]
    server.seize_resource(mock_entity)
    assert len(server.input_queue.contents) == 1

    # Test when only one resource and second entity
    mock_entity_2 = mocker.Mock(name="entity2")
    server.resources = [mock_resource_1]
    server.seize_resource(mock_entity_2)
    assert len(server.input_queue.contents) == 2

    # Set resource not seized and check if entity is the first in line
    mock_resource_1.resource_seized = False
    mock_entity_3 = mocker.Mock(name="entity3")
    server.seize_resource(mock_entity_3)
    assert mock_resource_1.processing_entity == mock_entity
    assert mock_resource_1.resource_seized
    assert len(server.input_queue.contents) == 2

    # Test when input queue is zero and multiple resources
    mock_resource_1.resource_seized = mock_resource_2.resource_seized = mock_resource_3.resource_seized = False
    server.resources = [mock_resource_1, mock_resource_2, mock_resource_3]
    server.input_queue.contents = []
    server.seize_resource(mock_entity)
    assert mock_resource_1.resource_seized
    assert mock_resource_1.processing_entity == mock_entity

    # Test when first resource is taken
    mock_resource_1.resource_seized = True
    mock_resource_2.resource_seized = mock_resource_3.resource_seized = False
    server.resources = [mock_resource_1, mock_resource_2, mock_resource_3]
    server.input_queue.contents = []
    server.seize_resource(mock_entity)
    assert mock_resource_2.resource_seized
    assert mock_resource_2.processing_entity == mock_entity


def test_enter_output_node(mocker):
    mock_simulator = mocker.Mock(simulator_time=1)
    mock_entity = mocker.Mock(name="entity")
    mock_vehicle = mocker.Mock(name="vehicle", entities_on_vehicle=[])

    # With vehicle
    server = Server(mock_simulator, vehicle_type=mock_vehicle)
    server.enter_output_node(mock_entity)
    assert isinstance(server.kwargs["vehicle_type"], object)

    # With wrong vehicle unit
    with pytest.raises(TypeError):
        vehicle_type = 1
        server = Server(mock_simulator, vehicle_type=vehicle_type)
        server.enter_output_node(mock_entity)

    # With wrong vehicle unit
    with pytest.raises(TypeError):
        vehicle_type = "vehicle"
        server = Server(mock_simulator, vehicle_type=vehicle_type)
        server.enter_output_node(mock_entity)

    # With vehicle speed
    server = Server(mock_simulator, vehicle_type=mock_vehicle, vehicle_speed=10)
    server.enter_output_node(mock_entity)
    assert isinstance(server.kwargs["vehicle_speed"], (int, float))


def test_exit_output_node(mocker):
    mock_simulator = mocker.Mock()
    mock_entity = mocker.Mock()

    next_1 = Server(mock_simulator)
    next_2 = Server(mock_simulator)

    server = Server(mock_simulator)

    # No next
    with pytest.raises(AttributeError):
        server.exit_output_node(mock_entity)

    # Test with only one next node
    server.next = next_1
    server.exit_output_node(mock_entity)

    # Test with two next nodes
    server.next = [next_1, next_2]
    server.exit_output_node(mock_entity)

    # Test with two nodes and selection weight
    next_1.selection_weight = 0.5
    next_2.selection_weight = 0.9
    server.exit_output_node(mock_entity)


if __name__ == '__main__':
    pytest.main()
