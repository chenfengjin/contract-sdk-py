class Response:
    def __init__(self, status, msg="", body=""):
        self.status = status
        self.msg = msg
        self.body = body

    @staticmethod
    def ok(body):
        return Response(status=200, body=body)

    @staticmethod
    def error(msg):
        return Response(status=500, body=msg)
