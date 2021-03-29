class BaseResponse():
    def __init__(self):
        pass

class Response(BaseResponse):

    def __init__(self, msg=None, json=None,data=None,code=200):
        self.code = code
        self.msg = msg

class JSONResponse(Response):
    def __init__(self, obj, code=200):
        #  TODO
        f = lambda x:x
        self.code = code
        self.msg = f(obj)
