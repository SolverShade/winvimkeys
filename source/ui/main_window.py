from PySide6.QtWidgets import QMainWindow, QListWidget, QVBoxLayout, QWidget, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QFocusEvent
from PySide6.QtGui import QKeyEvent
import keyboard

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 Window")
        self.setGeometry(150, 50, 1200, 36)

        # Hide the window title bar and make the window borderless
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Create a central widget and set it as the central widget of the main window
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a layout and add widgets to it
        layout = QVBoxLayout()
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)
        
        # Set the layout to the central widget
        central_widget.setLayout(layout)
        
        # Add items to the list widget
        items = [";    commands", "a    aseprite", "s    steam"]
        for item in items:
            self.list_widget.addItem(item)

        # Connect the item selection event to a handler
        self.list_widget.itemClicked.connect(self.on_item_clicked)

        # Set up a global hotkey listener
        keyboard.add_hotkey('ctrl+;', self.toggle_window)
        
    def on_item_clicked(self, item):
        QMessageBox.information(self, "Item Clicked", f"You clicked: {item.text()}")

    def toggle_window(self):
        if self.isHidden():
            self.show()
            self.activateWindow()
            self.raise_()
        else:
            self.hide()
            
    def closeEvent(self, event):
        # Unregister the hotkey when the application is closed
        keyboard.unhook_all_hotkeys()
        event.accept()
        
    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Escape:
            self.hide()
        super().keyPressEvent(event) 