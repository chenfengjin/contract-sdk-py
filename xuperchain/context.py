from xuperchain.contract_service.contract_service_pb2_grpc import SyscallStub
from xuperchain.contract import contract_pb2 as contract__pb2

DEFAULT_CAP = 1024


class Context():
    def __init__(self, ctxid, channel):
        self.contractArgs = None
        header = contract__pb2.SyscallHeader(ctxid=ctxid)
        self.header = header
        self.stub = SyscallStub(channel=channel)
        req = contract__pb2.GetCallArgsRequest(header=header)
        resp = self.stub.GetCallArgs(req)
        #     # TODO 这里得重写
        self.method = resp.method
        self.initiator = resp.initiator
        # TODO @fengjin
        self.callArgs = contract__pb2.CallArgs
        self.transfer_amoubnt = resp.transfer_amount
        # for key, value in resp.args:
        #     self.callArgs[key] = value
        self.auth_require = resp.auth_require

    def PutObject(self, key, value):
        req = contract__pb2.PutRequest(header=self.header, key=key, value=value)
        self.stub.PutObject(req)

    def GetObject(self, key):
        req = contract__pb2.GetRequest(header=self.header, key=key)
        resp = self.stub.GetObject(req)

    def DeleteObject(self, key):
        req = contract__pb2.DeleteRequest(header=self.header, key=key)
        resp = self.stub.DeleteObject(req)

    def QueryTx(self, txid):
        req = contract__pb2.QueryTxRequest(header=self.header, txid=txid)
        resp = self.stub.QueryTx(req)

    def QueryBlock(self, blockid):
        req = contract__pb2.QueryBlockRequest(header=self.header, blockid=blockid)

    def Intertor(self, start=None, stop=None, include_stop=False, prefix=None):
        if include_stop:
            # TODO @fengjin
            stop = "xxx"
        if prefix:
            start = prefix
            stop = prefix + "~"
        return KVIterator(start=start, stop=stop, include_stop=include_stop)

    def Args(self):
        return self.callArgs

    def Initiator(self):
        return self.callArgs.initiator

    def Caller(self):
        return self.callArgs.initiator

    def AuthRequire(self):
        self.callArgs.auth_require

    def Transfer(self, to, amount):
        req = contract__pb2.TransferRequest(header=self.header, to=to, amount=amount)
        resp = self.stub.Transfer(req)

    def TransferAmount(self):
        # TODO
        pass

    def Call(self, module, contract, method, args):
        argsPair = [contract__pb2.ArgPair(key=key, value=value) for key, value in args.items()]
        req = contract__pb2.ContractCallRequest(header=self.header, module=module, method=method, args=argsPair)
        resp = self.stub.ContractCall(req)

    def CrossQuery(self, uri, args):
        argsPair = [contract__pb2.ArgPair(key=key, value=value) for key, value in args.items()]
        req = contract__pb2.CrossContractQueryRequest(header=self.header, uri=uri, args=argsPair)
        resp = self.stub.CrossContractQuery(req)

    def EmitEvent(self, name, body, json=None):
        req = contract__pb2.EmitEventRequest(header=self.header, name=name, body=body)
        resp = self.stub.EmitEvent(req)

    # def EmitJSONEvent(self):
    #     pass

    def Logf(self, entry):
        # TODO
        req = contract__pb2.PostLogRequest(header=self.header, entry=entry)
        self.stub.PostLog(req)

    def SetOutput(self,output):
         contract__pb2.SetOutputRequest(header = self.header,resp = output)

class KVIterator():
    def __init__(self, start, stop, ctx: Context):
        self.start = start
        self.stop = stop
        self.ctx = ctx
        self.idx = 0
        self.buffer = None
        self._load()

    def __next__(self):
        #     TODO
        if self.idx > len(self.buffer):
            self.__load__()
        self.idx += 1
        return self.buffer[self.idx]

    def _load(self):
        req = contract__pb2.IteratorRequest(header=self.ctx.header, start=self.start, limit=self.limit, cap=DEFAULT_CAP)
        resp = self.ctx.stub.NewIterator(req)
