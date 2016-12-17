"""Mock class that allows to whitelist
the methods that can be called

"""
import mock


class SealedMockAttributeAccess(AttributeError):
    """Attempted to access an attribute of a sealed mock"""


class SealedMock(mock.Mock):
    def __init__(self, *args, **kwargs):
        super(SealedMock, self).__init__(*args, **kwargs)
        self.__dict__["_sealed"] = False

    def _get_child_mock(self, **kw):
        if self.sealed:
            raise SealedMockAttributeAccess(kw.get("name", "__call__"))
        else:
            return SealedMock(**kw)

    @property
    def sealed(self):
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
