class XuperException():
    def __init__(self,msg=None):
        self.code=599
        self.msg=msg


class ErrPermissionDenied(XuperException):
    pass

class MissingArgsException(XuperException):
    def __init__(self):
        pass

class ObjectNotFoundError(XuperException):
    pass
