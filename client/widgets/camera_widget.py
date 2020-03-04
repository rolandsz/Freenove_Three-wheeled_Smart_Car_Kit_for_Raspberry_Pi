import logging
import time

from PyQt5.QtWidgets import QGroupBox, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread, pyqtSignal
from generated.camera_control_pb2 import GetFrameRequest
from generated.camera_control_pb2_grpc import CameraControlStub

logger = logging.getLogger(__name__)


class CameraWidget(QGroupBox):

    class CameraFrame(QLabel):

        def __init__(self, services, width=352, height=288):
            super().__init__()
            self.resize(width, height)

            services['camera'].on_frame_ready.connect(self.on_frame_ready)

        def on_frame_ready(self, frame):
            self.setPixmap(self.frame_to_pixmap(frame))

        @staticmethod
        def frame_to_pixmap(frame):
            pixmap = QPixmap()
            pixmap.loadFromData(frame)
            return pixmap

    def __init__(self, services):
        super().__init__('Camera')
        layout = QVBoxLayout()
        layout.addWidget(CameraWidget.CameraFrame(services))
        self.setLayout(layout)
