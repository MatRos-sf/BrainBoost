from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from ..db.db import DATABASE_URL, engine, session
from .authorization import CreateAccountScreen, LoginScreen
from .menu import MenuScreen


class MyApp(App):
    def __init__(self, database_url=DATABASE_URL, **kwargs):
        super(MyApp, self).__init__(**kwargs)
        # Initialize database
        self.db_engine = engine(database_url)
        self.db_session = session(self.db_engine)

    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(session=self.db_session, name="login"))
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(
            CreateAccountScreen(session=self.db_session, name="create_account")
        )
        sm.current = "login"
        return sm

    def on_stop(self):
        # Clean up database session when app closes
        if hasattr(self, "db_session"):
            self.db_session.close()


if __name__ == "__main__":
    MyApp().run()
