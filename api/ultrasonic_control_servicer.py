import logging
import generated.ultrasonic_control_pb2_grpc

from generated.ultrasonic_control_pb2 import GetDistanceResponse, SetUltrasonicRotationResponse
from hardware.controller import Controller
from utils.servo import clip_horizontal_angle, angle_to_pwm

logger = logging.getLogger(__name__)


class UltrasonicControlServicer(generated.ultrasonic_control_pb2_grpc.UltrasonicControlServicer):

    def __init__(self, controller):
        self.controller = controller

    def SetRotation(self, request, context):
        logger.info('Set ultrasonic rotation to horizontal angle {}'.format(request.horizontal))

        horizontal_angle = clip_horizontal_angle(request.horizontal)
        logger.debug('Clipped horizontal angle is {}'.format(horizontal_angle))

        self.controller.write(Controller.CMD_SERVO2, angle_to_pwm(horizontal_angle))
        return SetUltrasonicRotationResponse()

    def GetDistance(self, request, context):
        logger.info('Get distance')

        echo_time = self.controller.read(Controller.CMD_SONIC)
        distance = echo_time * 17.0 / 1000.0

        return GetDistanceResponse(distance=distance)
