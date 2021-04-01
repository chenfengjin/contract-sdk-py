import os
import sys
import grpc
from xuperchain.code_service import NativeCodeServicer
from xuperchain.contract_service.contract_service_pb2_grpc import  add_NativeCodeServicer_to_server
import  xuperchain.contract_service.contract_service_pb2 as contract_service_pb2
import threading
from datetime import datetime
from concurrent import futures

from urllib import parse

class Driver():
    def __init__(self):
        self.code_service = None

    def serve(self,contract: any):
        chain_addr = parse.urlparse(os.environ.get("XCHAIN_CHAIN_ADDR"))
        if not chain_addr.scheme=="tcp":
            pass

        code_port = os.environ.get("XCHAIN_CODE_PORT")
        channel = grpc.insecure_channel(chain_addr.netloc)

        code_service = NativeCodeServicer(channel = channel)
        code_service.SetContract(contract=contract)
        self.code_service = code_service

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        add_NativeCodeServicer_to_server(servicer=code_service,server=server)

        # refrection for grpcurl
        from grpc_reflection.v1alpha import reflection
        SERVICE_NAMES = (
            contract_service_pb2.DESCRIPTOR.services_by_name['NativeCode'].full_name,
            reflection.SERVICE_NAME,
        )
        reflection.enable_server_reflection(SERVICE_NAMES, server)

        server.add_insecure_port('[::]:' + code_port)  # ipv4?
        server.start()
        # TODO
        # timer = threading.Timer(1,self.check_health)
        # timer.daemon=True
        # timer.start()
        self.check_health()
        print("listen at {}".format(code_port))
        server.wait_for_termination()

    def check_health(self):
        # TODO @fengjin
        print("check health")
        if (datetime.now()-self.code_service.lastPing).total_seconds() > 5: # TODO
            print("loss ping from xchian,exit")
            os._exit(0)
        timer = threading.Timer(1,self.check_health)
        timer.daemon=True
        timer.start()
            
            
            
            
