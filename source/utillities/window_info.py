import win32gui
import win32process
import win32api 
import win32con
from pywinauto import Application
from pynput import mouse

def get_window_title(hwnd):
    window_title = win32gui.GetWindowText(hwnd)
    if not window_title:
        try:
            app = Application().connect(handle=hwnd)
            window = app.window(handle=hwnd)
            window_title = window.window_text()
        except Exception as e:
            window_title = "Unknown"
    return window_title

def on_click(x, y, button, pressed):
    if pressed:
        hwnd = win32gui.WindowFromPoint((x, y))
        if hwnd:
            window_title = get_window_title(hwnd)
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            exe_path = getExePath(hwnd)
         
            print(f"Window Title: {window_title}")
            print(f"Executable Path: {exe_path}")
            print(f"Process ID: {pid}")
            
            return window_title, exe_path, pid
        
def getExePath(hwnd):
    try:
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process_handle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, pid)
        exe_path = win32process.GetModuleFileNameEx(process_handle, 0)
        win32api.CloseHandle(process_handle)
        return exe_path
    except Exception as e:
        print(f"Error getting exe path: {e}")
        return None


def main():
    print("Click on a window to get its information.")
    listener = mouse.Listener(on_click=on_click)
    listener.start()
    listener.join()

if __name__ == "__main__":
    main()