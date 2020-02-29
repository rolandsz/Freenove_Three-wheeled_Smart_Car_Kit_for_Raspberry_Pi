from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout
from widgets.camera_widget import CameraWidget


class MainWidget(QWidget):

    class MainWidgetLayout(QGridLayout):
        def __init__(self, app, channel):
            super().__init__()
            self.setAlignment(Qt.AlignLeft | Qt.AlignTop)

            self.addWidget(CameraWidget(app, channel), 1, 0)

    def __init__(self, app, channel):
        super().__init__()
        self.setWindowTitle('Freenove Three-wheeled Smart Car Kit for Raspberry Pi')
        self.resize(1280, 720)
        self.setLayout(MainWidget.MainWidgetLayout(app, channel))
