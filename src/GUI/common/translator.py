import json
import os
from typing import Dict, Optional

from src.GUI.common.app_config import AppConfig


class Translator:
    TRANSLATION_PATH = os.path.join(os.path.dirname(__file__), "languages_data")

    def __init__(self):
        self.__current_language = AppConfig.load_settings().get("language", "EN")
        self.translations: Optional[Dict[str, str]] = None
        self.load_language()

    @property
    def current_language(self):
        return self.__current_language

    @current_language.setter
    def current_language(self, value):
        if value != self.__current_language:
            self.__current_language = value
            self.load_language()
            AppConfig.save_settings("language", value)

    def load_language(self):
        path = os.path.join(self.TRANSLATION_PATH, f"{self.current_language}.json")
        with open(path, "r", encoding="utf-8") as f:
            self.translations = json.load(f)

    def get_labels_text(self, name_screen: str, key: str) -> str:
        return self.translations.get(name_screen).get("labels").get(key)

    def get_messages_text(self, name_screen: str, key: str) -> str:
        return self.translations.get(name_screen).get("messages").get(key)
