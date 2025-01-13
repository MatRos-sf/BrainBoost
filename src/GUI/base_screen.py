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

    def format_text(self, text: str, name_screen: str, key: str, **variables) -> str:
        """
        Format the given text by replacing placeholders with provided variables.

        This function takes a text string and formats it using the provided variables.
        If the text is None, it raises a ValueError with information about the missing message.

        Args:
            text (str): The text to be formatted.
            name_screen (str): The name of the screen associated with the text.
            key (str): The key identifying the specific text within the screen.
            **variables: Arbitrary keyword arguments representing variables to be inserted into the text.

        Returns:
            str: The formatted text with variables inserted.

        Raises:
            ValueError: If the input text is None, indicating a missing message implementation.
        """
        if text is None:
            raise ValueError(f"Please implement massage for: {name_screen=}, {key=}")
        return text.format(**variables)

    def get_label_with_variables(self, name_screen: str, key: str, **variables) -> str:
        """
        Retrieve and format a label text with variables.

        This function gets a label text for a specific screen and key, then formats it
        with the provided variables.

        Args:
            name_screen (str): The name of the screen associated with the label.
            key (str): The key identifying the specific label within the screen.
            **variables: Arbitrary keyword arguments representing variables to be
                         inserted into the label text.

        Returns:
            str: The formatted label text with variables inserted.
        """
        text = self.translation.get_labels_text(name_screen, key)
        return self.format_text(text, name_screen, key, **variables)

    def get_message_with_variables(
        self, name_screen: str, key: str, **variables
    ) -> str:
        """
        Retrieve and format a message text with variables.

        This function gets a message text for a specific screen and key, then formats it
        with the provided variables.

        Args:
            name_screen (str): The name of the screen associated with the message.
            key (str): The key identifying the specific message within the screen.
            **variables: Arbitrary keyword arguments representing variables to be
                         inserted into the message text.

        Returns:
            str: The formatted message text with variables inserted.
        """
        text = self.translation.get_messages_text(name_screen, key)
        return self.format_text(text, name_screen, key, **variables)

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
