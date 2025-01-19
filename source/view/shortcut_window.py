from PySide6.QtWidgets import (
    QMainWindow,
    QListWidget,
    QVBoxLayout,
    QWidget,
    QListWidgetItem,
    QLineEdit,
    QKeySequenceEdit,
)
from PySide6.QtCore import Qt


class ShortcutWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 Window")
        self.setGeometry(150, 50, 1200, 90)
        self.setWindowFlags(Qt.FramelessWindowHint)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.messageBox = QLineEdit()
        self.messageBox.setReadOnly(True)
        self.messageBox.setAlignment(Qt.AlignCenter)
        self.messageBox.setText("-select a shortcut-")
        self.messageBox.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        layout.addWidget(self.messageBox)

        self.appNameTextbox = QLineEdit()
        self.appNameTextbox.hide()
        layout.addWidget(self.appNameTextbox)

        self.shortcutInput = QKeySequenceEdit()
        self.shortcutInput.show()
        self.shortcutInput.setFocus()
        layout.addWidget(self.shortcutInput)

        self.shortcutAdder = QKeySequenceEdit()
        self.shortcutAdder.hide()
        layout.addWidget(self.shortcutAdder)

        self.list_widget = QListWidget()
        self.list_widget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        layout.addWidget(self.list_widget)

        central_widget.setLayout(layout)

    def set_items(self, items):
        for item in items:
            list_item = QListWidgetItem(f"{item.shortcutKeys:<8} {item.appName}")
            list_item.setData(Qt.UserRole, item)
            self.list_widget.addItem(list_item)

    def connect_item_clicked(self, handler):
        self.list_widget.itemClicked.connect(handler)
