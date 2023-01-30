"""
Created on: 26-1-2023 14:41

@author: IvS
"""

import pytest

from pydsol.model.node import Node


def test_node_class(mocker):
    mock_simulator = mocker.Mock()

    node = Node(mock_simulator)

    assert node.simulator == mock_simulator
    assert node.id == 1
    assert node.name == "Node 1"

    node_2 = Node(mock_simulator, capacity=3, name='test', test=0)

    assert node_2.id == 2
    assert node_2.name == 'test'
    assert node_2.kwargs == dict(name='test', test=0)


def test_enter_input_node(mocker):
    mock_simulator = mocker.Mock()
    mock_entity = mocker.Mock()

    node = Node(mock_simulator)

    node.enter_input_node(mock_entity)


def test_exit_output_node(mocker):
    mock_simulator = mocker.Mock()
    mock_entity = mocker.Mock()

    node = Node(mock_simulator)
    node_2 = Node(mock_simulator)

    # No next
    with pytest.raises(AttributeError):
        node.exit_output_node(mock_entity)

    # Test with only one next node
    node.next = node_2
    node.exit_output_node(mock_entity)

    # Test with two next nodes
    node_3 = Node(mock_simulator)
    node.next = [node_2, node_3]
    node.exit_output_node(mock_entity)

    # Test with two nodes and selection weight
    node_4 = Node(mock_simulator, selection_weight=0.5)
    node_5 = Node(mock_simulator, selection_weight=0.9)

    node.next = [node_4, node_5]
    node.exit_output_node(mock_entity)

    # Test the vehicle
    mock_simulator.simulator_time = 1
    mock_entity.name = "test"

    vehicle = mocker.Mock()
    vehicle.name = "vehicle"

    vehicle.entities_on_vehicle = []
    node_6 = Node(mock_simulator, vehicle_type=vehicle)

    node_6.next = [node_4, node_5]
    node_6.exit_output_node(mock_entity)

    # Test with vehicle speed
    vehicle_speed = 5
    node_7 = Node(mock_simulator, vehicle_type=vehicle, vehicle_speed=vehicle_speed)

    node_7.next = [node_4, node_5]
    node_7.exit_output_node(mock_entity)

    assert isinstance(vehicle_speed, (int, float))


if __name__ == '__main__':
    pytest.main()
