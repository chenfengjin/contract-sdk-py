from xuperchain.context import Context
from xuperchain.contract import contract_pb2
from datetime import datetime

import logging


class NativeCodeServicer(object):
    """service provided by chain code, called by xchain
    """

    def __init__(self, channel):
        self.contract = None
        self.lastPing = datetime.now()
        self.channel = channel

    def Call(self, request: contract_pb2.NativeCallRequest, grpcctx):
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
            resp = f(ctx)
            # print(resp.body)
            resp = contract_pb2.Response(status=resp.status, message=resp.msg, body=resp.body.encode())
            ctx.SetOutput(resp)
        except Exception as e:
            status = 500
            logging.exception(e)
            msg = "method:{},msg:{}".format(method, str(e))
            resp = contract_pb2.Response(status=status, message=msg, body=None)
            ctx.SetOutput(resp)
        return contract_pb2.NativeCallResponse()

    def Ping(self, request, ctx):
        self.lastPing = datetime.now()
        return contract_pb2.PingResponse()

    def SetContract(self, contract):
        self.contract = contract
