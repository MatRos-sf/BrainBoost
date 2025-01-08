from functools import partial

from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from src.db.session import GameManager
from src.models.enum_types import GameName, PointsCategory

from ..models.games import AssociativeChangingModel, ResultKeeperModel
from .base_screen import BaseScreen


class MenuScreen(BaseScreen):
    def __init__(self, session_manager: GameManager, translation, **kwargs) -> None:
        super(MenuScreen, self).__init__(session_manager, translation, **kwargs)
        # layouts
        self.layout = GridLayout(
            cols=1, size_hint=(0.6, 0.7), pos_hint={"center_x": 0.5, "center_y": 0.5}
        )

        # User info section
        self.welcome_message = Label(text="", size_hint=(1, 0.3))
        self.layout.add_widget(self.welcome_message)

        # Options
        self.result_keeper_button = Button(size_hint=(1, 0.3))
        self.as_button = Button(size_hint=(1, 0.3))
        self.settings_button = Button(size_hint=(1, 0.3))
        self.logout_button = Button(size_hint=(1, 0.3))

        # Bind button events
        self.logout_button.bind(on_press=self.go_back)
        self.result_keeper_button.bind(
            on_press=partial(
                self.start_game_generic,
                PointsCategory.FIRST_RESULT_KEEPER,
                "result_keeper_game",
                GameName.RESULT_KEEPER,
                ResultKeeperModel,
            )
        )
        self.as_button.bind(
            on_press=partial(
                self.start_game_generic,
                PointsCategory.FIRST_ASSOCIATIVE_CHANGING,
                "associative_changing_game",
                GameName.ASSOCIATIVE_CHANGING,
                AssociativeChangingModel,
            )
        )

        self.settings_button.bind(on_press=self.settings_screen)
        self.layout.add_widget(self.result_keeper_button)
        self.layout.add_widget(self.as_button)
        self.layout.add_widget(self.settings_button)
        self.layout.add_widget(self.logout_button)

        self.add_widget(self.layout)

    def on_enter(self) -> None:
        """
        Before entering screen:
            * update welcome message
            * update buttons text
        """
        # Update welcome message
        points = self.session_manager.current_session.point
        username = self.session_manager.current_session.username
        self.welcome_message.text = self.get_message_with_variables(
            "menu", "user_info", points=points, username=username
        )  # f"Welcome {username}!\nPoints: {points}"
        # set text button
        self.set_label_text(**self.translation.translations.get("menu").get("labels"))

    def go_back(self, instance) -> None:
        del self.session_manager.current_session
        self.manager.current = "login"

    def settings_screen(self, intsnace):
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
