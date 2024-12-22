from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner

from src.db.session import GameManager
from src.models.enum_types import Language

from .base_screen import BaseScreen


class SettingsScreen(BaseScreen):
    def __init__(self, session_manager: GameManager, **kwargs) -> None:
        super(SettingsScreen, self).__init__(session_manager, **kwargs)
        # Info layout
        self.info_layout = GridLayout(
            cols=1, size_hint=(0.6, 0.1), pos_hint={"center_x": 0.5, "center_y": 0.9}
        )
        self.info_label = Label(text="", size_hint=(1, 1))
        self.info_layout.add_widget(self.info_label)
        self.add_widget(self.info_layout)

        # layouts
        self.layout = GridLayout(
            cols=1, size_hint=(0.6, 0.3), pos_hint={"center_x": 0.5, "center_y": 0.5}
        )

        # Language selection section
        session_language = self.session_manager.get_language()
        self.language_layout = GridLayout(cols=2, size_hint=(1, 0.2))
        self.language_label = Label(text="Language", size_hint=(0.5, 1))
        self.language_spinner = Spinner(
            text=Language.EN.value if not session_language else session_language,
            values=[lang.value for lang in Language],
            size_hint=(0.5, 0.3),
            background_color=(0.2, 0.6, 0.8, 1),
            color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.4},
        )
        self.language_layout.add_widget(self.language_label)
        self.language_layout.add_widget(self.language_spinner)
        self.layout.add_widget(self.language_layout)

        # User info section
        self.user_info = Label(text="", size_hint=(1, 0.3))
        self.layout.add_widget(self.user_info)

        # Save and Back to Menu buttons
        self.buttons_layout = GridLayout(cols=2, size_hint=(1, 0.2))
        self.save_button = Button(text="Save", size_hint=(0.5, 1))
        self.back_button = Button(text="Back to Menu", size_hint=(0.5, 1))

        # Bind button events
        self.back_button.bind(on_press=self.back_to_menu)
        self.save_button.bind(on_press=self.save_settings)

        self.buttons_layout.add_widget(self.save_button)
        self.buttons_layout.add_widget(self.back_button)
        self.layout.add_widget(self.buttons_layout)

        self.add_widget(self.layout)

    # Button events
    def back_to_menu(self, instance):
        """Return to the main menu."""
        self.manager.current = "menu"

    def save_settings(self, instance):
        self.info_label.text = "Settings saved."
        # TODO: implemented body
