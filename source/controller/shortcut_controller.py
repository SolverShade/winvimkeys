import keyboard
import psutil
import os
from PySide6.QtCore import Qt, QMetaObject, Q_ARG
from PySide6.QtWidgets import QMessageBox 
from PySide6.QtGui import QKeySequence, QShortcut
from source.model.shortcut_model import ShortcutModel
from source.view.shortcut_window import ShortcutWindow
from env import ROOT_DIR
from pywinauto import Application
import win32gui
import win32con
import win32process

class ShortcutController:
    def __init__(self):
        self.view = ShortcutWindow()

        shortcuts = ShortcutModel.load_from_json(
            ROOT_DIR + "\\data\\app_shortcuts.json"
        )

        self.view.set_items(shortcuts)
        self.view.connect_item_clicked(self.onItemClick)
        
        for shortcut in shortcuts: 
            appShortcut = QShortcut(QKeySequence(shortcut.shortcutKey), self.view)
            appShortcut.activated.connect(lambda path=shortcut.path, pid = shortcut.pid: self.activateApp(path, pid))
            appShortcut.activated.connect(self.ToggleWindow)
            
        exitShortcut = QShortcut(QKeySequence("ESC"), self.view)
        exitShortcut.activated.connect(self.ToggleWindow)

        keyboard.add_hotkey("ctrl+;", self.ToggleWindow)

    def loadShortcutWindow(self):
        self.view.show()
        self.view.hide()

    def onItemClick(self, item):
        shortcut = item.data(Qt.UserRole)
        if shortcut:
            self.activateApp(shortcut.path, shortcut.pid)

    def activateApp(self, path, pid):
        if self.isAppOpen(pid): 
            self.focusApp(pid, path)
            return
        
        if os.path.exists(path):
            os.startfile(path)
        else:
            QMessageBox.warning(
                self.view, "Error", f"Application path not found: {path}"
            )
            
    def isAppOpen(self, pid):
        try:
            proc = psutil.Process(pid)
            return proc.is_running()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return False
        
    def findWindow(self, pid, window_title):
        def callback(hwnd, pid):
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid == pid:
                if window_title and window_title.lower() in win32gui.GetWindowText(hwnd).lower():
                    hwnds.insert(0, hwnd)  
                else:
                    hwnds.append(hwnd)
            return True
        
        hwnds = []
        win32gui.EnumWindows(callback, pid)
        return hwnds

    def focusApp(self, pid, path):
        appName =  os.path.splitext(os.path.basename(path))[0]
        hwnds = self.findWindow(pid, appName)
        if hwnds:
            hwnd = hwnds[0]
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
            print(f"Window for PID {pid} found and focused.")
        else:
            print(f"No window found for PID {pid}.")
            
    def ToggleWindow(self):
        QMetaObject.invokeMethod(self.view, "setVisible", Qt.QueuedConnection, Q_ARG(bool, not self.view.isVisible()))         
        if self.view.isVisible():
            self.view.activateWindow()
            self.view.raise_()