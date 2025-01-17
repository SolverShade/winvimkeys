import sys
from PySide6.QtWidgets import QApplication
from env import PROJECT_DIR
from PySide6.QtCore import QFile, QTextStream

# this import may appear unused, but allows the theme to import its resources
from resources import breeze_pyside6


def setStyle(app):
    file = QFile(PROJECT_DIR + "\\dist\\dark\\stylesheet.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())


def run():
    app = QApplication(sys.argv)
    setStyle(app)

    # must create app first (controller imports modules that have other threads. QApplication
    # Thread must start first)
    from source.controller.shortcut_controller import ShortcutController

    controller = ShortcutController()
    controller.loadShortcutWindow()
    sys.exit(app.exec())
