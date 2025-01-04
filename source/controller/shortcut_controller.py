import keyboard
import os
from PySide6.QtCore import Qt, QEvent, QObject
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QKeySequence
from source.model.shortcut_model import ShortcutModel
from source.view.shortcut_window import ShortcutWindow
from source.controller.window_manager import WindowManager
from env import PROJECT_DIR


class ShortcutController(QObject):
    def __init__(self):
        super().__init__()
        self.view = ShortcutWindow()
        self.view.installEventFilter(self)

        self.shortcuts = ShortcutModel.load_from_json(
            PROJECT_DIR + "\\data\\app_shortcuts.json"
        )

        self.view.set_items(self.shortcuts)

        # the following is a global hotkey so the window can be toggled even when closed
        keyboard.add_hotkey("ctrl+;", self.ToggleWindow)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            key_char = QKeySequence(event.key()).toString().lower()

            for shortcut in self.shortcuts:
                if key_char == shortcut.shortcutKey:
                    self.activateApp(shortcut.path, shortcut.pid)
                    self.ToggleWindow()

            if event.key() is Qt.Key.Key_A:
                self.addApp()

            if event.key() == Qt.Key_Escape:
                self.ToggleWindow()

        return super().eventFilter(obj, event)

    def activateApp(self, path, pid):
        if WindowManager.is_window_open(pid):
            WindowManager.focus_window(pid, path)
            return

        if os.path.exists(path):
            os.startfile(path)
        else:
            QMessageBox.warning(
                self.view, "Error", f"Application path not found: {path}"
            )

    def ToggleWindow(self):
        WindowManager.toggle_qt_window(self.view)

    def loadShortcutWindow(self):
        self.view.show()
        self.view.hide()
