[![Build Status](https://travis-ci.org/Mariocj89/sealedmock.svg?branch=master)](https://travis-ci.org/Mariocj89/sealedmock)
# Sealed Mock
Small utility to ease the process of defining and working with mocks.

It allows you to stop the process of the mocks automatically creating
other mocks at any point.

SealedMock allows you to define a point in your test where the mocks provided
should stop generating mocks automatically preventing test pass when they call
attributes they should not have been called.

# Install
```pip install sealedmock```

# Usage

Given you have a file like:
```python
import urllib2

class SampleCodeClass(object):
    """This is sample code"""
    def calling_urlopen(self):
        return urllib2.urlopen("http://chooserandom.com")

    def calling_splithost(self):
        return urllib2.splithost("//host:port/path")
```

You can write a test like:
```python
@patch("tests.sample_code.urllib2")
def test_using_decorator(mock):
        sample = sample_code.SampleCodeClass()
        mock.urlopen.return_value = 2
        mock.sealed = True

        # calling urlopen succeeds as mock.urlopen has been defined
        assert sample.calling_urlopen()

        # This will fail as mock.splithost has not been defined
        sample.calling_splithost()
```
