from kivy.uix.screenmanager import Screen

from src.db.session import GameManager


class BaseScreen(Screen):
    def __init__(self, session_manager: GameManager, **kwargs):
        super(BaseScreen, self).__init__(**kwargs)
        self.session_manager = session_manager

    def set_label_text(self, **kwargs):
        for key, value in kwargs.items():
            attr = getattr(self, key)
            setattr(attr, "text", value)
