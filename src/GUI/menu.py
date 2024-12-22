from functools import partial

from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from src.db.session import GameManager
from src.models.enum_types import GameName, PointsCategory

from ..models.games import AssociativeChangingModel, ResultKeeperModel
from .base_screen import BaseScreen


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
        self.option3 = Button(text="Settings", size_hint=(1, 0.3))
        self.back_button = Button(text="Logout", size_hint=(1, 0.3))

        # Bind button events
        self.back_button.bind(on_press=self.go_back)
        self.result_keeper.bind(
            on_press=partial(
                self.start_game_generic,
                PointsCategory.FIRST_RESULT_KEEPER,
                "result_keeper_game",
                GameName.RESULT_KEEPER,
                ResultKeeperModel,
            )
        )
        self.option2.bind(
            on_press=partial(
                self.start_game_generic,
                PointsCategory.FIRST_ASSOCIATIVE_CHANGING,
                "associative_changing_game",
                GameName.ASSOCIATIVE_CHANGING,
                AssociativeChangingModel,
            )
        )

        self.option3.bind(on_press=self.settingss_screen)
        self.layout.add_widget(self.result_keeper)
        self.layout.add_widget(self.option2)
        self.layout.add_widget(self.option3)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)

    def on_enter(self) -> None:
        # Update user_session when screen is entered
        points = self.session_manager.current_session.point
        username = self.session_manager.current_session.username
        self.user_info.text = f"Welcome {username}!\nPoints: {points}"
        print(self.session_manager.current_session)

    def go_back(self, instance) -> None:
        del self.session_manager.current_session
        self.manager.current = "login"

    def settingss_screen(self, intsnace):
        self.manager.current = "settings"

    def start_game_generic(
        self, points_category, screen_name, game_name, model, instance
    ):
        level = self.session_manager.get_level_game(game_name)
        game_id = self.session_manager.get_id_game(game_name)

        if level is None:
            # update PointModel
            self.session_manager.db.add_points_for_first_game(
                user_id=self.session_manager.current_session.id,
                category=points_category,
            )
            # Update record GameModel
            self.session_manager.db.update_record(model, game_id, {"level": 1})
            # Update level current session
            self.session_manager.update_level_of_game(game_name, 1)
            # popup with information
            self.init_first_game(screen_name)

        else:
            self.manager.current = screen_name
