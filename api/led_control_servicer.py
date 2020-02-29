import logging
import generated.led_control_pb2_grpc

from generated.led_control_pb2 import SetColorResponse
from hardware.controller import Controller

logger = logging.getLogger(__name__)


class LedControlServicer(generated.led_control_pb2_grpc.LedControlServicer):

    def __init__(self, controller):
        self.controller = controller

    def SetColor(self, request, context):
        logger.info('Set color to R={} G={} B={}'.format(request.r, request.g, request.b))

        self.controller.write(Controller.CMD_IO1, int(not request.r))
        self.controller.write(Controller.CMD_IO2, int(not request.g))
        self.controller.write(Controller.CMD_IO3, int(not request.b))
        return SetColorResponse()
