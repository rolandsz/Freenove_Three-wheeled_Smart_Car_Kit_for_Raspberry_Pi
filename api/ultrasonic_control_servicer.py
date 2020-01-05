import logging
import generated.ultrasonic_control_pb2_grpc

from generated.ultrasonic_control_pb2 import GetDistanceResponse
from hardware.controller import Controller

logger = logging.getLogger(__name__)


class UltrasonicControlServicer(generated.ultrasonic_control_pb2_grpc.UltrasonicControlServicer):

    def __init__(self, controller):
        self.controller = controller

    def GetDistance(self, request, context):
        logger.info('Get distance')

        echo_time = self.controller.read(Controller.CMD_SONIC)
        distance = echo_time * 17.0 / 1000.0

        return GetDistanceResponse(distance=distance)
