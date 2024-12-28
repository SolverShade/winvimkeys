import keyboard
import psutil
import os
from PySide6.QtCore import Qt, QMetaObject, Q_ARG
from PySide6.QtWidgets import QMessageBox 
from PySide6.QtGui import QKeySequence, QShortcut
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
        
        for shortcut in shortcuts: 
            appShortcut = QShortcut(QKeySequence(shortcut.shortcutKey), self.view)
            appShortcut.activated.connect(lambda path=shortcut.path: self.launch_application(path))
            appShortcut.activated.connect(self.toggle_window)
            
        exitShortcut = QShortcut(QKeySequence("ESC"), self.view)
        exitShortcut.activated.connect(self.toggle_window)

        keyboard.add_hotkey("ctrl+;", self.toggle_window)

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
            
    def is_application_open(self, executable_path):
        executable_name = os.path.basename(executable_path)
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] == executable_name:
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False
    
    def toggle_window(self):
        QMetaObject.invokeMethod(self.view, "setVisible", Qt.QueuedConnection, Q_ARG(bool, not self.view.isVisible()))           
