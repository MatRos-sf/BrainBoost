from typing import Optional

from kivy.uix.screenmanager import Screen

from src.db.session import GameManager
from src.GUI.common.translator import Translator

from .games.popups import InstructionPopup


class BaseScreen(Screen):
    def __init__(self, session_manager: GameManager, translation: Translator, **kwargs):
        super(BaseScreen, self).__init__(**kwargs)
        self.session_manager = session_manager
        self.translation = translation

    def on_enter(self, name_screen: Optional[str] = None, *args):
        super(BaseScreen, self).on_enter()
        # set text in button and labels
        if name_screen:
            self.set_label_text(
                **self.translation.translations.get(name_screen).get("labels")
            )

    def set_label_text(self, **kwargs):
        for key, value in kwargs.items():
            attr = getattr(self, key)
            setattr(attr, "text", value)

    def get_message_with_variables(self, name_screen: str, key: str, **variables):
        """
        Format the message using the provided variables
        """
        text = self.translation.get_messages_text(name_screen, key)
        if text is None:
            raise ValueError(f"Please implement massage for: {name_screen=}, {key=}")
        return text.format(**variables)

    def init_first_game(self, target_screen: str):
        """
        The methods initial first game. First create new row in PointsModel then display window with information about game.
        Args:
            target_screen (str): The name 'target_screen' which will be displayed after pressing the close button.
        """
        popup = InstructionPopup(
            title="Game result",
            message="It's your first time ;) GL",
            manager=self.manager,
            target_screen=target_screen,
        )
        popup.open()
