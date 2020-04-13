import numpy as np
import os
import logging
import grpc

from core.property import PropertyUpdateThread, CarVelocityProperty, CarSteeringAngleProperty, CameraRotationProperty, \
    LedColorProperty

logger = logging.getLogger(__name__)


class CarKey(grpc.AuthMetadataPlugin):

    def __init__(self, car_key):
        self.car_key = car_key

    def __call__(self, context, callback):
        callback((('x-car-key', self.car_key),), None)


class ApiConnection:
    
    def __init__(self, address, port, car_key):
        self.address = address
        self.port = port
        self.car_key = car_key
        self.properties = {
            'car.velocity': CarVelocityProperty(0.0),
            'car.steering_angle': CarSteeringAngleProperty(0.0),
            'led.color': LedColorProperty([0, 255, 0]),
            'camera.rotation': CameraRotationProperty(0)
        }

    def __enter__(self):
        self.channel = self.create_client_channel()
        self.property_update_thread = PropertyUpdateThread(self.properties, self.channel)
        self.property_update_thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.property_update_thread.is_running = False
        self.property_update_thread.join()
        self.channel.close()

    @staticmethod
    def read_pem(file_path):
        with open(os.path.join(os.path.dirname(__file__), '..', file_path), 'r') as key_file:
            return key_file.read().encode('ascii')

    def create_client_channel(self):
        call_credentials = grpc.metadata_call_credentials(CarKey(self.car_key),
                                                          name='Virtual key for the car')

        channel_credentials = grpc.ssl_channel_credentials(self.read_pem('ssl/ca.pem'),
                                                           self.read_pem('ssl/client-key.pem'),
                                                           self.read_pem('ssl/client.pem'))

        composite_credentials = grpc.composite_channel_credentials(
            channel_credentials,
            call_credentials,
        )

        return grpc.secure_channel('{}:{}'.format(self.address, self.port), composite_credentials)
