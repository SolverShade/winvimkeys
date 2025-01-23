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
        self.setGeometry(150, 50, 1200, 240)
        self.setWindowFlags(Qt.FramelessWindowHint)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.message_box = QLineEdit()
        self.message_box.setReadOnly(True)
        self.message_box.setAlignment(Qt.AlignCenter)
        self.message_box.setText("-select a shortcut-")
        self.message_box.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        layout.addWidget(self.message_box)

        self.app_name_textbox = QLineEdit()
        self.app_name_textbox.hide()
        layout.addWidget(self.app_name_textbox)

        self.shortcut_input = QKeySequenceEdit()
        self.shortcut_input.show()
        self.shortcut_input.setFocus()
        layout.addWidget(self.shortcut_input)

        self.shortcut_adder = QKeySequenceEdit()
        self.shortcut_adder.hide()
        layout.addWidget(self.shortcut_adder)

        self.list_widget = QListWidget()
        self.list_widget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.list_widget.setSortingEnabled(True)
        layout.addWidget(self.list_widget)

        central_widget.setLayout(layout)

    def add_shortcuts_to_list(self, items):
        for item in items:
            list_item = QListWidgetItem(f"{item.shortcutKeys:<8} {item.appName}")
            list_item.setData(Qt.UserRole, item)
            self.list_widget.addItem(list_item)

    def add_item_to_list(self, keys, name, data):
        list_item = QListWidgetItem(f"{keys:<8} {name}")
        list_item.setData(Qt.UserRole, data)
        self.list_widget.addItem(list_item)

    def connect_item_clicked(self, handler):
        self.list_widget.itemClicked.connect(handler)
