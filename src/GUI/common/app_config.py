import os
from configparser import ConfigParser
from pathlib import Path


class AppConfig:
    """Class for reading and modifying config files"""

    CONFIG_FILE = os.path.join(Path.cwd(), Path("src/config/config.ini"))
    config = ConfigParser()

    @staticmethod
    def load_settings():
        AppConfig.config.read(AppConfig.CONFIG_FILE)
        return AppConfig.config["Settings"]

    @staticmethod
    def save_settings(key, value):
        if "Settings" not in AppConfig.config:
            AppConfig.config["Settings"] = {}
        AppConfig.config["Settings"][key] = value
        with open(AppConfig.CONFIG_FILE, "w") as configfile:
            AppConfig.config.write(configfile)
