import logging
import threading
import time

from abc import ABC
from generated.camera_control_pb2 import SetCameraRotationRequest
from generated.camera_control_pb2_grpc import CameraControlStub
from generated.car_control_pb2 import SetVelocityRequest, SetSteeringAngleRequest
from generated.car_control_pb2_grpc import CarControlStub
from generated.led_control_pb2 import SetColorRequest
from generated.led_control_pb2_grpc import LedControlStub

logger = logging.getLogger(__name__)


class Property(ABC):

    def __init__(self, value):
        self.commit_value = None
        self.dirty_value = value

    def set(self, value):
        self.dirty_value = value

    def get(self):
        return self.dirty_value

    def commit(self, channel):
        raise NotImplementedError()


class PropertyUpdateThread(threading.Thread):

    def __init__(self, properties, channel):
        threading.Thread.__init__(self)
        self.properties = properties
        self.channel = channel
        self.is_running = False

    def run(self):
        self.is_running = True

        while self.is_running:
            needs_to_sleep = True

            for name, property in self.properties.items():
                if isinstance(property, Property):
                    # No locking, it does not matter if dirty_value changes in the meantime
                    if property.commit_value != property.dirty_value:
                        property.commit_value = property.dirty_value
                        property.commit(self.channel)
                        logging.debug('Committed property "{}" with value "{}"'.format(name, property.commit_value))
                        needs_to_sleep = False

            if needs_to_sleep:
                time.sleep(0.01)

        logger.debug('Property update thread exited')


class CarVelocityProperty(Property):

    def commit(self, channel):
        CarControlStub(channel).SetVelocity(SetVelocityRequest(velocity=self.commit_value))


class CarSteeringAngleProperty(Property):

    def commit(self, channel):
        CarControlStub(channel).SetSteeringAngle(SetSteeringAngleRequest(angle=self.commit_value))


class LedColorProperty(Property):

    def commit(self, channel):
        LedControlStub(channel).SetColor(SetColorRequest(r=self.commit_value[0],
                                                         g=self.commit_value[1],
                                                         b=self.commit_value[2]))


class CameraRotationProperty(Property):

    def commit(self, channel):
        CameraControlStub(channel).SetRotation(SetCameraRotationRequest(angle=self.commit_value))
