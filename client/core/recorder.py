import cv2
import logging
import os
import threading
import time
import pandas as pd

from datetime import datetime

logger = logging.getLogger(__name__)


class RecordSessionThread(threading.Thread):

    def __init__(self, parent):
        threading.Thread.__init__(self)
        self.is_running = False
        self.parent = parent
        self.lock = threading.Lock()
        self.batch = []
        self.annotations = []

        self.output_dir = os.path.join(parent.output_dir, str(self.stamp()))
        os.makedirs(self.output_dir, exist_ok=True)

        self.output_dir_frames = os.path.join(self.output_dir, 'frames')
        os.makedirs(self.output_dir_frames, exist_ok=True)

        logger.info('Record session thread initialized')
        logger.info('Output directory is "{}"'.format(self.output_dir))

    def enqueue(self, frame, properties):
        self.lock.acquire()

        try:
            self.batch.append((frame, properties))
        finally:
            self.lock.release()

    def commit(self):
        df = pd.DataFrame(self.annotations)
        df.to_csv(os.path.join(self.output_dir, 'annotations.csv'), index_label='sequence')

    @staticmethod
    def stamp():
        return int(datetime.utcnow().timestamp() * 1000 * 1000)

    def get_next_in_sequence(self):
        return len(self.annotations)

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
                sequence = self.get_next_in_sequence()

                annotation = {}

                for key, value in properties.items():
                    annotation[key] = value.get()

                cv2.imwrite(os.path.join(self.output_dir_frames, '{}.jpg'.format(sequence)), frame)
                self.annotations.append(annotation)

            time.sleep(1)

        self.commit()
        logger.info('Record session thread exited')


class Recorder:

    def __init__(self, output_dir):
        self.output_dir = output_dir
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
