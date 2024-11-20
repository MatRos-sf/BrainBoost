from unittest.mock import MagicMock, patch

import pytest
from kivy.tests.common import GraphicUnitTest
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput

from src.GUI.authorization import CreateAccountScreen, LoginScreen


class TestLoginScreen(GraphicUnitTest):
    def setUp(self):
        super(TestLoginScreen, self).setUp()
        self.screen_manager = ScreenManager()
        # Create a mock session
        self.mock_session = MagicMock()

        # Add all necessary screens
        self.login_screen = LoginScreen(session=self.mock_session, name="login")
        self.create_account_screen = CreateAccountScreen(
            session=self.mock_session, name="create_account"
        )
        self.menu_screen = Screen(name="menu")  # Mock menu screen

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

    def test_create_account_button_changes_screen(self):
        """Test that create account button changes screen to create_account"""
        # Set current screen to login
        self.screen_manager.current = "login"

        # Click create account button
        create_button = self.login_screen.create_button
        create_button.dispatch("on_press")

        # Verify screen changed
        self.assertEqual(self.screen_manager.current, "create_account")

    @patch("src.GUI.authorization.verify_password")
    def test_failed_login_shows_error(self, mock_verify):
        """Test that failed login shows error message"""
        # Setup mocks
        mock_verify.return_value = False
        mock_user = MagicMock()
        mock_user.password = "stored_hash"
        self.mock_session.query().filter_by().first.return_value = mock_user

        # Set test values
        self.login_screen.user_field.text = "test_user"
        self.login_screen.password_field.text = "wrong_password"

        # Trigger login
        self.login_screen.login_button.dispatch("on_press")

        # Check error message
        self.assertEqual(self.login_screen.info_label.text, "Login failed!")
        mock_verify.assert_called_once_with("stored_hash", "wrong_password")

    @patch("src.GUI.authorization.verify_password")
    def test_successful_login_changes_screen(self, mock_verify):
        """Test that successful login changes screen and shows success message"""
        # Setup mocks
        mock_verify.return_value = True
        mock_user = MagicMock()
        mock_user.password = "stored_hash"
        self.mock_session.query().filter_by().first.return_value = mock_user

        # Set test values
        self.login_screen.user_field.text = "test_user"
        self.login_screen.password_field.text = "correct_password"

        # Set current screen to login
        self.screen_manager.current = "login"

        # Trigger login
        self.login_screen.login_button.dispatch("on_press")

        # Check success message and screen change
        self.assertEqual(self.login_screen.info_label.text, "Login successful!")
        self.assertEqual(self.screen_manager.current, "menu")
        mock_verify.assert_called_once_with("stored_hash", "correct_password")


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
