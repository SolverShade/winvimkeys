import json
import keyboard
import os
from PySide6.QtCore import Qt, QObject, Slot, Signal
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QKeySequence
from source.model.shortcut_model import ShortcutModel
from source.view.shortcut_window import ShortcutWindow
from source.utility.window_manager import WindowManager
from env import PROJECT_DIR
from pynput import mouse
from source.controller.app_adder import AppAdder


class ShortcutController(QObject):
    appWindowSelected = Signal(str, str, int)

    def __init__(self):
        super().__init__()

        self.view = ShortcutWindow()
        self.view.shortcut_input.keySequenceChanged.connect(self.runShortcut)
        self.app_adder = AppAdder(self.view)

        # the following is a global hotkey so the window can be toggled even when closed
        keyboard.add_hotkey("ctrl+;", self.toggleWindow)

        self.loadShortcuts()

    def loadShortcuts(self):
        self.shortcuts = ShortcutModel.load_from_json(
            PROJECT_DIR + "\\data\\app_shortcuts.json"
        )
        self.view.add_shortcuts_to_list(self.shortcuts)
        self.view.add_item_to_list("A", "Add Shortcut", None)

    def runShortcut(self):
        keySequence = self.view.shortcut_input.keySequence()
        print(keySequence.toString())

        for shortcut in self.shortcuts:
            if keySequence == QKeySequence(shortcut.shortcutKeys):
                self.activateApp(shortcut.path, shortcut.pid)
                self.toggleWindow()

        if keySequence == Qt.Key_Escape:
            self.toggleWindow()

        if keySequence == QKeySequence("Shift+A"):
            self.app_adder.start_adding_shortcut()

        self.view.shortcut_input.clear()

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

    def toggleWindow(self):
        WindowManager.toggle_qt_window(self.view)

    def loadShortcutWindow(self):
        self.view.show()
        self.view.hide()
        self.view.setFocus()
