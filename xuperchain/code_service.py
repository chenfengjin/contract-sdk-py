from xuperchain.context import Context
from xuperchain.contract import contract_pb2
from datetime import datetime
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

        if not hasattr(self.contract, method):
            # TODO body should be bytes
            resp = contract_pb2.Response(status=500,message="method {} not found".format(method),body=None)
            ctx.SetOutput(resp)
            return
        f = getattr(self.contract, method)
        #     check
        try:
            pass
            # TODO Add things here
            # out = f(ctx)
        except Exception as e:
            pass
        resp = contract_pb2.Response(status=500, message="method {} not found".format(method), body=None)
        ctx.set_output(resp)
        # Return JSON
        return contract_pb2.NativeCallResponse()

    def Ping(self, request, ctx):
        self.lastPing = datetime.now()
        return contract_pb2.PingResponse()

    def SetContract(self, contract):
        self.contract = contract
