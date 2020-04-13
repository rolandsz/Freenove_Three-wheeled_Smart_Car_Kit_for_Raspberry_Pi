import os
import cv2
import pandas as pd

from datetime import datetime


class Dataset:
    FRAMES_DIRECTORY = 'frames'

    def __init__(self, datasets_dir, stamp):
        self.datasets_dir = datasets_dir
        self.stamp = stamp

    def get_dataset_directory_path(self):
        return os.path.join(self.datasets_dir, str(self.stamp))

    @staticmethod
    def get_frame_filename(sequence):
        return '{}.jpg'.format(sequence)

    def get_frames_directory_path(self):
        return os.path.join(self.get_dataset_directory_path(), Dataset.FRAMES_DIRECTORY)

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
        annotation = {
            'frame': '{}/{}.jpg'.format(Dataset.FRAMES_DIRECTORY, sequence)
        }

        for key, value in properties.items():
            annotation[key] = value.get()

        self.annotations.append(annotation)

    def write(self, frame, properties):
        sequence = self.get_next_in_sequence()
        self.write_frame(sequence, frame)
        self.write_annotation(sequence, properties)

    def flush(self):
        df = pd.DataFrame(self.annotations)
        df.to_csv(self.get_annotations_csv_path(), index=False)
