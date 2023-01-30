"""
Created on: 30-1-2023 14:59

@author: IvS
"""
import pytest
import numpy as np

from pydsol.model.sink import Sink


def test_sink_class(mocker):
    mock_simulator = mocker.Mock()

    sink = Sink(mock_simulator)

    assert isinstance(sink.transfer_in_time, (int, float))
    assert sink.id == 1
    assert sink.name == "Sink 1"
    assert isinstance(sink.name, str)

    sink_2 = Sink(mock_simulator, transfer_in_time=(0, 1, 2), distribution=np.random.triangular, name="test")

    assert sink_2.id == 2
    assert isinstance(sink_2.name, str)


def test_enter_input_node(mocker):
    mock_simulator = mocker.Mock()
    mock_entity = mocker.Mock()

    # Iterable distribution
    sink = Sink(mock_simulator, transfer_in_time=(0, 1, 2), distribution=np.random.triangular)
    sink.enter_input_node(mock_entity)

    # None-iterable distribution
    sink = Sink(mock_simulator, transfer_in_time=1, distribution=np.random.normal)
    sink.enter_input_node(mock_entity)

    # Not matching distribution and transfer_in_time
    with pytest.raises(TypeError):
        sink = Sink(mock_simulator, transfer_in_time=1, distribution=np.random.triangular)
        sink.enter_input_node(mock_entity)

    # Only tranfer time
    sink = Sink(mock_simulator, transfer_in_time=1)
    sink.enter_input_node(mock_entity)


def test_exit_output_node(mocker):
    mock_simulator = mocker.Mock()
    mock_entity = mocker.Mock()

    sink = Sink(mock_simulator)
    sink.exit_input_node(mock_entity)
    assert isinstance(mock_entity, object)


def test_destroy_entity(mocker):
    mock_simulator = mocker.Mock(simulator_time=1)
    mock_entity = mocker.Mock(name="entity")

    sink = Sink(mock_simulator)
    sink.destroy_entity(mock_entity)


if __name__ == '__main__':
    pytest.main()
