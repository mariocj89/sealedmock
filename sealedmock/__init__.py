"""Mock class that allows to whitelist the methods that can be called"""
try:
    from unittest.mock import *
except ImportError:
    from mock import *
import functools
from ._version import __version__


def _extract_mock_name(in_mock):
    """Prints the mock access path

    Code from __repr__ code in mock.py

    Given a mock prints the whole access chain since the root mock
    """
    _name_list = [in_mock._mock_new_name]
    _parent = in_mock._mock_new_parent
    last = in_mock

    dot = '.'
    if _name_list == ['()']:
        dot = ''
    seen = set()
    while _parent is not None:
        last = _parent

        _name_list.append(_parent._mock_new_name + dot)
        dot = '.'
        if _parent._mock_new_name == '()':
            dot = ''

        _parent = _parent._mock_new_parent

        # use ids here so as not to call __hash__ on the mocks
        if id(_parent) in seen:
            break
        seen.add(id(_parent))

    _name_list = list(reversed(_name_list))
    _first = last._mock_name or 'mock'
    if len(_name_list) > 1:
        if _name_list[1] not in ('()', '().'):
            _first += '.'
    _name_list[0] = _first
    return ''.join(_name_list)


def _get_child_mock(mock, **kw):
    """Intercepts call to generate new mocks and raises instead"""
    attribute = "." + kw["name"] if "name" in kw else "()"
    mock_name = _extract_mock_name(mock) + attribute
    raise AttributeError(mock_name)


def _frankeinstainize(mock):
    """Given a mock dirty patches it to behave like a sealed mock

    I know... give me a better way to do this.
    """
    mock._get_child_mock = functools.partial(_get_child_mock, mock)


def seal(mock):
    """Disable the automatic generation of "submocks"

    Given an input Mock, seals it to ensure no further mocks will be generated
    when accessing an attribute that was not already defined.

    Submocks are defined as all mocks which were created DIRECTLY from the
    parent. If a mock is assigned to an attribute of an existing mock,
    it is not considered a submock.
    """
    _frankeinstainize(mock)
    for attr in dir(mock):
        try:
            m = getattr(mock, attr)
        except AttributeError:
            continue
        if not isinstance(m, NonCallableMock):
            continue
        if m._mock_new_parent is mock:
            seal(m)


