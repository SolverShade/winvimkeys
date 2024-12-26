import sys
from PySide6.QtWidgets import QApplication
from source.ui.main_window import MainWindow
import keyboard

def run():
    app = QApplication(sys.argv)
    window = MainWindow()
    
    # window must be shown before being hidden
    window.show()
    window.hide()
    
    sys.exit(app.exec())
    