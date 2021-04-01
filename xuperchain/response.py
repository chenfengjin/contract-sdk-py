class BaseResponse():
    def __init__(self):
        # TODO raie exception
        pass

    @property
    def code(self):
        return self.code

    @property
    def msg(self):
        return self.msg

class MissingParameterResponse():
    pass

class PermissionDeniedResponse():
    pass

class ParameterValidateFailedResponse():
    pass
