import logging
import numpy as np
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame

from utils.provider import Service
from PyQt5.QtCore import pyqtSignal
from pygame.event import EventType

logger = logging.getLogger(__name__)


class JoystickProvider(Service):
    on_input_ready = pyqtSignal(EventType)
    on_velocity_ready = pyqtSignal(float)
    on_steering_angle_ready = pyqtSignal(float)

    def __init__(self, app, id=0):
        super().__init__(app)
        pygame.init()
        pygame.joystick.init()
        logger.debug('Number of available joysticks: {}'.format(pygame.joystick.get_count()))

        self.joystick = pygame.joystick.Joystick(id)
        self.joystick.init()

    def update(self):
        while self.running:
            for event in pygame.event.get():
                logger.debug('Received joystick event: {}'.format(event))
                self.on_input_ready.emit(event)

                if event.type == pygame.JOYAXISMOTION:
                    if event.axis == 1:
                        self.on_velocity_ready.emit(-event.value)
                    if event.axis == 2:
                        angle = np.interp(-pow(event.value, 3), [-1, 1], [np.deg2rad(30), np.deg2rad(150)])
                        self.on_steering_angle_ready.emit(angle)
