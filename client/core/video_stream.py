import logging
import cv2
import threading

logger = logging.getLogger(__name__)


class VideoStream:

    class CaptureThread(threading.Thread):

        def __init__(self, parent, address, port):
            threading.Thread.__init__(self)
            self.is_running = False
            self.parent = parent
            self.stream = cv2.VideoCapture('http://{}:{}/?action=stream'.format(address, port), cv2.CAP_FFMPEG)

            logger.debug('Capture thread initialized')

        def run(self):
            self.is_running = True
            logger.debug('Capture thread started')

            while self.is_running:
                ret, self.parent.current_frame = self.stream.read()
                self.is_running &= ret

            self.stream.release()
            logger.debug('Capture thread exited')

    class PlaybackThread(threading.Thread):

        def __init__(self, parent):
            threading.Thread.__init__(self)
            self.is_running = False
            self.parent = parent

            logger.debug('Playback thread initialized')

        def run(self):
            self.is_running = True
            logger.debug('Playback thread started')

            while self.is_running:
                if self.parent.current_frame is not None:
                    cv2.imshow('Video stream', self.parent.current_frame)
                    cv2.waitKey(1)

            cv2.destroyAllWindows()
            logger.debug('Playback thread exited')

    def __init__(self, address, port):
        self.current_frame = None
        self.capture_thread = VideoStream.CaptureThread(self, address, port)
        self.playback_thread = VideoStream.PlaybackThread(self)

    def __enter__(self):
        self.capture_thread.start()
        self.playback_thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.playback_thread.is_running = False
        self.playback_thread.join()

        self.capture_thread.is_running = False
        self.capture_thread.join()
