"""Integration test for SealedMock"""
import pytest

from tests import sample_code
from sealedmock import patch
from mock import patch as patch2


def test_using_context_manager():
    with patch("tests.sample_code.urllib2") as mock:
        sample = sample_code.SampleCodeClass()
        mock.urlopen.return_value = 2
        mock.sealed = True

        assert sample.calling_urlopen() == 2
        with pytest.raises(AttributeError):
            sample.calling_splithost()


@patch("tests.sample_code.urllib2")
def test_using_decorator(mock):
        sample = sample_code.SampleCodeClass()
        mock.urlopen.return_value = 2
        mock.sealed = True

        assert sample.calling_urlopen() == 2
        with pytest.raises(AttributeError):
            sample.calling_splithost()
