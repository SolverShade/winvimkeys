from PySide6.QtWidgets import (
    QMainWindow,
    QListWidget,
    QVBoxLayout,
    QWidget,
    QListWidgetItem,
    QLineEdit
)
from PySide6.QtCore import Qt


class ShortcutWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 Window")
        self.setGeometry(150, 50, 1200, 36)
        self.setWindowFlags(Qt.FramelessWindowHint)
         
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        
        self.textbox = QLineEdit()
        self.textbox.setReadOnly(True)
        self.textbox.setAlignment(Qt.AlignCenter)
        self.textbox.setText("-select a shortcut-")
        layout.addWidget(self.textbox)

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)
        central_widget.setLayout(layout)

    def set_items(self, items):
        for item in items:
            list_item = QListWidgetItem(f"{item.shortcutKey:<8} {item.appName}")
            list_item.setData(Qt.UserRole, item)
            self.list_widget.addItem(list_item)

    def connect_item_clicked(self, handler):
        self.list_widget.itemClicked.connect(handler)
