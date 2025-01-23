from PySide6.QtCore import Qt, QMetaObject, Q_ARG
from PySide6.QtWidgets import QMainWindow
import psutil
import os
import win32gui
import win32con
import win32process
import win32api
from pywinauto import Application


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
                if (
                    window_title
                    and window_title.lower() in win32gui.GetWindowText(hwnd).lower()
                ):
                    hwnds.insert(0, hwnd)
                else:
                    hwnds.append(hwnd)
            return True

        hwnds = []
        win32gui.EnumWindows(callback, pid)
        return hwnds

    @staticmethod
    def _getWindowTitle(hwnd):
        window_title = win32gui.GetWindowText(hwnd)
        if not window_title:
            try:
                app = Application().connect(handle=hwnd)
                window = app.window(handle=hwnd)
                window_title = window.window_text()
            except Exception as e:
                window_title = "Unknown"
        return window_title

    @staticmethod
    def _getExePath(hwnd):
        try:
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            process_handle = win32api.OpenProcess(
                win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ,
                False,
                pid,
            )
            exe_path = win32process.GetModuleFileNameEx(process_handle, 0)
            win32api.CloseHandle(process_handle)
            return exe_path
        except Exception as e:
            print(f"Error getting exe path: {e}")
            return None

    @staticmethod
    def getAppInfoUnderCursor():
        x, y = win32api.GetCursorPos()
        hwnd = win32gui.WindowFromPoint((x, y))
        if hwnd:
            window_title = WindowManager._getWindowTitle(hwnd)
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            exe_path = WindowManager._getExePath(hwnd)
            return window_title, exe_path, pid
        return None

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
        QMetaObject.invokeMethod(
            window,
            "setVisible",
            Qt.QueuedConnection,
            Q_ARG(bool, not window.isVisible()),
        )
        if window.isVisible():
            window.activateWindow()
            window.raise_()
