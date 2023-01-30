"""
Created on: 26-1-2023 12:33

@author: IvS
"""

import pytest
import numpy as np

from pydsol.model.source import Source
from pydsol.model.server import Server


def test_source_class(mocker):
    mock_simulator = mocker.Mock()
    source = Source(mock_simulator)

    assert source.simulator == mock_simulator
    assert source.id == 1
    assert source.name == "Source 1"

    mock_entity_type = mocker.Mock()
    source_2 = Source(mock_simulator, interarrival_time=1, num_entities=3, entity_type=mock_entity_type, name="test",
                      distribution=np.random.exponential)
    assert source_2.id == 2
    assert source_2.interarrival_time == 1
    assert source_2.num_entities == 3
    assert source_2.entity_type == mock_entity_type
    assert source_2.name == "test"
    assert source_2.distribution == np.random.exponential


def test_create_entities(mocker):
    mock_simulator = mocker.Mock()
    mock_simulator.simulator_time = 1

    # Test with default interarrival time and default entity
    source = Source(mock_simulator)
    source.create_entities()

    # Test with multiple entities
    source = Source(mock_simulator, num_entities=3)
    source.create_entities()

    # Test with other interarrival time
    source = Source(mock_simulator, interarrival_time=1)
    source.create_entities()

    # Test with other interarrival time and distribution
    source = Source(mock_simulator, interarrival_time=(0, 1, 2), distribution=np.random.triangular)
    source.create_entities()

    # Test with all variables
    source = Source(mock_simulator, interarrival_time=(0, 1, 2), distribution=np.random.triangular, num_entities=5)
    source.create_entities()

    # Test with wrong interarrival time
    with pytest.raises(TypeError):
        source = Source(mock_simulator, interarrival_time=(0, 1, 2), distribution=np.random.exponential)
        source.create_entities()


def test_enter_output_node(mocker):
    mock_simulator = mocker.Mock()
    mock_simulator.simulator_time = 1

    mock_entity = mocker.Mock()
    mock_entity.name = "test"

    vehicle = mocker.Mock()
    vehicle.name = "vehicle"
    vehicle.entities_on_vehicle = []

    # With vehicle
    source = Source(mock_simulator, vehicle_type=vehicle)
    source.enter_output_node(mock_entity)

    # With wrong vehicle unit
    with pytest.raises(TypeError):
        vehicle_type = 1
        source = Source(mock_simulator, vehicle_type=vehicle_type)
        source.enter_output_node(mock_entity)

    # With vehicle speed
    vehicle_speed = 10
    source = Source(mock_simulator, vehicle_type=vehicle, vehicle_speed=vehicle_speed)
    source.enter_output_node(mock_entity)

    assert isinstance(vehicle_speed, (int, float))


def test_exit_output_node(mocker):
    mock_simulator = mocker.Mock()
    mock_entity = mocker.Mock()

    server_next = Server(mock_simulator)

    source = Source(mock_simulator)

    # No next
    with pytest.raises(AttributeError):
        source.exit_output_node(mock_entity)

    # Test with only one next node
    source.next = server_next
    source.exit_output_node(mock_entity)

    # Test with two next nodes
    server_1 = Server(mock_simulator)
    source.next = [server_next, server_1]
    source.exit_output_node(mock_entity)

    # Test with two nodes and selection weight
    server_next.selection_weight = 0.5
    server_1.selection_weight = 0.9

    source.exit_output_node(mock_entity)


if __name__ == '__main__':
    pytest.main()
