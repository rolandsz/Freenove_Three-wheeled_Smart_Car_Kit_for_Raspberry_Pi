import logging
import argparse
import numpy as np
import pygame

from core.api_connection import ApiConnection
from core.video_stream import VideoStream

logger = logging.getLogger(__name__)


def main(args):
    logging.basicConfig(level=logging.DEBUG if args['verbose'] else logging.INFO)

    pygame.init()
    pygame.joystick.init()
    logger.debug('Number of available joysticks: {}'.format(pygame.joystick.get_count()))

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    with VideoStream(args['address'], args['stream_port']) as stream:
        with ApiConnection(args['address'], args['api_port'], args['car_key']) as api:
            is_running = True

            while is_running:
                for event in pygame.event.get():
                    logger.debug('Received event {}'.format(event))

                    if event.type == pygame.JOYAXISMOTION:
                        if event.axis == 1:
                            api.properties['car.velocity'].set(-event.value / 1.5)
                        if event.axis == 2:
                            angle = np.interp(-pow(event.value, 3), [-1, 1], [np.deg2rad(-60), np.deg2rad(60)])
                            api.properties['car.steering_angle'].set(angle)
                    elif event.type == pygame.JOYHATMOTION:
                        if event.value == (0, 1):
                            api.properties['camera.rotation'].set(np.deg2rad(0))
                        elif event.value == (-1, 0):
                            api.properties['camera.rotation'].set(np.deg2rad(90))
                        elif event.value == (1, 0):
                            api.properties['camera.rotation'].set(np.deg2rad(-90))
                    elif event.type == pygame.JOYBUTTONDOWN and event.button == 9:
                        is_running = False


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-a', '--address', default='raspberrypi', help='Address of the Raspberry PI')
    ap.add_argument('-ap', '--api-port', type=int, default=50051, help='Listening port of the API')
    ap.add_argument('-sp', '--stream-port', type=int, default=8080, help='Listening port of the MJPG stream')
    ap.add_argument('-ck', '--car-key', required=True, help='Key of the car')
    ap.add_argument('-v', '--verbose', help='Show all log messages', action='store_true')
    args = vars(ap.parse_args())

    main(args)
