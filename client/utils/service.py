from PyQt5.QtCore import QThread


class Service(QThread):

    def __init__(self, app):
        super().__init__()
        self.running = False
        app.aboutToQuit.connect(self.stop)

    def run(self):
        self.running = True

        while self.running:
            self.update()

    def update(self):
        raise NotImplementedError()

    def stop(self):
        self.running = False
