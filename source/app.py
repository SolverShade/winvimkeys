import sys
from PySide6.QtWidgets import QApplication
from source.controller.shortcut_controller import ShortcutController

def run():
    app = QApplication(sys.argv)
    controller = ShortcutController()
    controller.loadShortcutWindow()
    sys.exit(app.exec())