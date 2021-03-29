from xuperchain.context import Context
from xuperchain.driver import Driver
from xuperchain.response import Response
from xuperchain.exception import MissingArgsException, ObjectNotFoundError, XuperException


#  类名暂未定

class Counter():
    def __init__(self):
        pass

    def Put(self, ctx: Context) -> Response:
        name=ctx.GetObject("name")
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

    def list(self, ctx: Context) -> Response:
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
