import logging
import numpy as np
import generated.camera_control_pb2_grpc

from generated.camera_control_pb2 import SetRotationResponse
from hardware.controller import Controller
from utils.servo import angle_to_pwm

logger = logging.getLogger(__name__)


class CameraControlServicer(generated.camera_control_pb2_grpc.CameraControlServicer):

    def __init__(self, controller):
        self.controller = controller

    def SetRotation(self, request, context):
        logger.info('Set camera rotation to horizontal angle {} and vertical angle {}'.format(request.horizontal,
                                                                                              request.vertical))

        horizontal_angle = np.clip(request.horizontal, np.deg2rad(0), np.deg2rad(180))
        logger.debug('Normalized horizontal angle is {}'.format(horizontal_angle))

        vertical_angle = np.clip(request.vertical, np.deg2rad(90), np.deg2rad(180))
        logger.debug('Normalized vertical angle is {}'.format(vertical_angle))

        self.controller.write(Controller.CMD_SERVO2, angle_to_pwm(horizontal_angle))
        self.controller.write(Controller.CMD_SERVO3, angle_to_pwm(vertical_angle))
        return SetRotationResponse()
