import subprocess
import pygetwindow as gw
import keyboard
import psutil
import os
import time
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox
from source.model.shortcut_model import ShortcutModel
from source.view.shortcut_window import ShortcutWindow
from env import ROOT_DIR


class ShortcutController:
    def __init__(self):
        self.view = ShortcutWindow()

        shortcuts = ShortcutModel.load_from_json(
            ROOT_DIR + "\\data\\app_shortcuts.json"
        )

        self.view.set_items(shortcuts)
        self.view.connect_item_clicked(self.on_item_clicked)

        keyboard.add_hotkey("ctrl+;", self.toggle_window)
        keyboard.add_hotkey("ESC", self.toggle_window)

    def load_shortcut_window(self):
        self.view.show()
        self.view.hide()

    def on_item_clicked(self, item):
        shortcut = item.data(Qt.UserRole)
        if shortcut:
            self.launch_application(shortcut.path)

    def launch_application(self, path):
        if os.path.exists(path):
            os.startfile(path)
        else:
            QMessageBox.warning(
                self.view, "Error", f"Application path not found: {path}"
            )

    def toggle_window(self):
        if self.view.isHidden():
            self.view.show()
            self.view.activateWindow()
            self.view.raise_()
        else:
            self.view.hide()
