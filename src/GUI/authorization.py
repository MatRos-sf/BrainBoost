import json
import os.path
from pathlib import Path

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

from ..db.session import GameManager
from ..models.user import Login, User
from ..user.session import verify_password
from .base_screen import BaseScreen

PATH_CREDENTIALS = os.path.join(Path.cwd(), ".credentials")


class MessagePopup(Popup):
    def __init__(self, title, message, **kwargs):
        super(MessagePopup, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (400, 200)
        self.title = title

        # Create content layout
        content = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # Message label
        message_label = Label(text=message, size_hint_y=0.7)
        content.add_widget(message_label)

        # OK button
        ok_button = Button(
            text="OK",
            size_hint=(None, None),
            size=(100, 40),
            pos_hint={"center_x": 0.5},
        )
        ok_button.bind(on_press=self.dismiss)
        content.add_widget(ok_button)

        self.content = content


class LoginScreen(BaseScreen):
    def __init__(self, session_manager: GameManager, translation, **kwargs):
        super(LoginScreen, self).__init__(session_manager, translation, **kwargs)
        self._popup = []  # List to store active popups

        # Initialize widgets
        self.info_label = Label(
            font_size=18,
            size_hint=(1, 0.15),
            halign="center",
            valign="middle",
        )
        self.user_field = TextInput(
            hint_text="Username",
            multiline=False,
            padding=(20, 20, 20, 20),
            size_hint=(1, 0.25),
        )
        self.password_field = TextInput(
            hint_text="Password",
            multiline=False,
            padding=(20, 20, 20, 20),
            size_hint=(1, 0.25),
            password=True,
        )
        self.remember_me = CheckBox(active=False, size_hint=(0.2, 1))
        self.login_button = Button(
            size_hint=(1, 0.25),
            bold=True,
            background_color=(0.2, 0.8, 0.2, 1),
        )
        self.create_button = Button(
            size_hint=(1, 0.25),
            bold=True,
            background_color=(0.2, 0.2, 0.8, 1),
        )
        self.remember_label = Label(size_hint=(0.8, 1))

        # Bind button events
        self.login_button.bind(on_press=self.authorization)
        self.create_button.bind(on_press=self.switch_to_create_account)

        # Setup layout
        self.setup_layout()

        # Load saved credentials
        self.load_credentials()

    def on_enter(self, *args):
        super().on_enter(name_screen="login", *args)

    def setup_layout(self):
        """Setup the screen layout with all widgets"""
        self.layout = GridLayout()
        self.layout.cols = 1
        self.layout.size_hint = (0.6, 0.7)
        self.layout.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.layout.spacing = 10

        # Add info label
        self.layout.add_widget(self.info_label)

        # Add username field
        self.user_field.bind(on_text_validate=self.on_user_field_enter)
        self.layout.add_widget(self.user_field)

        # Add password field
        self.password_field.bind(on_text_validate=self.on_password_field_enter)
        self.layout.add_widget(self.password_field)

        # Remember me layout
        remember_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.15))
        remember_layout.add_widget(self.remember_label)
        remember_layout.add_widget(self.remember_me)
        self.layout.add_widget(remember_layout)

        # Buttons layout
        buttons_layout = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.25), spacing=10
        )
        buttons_layout.add_widget(self.login_button)
        buttons_layout.add_widget(self.create_button)
        self.layout.add_widget(buttons_layout)

        self.add_widget(self.layout)

    def show_message(self, title, message):
        """Show a popup message"""
        popup = MessagePopup(title=title, message=message)
        self._popup.append(popup)
        popup.bind(on_dismiss=lambda _: self._popup.remove(popup))
        popup.open()

    def authorization(self, instance):
        username = self.user_field.text.strip()
        password = self.password_field.text
        user = self.session_manager.db.find_record(User, username=username)
        if user and verify_password(user.password, password):
            self.show_message(
                title=self.get_message_with_variables("login", "success_login_title"),
                message=self.get_message_with_variables(
                    "login", "success_login_message"
                ),
            )
            self.password_field.text = ""
            self.user_field.text = ""

            # Save credentials if remember me is checked
            if self.remember_me.active:
                self.save_credentials(username, password)
            # save login
            self.session_manager.db.add_record(Login, user_id=user.id)
            # load the current_session
            self.session_manager.load_session(user.id)
            # go to the 'menu' screen
            self.manager.current = "menu"
        else:
            self.show_message(
                title=self.get_message_with_variables("login", "fail_login_title"),
                message=self.get_message_with_variables("login", "fail_login_message"),
            )

    def save_credentials(self, username, password):
        credentials = {
            "username": username,
            "password": password,  # In production, this should be encrypted
        }

        with open(PATH_CREDENTIALS, "w") as f:
            json.dump(credentials, f)

    def load_credentials(self):
        # config_file = Path.home() / ".brainboost" / "credentials.json"
        # if config_file.exists():
        if PATH_CREDENTIALS:
            try:
                with open(PATH_CREDENTIALS) as f:
                    credentials = json.load(f)
                    self.user_field.text = credentials.get("username", "")
                    self.password_field.text = credentials.get("password", "")
                    self.remember_me.active = True
            except (IOError, json.JSONDecodeError) as e:
                print(f"Error loading credentials: {e}")
        else:
            # Create the file if it doesn't exist'
            with open(PATH_CREDENTIALS, "a"):
                pass

    def switch_to_create_account(self, instance) -> None:
        self.manager.current = "create_account"

    def on_user_field_enter(self, instance) -> None:
        """When user presses enter in username field, focus moves to password field"""
        self.password_field.focus = True

    def on_password_field_enter(self, instance) -> None:
        """When user presses enter in password field, call authorization method"""
        self.authorization(instance)


class CreateAccountScreen(BaseScreen):
    def __init__(self, session_manager: GameManager, translation, **kwargs) -> None:
        super(CreateAccountScreen, self).__init__(
            session_manager, translation, **kwargs
        )
        self.layout = GridLayout()
        self.layout.cols = 1
        self.layout.size_hint = (0.6, 0.7)
        self.layout.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        # info label
        self.info_label = Label(font_size=18, color="#00FFCF")
        self.layout.add_widget(self.info_label)

        # user field
        self.user_field = TextInput(
            multiline=False,
            padding_y=(20, 20),
            size_hint=(1, 0.25),
            hint_text="Username",
        )
        self.user_field.bind(on_text_validate=self.on_user_field_enter)
        self.layout.add_widget(self.user_field)

        # password fields
        self.password_field_one = TextInput(
            multiline=False,
            padding=(20, 20, 20, 20),
            size_hint=(1, 0.25),
            password=True,
            hint_text="Password",
        )
        self.password_field_one.bind(on_text_validate=self.on_password_one_enter)
        self.layout.add_widget(self.password_field_one)

        self.password_field_two = TextInput(
            multiline=False,
            padding=(20, 20, 20, 20),
            size_hint=(1, 0.25),
            password=True,
            hint_text="Confirm Password",
        )
        self.password_field_two.bind(on_text_validate=self.create_account)
        self.layout.add_widget(self.password_field_two)

        # create button
        self.create_button = Button(
            size_hint=(1, 0.25),
            bold=True,
            background_color="#FFFF00",
        )
        self.create_button.bind(on_press=self.create_account)
        self.layout.add_widget(self.create_button)

        # Add the layout only once
        self.add_widget(self.layout)

    def on_enter(self, *args):
        super(CreateAccountScreen, self).on_enter(name_screen="create_account", *args)

    def validation_password(self, password_one, password_two):
        if password_one != password_two:
            self.info_label.text = self.get_message_with_variables(
                "create_account", "password_not_match"
            )
            return False

        if len(password_one) <= 5:
            self.info_label.text = self.get_message_with_variables(
                "create_account", "short_password"
            )
            return False
        return True

    def create_account(self, instance) -> None:
        # Validate input
        username = self.user_field.text.strip()
        if not username:
            self.info_label.text = self.get_message_with_variables(
                "create_account", "empty_user"
            )
            return
        # Check if username exists
        elif self.session_manager.db.find_record(User, username=username):
            self.info_label.text = self.get_message_with_variables(
                "create_account", "user_exists"
            )
            return

        password_one = self.password_field_one.text
        password_two = self.password_field_two.text
        # check passwords validation
        if not self.validation_password(password_one, password_two):
            return

        # Create a new user with game levels
        self.session_manager.db.create_account(username, password_one)

        self.info_label.text = self.get_message_with_variables(
            "create_account", "account_created"
        )
        self.manager.current = "login"

    def on_user_field_enter(self, instance) -> None:
        """When user presses enter in username field, focus moves to first password field"""
        self.password_field_one.focus = True

    def on_password_one_enter(self, instance) -> None:
        """When user presses enter in first password field, focus moves to second password field"""
        self.password_field_two.focus = True
