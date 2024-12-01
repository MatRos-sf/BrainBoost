from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from src.db.session import GameManager

from ..db.db import DATABASE_URL
from .authorization import CreateAccountScreen, LoginScreen
from .games.result_keeper import ResultKeeperScreen
from .menu import MenuScreen


class MyApp(App):
    def __init__(self, database_url=DATABASE_URL, **kwargs):
        super(MyApp, self).__init__(**kwargs)
        # Initialize database
        self.session_manager = GameManager(database_url)

    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(session_manager=self.session_manager, name="login"))
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(
            CreateAccountScreen(
                session_manager=self.session_manager, name="create_account"
            )
        )
        sm.add_widget(
            ResultKeeperScreen(
                session_manager=self.session_manager, name="result_keeper_game"
            )
        )
        sm.current = "login"
        return sm

    def on_stop(self):
        # Clean up database session when app closes
        if hasattr(self, "db_session"):
            self.db_session.close()


if __name__ == "__main__":
    MyApp().run()
