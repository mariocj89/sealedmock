"""Integration test for SealedMock"""
import pytest

from tests import sample_code
from sealedmock import patch


def test_using_context_manager():
    with patch("tests.sample_code.os") as mock:
        sample = sample_code.SampleCodeClass()
        mock.rm.return_value = 2
        mock.sealed = True

        assert sample.calling_rm() == 2
        with pytest.raises(AttributeError):
            sample.calling_pardir()


@patch("tests.sample_code.os")
def test_using_decorator(mock):
    sample = sample_code.SampleCodeClass()
    mock.rm.return_value = 2
    mock.sealed = True

    assert sample.calling_rm() == 2
    with pytest.raises(AttributeError):
        sample.calling_pardir()
