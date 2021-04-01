from xuperchain.context import Context
from xuperchain.driver import Driver
from xuperchain.contract_method import contract_method
from xuperchain.exception import MissingArgsException, ObjectNotFoundError, ErrPermissionDenied,XuperException


class Counter():

    @contract_method
    def initialize(self, ctx: Context):
        # TODO default value?
        creator = ctx.Args().get("creator",None)
        if not creator:
            raise MissingArgsException
        ctx.PutObject("name", ctx.Initiator())
        ctx.PutObject("creator",creator)
        return "ok"

    @contract_method
    def Increase(self, ctx: Context):
        key = ctx.Args().get("key")
        ctx.PutObject(key,"1")
        return "1"

    @contract_method
    def Get(self, ctx: Context):
        key = ctx.Args().get("key")
        name = ctx.GetObject(key)
        return name



    def Caller(self,ctx:Context):
        caller = ctx.Caller()
        return caller

    @contract_method
    def admin_method(self, ctx: Context):
        pass
    #     admin = ctx.GetObject("admin")
    #     caller = ctx.Initiator()
    #     if not admin == caller:
    #         raise ErrPermissionDenied
    #     pass

    # def Put(self, ctx: Context) -> Response:
    #     pass
    # # 抛出预定义异常
    # if permission_check_failed:  # 权限校验
    #     raise PermissionDeniedException
    # # 捕获 SDK 异常,日志记录并继续,some_key 可以不存在
    # try:
    #     ctx.GetObject("some_key")
    # except ObjectNotFoundError as e:
    #     ctx.Log("find error{},", args={}, kwargs={})
    #
    # #  key 必须存在，不然进程就应该退出，这种无需处理
    # # try:
    # ctx.GetObject("key_must_exist")
    # # except ObjectNotFoundError as e:
    # #     raise e
    #
    # # 可以自定义异常信息
    # if some_condition:
    #     raise XuperException(msg="custome exception")
    #
    # # 这SDK 将 msg 和 json 转换成 byte 作为合约调用的输出，byte 则直接作为调用输出
    # return Response(msg="ok")
    # # return Response(json={"status": "ok", "id": 1000})
    # # return Response(body=b"binady object")

    def list(self, ctx: Context):
        pass
        # prefix = ctx.Args().get("prefix", None)
        # if prefix is None:
        #     raise MissingArgsException
        # result = [key for key, _ in ctx.NewIterator(prefix=prefix)]
        #
        # return Response(json=result)


if __name__ == "__main__":
    # 这里传递类还是传递变量?
    Driver().serve(Counter())
