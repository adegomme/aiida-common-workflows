# -*- coding: utf-8 -*-
# pylint: disable=function-redefined
import pytest

from aiida_common_workflows.protocol import ProtocolRegistry


@pytest.fixture
def protocol_registry():

    class SubProtocolRegistry(ProtocolRegistry):

        _protocols = {'efficiency': {'description': 'description'}, 'precision': {'description': 'description'}}
        _default_protocol = 'efficiency'

    return SubProtocolRegistry()


def test_validation():
    """Test the validation of subclasses of `ProtocolRegistry`."""

    class SubProtocolRegistry(ProtocolRegistry):

        _protocols = None
        _default_protocol = None

    with pytest.raises(RuntimeError):
        SubProtocolRegistry()

    class SubProtocolRegistry(ProtocolRegistry):

        _protocols = {'efficiency': {}, 'precision': 'wrong_type'}
        _default_protocol = None

    with pytest.raises(RuntimeError):
        SubProtocolRegistry()

    class SubProtocolRegistry(ProtocolRegistry):

        _protocols = {'efficiency': {'description': 'description'}, 'precision': {}}
        _default_protocol = None

    with pytest.raises(RuntimeError):
        SubProtocolRegistry()

    class SubProtocolRegistry(ProtocolRegistry):

        _protocols = {'efficiency': {'description': 'description'}, 'precision': {'description': 'description'}}
        _default_protocol = None

    with pytest.raises(RuntimeError):
        SubProtocolRegistry()

    class SubProtocolRegistry(ProtocolRegistry):

        _protocols = {'efficiency': {'description': 'description'}, 'precision': {'description': 'description'}}
        _default_protocol = 'non-existant'

    with pytest.raises(RuntimeError):
        SubProtocolRegistry()


def test_is_valid_protocol(protocol_registry):
    """Test `ProtocolRegistry.is_valid_protocol`."""
    assert protocol_registry.is_valid_protocol('efficiency')
    assert not protocol_registry.is_valid_protocol('non-existant')


def test_get_protocol_names(protocol_registry):
    """Test `ProtocolRegistry.get_protocol_names`."""
    assert sorted(protocol_registry.get_protocol_names()) == sorted(['efficiency', 'precision'])


def test_get_default_protocol_name(protocol_registry):
    """Test `ProtocolRegistry.get_default_protocol_name`."""
    assert protocol_registry.get_default_protocol_name() == 'efficiency'


def test_get_protocol(protocol_registry):
    """Test `ProtocolRegistry.get_protocol`."""
    assert protocol_registry.get_protocol('efficiency') == {'description': 'description'}

    with pytest.raises(ValueError):
        protocol_registry.get_protocol('non-existant')
