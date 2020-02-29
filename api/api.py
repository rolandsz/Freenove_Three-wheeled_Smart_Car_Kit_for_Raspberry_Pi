import argparse
import contextlib
import logging
import signal
import grpc

from concurrent import futures
from buzzer_control_servicer import BuzzerControlServicer
from camera_control_servicer import CameraControlServicer
from car_control_servicer import CarControlServicer
from generated.buzzer_control_pb2_grpc import add_BuzzerControlServicer_to_server
from generated.camera_control_pb2_grpc import add_CameraControlServicer_to_server
from generated.car_control_pb2_grpc import add_CarControlServicer_to_server
from generated.led_control_pb2_grpc import add_LedControlServicer_to_server
from generated.ultrasonic_control_pb2_grpc import add_UltrasonicControlServicer_to_server
from hardware.controller import Controller
from led_control_servicer import LedControlServicer
from ultrasonic_control_servicer import UltrasonicControlServicer
from utils.security import read_pem, CarKeyValidationInterceptor, get_car_key


@contextlib.contextmanager
def run_server(controller, port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1),
                         interceptors=(CarKeyValidationInterceptor(),))

    add_BuzzerControlServicer_to_server(BuzzerControlServicer(controller), server)
    add_CameraControlServicer_to_server(CameraControlServicer(controller), server)
    add_CarControlServicer_to_server(CarControlServicer(controller), server)
    add_LedControlServicer_to_server(LedControlServicer(controller), server)
    add_UltrasonicControlServicer_to_server(UltrasonicControlServicer(controller), server)

    server_credentials = grpc.ssl_server_credentials(
            [(read_pem('ssl/api-key.pem'), read_pem('ssl/api.pem'))],
            root_certificates=read_pem('ssl/ca.pem'),
            require_client_auth=True
    )

    server.add_secure_port('[::]:{}'.format(port), server_credentials)

    server.start()
    logging.info('Listening on port {}'.format(port))

    try:
        yield server
    finally:
        server.stop(0)


def main(args):
    logging.basicConfig(level=logging.DEBUG if args['verbose'] else logging.INFO)

    controller = Controller(0x18)

    logging.info('The key of the car is {}'.format(get_car_key()))

    with run_server(controller, args['port']):
        signal.pause()


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-p', '--port', type=int, default=50051, help='Listening port')
    ap.add_argument('-v', '--verbose', help='Show all log messages', action='store_true')
    args = vars(ap.parse_args())

    main(args)
