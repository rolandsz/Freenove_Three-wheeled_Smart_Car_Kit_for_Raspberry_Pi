import logging
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
        logger.info('Set camera rotation to horizontal angle {} and vertical angle {}'.format(request.horizontal,
                                                                                              request.vertical))

        horizontal_angle = clip_horizontal_angle(request.horizontal)
        logger.debug('Clipped horizontal angle is {}'.format(horizontal_angle))

        vertical_angle = clip_vertical_angle(request.vertical)
        logger.debug('Clipped vertical angle is {}'.format(vertical_angle))

        self.controller.write(Controller.CMD_SERVO2, angle_to_pwm(horizontal_angle))
        self.controller.write(Controller.CMD_SERVO3, angle_to_pwm(vertical_angle))
        return SetCameraRotationResponse()
