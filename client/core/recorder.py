import logging
import threading
import time

from core.dataset import DatasetWriter

logger = logging.getLogger(__name__)


class RecordSessionThread(threading.Thread):

    def __init__(self, parent):
        threading.Thread.__init__(self)
        self.is_running = False
        self.parent = parent
        self.lock = threading.Lock()
        self.batch = []
        self.writer = DatasetWriter(parent.datasets_dir)

        logger.info('Record session thread initialized')

    def enqueue(self, frame, properties):
        self.lock.acquire()

        try:
            self.batch.append((frame, properties))
        finally:
            self.lock.release()

    def flush(self):
        self.writer.flush()

    def run(self):
        self.is_running = True
        logger.info('Record session thread started')

        while self.is_running:
            self.lock.acquire()

            try:
                batch = self.batch
                self.batch = []
            finally:
                self.lock.release()

            logger.debug('Local batch size: {}'.format(len(batch)))

            for frame, properties in batch:
                self.writer.write(frame, properties)

            time.sleep(1)

        self.flush()
        logger.info('Record session thread exited')


class Recorder:

    def __init__(self, datasets_dir):
        self.datasets_dir = datasets_dir
        self.output_thread = None

    def enable(self):
        self.output_thread = RecordSessionThread(self)
        self.output_thread.start()

    def disable(self):
        self.output_thread.is_running = False
        self.output_thread.join()
        self.output_thread = None

    def is_enabled(self):
        return self.output_thread is not None

    def record(self, frame, properties):
        if self.is_enabled():
            self.output_thread.enqueue(frame, properties)
