import logging
import generated.buzzer_control_pb2_grpc
from generated.buzzer_control_pb2 import SetFrequencyResponse

logger = logging.getLogger(__name__)


class BuzzerControlServicer(generated.buzzer_control_pb2_grpc.BuzzerControlServicer):

    def __init__(self, controller):
        self.controller = controller

    def SetFrequency(self, request, context):
        logger.info('Set frequency to {} Hz'.format(request.frequency))

        self.controller.write(self.controller.CMD_BUZZER, request.frequency)
        return SetFrequencyResponse()
