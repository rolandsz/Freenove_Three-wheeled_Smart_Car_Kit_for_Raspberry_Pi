import logging
import time

from PyQt5.QtWidgets import QGroupBox, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread, pyqtSignal
from generated.camera_control_pb2 import GetFrameRequest
from generated.camera_control_pb2_grpc import CameraControlStub

logger = logging.getLogger(__name__)


class CameraWidget(QGroupBox):

    class CameraStream(QLabel):

        class CameraFrameFetchThread(QThread):
            frame_ready = pyqtSignal(QPixmap)

            def __init__(self, channel, target_fps):
                super().__init__()
                self.running = False
                self.target_fps = target_fps
                self.camera_control = CameraControlStub(channel)

            def run(self):
                self.running = True

                while self.running:
                    start = time.time()

                    response = self.camera_control.GetFrame(GetFrameRequest())
                    frame = response.frame
                    logger.debug('Received camera frame contains {} bytes'.format(len(frame)))

                    self.frame_ready.emit(self.frame_to_pixmap(frame))

                    end = time.time()
                    sleep_for = (1 / self.target_fps) - (end - start)
                    logger.debug('sleep_for={}'.format(sleep_for))

                    if sleep_for > 0:
                        time.sleep(sleep_for)

            @staticmethod
            def frame_to_pixmap(frame):
                pixmap = QPixmap()
                pixmap.loadFromData(frame)
                return pixmap

            def stop(self):
                self.running = False

        def __init__(self, app, channel, width=352, height=288, target_fps=8):
            super().__init__()
            logger.debug('Initialized camera stream with parameters width={} height={} target_fps={}'.format(width, height, target_fps))

            self.resize(width, height)

            self.thread = CameraWidget.CameraStream.CameraFrameFetchThread(channel, target_fps)
            self.thread.frame_ready.connect(self.on_frame_ready)
            app.aboutToQuit.connect(self.thread.stop)
            self.thread.start()

        def on_frame_ready(self, frame):
            self.setPixmap(frame)

    def __init__(self, app, channel):
        super().__init__('Camera')
        layout = QVBoxLayout()
        layout.addWidget(CameraWidget.CameraStream(app, channel))
        self.setLayout(layout)
