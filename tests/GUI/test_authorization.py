from unittest.mock import MagicMock, patch

import pytest
from kivy.tests.common import GraphicUnitTest
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput

from src.GUI.authorization import CreateAccountScreen, LoginScreen, MessagePopup


class TestLoginScreen(GraphicUnitTest):
    def setUp(self):
        super(TestLoginScreen, self).setUp()
        self.session = MagicMock()
        self.login_screen = LoginScreen(session=self.session, name="login")
        self.create_account_screen = CreateAccountScreen(
            session=self.session, name="create_account"
        )
        self.menu_screen = Screen(name="menu")  # Mock menu screen

        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(self.login_screen)
        self.screen_manager.add_widget(self.create_account_screen)
        self.screen_manager.add_widget(self.menu_screen)

        self.screen_manager.current = "login"

    def test_widgets_exist(self):
        """Verifies that all widgets exist"""
        assert isinstance(self.login_screen.info_label, Label)
        assert isinstance(self.login_screen.user_field, TextInput)
        assert isinstance(self.login_screen.password_field, TextInput)
        assert isinstance(self.login_screen.login_button, Button)
        assert isinstance(self.login_screen.create_button, Button)
        assert isinstance(self.login_screen.remember_me, CheckBox)

    @patch("pathlib.Path.exists")
    @patch("builtins.open")
    def test_load_credentials(self, mock_open, mock_exists):
        """Test loading saved credentials"""
        # Mock the file operations
        mock_exists.return_value = True
        mock_file = MagicMock()
        mock_file.__enter__.return_value.read.return_value = '{"username": "test_user"}'
        mock_open.return_value = mock_file

        # Call load_credentials
        self.login_screen.load_credentials()

        # Check if credentials were loaded
        assert self.login_screen.user_field.text == "test_user"
        assert self.login_screen.remember_me.active is True

    @patch("pathlib.Path.mkdir")
    @patch("builtins.open")
    def test_save_credentials(self, mock_open, mock_mkdir):
        """Test saving credentials"""
        username = "test_user"
        password = "test_pass"

        # Call save_credentials
        self.login_screen.save_credentials(username, password)

        # Verify mkdir was called
        mock_mkdir.assert_called_once_with(exist_ok=True)

        # Verify file was written
        mock_open.assert_called_once()

    def test_show_message(self):
        """Test that show_message creates and shows a popup"""
        title = "Test Title"
        message = "Test Message"

        # Show message
        self.login_screen.show_message(title, message)

        # Get the popup from the list
        assert len(self.login_screen._popup) == 1
        popup = self.login_screen._popup[0]

        # Verify popup properties
        assert isinstance(popup, MessagePopup)
        assert popup.title == title

    @patch("src.GUI.authorization.verify_password")
    def test_failed_login_shows_popup(self, mock_verify):
        """Test that failed login shows error popup"""
        # Setup mocks
        mock_verify.return_value = False
        mock_user = MagicMock()
        mock_user.password = "stored_hash"
        self.session.query().filter_by().first.return_value = mock_user

        # Set test values
        self.login_screen.user_field.text = "test_user"
        self.login_screen.password_field.text = "wrong_password"

        # Trigger login
        self.login_screen.login_button.dispatch("on_press")

        # Get the popup from the list
        assert len(self.login_screen._popup) == 1
        popup = self.login_screen._popup[0]

        # Verify popup
        assert isinstance(popup, MessagePopup)
        assert popup.title == "Error"
        mock_verify.assert_called_once_with("stored_hash", "wrong_password")

    @patch("src.GUI.authorization.verify_password")
    def test_successful_login_shows_popup(self, mock_verify):
        """Test that successful login shows success popup"""
        # Setup mocks
        mock_verify.return_value = True
        mock_user = MagicMock()
        mock_user.password = "stored_hash"
        self.session.query().filter_by().first.return_value = mock_user

        # Set test values
        self.login_screen.user_field.text = "test_user"
        self.login_screen.password_field.text = "correct_password"

        # Set current screen to login
        self.screen_manager.current = "login"

        # Trigger login
        self.login_screen.login_button.dispatch("on_press")

        # Get the popup from the list
        assert len(self.login_screen._popup) == 1
        popup = self.login_screen._popup[0]

        # Verify popup and screen change
        assert isinstance(popup, MessagePopup)
        assert popup.title == "Success"
        assert self.screen_manager.current == "menu"
        mock_verify.assert_called_once_with("stored_hash", "correct_password")

    @patch("src.GUI.authorization.verify_password")
    def test_successful_login_clears_fields(self, mock_verify):
        """Test that successful login clears input fields"""
        # Setup mocks
        mock_verify.return_value = True
        mock_user = MagicMock()
        mock_user.password = "stored_hash"
        self.session.query().filter_by().first.return_value = mock_user

        # Set test values
        self.login_screen.user_field.text = "test_user"
        self.login_screen.password_field.text = "correct_password"

        # Trigger login
        self.login_screen.login_button.dispatch("on_press")

        # Verify fields are cleared
        assert self.login_screen.user_field.text == ""
        assert self.login_screen.password_field.text == ""


class TestCreateAccountScreen:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.screen_manager = ScreenManager()
        # Create a mock session
        self.mock_session = MagicMock()

        # Add all necessary screens
        self.create_account_screen = CreateAccountScreen(
            session=self.mock_session, name="create_account"
        )
        self.login_screen = Screen(name="login")  # Mock login screen
        self.menu_screen = Screen(name="menu")  # Mock menu screen

        self.screen_manager.add_widget(self.login_screen)
        self.screen_manager.add_widget(self.create_account_screen)
        self.screen_manager.add_widget(self.menu_screen)

        self.screen_manager.current = "create_account"

    def test_widgets_exist(self):
        """Verifies that all widgets exists"""
        assert isinstance(self.create_account_screen.info_label, Label)
        assert isinstance(self.create_account_screen.user_field, TextInput)
        assert isinstance(self.create_account_screen.password_field_one, TextInput)
        assert isinstance(self.create_account_screen.password_field_two, TextInput)
        assert isinstance(self.create_account_screen.create_button, Button)

    def test_create_account(self, fake_user_name):
        """Test that create account creates a new user"""
        # Generate a random username
        username = fake_user_name(8)  # Generate an 8-character username
        password = "123456789"
        self.create_account_screen.user_field.text = username
        self.create_account_screen.password_field_one.text = password
        self.create_account_screen.password_field_two.text = password
        self.mock_session.query().filter_by().first.return_value = None
        self.mock_session.add.return_value = None
        self.mock_session.commit.return_value = None
        # trigger create account
        self.create_account_screen.create_button.dispatch("on_press")

        assert self.mock_session.query().filter_by().first.called
        assert self.mock_session.add.called
        assert self.mock_session.commit.called
        assert (
            self.create_account_screen.info_label.text
            == "Account created successfully!"
        )
        assert self.screen_manager.current == "login"

    def test_create_account_password_mismatch(self, fake_user_name):
        # Generate a random username
        username = fake_user_name(8)  # Generate an 8-character username
        password = "123456789"
        password_two = "12345678"
        self.create_account_screen.user_field.text = username
        self.create_account_screen.password_field_one.text = password
        self.create_account_screen.password_field_two.text = password_two

        # trigger create account
        self.create_account_screen.create_button.dispatch("on_press")

        assert self.create_account_screen.info_label.text == "Passwords do not match!"

    @pytest.mark.parametrize("password_length", list(range(1, 6)))
    def test_create_account_password_too_short(self, password_length, fake_user_name):
        # Generate a random username
        username = fake_user_name(8)  # Generate an 8-character username
        password = fake_user_name(password_length)  # generate a random password
        self.create_account_screen.user_field.text = username
        self.create_account_screen.password_field_one.text = password
        self.create_account_screen.password_field_two.text = password

        # trigger create account
        self.create_account_screen.create_button.dispatch("on_press")

        assert (
            self.create_account_screen.info_label.text
            == "Password must be longer than 5 characters!"
        )

    def test_create_account_user_name_empty(self):
        password = "123456789"
        self.create_account_screen.user_field.text = ""
        self.create_account_screen.password_field_one.text = password
        self.create_account_screen.password_field_two.text = password

        # trigger create account
        self.create_account_screen.create_button.dispatch("on_press")

        assert self.create_account_screen.info_label.text == "Username cannot be empty!"

    def test_create_account_when_user_exists(self):
        # setup the mock chain
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_first = MagicMock()
        self.mock_session.query.return_value = mock_query
        mock_query.filter_by.return_value = mock_filter
        mock_filter.first.return_value = mock_first

        self.create_account_screen.user_field.text = "test_user"
        self.create_account_screen.password_field_one.text = "123456789"
        self.create_account_screen.password_field_two.text = "123456789"

        # mock user exists
        # self.mock_session.query().filter_by().first.return_value = True

        # trigger create account
        self.create_account_screen.create_button.dispatch("on_press")

        assert self.create_account_screen.info_label.text == "Username already exists!"

    def test_create_account_database_error(self):
        # Setup valid input data
        self.create_account_screen.user_field.text = "test_user"
        self.create_account_screen.password_field_one.text = "123456789"
        self.create_account_screen.password_field_two.text = "123456789"

        # Setup the mock chain for checking existing user
        mock_query = MagicMock()
        mock_filter = MagicMock()
        self.mock_session.query.return_value = mock_query
        mock_query.filter_by.return_value = mock_filter
        mock_filter.first.return_value = None  # User doesn't exist

        # Make session.commit raise an exception
        self.mock_session.commit.side_effect = Exception("Database error")

        # Trigger create account
        self.create_account_screen.create_button.dispatch("on_press")

        # Verify error handling
        assert (
            self.create_account_screen.info_label.text
            == "Error creating account: Database error"
        )
        assert self.mock_session.rollback.called  # Verify rollback was called
