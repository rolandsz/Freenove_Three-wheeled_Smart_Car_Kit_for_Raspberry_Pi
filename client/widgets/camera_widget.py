import logging
import threading
import time

from PyQt5.QtWidgets import QGroupBox, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from generated.camera_control_pb2 import GetFrameRequest
from generated.camera_control_pb2_grpc import CameraControlStub

logger = logging.getLogger(__name__)


class CameraWidget(QGroupBox):

    class CameraStream(QLabel):

        class CameraFrame(QPixmap):
            def __init__(self, frame):
                super().__init__()
                self.loadFromData(frame)

        def __init__(self, channel, width=352, height=288, fps=8):
            super().__init__()
            logger.debug('Initialized camera stream with parameters width={} height={} fps={}'.format(width, height, fps))

            self.resize(width, height)
            self.fps = fps

            self.camera_control = CameraControlStub(channel)

            self.fetch_thread = threading.Thread(target=self.fetch_frame)
            self.fetch_thread.start()

        def fetch_frame(self):
            while True:
                response = self.camera_control.GetFrame(GetFrameRequest())
                frame = response.frame
                logger.debug('Received camera frame contains {} bytes'.format(len(frame)))

                self.setPixmap(CameraWidget.CameraStream.CameraFrame(frame))

                time.sleep(1 / self.fps)

    def __init__(self, channel):
        super().__init__('Camera')
        layout = QVBoxLayout()
        layout.addWidget(CameraWidget.CameraStream(channel))
        self.setLayout(layout)
