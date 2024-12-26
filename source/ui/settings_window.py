from PySide6.QtWidgets import QMainWindow

class SettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings Window")
        self.setGeometry(200, 100, 800, 600)