import logging
import time

from PyQt5.QtCore import pyqtSignal
from generated.camera_control_pb2 import GetFrameRequest
from generated.camera_control_pb2_grpc import CameraControlStub
from utils.service import Service

logger = logging.getLogger(__name__)


class CameraService(Service):
    on_frame_ready = pyqtSignal(bytes)

    def __init__(self, app, channel, target_fps=8):
        super().__init__(app)
        self.target_fps = target_fps
        self.camera_control = CameraControlStub(channel)

    def update(self):
        start = time.time()

        response = self.camera_control.GetFrame(GetFrameRequest())
        frame = response.frame
        logger.debug('Received camera frame contains {} bytes'.format(len(frame)))

        self.on_frame_ready.emit(frame)

        end = time.time()
        sleep_for = (1 / self.target_fps) - (end - start)
        logger.debug('sleep_for={}'.format(sleep_for))

        if sleep_for > 0:
            time.sleep(sleep_for)
