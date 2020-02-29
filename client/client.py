import sys
import contextlib
import logging
import grpc
import argparse

from PyQt5.QtWidgets import QApplication
from widgets.main_widget import MainWidget
from utils.security import CarKey, read_pem


@contextlib.contextmanager
def create_client_channel(host, car_key):
    call_credentials = grpc.metadata_call_credentials(CarKey(car_key), name='Virtual key for the car')

    channel_credentials = grpc.ssl_channel_credentials(read_pem('ssl/ca.pem'),
                                                       read_pem('ssl/client-key.pem'),
                                                       read_pem('ssl/client.pem'))

    composite_credentials = grpc.composite_channel_credentials(
        channel_credentials,
        call_credentials,
    )

    yield grpc.secure_channel(host, composite_credentials)


def main(args):
    logging.basicConfig(level=logging.DEBUG if args['verbose'] else logging.INFO)

    app = QApplication(sys.argv)

    with create_client_channel('{}:{}'.format(args['address'], args['port']), args['car_key']) as channel:
        main_widget = MainWidget(channel)
        main_widget.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-a', '--address', default='raspberrypi', help='Address of the Raspberry PI')
    ap.add_argument('-p', '--port', type=int, default=50051, help='Listening port of the API')
    ap.add_argument('-ck', '--car-key', required=True, help='Key of the car')
    ap.add_argument('-v', '--verbose', help='Show all log messages', action='store_true')
    args = vars(ap.parse_args())

    main(args)
