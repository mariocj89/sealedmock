[![Build Status](https://travis-ci.org/Mariocj89/sealedmock.svg?branch=master)](https://travis-ci.org/Mariocj89/sealedmock)
[![PyPI Version](https://img.shields.io/pypi/v/sealedmock.svg)](https://pypi.python.org/pypi/sealedmock/)

# Sealed Mock
Whitelist the attributes/methods of your mocks instead of just letting it create new
mock objects.

SealedMock allows specify when you are done defining the mock, ensuring that
any unexpected call to the mock is cached.

Sample:
```python
import sealedmock
m = sealedmock.SealedMock()
m.method1.return_value.attr1.method2.return_value = 1
m.sealed = True
m.method1().attr1.method2()
# 1
m.method1().attr2
# Exception: SealedMockAttributeAccess: mock.method1().attr2
```


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
from sealedmock import patch
@patch("tests.sample_code.urllib2")
def test_using_decorator(mock):
        sample = sample_code.SampleCodeClass()
        mock.urlopen.return_value = 2

        mock.sealed = True  # No new attributes can be declared

        # calling urlopen succeeds as mock.urlopen has been defined
        assert sample.calling_urlopen()

        # This will fail as mock.splithost has not been defined
        sample.calling_splithost()
```

If you use an common Mock the second part will pass as it will create a
mock for you and return it. With SealedMock you can choose when to stop
that behaviour.

This is recursive so you can write:
```python
@patch("sample_code.secret")
def test_recursive(mock):
        sample = sample_code.SampleCodeClass()
        mock.secret.call1.call2.call3.return_value = 1
        mock.sealed = True  # No new attributes can be declared

        # If secret is not used as specified above it will fail
        # ex: if do_stuff also calls secret.call1.call9
        sample.do_stuff()
```


It also prevents typos on tests if used like this:
```python
@patch("sample_code.secret")
def test_recursive(mock):
        sample = sample_code.SampleCodeClass()

        sample.do_stuff()

        mock.sealed = True
        mock.asert_called_with(1)
        # Note the typo in asert (should be assert)
        # Sealed mock will rise, normal mock won't
```
