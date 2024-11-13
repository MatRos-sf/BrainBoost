from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from src.GUI.authorization import LoginScreen
from src.GUI.menu import MenuScreen

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(MenuScreen(name="menu"))
        sm.current = "login"
        return sm

if __name__ == "__main__":
    MyApp().run()