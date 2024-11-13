from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager
from kivy.tests.common import GraphicUnitTest

from src.GUI.authorization import LoginScreen

class TestLoginScreen(GraphicUnitTest):
    def setUp(self):
        super(TestLoginScreen, self).setUp()
        self.screen_manager = ScreenManager()
        self.login_screen = LoginScreen(name='login')
        self.screen_manager.add_widget(self.login_screen)
        self.screen_manager.current = 'login'

    def test_widgets_exist(self):
        """Verifies that all widgets exist"""
        assert isinstance(self.login_screen.info_label, Label)
        assert isinstance(self.login_screen.user_field, TextInput)
        assert isinstance(self.login_screen.password_field, TextInput)
        assert isinstance(self.login_screen.login_button, Button)
        assert isinstance(self.login_screen.create_button, Button)

    def test_create_account_button_raises_not_implemented_error(self):
        create_button = self.login_screen.create_button
        with self.assertRaises(NotImplementedError):
            create_button.dispatch('on_press')

    def test_authorization_button_raises_not_implemented_error(self):
        login_button = self.login_screen.login_button
        with self.assertRaises(NotImplementedError):
            login_button.dispatch('on_press')

