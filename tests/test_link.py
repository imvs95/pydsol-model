"""
Created on: 26-1-2023 14:07

@author: IvS
"""

import pytest

from pydsol.model.link import Link, TimePath


def test_link_class(mocker):
    mock_simulator = mocker.Mock()
    mock_origin = mocker.Mock()
    mock_destination = mocker.Mock()

    mock_length = 5
    assert isinstance(mock_length, (int, float))

    link = Link(mock_simulator, mock_origin, mock_destination, mock_length)

    assert link.simulator == mock_simulator
    assert link.origin == mock_origin
    assert link.destination == mock_destination
    assert link.length == mock_length
    assert link.selection_weight == 1
    assert link.id == 1
    assert link.name == "Link 1"

    link_2 = Link(mock_simulator, mock_origin, mock_destination, mock_length, selection_weight=2, name="test", test=0)

    assert link_2.id == 2
    assert link_2.selection_weight == 2
    assert link_2.name == "test"
    assert link_2.kwargs == dict(name="test", test=0)


def test_link_enter_input_node(mocker):
    mock_simulator = mocker.Mock()
    mock_simulator.simulator_time = 1

    mock_origin = mocker.Mock()
    mock_origin.name = "origin"

    mock_destination = mocker.Mock()
    mock_destination.name = "destination"

    mock_length = 5

    link = Link(mock_simulator, mock_origin, mock_destination, mock_length)

    mock_entity = mocker.Mock()
    mock_entity.speed = 10
    mock_entity.name = "test"

    link.enter_input_node(mock_entity)


def test_link_exit_link(mocker):
    mock_simulator = mocker.Mock()
    mock_simulator.simulator_time = 1

    mock_origin = mocker.Mock()
    mock_origin.name = "origin"

    mock_destination = mocker.Mock()
    mock_destination.name = "destination"

    mock_length = 5

    link = Link(mock_simulator, mock_origin, mock_destination, mock_length)
    link_2 = Link(mock_simulator, mock_origin, mock_destination, 10)

    link.next = link_2

    mock_entity = mocker.Mock()
    mock_entity.speed = 10
    mock_entity.name = "test"

    link.exit_link(mock_entity)


def test_timepath_class(mocker):
    mock_simulator = mocker.Mock()
    mock_origin = mocker.Mock()
    mock_destination = mocker.Mock()

    mock_time = 5
    assert isinstance(mock_time, (int, float))

    timepath = TimePath(mock_simulator, mock_origin, mock_destination, mock_time)

    assert timepath.simulator == mock_simulator
    assert timepath.origin == mock_origin
    assert timepath.destination == mock_destination
    assert timepath.time == mock_time
    assert timepath.selection_weight == 1
    assert timepath.id == 1
    assert timepath.name == "TimePath 1"

    timepath_2 = TimePath(mock_simulator, mock_origin, mock_destination, mock_time, selection_weight=2, name="test",
                          test=0)

    assert timepath_2.id == 2
    assert timepath_2.selection_weight == 2
    assert timepath_2.name == "test"
    assert timepath_2.kwargs == dict(name="test", test=0)


def test_timepath_enter_input_node(mocker):
    mock_simulator = mocker.Mock()
    mock_simulator.simulator_time = 1

    mock_origin = mocker.Mock()
    mock_origin.name = "origin"

    mock_destination = mocker.Mock()
    mock_destination.name = "destination"

    mock_time = 5

    timepath = TimePath(mock_simulator, mock_origin, mock_destination, mock_time)

    mock_entity = mocker.Mock()
    mock_entity.name = "test"

    timepath.enter_input_node(mock_entity)


def test_timepath_exit_path(mocker):
    mock_simulator = mocker.Mock()
    mock_simulator.simulator_time = 1

    mock_origin = mocker.Mock()
    mock_origin.name = "origin"

    mock_destination = mocker.Mock()
    mock_destination.name = "destination"

    mock_time = 5

    timepath = TimePath(mock_simulator, mock_origin, mock_destination, mock_time)
    timepath_2 = TimePath(mock_simulator, mock_origin, mock_destination, mock_time)

    timepath.next = timepath_2

    mock_entity = mocker.Mock()
    mock_entity.name = "test"

    timepath.exit_path(mock_entity)


if __name__ == '__main__':
    pytest.main()
