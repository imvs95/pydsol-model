"""
Created on: 30-1-2023 14:22

@author: IvS
"""
import pytest
import numpy as np

from pydsol.model.resource import Resource


def test_resource_class(mocker):
    mock_simulator = mocker.Mock()
    mock_queue = mocker.Mock(contents=[], attached_to=mocker.Mock())

    resource = Resource(1, mock_simulator, mock_queue, np.random.triangular, (0.1, 0.2, 0.3), 0)
    assert resource.name == "Resource 1"

    resource = Resource(5, mock_simulator, mock_queue, np.random.triangular, (0.1, 0.2, 0.3), 0)
    assert resource.name == "Resource 5"


def test_exit_input_node(mocker):
    mock_simulator = mocker.Mock(simulator_time=1)
    mock_queue = mocker.Mock(contents=[], attached_to=mocker.Mock())
    mock_entity = mocker.Mock(name="entity1")

    resource = Resource(1, mock_simulator, mock_queue, np.random.triangular, (0.1, 0.2, 0.3), 0)
    resource.processing_entity = mock_entity
    assert isinstance(resource.processing_entity, object)
    resource.exit_input_node()


def test_enter_resource(mocker):
    mock_simulator = mocker.Mock(simulator_time=1)
    mock_queue = mocker.Mock(contents=[], attached_to=mocker.Mock())
    mock_entity = mocker.Mock(name="entity1")

    resource = Resource(1, mock_simulator, mock_queue, np.random.triangular, (0.1, 0.2, 0.3), 0)
    resource.processing_entity = mock_entity
    assert isinstance(resource.processing_entity, object)
    assert isinstance(resource.transfer_in_time, (int, float))
    resource.enter_resource()


def test_processing(mocker):
    mock_simulator = mocker.Mock(simulator_time=1)
    mock_queue = mocker.Mock(contents=[], attached_to=mocker.Mock())
    mock_entity = mocker.Mock(name="entity1")

    # Basic
    resource = Resource(1, mock_simulator, mock_queue, np.random.triangular, (0.1, 0.2, 0.3), 0)
    resource.processing_entity = mock_entity
    resource.processing()

    # With wrong distribution and unit
    with pytest.raises(TypeError):
        resource = Resource(1, mock_simulator, mock_queue, np.random.random, (0.1, 0.2, 0.3), 0)
        resource.processing_entity = mock_entity
        resource.processing()

    # With distribution and wrong unit
    with pytest.raises(TypeError):
        resource = Resource(1, mock_simulator, mock_queue, np.random.triangular, 1, 0)
        resource.processing_entity = mock_entity
        resource.processing()

    # With no distribution
    resource = Resource(1, mock_simulator, mock_queue, distribution=None, processing_time=1, transfer_in_time=0)
    resource.processing_entity = mock_entity
    resource.processing()

    # With no distribution but wrong unit processing time
    with pytest.raises(TypeError):
        resource = Resource(1, mock_simulator, mock_queue, distribution=None, processing_time=(0, 1, 3),
                            transfer_in_time=0)
        resource.processing_entity = mock_entity
        resource.processing()

    # With no processing time
    with pytest.raises(TypeError):
        resource = Resource(1, mock_simulator, mock_queue, np.random.triangular, None, 0)
        resource.processing_entity = mock_entity
        resource.processing()

    # Test processing entity in kwargs
    resource = Resource(1, mock_simulator, mock_queue, np.random.triangular, (0.1, 0.2, 0.3), 0)
    resource.processing(processing_entity=mock_entity)
    assert resource.processing_entity == mock_entity


def test_exit_resource(mocker):
    mock_simulator = mocker.Mock(simulator_time=1)
    mock_queue = mocker.Mock(contents=[], attached_to=mocker.Mock())
    mock_entity = mocker.Mock(name="entity1")

    resource = Resource(1, mock_simulator, mock_queue, np.random.triangular, (0.1, 0.2, 0.3), 0)
    resource.processing_entity = mock_entity
    resource.server = mocker.Mock(name="server1")

    assert isinstance(resource.processing_entity, object)
    assert isinstance(resource.server, object)

    resource.exit_resource()


def test_check_queue(mocker):
    mock_simulator = mocker.Mock(simulator_time=1)
    mock_queue = mocker.Mock(contents=[], attached_to=mocker.Mock())
    mock_entity = mocker.Mock(name="entity1")

    resource = Resource(1, mock_simulator, mock_queue, np.random.triangular, (0.1, 0.2, 0.3), 0)

    # When queue is zero
    resource.check_queue()
    assert len(resource.input_queue.contents) == 0
    assert not resource.resource_seized

    # When there is a queue get the first item
    resource.input_queue.contents = [mock_entity]
    assert len(resource.input_queue.contents) == 1

    resource.check_queue()
    assert resource.resource_seized
    assert resource.processing_entity == mock_entity
    assert len(resource.input_queue.contents) == 0


if __name__ == '__main__':
    pytest.main()
