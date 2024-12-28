import json


class ShortcutModel:
    def __init__(self, shortcutKey, appName, path, pid):
        self.shortcutKey = shortcutKey
        self.appName = appName
        self.path = path
        self.pid = pid

    @staticmethod
    def load_from_json(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
            return [
                ShortcutModel(item["shortcutKey"],
                              item["appName"], item["path"], item["pid"])
                for item in data
            ]

    def __repr__(self):
        return f"ShortcutModel(shortcutKey={self.shortcutKey}, appName={self.appName}, path={self.path})"
