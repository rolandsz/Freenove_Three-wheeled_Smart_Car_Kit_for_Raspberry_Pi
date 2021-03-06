import os
import cv2
import pandas as pd
import numpy as np

from datetime import datetime


class Dataset:
    def __init__(self, datasets_dir, stamp):
        self.datasets_dir = datasets_dir
        self.stamp = stamp

    def get_dataset_directory_path(self):
        return os.path.join(self.datasets_dir, str(self.stamp))

    @staticmethod
    def get_frame_filename(sequence):
        return '{}.jpg'.format(sequence)

    def get_frames_directory_path(self):
        return os.path.join(self.get_dataset_directory_path(), 'frames')

    def get_frame_jpg_path(self, sequence):
        return os.path.join(self.get_frames_directory_path(), self.get_frame_filename(sequence))

    def get_annotations_csv_path(self):
        return os.path.join(self.get_dataset_directory_path(), 'annotations.csv')


class DatasetWriter(Dataset):

    def __init__(self, datasets_dir):
        super().__init__(datasets_dir, self.stamp())
        self.annotations = []

        self.ensure_directories_exist()

    def ensure_directories_exist(self):
        os.makedirs(self.get_dataset_directory_path(), exist_ok=True)
        os.makedirs(self.get_frames_directory_path(), exist_ok=True)

    @staticmethod
    def stamp():
        return int(datetime.utcnow().timestamp() * 1000 * 1000)

    def get_next_in_sequence(self):
        return len(self.annotations)

    def write_frame(self, sequence, frame):
        cv2.imwrite(self.get_frame_jpg_path(sequence), frame)

    def write_annotation(self, sequence, properties):
        annotation = {}

        for key, value in properties.items():
            annotation[key] = value.get()

        self.annotations.append(annotation)

    def write(self, frame, properties):
        sequence = self.get_next_in_sequence()
        self.write_frame(sequence, frame)
        self.write_annotation(sequence, properties)

    def flush(self):
        df = pd.DataFrame(self.annotations)
        df.to_csv(self.get_annotations_csv_path(), index_label='sequence')


class DatasetReader(Dataset):

    def __init__(self, datasets_dir, stamp, batch_size=60):
        super().__init__(datasets_dir, stamp)
        self.annotations = pd.read_csv(self.get_annotations_csv_path(), index_col='sequence')
        self.batch_size = batch_size
        self.X = None
        self.y = None
        self.sequence = 0

    def first(self):
        initial_batch = self.annotations.iloc[0:self.batch_size]

        if initial_batch.shape[0] == self.batch_size:
            X = []
            y = []

            for sequence, annotation in initial_batch.iterrows():
                X.append(self.read_frame(sequence))
                y.append([annotation['car.velocity'], annotation['car.steering_angle']])

            self.X = np.array(X)
            self.y = np.array(y)

            self.sequence = self.batch_size

        return self.X, self.y

    def next(self):
        if self.sequence == self.annotations.shape[0]:
            return None

        self.X = np.delete(self.X, 0, axis=0)
        self.X = np.append(self.X, [self.read_frame(self.sequence)], axis=0)

        self.y = np.delete(self.y, 0, axis=0)

        annotation = self.annotations.iloc[self.sequence]
        self.y = np.append(self.y, [[annotation['car.velocity'], annotation['car.steering_angle']]], axis=0)

        self.sequence += 1
        return self.X, self.y

    def num_batches(self):
        return self.annotations.shape[0] - self.batch_size + 1

    def read_frame(self, sequence):
        return cv2.imread(self.get_frame_jpg_path(sequence))
