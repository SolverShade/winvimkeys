from PySide6.QtCore import Qt, QMetaObject, Q_ARG
from PySide6.QtWidgets import QMainWindow
import psutil
import os
import win32gui
import win32con
import win32process

class WindowManager:
    @staticmethod
    def is_window_open(pid):
        try:
            proc = psutil.Process(pid)
            return proc.is_running()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return False

    @staticmethod
    def find_window(pid, window_title):
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

    @staticmethod
    def focus_window(pid, path):
        app_name = os.path.splitext(os.path.basename(path))[0]
        hwnds = WindowManager.find_window(pid, app_name)
        if hwnds:
            hwnd = hwnds[0]
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
            print(f"Window for PID {pid} found and focused.")
            
    @staticmethod 
    def toggle_qt_window(window: QMainWindow):
        QMetaObject.invokeMethod(window, "setVisible", Qt.QueuedConnection, Q_ARG(bool, not window.isVisible()))         
        if window.isVisible():
            window.activateWindow()
            window.raise_()