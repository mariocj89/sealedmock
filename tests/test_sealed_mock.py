from sealedmock import SealedMock
import pytest


def test_new_attributes_can_be_accessed_before_seal():
    m = SealedMock()
    m.test
    m.test()
    m.test().test2


def test_attributes_return_more_mocks_by_default():
    m = SealedMock()

    assert isinstance(m.test, SealedMock)
    assert isinstance(m.test(), SealedMock)
    assert isinstance(m.test().test2(), SealedMock)


def test_new_attributes_cannot_be_accessed_on_seal():
    m = SealedMock()

    m.sealed = True
    with pytest.raises(AttributeError):
        m.test
    with pytest.raises(AttributeError):
        m.test()


def test_sealed_exception_has_attribute_name():
    m = SealedMock()

    m.sealed = True
    try:
        m.SECRETE_name
    except AttributeError as ex:
        assert "SECRETE_name" in str(ex)


def test_existing_attributes_allowed_after_seal():
    m = SealedMock()

    m.test.return_value = 3

    m.sealed = True
    assert m.test() == 3


def test_initialized_attributes_allowed_after_seal():
    m = SealedMock(test_value=1)

    m.sealed = True
    assert m.test_value == 1


def test_call_on_sealed_mock_fails():
    m = SealedMock()

    m.sealed = True
    with pytest.raises(AttributeError):
        m()


def test_call_on_defined_sealed_mock_succeeds():
    m = SealedMock(return_value=5)

    m.sealed = True
    assert m() == 5


def test_seals_recurse_on_added_attributes():
    m = SealedMock()

    m.test1.test2().test3 = 4

    m.sealed = True
    assert m.test1.test2().test3 == 4
    with pytest.raises(AttributeError):
        m.test1.test3.test2


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
    m = SealedMock(SampleObject)

    m.attr_sample1 = 1
    m.attr_sample3 = 3

    m.sealed = True
    assert m.attr_sample1 == 1
    assert m.attr_sample3 == 3
    with pytest.raises(AttributeError):
        m.attr_sample2


def test_integration_with_spec_method_definition():
    """You need to defin the methods, even if they are in the spec"""
    m = SealedMock(SampleObject)

    m.method_sample1.return_value = 1

    m.sealed = True
    assert m.method_sample1() == 1
    with pytest.raises(AttributeError):
        m.method_sample2()


def test_integration_with_spec_method_definition_respects_spec():
    """You cannot define methods out of the spec"""
    m = SealedMock(SampleObject)

    with pytest.raises(AttributeError):
        m.method_sample3.return_value = 3
