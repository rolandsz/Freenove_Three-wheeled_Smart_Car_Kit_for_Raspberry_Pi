import logging
import generated.led_control_pb2_grpc
from generated.led_control_pb2 import SetColorResponse

logger = logging.getLogger(__name__)


class LedControlServicer(generated.led_control_pb2_grpc.LedControlServicer):

    def __init__(self, controller):
        self.controller = controller

    def SetColor(self, request, context):
        logger.info('Set color to R={} G={} B={}'.format(request.r, request.g, request.b))

        self.controller.write(self.controller.CMD_IO1, int(request.r))
        self.controller.write(self.controller.CMD_IO2, int(request.g))
        self.controller.write(self.controller.CMD_IO3, int(request.b))
        return SetColorResponse()
