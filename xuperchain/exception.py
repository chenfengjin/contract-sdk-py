class XuperException():
    def __init__(self,msg=None):
        self._code=500
        self._msg=msg

    @property
    def status(self):
        return self._code
    @property
    def msg(self):
        return self._msg

class ErrPermissionDenied(XuperException):
    pass

class MissingArgsException(XuperException):
    def __init__(self):
        pass

class ObjectNotFoundError(XuperException):
    pass

