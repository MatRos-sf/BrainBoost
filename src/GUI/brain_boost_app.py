from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from ..db.db import DATABASE_URL, engine, session
from .authorization import LoginScreen
from .menu import MenuScreen


class MyApp(App):
    def __init__(self, database_url=DATABASE_URL, **kwargs):
        super(MyApp, self).__init__(**kwargs)
        # Initialize database
        self.db_engine = engine(database_url)
        self.session = session(self.db_engine)

    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(MenuScreen(name="menu"))
        sm.current = "login"
        return sm


if __name__ == "__main__":
    MyApp().run()
