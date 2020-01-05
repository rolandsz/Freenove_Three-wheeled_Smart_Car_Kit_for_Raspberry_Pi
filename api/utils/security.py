import hashlib
import os
import re
import grpc

from functools import lru_cache


def read_pem(file_path):
    with open(os.path.join(os.path.dirname(__file__), '..', file_path), 'r') as pem_file:
        return pem_file.read().encode('ascii')


@lru_cache(maxsize=1)
def get_car_key():
    with open('/proc/cpuinfo', 'r') as cpuinfo:
        match = re.search('Serial\s+:\s+(.+)', cpuinfo.read())

        if match:
            serial = 'car-key-{}'.format(match.group(1)).encode('utf-8')
            return hashlib.sha256(serial).hexdigest()

    return None


class CarKeyValidationInterceptor(grpc.ServerInterceptor):

    def __init__(self):
        def abort(request, context):
            context.abort(grpc.StatusCode.UNAUTHENTICATED, 'Invalid car key')

        self.abort_handler = grpc.unary_unary_rpc_method_handler(abort)

    def intercept_service(self, continuation, handler_call_details):
        if ('x-car-key', get_car_key()) in handler_call_details.invocation_metadata:
            return continuation(handler_call_details)
        else:
            return self.abort_handler
