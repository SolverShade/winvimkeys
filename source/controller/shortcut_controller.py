import json
import keyboard
import os
from PySide6.QtCore import Qt, QObject, Slot, Signal
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QKeySequence
from source.model.shortcut_model import ShortcutModel
from source.view.shortcut_window import ShortcutWindow
from source.controller.window_manager import WindowManager
from env import PROJECT_DIR
from pynput import mouse


class ShortcutController(QObject):
    appWindowSelected = Signal(str, str, int)

    def __init__(self):
        super().__init__()

        self.view = ShortcutWindow()
        self.view.shortcutInput.keySequenceChanged.connect(self.runShortcut)
        self.view.shortcutAdder.keySequenceChanged.connect(self.addShortcutKeys)
        self.view.appNameTextbox.returnPressed.connect(self.submitAppName)

        # listen to method that will emit signal to main thread
        self.mouse_listener = mouse.Listener(on_click=self.addApp)
        self.mouse_listener.start()
        self.appWindowSelected.connect(self.handleAppAdded)

        # the following is a global hotkey so the window can be toggled even when closed
        keyboard.add_hotkey("ctrl+;", self.toggleWindow)

        self.shortcutToAdd = ShortcutModel("", "", "", "")
        self.loadShortcuts()

    def loadShortcuts(self):
        self.shortcuts = ShortcutModel.load_from_json(
            PROJECT_DIR + "\\data\\app_shortcuts.json"
        )
        self.view.set_items(self.shortcuts)

    def runShortcut(self):
        keySequence = self.view.shortcutInput.keySequence()
        print(keySequence.toString())

        for shortcut in self.shortcuts:
            if keySequence == QKeySequence(shortcut.shortcutKeys):
                self.activateApp(shortcut.path, shortcut.pid)
                self.toggleWindow()

        if keySequence == Qt.Key_Escape:
            self.toggleWindow()

        if keySequence == QKeySequence("Shift+A"):
            self.view.shortcutInput.hide()
            self.view.list_widget.hide()

            self.view.messageBox.setText("-enter the name of the application-")
            self.view.appNameTextbox.show()
            self.view.appNameTextbox.setFocus()

        self.view.shortcutInput.clear()

    def submitAppName(self):
        name = self.view.appNameTextbox.text()

        if name != "":
            self.shortcutToAdd.appName = name
            self.view.appNameTextbox.clear()
            self.view.appNameTextbox.hide()

            self.view.messageBox.setText("-enter the shortcut keys for application-")
            self.view.shortcutAdder.show()
            self.view.shortcutAdder.setFocus()
        else:
            self.view.messageBox.setText("Name cannot be empty. Try again")

    def addShortcutKeys(self):
        keySequence = self.view.shortcutAdder.keySequence()

        if keySequence.isEmpty() == False:
            # ensures the event filter continues to run while user clicks outside window
            self.view.setWindowFlags(self.view.windowFlags() & ~Qt.WindowStaysOnTopHint)

            self.shortcutToAdd.shortcutKeys = keySequence
            self.view.shortcutAdder.clear()
            self.view.shortcutAdder.hide()
            self.view.setFocus()
            self.view.messageBox.setText(
                "-press control + right click on the application window"
            )
        else:
            self.view.messageBox.setText("Shortcut cannot be empty. Try again")

    def addApp(self, x, y, button, pressed):
        if pressed and button == mouse.Button.right and keyboard.is_pressed("ctrl"):
            windowInfo = WindowManager.getAppInfoUnderCursor()

            if windowInfo is None:
                self.view.messageBox.textChanged.emit("-no window found, try again-")
            else:
                windowTitle, appExe, appPid = windowInfo
                self.appWindowSelected.emit(windowTitle, appExe, appPid)

    @Slot(str, str, int)
    def handleAppAdded(self, windowTitle, appExe, appPid):
        self.shortcutToAdd.pid = appPid
        self.shortcutToAdd.path = appExe

        shortcut_data = {
            "shortcutKey": self.shortcutToAdd.shortcutKeys.toString().lower(),
            "appName": self.shortcutToAdd.appName,
            "path": self.shortcutToAdd.path,
            "pid": self.shortcutToAdd.pid,
        }

        # add shortcut to app_shortcuts.json
        file_path = os.path.join(PROJECT_DIR, "data", "app_shortcuts.json")
        try:
            with open(file_path, "r+") as file:
                data = json.load(file)
                data.append(shortcut_data)
                file.seek(0)
                json.dump(data, file, indent=4)
        except FileNotFoundError:
            with open(file_path, "w") as file:
                json.dump([shortcut_data], file, indent=4)

        self.shortcutToAdd.clear()

        self.view.messageBox.setText(f"shortcut for {windowTitle} added")
        self.view.shortcutInput.show()
        self.view.shortcutInput.setFocus()
        self.view.list_widget.show()

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
