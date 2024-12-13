from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from src.db.session import GameManager

from ..models.games import GameName
from .base_screen import BaseScreen
from .games.popups import InstructionPopup


class MenuScreen(BaseScreen):
    def __init__(self, session_manager: GameManager, **kwargs) -> None:
        super(MenuScreen, self).__init__(session_manager, **kwargs)
        # layouts
        self.layout = GridLayout(
            cols=1, size_hint=(0.6, 0.7), pos_hint={"center_x": 0.5, "center_y": 0.5}
        )

        # User info section
        self.user_info = Label(text="", size_hint=(1, 0.3))
        self.layout.add_widget(self.user_info)

        # Options
        self.result_keeper = Button(text="Result Keeper", size_hint=(1, 0.3))
        self.option2 = Button(text="AS", size_hint=(1, 0.3))
        self.option3 = Button(text="Option 3", size_hint=(1, 0.3))
        self.back_button = Button(text="Logout", size_hint=(1, 0.3))

        # Bind button events
        self.back_button.bind(on_press=self.go_back)
        self.result_keeper.bind(on_press=self.start_game_result_keeper)
        self.option2.bind(on_press=self.start_game_as)

        self.layout.add_widget(self.result_keeper)
        self.layout.add_widget(self.option2)
        self.layout.add_widget(self.option3)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)

    def on_enter(self) -> None:
        # Update user_session when screen is entered
        points = self.session_manager.current_session.points
        username = self.session_manager.current_session.username
        self.user_info.text = f"Welcome {username}!\nPoints: {points}"
        print(self.session_manager.current_session)

    def go_back(self, instance) -> None:
        del self.session_manager.current_session
        self.manager.current = "login"

    def start_game_result_keeper(self, instance) -> None:
        level = self.session_manager.get_level_game(GameName.RESULT_KEEPER)
        if level is None:
            popup = InstructionPopup(
                title="Game result",
                message="It's your first time ;) GL",
                manager=self.manager,
                target_screen="result_keeper_game",
            )
            popup.open()
        else:
            self.manager.current = "result_keeper_game"

    def start_game_as(self, instance) -> None:
        self.manager.current = "associative_changing_game"
