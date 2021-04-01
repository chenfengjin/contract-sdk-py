from xuperchain.context import Context
from xuperchain.driver import Driver
from xuperchain.contract_method import contract_method
from xuperchain.exception import MissingArgsException, ObjectNotFoundError, ErrPermissionDenied, XuperException


class C1():

    @contract_method
    def initialize(self, ctx: Context):
        return "ok"
    @contract_method
    def invoke(self,ctx:Context):
        # to = ctx.GetObject("to")
        # ctx.Transfer(to,1)
        # contract = ctx.Args().get("contract")
        # if contract
        args= {}
        resp = ctx.Call(module="native",contract="c2",method="invoke",args=args)
        return resp.body
        # ctx.PutObject("call",resp.body)

if __name__ == "__main__":
    # 这里传递类还是传递变量?
    Driver().serve(C1())
