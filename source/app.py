import sys
from PySide6.QtWidgets import QApplication
from env import ROOT_DIR
from source.controller.shortcut_controller import ShortcutController
from PySide6.QtCore import QFile, QTextStream

# this import may appear unused, but allows the theme to import its resources
from resources import breeze_pyside6

def run():
    app = QApplication(sys.argv)
    
    file = QFile(ROOT_DIR + "\\dist\\dark\\stylesheet.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())
    
    controller = ShortcutController()
    controller.loadShortcutWindow()
    sys.exit(app.exec())