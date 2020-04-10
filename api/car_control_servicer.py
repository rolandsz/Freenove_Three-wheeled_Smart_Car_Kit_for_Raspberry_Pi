import logging
import numpy as np
import generated.car_control_pb2_grpc

from generated.car_control_pb2 import SetVelocityResponse, SetSteeringAngleResponse
from hardware.controller import Controller
from utils.servo import angle_to_pwm

logger = logging.getLogger(__name__)


class CarControlServicer(generated.car_control_pb2_grpc.CarControlServicer):

    def __init__(self, controller):
        self.controller = controller

    def SetVelocity(self, request, context):
        logger.info('Set velocity to {}'.format(request.velocity))

        direction = Controller.DIRECTION_FORWARD if request.velocity > 0 else Controller.DIRECTION_BACKWARD
        speed = np.clip(abs(request.velocity), 0.0, 1.0)
        pwm = int(speed * 1000)

        logger.debug('Resolved velocity {} to direction {} and speed {}'.format(request.velocity, direction, speed))

        self.controller.write(Controller.CMD_DIR1, direction)
        self.controller.write(Controller.CMD_DIR2, direction)
        self.controller.write(Controller.CMD_PWM1, pwm)
        self.controller.write(Controller.CMD_PWM2, pwm)

        return SetVelocityResponse()

    def SetSteeringAngle(self, request, context):
        logger.info('Set steering angle to {}'.format(request.angle))

        angle = np.clip(request.angle, np.deg2rad(-60), np.deg2rad(60))
        angle = np.interp(angle, [np.deg2rad(-60), np.deg2rad(60)], [np.deg2rad(30), np.deg2rad(150)])

        logger.debug('Normalized steering angle is {}'.format(angle))

        self.controller.write(Controller.CMD_SERVO1, angle_to_pwm(angle))
        return SetSteeringAngleResponse()
