from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout
from widgets.camera_widget import CameraWidget
from widgets.joystick_widget import JoystickWidget


class MainWidget(QWidget):

    class MainWidgetLayout(QGridLayout):
        def __init__(self, services):
            super().__init__()
            self.setAlignment(Qt.AlignLeft | Qt.AlignTop)

            self.addWidget(CameraWidget(services), 0, 0)
            self.addWidget(JoystickWidget(services), 1, 0)

    def __init__(self, services):
        super().__init__()
        self.setWindowTitle('Freenove Three-wheeled Smart Car Kit for Raspberry Pi')
        self.resize(1280, 720)
        self.setLayout(MainWidget.MainWidgetLayout(services))
