import logging

from PyQt5.QtWidgets import QGroupBox, QLabel, QVBoxLayout

logger = logging.getLogger(__name__)


class JoystickWidget(QGroupBox):

    class LastJoystickEvent(QLabel):

        def __init__(self, services):
            super().__init__()
            services['joystick'].on_input_ready.connect(self.on_input_ready)

        def on_input_ready(self, event):
            self.setText(str(event))

    def __init__(self, services):
        super().__init__('Joystick')
        layout = QVBoxLayout()
        layout.addWidget(JoystickWidget.LastJoystickEvent(services))
        self.setLayout(layout)
