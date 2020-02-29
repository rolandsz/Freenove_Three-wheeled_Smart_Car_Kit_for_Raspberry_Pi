import os
import grpc


def read_pem(file_path):
    with open(os.path.join(os.path.dirname(__file__), '..', file_path), 'r') as key_file:
        return key_file.read().encode('ascii')


class CarKey(grpc.AuthMetadataPlugin):

    def __init__(self, car_key):
        self.car_key = car_key

    def __call__(self, context, callback):
        callback((('x-car-key', self.car_key),), None)
