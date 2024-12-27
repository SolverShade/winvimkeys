import sys
from PySide6.QtWidgets import QApplication
from source.view.shortcut_window import ShortcutWindow
from source.controller.shortcut_controller import ShortcutController

def run():
    app = QApplication(sys.argv)
    controller = ShortcutController()
    controller.load_shortcut_window()
    sys.exit(app.exec())