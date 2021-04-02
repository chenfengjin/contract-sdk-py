from .contract_service.contract_service_pb2_grpc import SyscallStub
from .contract import contract_pb2 as contract__pb2

DEFAULT_CAP = 1024


class Context():
    def __init__(self, ctxid, channel):
        self.contractArgs = None
        self.header = contract__pb2.SyscallHeader(ctxid=ctxid)
        self.stub = SyscallStub(channel=channel)

        req = contract__pb2.GetCallArgsRequest(header=self.header)
        resp = self.stub.GetCallArgs(req)
        self.method = resp.method
        self.initiator = resp.initiator
        self.transfer_amoubnt = resp.transfer_amount

        # TODO @fengjin
        self.callArgs = {}
        for item in resp.args:
            self.callArgs[item.key] = item.value.decode()
        self.auth_require = resp.auth_require

    def PutObject(self, key, value):
        req = contract__pb2.PutRequest(header=self.header, key=key.encode(), value=value.encode())
        self.stub.PutObject(req)

    def GetObject(self, key: str):
        req = contract__pb2.GetRequest(header=self.header, key=key.encode())
        resp = self.stub.GetObject(req)
        return resp.value.decode()

    def DeleteObject(self, key):
        req = contract__pb2.DeleteRequest(header=self.header, key=key.encode())
        self.stub.DeleteObject(req)

    def QueryTx(self, txid):
        req = contract__pb2.QueryTxRequest(header=self.header, txid=txid)
        resp = self.stub.QueryTx(req)
        return resp.tx

    def QueryBlock(self, blockid):
        req = contract__pb2.QueryBlockRequest(header=self.header, blockid=blockid)
        resp = self.stub.QueryBlock(req)
        return resp.block

    def Iterator(self, start=None, limit=None, prefix=None):
        if prefix:
            start = prefix
            limit = prefix + "~"
        return KVIterator(start=start, limit=limit, ctx=self)

    def Args(self):
        return self.callArgs

    def Initiator(self):
        return self.initiator

    def Caller(self):
        return self.initiator

    def AuthRequire(self):
        self.callArgs.auth_require

    def Transfer(self, to, amount):
        req = contract__pb2.TransferRequest(header=self.header, to=to, amount=amount)
        resp = self.stub.Transfer(req)

    def TransferAmount(self):
        # TODO
        pass

    def Call(self, module, contract, method, args):
        args = [contract__pb2.ArgPair(key=key, value=value) for key, value in args.items()]
        req = contract__pb2.ContractCallRequest(header=self.header, contract=contract, module=module, method=method,
                                                args=args)
        resp = self.stub.ContractCall(req)
        return resp.response

    def CrossQuery(self, uri, args):
        argsPair = [contract__pb2.ArgPair(key=key, value=value) for key, value in args.items()]
        req = contract__pb2.CrossContractQueryRequest(header=self.header, uri=uri, args=argsPair)
        resp = self.stub.CrossContractQuery(req)

    def EmitEvent(self, name, body):
        # TODO
        req = contract__pb2.EmitEventRequest(header=self.header, name=name, body=body)
        self.stub.EmitEvent(req)

    def Log(self, msg, *args, **kwargs):
        # TODO add args and kwargs
        import logging
        import io
        # TODO 级别,位置，代码风格
        log_capture_string = io.StringIO()
        ch = logging.StreamHandler(log_capture_string)
        logger = logging.getLogger('root')
        logger.addHandler(ch)
        logger.error(msg, *args, **kwargs)
        entry = log_capture_string.getvalue()
        log_capture_string.close()
        print("entry:",entry)
        req = contract__pb2.PostLogRequest(header=self.header, entry=entry)
        # PostLog has response, but we just ignore it
        _ = self.stub.PostLog(req)

    def SetOutput(self, output):
        resp = contract__pb2.SetOutputRequest(header=self.header, response=output)
        self.stub.SetOutput(resp)


class KVIterator():
    def __init__(self, start, limit, ctx: Context):
        self.start = start
        self.limit = limit
        self.ctx = ctx
        self.idx = 0
        self.items = None
        self.newStart = None
        self._load()

    def __next__(self):
        if self.idx == len(self.items):
            raise StopIteration()
        #     self.items = None
        #     self.idx = 0
        #     try:
        #         self._load()
        #     except StopIteration as e:
        #         TODO  resource release here
        # raise StopIteration()
        item = self.items[self.idx]
        self.idx += 1
        # self.start = self.items[-1].value

        return item.key.decode(), item.value.decode()

    def __iter__(self):
        return self

    def _load(self):
        req = contract__pb2.IteratorRequest(header=self.ctx.header, start=self.start.encode(),
                                            limit=self.limit.encode(), cap=DEFAULT_CAP)
        resp = self.ctx.stub.NewIterator(req)
        if len(resp.items) == 0:
            raise StopIteration()

        self.items = resp.items
