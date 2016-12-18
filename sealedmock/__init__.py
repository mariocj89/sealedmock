"""Mock class that allows to whitelist
the methods that can be called

"""
import mock
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



class SealedMockAttributeAccess(AttributeError):
    """Attempted to access an attribute of a sealed mock"""


class SealedMock(mock.Mock):
    """A Mock that can be sealed at any point of time

    Once the mock is sealed it prevents any implicit mock creation

    To seal the mock call seled_mock.sealed = True

    :Example:

    >>> import sealedmock
    >>> m = sealedmock.SealedMock()
    >>> m.method1.return_value.attr1.method2.return_value = 1
    >>> m.sealed = True
    >>> m.method1().attr1.method2()
    >>> # 1
    >>> m.method1().attr2
    >>> # Exception: SealedMockAttributeAccess: mock.method1().attr2

    """
    def __init__(self, *args, **kwargs):
        super(SealedMock, self).__init__(*args, **kwargs)
        self.__dict__["_sealed"] = False

    def _get_child_mock(self, **kw):
        if self.sealed:
            attribute = "." + kw["name"] if "name" in kw else "()"
            mock_name = _extract_mock_name(self) + attribute
            raise SealedMockAttributeAccess(mock_name)
        else:
            return SealedMock(**kw)

    @property
    def sealed(self):
        """Attribute that marks whether the mock can be extended dynamically

        Once sealed is set to True no attribute that was not defined before can
        be accessed.
        :raises: SealedMockAttributeAccess
        """
        return self._sealed

    @sealed.setter
    def sealed(self, value):
        self._sealed = value
        for attr in dir(self):
            try:
                m = getattr(self, attr)
            except AttributeError:
                pass
            else:
                if isinstance(m, SealedMock):
                    m.sealed = value


patch = functools.partial(mock.patch, new_callable=SealedMock)

