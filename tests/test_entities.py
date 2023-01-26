"""
Created on: 26-1-2023 13:47

@author: IvS
"""

import pytest

from pydsol.model.entities import Entity, Vehicle


def test_entity(mocker):
    mock_simulator = mocker.Mock()
    mock_time = 1

    entity = Entity(mock_simulator, mock_time)

    assert entity.simulator == mock_simulator
    assert entity.time_creations == mock_time
    assert entity.id == 1
    assert entity.name == "Entity 1"

    entity_2 = Entity(mock_simulator, mock_time, speed=2, test=0, more_test=0)

    assert entity_2.id == 2
    assert entity_2.speed == 2
    assert entity_2.kwargs == dict(test=0, more_test=0)


def test_vehicle(mocker):
    mock_simulator = mocker.Mock()

    vehicle = Vehicle(mock_simulator)

    assert vehicle.speed == 10
    assert len(vehicle.entities_on_vehicle) == 0

    vehicle.entities_on_vehicle = ["1", "2", "3"]

    assert vehicle.entities_on_vehicle == ["1", "2", "3"]


if __name__ == '__main__':
    pytest.main()
