import logging
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame

from utils.service import Service
from PyQt5.QtCore import pyqtSignal
from pygame.event import EventType

logger = logging.getLogger(__name__)


class JoystickService(Service):
    on_input_ready = pyqtSignal(EventType)

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
