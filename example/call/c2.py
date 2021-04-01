from xuperchain.context import Context
from xuperchain.driver import Driver
from xuperchain.contract_method import contract_method
from xuperchain.exception import MissingArgsException, ObjectNotFoundError, ErrPermissionDenied, XuperException


class C2():

    @contract_method
    def initialize(self, ctx: Context):
        return "ok"
    def invoke(self,ctx:Context):
        return "I am c2"
        # to = ctx.GetObject("to")
        # try:
            # value = ctx.GetObject("to")
        # except:
        #     value = "0"
        # ctx.Transfer(to,amount=1)
        # ctx.Call("native")



if __name__ == "__main__":
    # 这里传递类还是传递变量?
    Driver().serve(C2())
