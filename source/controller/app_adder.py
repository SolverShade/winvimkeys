import json
import os
from source.controller.window_manager import WindowManager
from source.model.shortcut_model import ShortcutModel
from source.view.shortcut_window import ShortcutWindow
from PySide6.QtCore import Qt, QObject, Signal, Slot
from pynput import mouse
import keyboard
from env import PROJECT_DIR


class AppAdder(QObject):
    appWindowSelected = Signal(str, int)

    def __init__(self, view: ShortcutWindow):
        super().__init__()

        self.view = view
        self.adding_shortcut = False
        self.view.shortcut_adder.keySequenceChanged.connect(self.add_shortcut_keys)
        self.view.app_name_textbox.returnPressed.connect(self.submit_app_name)

        # listen to method that will emit signal to main thread
        self.mouse_listener = mouse.Listener(on_click=self.add_app)
        self.mouse_listener.start()
        self.appWindowSelected.connect(self.handle_app_added)

        self.shortcut_to_add = ShortcutModel("", "", "", "")

    def start_adding_shortcut(self):
        self.adding_shortcut = True
        self.view.shortcut_input.hide()
        self.view.list_widget.hide()

        self.view.message_box.setText("-enter the name of the application-")
        self.view.app_name_textbox.show()
        self.view.app_name_textbox.setFocus()

    def exit_adding_shortcut(self, message):
        self.view.shortcut_adder.hide()
        self.view.app_name_textbox.hide()
        self.view.message_box.show()
        self.view.message_box.setText(message)
        self.view.shortcut_input.show()
        self.view.shortcut_input.setFocus()
        self.view.list_widget.show()

        self.adding_shortcut = False
        self.shortcut_to_add.clear()

    def add_shortcut_keys(self):
        keySequence = self.view.shortcut_adder.keySequence()

        if keySequence.isEmpty() == False:
            self.view.setWindowFlags(self.view.windowFlags() & ~Qt.WindowStaysOnTopHint)

            self.shortcut_to_add.shortcutKeys = keySequence
            self.view.shortcut_adder.clear()
            self.view.shortcut_adder.hide()
            self.view.setFocus()
            self.view.message_box.setText(
                "-press control + right click on the application window"
            )
        else:
            self.view.message_box.setText("Shortcut cannot be empty. Try again")

    def submit_app_name(self):
        name = self.view.app_name_textbox.text()

        if name != "":
            self.shortcut_to_add.appName = name
            self.view.app_name_textbox.clear()
            self.view.app_name_textbox.hide()

            self.view.message_box.setText("-enter the shortcut keys for application-")
            self.view.shortcut_adder.show()
            self.view.shortcut_adder.setFocus()
        else:
            self.view.message_box.setText("Name cannot be empty. Try again")

    def add_app(self, x, y, button, pressed):
        if (
            pressed
            and button == mouse.Button.right
            and keyboard.is_pressed("ctrl")
            and self.adding_shortcut is True
        ):
            windowInfo = WindowManager.getAppInfoUnderCursor()

            if windowInfo is None:
                self.view.message_box.textChanged.emit("-no window found, try again-")
            else:
                windowTitle, appExe, appPid = windowInfo
                self.appWindowSelected.emit(appExe, appPid)
                self.exit_adding_shortcut(f"shortcut for {windowTitle} added.")

    @Slot(str, int)
    def handle_app_added(self, appExe, appPid):
        self.shortcut_to_add.pid = appPid
        self.shortcut_to_add.path = appExe

        shortcut_data = {
            "shortcutKey": self.shortcut_to_add.shortcutKeys.toString().lower(),
            "appName": self.shortcut_to_add.appName,
            "path": self.shortcut_to_add.path,
            "pid": self.shortcut_to_add.pid,
        }

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
