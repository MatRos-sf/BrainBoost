from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager
from kivy.tests.common import GraphicUnitTest
from unittest.mock import MagicMock

from src.GUI.menu import MenuScreen

class TestMenuScreen(GraphicUnitTest):
    def setUp(self):
        super(TestMenuScreen, self).setUp()
        self.screen_manager = ScreenManager()
        self.menu_screen = MenuScreen(name='menu')
        self.screen_manager.add_widget(self.menu_screen)
        self.screen_manager.current ='menu'

    def test_widgets_exists(self):
        """Verifies that all widgets exist"""
        assert isinstance(self.menu_screen.option1, Label)
        assert isinstance(self.menu_screen.option2, Button)
        assert isinstance(self.menu_screen.option3, Button)
        assert isinstance(self.menu_screen.back_button, Button)


