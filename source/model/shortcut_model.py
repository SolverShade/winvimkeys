import json


class ShortcutModel:
    def __init__(self, shortcutKeys, appName, path, pid):
        self.shortcutKeys = shortcutKeys
        self.appName = appName
        self.path = path
        self.pid = pid

    @staticmethod
    def load_from_json(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
            return [
                ShortcutModel(
                    item["shortcutKey"], item["appName"], item["path"], item["pid"]
                )
                for item in data
            ]

    def clear(self):
        self.shortcutKeys = ""
        self.appName = ""
        self.path = ""
        self.pid = ""

    def __repr__(self):
        return f"ShortcutModel(shortcutKey={self.shortcutKeys}, appName={self.appName}, path={self.path})"
