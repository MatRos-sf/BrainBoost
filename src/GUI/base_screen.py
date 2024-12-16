from kivy.uix.screenmanager import Screen

from src.db.session import GameManager

from .games.popups import InstructionPopup


class BaseScreen(Screen):
    def __init__(self, session_manager: GameManager, **kwargs):
        super(BaseScreen, self).__init__(**kwargs)
        self.session_manager = session_manager

    def set_label_text(self, **kwargs):
        for key, value in kwargs.items():
            attr = getattr(self, key)
            setattr(attr, "text", value)

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
