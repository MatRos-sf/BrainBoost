from kivy.tests.common import GraphicUnitTest
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager

from src.GUI.menu import MenuScreen


class TestMenuScreen(GraphicUnitTest):
    def setUp(self):
        super(TestMenuScreen, self).setUp()
        self.screen_manager = ScreenManager()
        self.menu_screen = MenuScreen(name="menu")
        self.screen_manager.add_widget(self.menu_screen)
        self.screen_manager.current = "menu"

    def test_widgets_exists(self):
        """Verifies that all widgets exist"""
        assert isinstance(self.menu_screen.result_keep, Button)
        assert isinstance(self.menu_screen.option2, Button)
        assert isinstance(self.menu_screen.settings_button, Button)
        assert isinstance(self.menu_screen.logout_button, Button)
