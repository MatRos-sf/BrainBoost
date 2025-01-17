from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner

from src.db.session import GameManager
from src.models.enum_types import Language
from src.models.user import User

from .base_screen import BaseScreen


class SettingsScreen(BaseScreen):
    def __init__(self, session_manager: GameManager, translation, **kwargs) -> None:
        super(SettingsScreen, self).__init__(session_manager, translation, **kwargs)
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
        self.language_layout = GridLayout(cols=2, size_hint=(1, 0.2))
        self.language_label = Label(
            text=self.translation.get_labels_text("settings", "language_label"),
            size_hint=(0.5, 1),
        )
        self.language_spinner = Spinner(
            text=Language.EN.value,
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
        self.save_button = Button(
            text=self.translation.get_labels_text("settings", "save_button"),
            size_hint=(0.5, 1),
        )
        self.back_button = Button(
            text=self.translation.get_labels_text("settings", "back_button"),
            size_hint=(0.5, 1),
        )

        # Bind button events
        self.back_button.bind(on_press=self.back_to_menu)
        self.save_button.bind(on_press=self.save_settings)

        self.buttons_layout.add_widget(self.save_button)
        self.buttons_layout.add_widget(self.back_button)
        self.layout.add_widget(self.buttons_layout)

        self.add_widget(self.layout)

    def on_enter(self, *args):
        super().on_enter(name_screen="settings", *args)
        self.language_spinner.text = self.session_manager.get_language()

    # Button events
    def back_to_menu(self, instance):
        """Return to the main menu."""
        # clear the message
        self.info_label.text = ""
        # Go back to the menu screen
        self.manager.current = "menu"

    def save_settings(self, instance):
        """
        Saves user settings if any changes are detected.

        This method checks if the user's language settings has been changed.
        If a change is detected, it performs the following actions:
            - Update user's language in the database.
            - Update current language in the translation.
            - Update labels.
            - Show success message.
        """
        message = ""
        if self.language_spinner.text != self.session_manager.get_language():
            self.session_manager.current_session.language = Language(
                self.language_spinner.text
            )
            self.session_manager.db.update_record(
                User,
                self.session_manager.current_session.id,
                {"language": self.language_spinner.text},
            )
            self.translation.current_language = self.language_spinner.text
            self.set_label_text(
                **self.translation.translations.get("settings").get("labels")
            )
            message += self.get_message_with_variables("settings", "changed_language")

        if message:
            self.info_label.text = (
                self.get_message_with_variables("settings", "saved_settings")
                + "\n"
                + message
            )
