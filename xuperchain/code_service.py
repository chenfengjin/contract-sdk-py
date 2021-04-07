from xuperchain.context import Context
from xuperchain.contract import contract_pb2
from datetime import datetime
from xuperchain.exception import XuperException

import logging


class NativeCodeServicer(object):
    """service provided by chain code, called by xchain
    """

    def __init__(self, channel):
        self.contract = None
        self.lastPing = datetime.now()
        self.channel = channel

    def Call(self, request: contract_pb2.NativeCallRequest, ctx):
        """Missing associated documentation comment in .proto file."""
        ctxid = request.ctxid
        ctx = Context(ctxid=ctxid, channel=self.channel)

        method = ctx.method
        found = True

        if not hasattr(self.contract, method):
            found = False
        f = getattr(self.contract, method)
        if not f.__name__ == "contract_method_wraper":
            found = False
        if not found:
            resp = contract_pb2.Response(status=500, message="method {} not found".format(method), body=None)
            ctx.SetOutput(resp)
            return contract_pb2.NativeCallResponse()
        try:
            out = f(ctx)
            if type(out) == type(""):
                out = out.encode()

            if not type(out) == type(bytes("", "UTF-8")):
                import json
                # TODO @fegjin
                out = json.dumps(out).encode()
            resp = contract_pb2.Response(status=200, message=None, body=out)

            ctx.SetOutput(resp)

        except Exception as e:
            if isinstance(e, XuperException):
                status = 501
                msg = e.msg
            else:
                status = 502

                logging.exception(e)
                msg = "method:{},msg:{}".format(method,str(e))  # error message should not be longer than 1000, which may cause problems
            resp = contract_pb2.Response(status=status, message=msg, body=None)
            ctx.SetOutput(resp)
        return contract_pb2.NativeCallResponse()

    def Ping(self, request, ctx):
        self.lastPing = datetime.now()
        return contract_pb2.PingResponse()

    def SetContract(self, contract):
        self.contract = contract
