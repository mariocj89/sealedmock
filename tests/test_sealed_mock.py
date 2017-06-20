from sealedmock import Mock, seal
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock
import pytest


def test_new_attributes_can_be_accessed_before_seal():
    m = Mock()
    m.test
    m.test()
    m.test().test2


def test_attributes_return_more_mocks_by_default():
    m = Mock()

    assert isinstance(m.test, Mock)
    assert isinstance(m.test(), Mock)
    assert isinstance(m.test().test2(), Mock)


def test_new_attributes_cannot_be_accessed_on_seal():
    m = Mock()

    seal(m)
    with pytest.raises(AttributeError):
        m.test
    with pytest.raises(AttributeError):
        m.test()


def test_existing_attributes_allowed_after_seal():
    m = Mock()

    m.test.return_value = 3

    seal(m)
    assert m.test() == 3


def test_initialized_attributes_allowed_after_seal():
    m = Mock(test_value=1)

    seal(m)
    assert m.test_value == 1


def test_call_on_sealed_mock_fails():
    m = Mock()

    seal(m)
    with pytest.raises(AttributeError):
        m()


def test_call_on_defined_sealed_mock_succeeds():
    m = Mock(return_value=5)

    seal(m)
    assert m() == 5


def test_seals_recurse_on_added_attributes():
    m = Mock()

    m.test1.test2().test3 = 4

    seal(m)
    assert m.test1.test2().test3 == 4
    with pytest.raises(AttributeError):
        m.test1.test2.test4


class SampleObject(object):
    def __init__(self):
        self.attr_sample1 = 1
        self.attr_sample2 = 1

    def method_sample1(self):
        pass

    def method_sample2(self):
        pass


def test_integration_with_spec_att_definition():
    """You are not restricted when defining attributes on a mock with spec"""
    m = Mock(SampleObject)

    m.attr_sample1 = 1
    m.attr_sample3 = 3

    seal(m)
    assert m.attr_sample1 == 1
    assert m.attr_sample3 == 3
    with pytest.raises(AttributeError):
        m.attr_sample2


def test_integration_with_spec_method_definition():
    """You need to defin the methods, even if they are in the spec"""
    m = Mock(SampleObject)

    m.method_sample1.return_value = 1

    seal(m)
    assert m.method_sample1() == 1
    with pytest.raises(AttributeError):
        m.method_sample2()


def test_integration_with_spec_method_definition_respects_spec():
    """You cannot define methods out of the spec"""
    m = Mock(SampleObject)

    with pytest.raises(AttributeError):
        m.method_sample3.return_value = 3


def test_sealed_exception_has_attribute_name():
    m = Mock()

    seal(m)
    try:
        m.SECRETE_name
    except AttributeError as ex:
        assert "SECRETE_name" in str(ex)


def test_attribute_chain_is_maintained():
    m = Mock(name="mock_name")
    m.test1.test2.test3.test4

    seal(m)
    try:
        m.test1.test2.test3.test4.boom
    except AttributeError as ex:
        assert "mock_name.test1.test2.test3.test4.boom" in str(ex)


def test_call_chain_is_maintained():
    m = Mock()
    m.test1().test2.test3().test4

    seal(m)
    try:
        m.test1().test2.test3().test4()
    except AttributeError as ex:
        assert "mock.test1().test2.test3().test4" in str(ex)
