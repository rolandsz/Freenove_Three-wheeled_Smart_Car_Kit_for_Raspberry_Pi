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

            logger.info('Capture thread initialized')

        def run(self):
            self.is_running = True
            logger.info('Capture thread started')

            while self.is_running:
                ret, frame = self.stream.read()

                if ret:
                    self.parent.on_new_frame(frame)

                self.is_running &= ret

            self.stream.release()
            logger.info('Capture thread exited')

    class PlaybackThread(threading.Thread):

        def __init__(self, parent):
            threading.Thread.__init__(self)
            self.is_running = False
            self.parent = parent
            self.parent.register_callback(self.on_new_frame)
            self.last_frame = None

            logger.info('Playback thread initialized')

        def on_new_frame(self, frame):
            self.last_frame = frame

        def run(self):
            self.is_running = True
            logger.info('Playback thread started')

            while self.is_running:
                while self.last_frame is not None:
                    cv2.imshow('Video stream', self.last_frame)
                    cv2.waitKey(16)

            cv2.destroyAllWindows()
            logger.info('Playback thread exited')

    def __init__(self, address, port):
        self.frame = None
        self.callbacks = []
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

    def register_callback(self, cb):
        if not callable(cb):
            logger.error('The provided callback is not callable')
            return

        self.callbacks.append(cb)
        logger.debug('Added new callback: {}'.format(cb))

    def on_new_frame(self, frame):
        for callback in self.callbacks:
            callback(frame)
