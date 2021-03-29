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
            ctx.SetOutput("method {} not found".format(method))
            return
        f = getattr(self.contract, method)
        #     check
        try:
            out = f(ctx)
        except Exception as e:
            pass
        ctx.set_output(out)
        # Return JSON
        # return contract_pb2.NativeCallResponse

    def Ping(self, request, ctx):
        self.lastPing = datetime.now()
        return contract_pb2.PingResponse()

    def SetContract(self, contract):
        self.contract = contract
