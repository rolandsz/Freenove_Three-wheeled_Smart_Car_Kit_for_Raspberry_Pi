import logging
import numpy as np
import threading
import generated.camera_control_pb2_grpc

from generated.camera_control_pb2 import SetCameraRotationResponse
from hardware.controller import Controller
from utils.servo import angle_to_pwm, clip_horizontal_angle, clip_vertical_angle

logger = logging.getLogger(__name__)


class CameraControlServicer(generated.camera_control_pb2_grpc.CameraControlServicer):

    def __init__(self, controller):
        self.controller = controller

    def SetRotation(self, request, context):
        logger.info('Set camera rotation to angle {}'.format(request.angle))

        angle = request.angle
        angle = np.clip(request.angle, np.deg2rad(-90), np.deg2rad(90))
        angle = np.interp(angle, [np.deg2rad(-90), np.deg2rad(90)], [np.deg2rad(0), np.deg2rad(180)])

        logger.debug('Normalized camera angle is {}'.format(angle))

        self.controller.write(Controller.CMD_SERVO2, angle_to_pwm(angle))
        return SetCameraRotationResponse()
