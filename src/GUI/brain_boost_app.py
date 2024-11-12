from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from src.GUI.authorization import LoginScreen
from src.GUI.menu import MenuScreen

class NavigationManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Adding screen to the manager
        self.add_widget(LoginScreen(name="login"))
        self.add_widget(MenuScreen(name="menu"))

    def go_to_screen(self, screen_name: str) -> None:
        self.current = screen_name

class BrainBoostApp(App):
    def build(self):
        return NavigationManager()

if __name__ == "__main__":
    BrainBoostApp().run()