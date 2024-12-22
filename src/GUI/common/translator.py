import json
import os
from typing import Dict, Optional


class Translator:
    PATH = os.path.join(os.path.dirname(__file__), "languages_data")

    def __init__(self, default_language="EN"):
        self.current_language = default_language
        self.translations: Optional[Dict[str, str]] = None
        self.load_language()

    def load_language(self):
        path = os.path.join(self.PATH, f"{self.current_language}.json")
        with open(path, "r", encoding="utf-8") as f:
            self.translations = json.load(f)

    def get_labels_text(self, name_screen: str, key: str) -> str:
        return self.translations.get(name_screen).get("labels").get(key)

    def get_messages_text(self, name_screen: str, key: str) -> str:
        return self.translations.get(name_screen).get("messages").get(key)
