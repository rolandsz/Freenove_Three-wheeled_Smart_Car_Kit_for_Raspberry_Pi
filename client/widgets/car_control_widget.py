import logging

from PyQt5.QtWidgets import QGroupBox, QLabel, QVBoxLayout

from generated.car_control_pb2 import SetVelocityRequest, SetSteeringAngleRequest
from generated.car_control_pb2_grpc import CarControlStub

logger = logging.getLogger(__name__)


class CarControlWidget(QGroupBox):

    class CarControlDecision(QLabel):

        def __init__(self, services, channel):
            super().__init__()
            self.car_control = CarControlStub(channel)

            services['joystick'].on_velocity_ready.connect(self.on_velocity_ready)
            services['joystick'].on_steering_angle_ready.connect(self.on_steering_angle_ready)

        def on_velocity_ready(self, velocity):
            self.setText('Velocity = {}'.format(velocity))
            self.car_control.SetVelocity(SetVelocityRequest(velocity=velocity / 1.5))

        def on_steering_angle_ready(self, angle):
            self.setText('Steering angle = {}'.format(angle))
            self.car_control.SetSteeringAngle(SetSteeringAngleRequest(angle=angle))

    def __init__(self, services, channel):
        super().__init__('Car control')
        layout = QVBoxLayout()
        layout.addWidget(CarControlWidget.CarControlDecision(services, channel))
        self.setLayout(layout)
