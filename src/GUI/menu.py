from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)

        self.layout = GridLayout(
            cols=1, size_hint=(0.6, 0.7), pos_hint={"center_x": 0.5, "center_y": 0.5}
        )

        # Options
        self.result_keeper = Button(text="Result Keeper", size_hint=(1, 0.3))
        self.option2 = Button(text="Option 2", size_hint=(1, 0.3))
        self.option3 = Button(text="Option 3", size_hint=(1, 0.3))
        self.back_button = Button(text="Logout", size_hint=(1, 0.3))

        # Bind button events
        self.back_button.bind(on_press=self.go_back)
        self.result_keeper.bind(on_press=self.start_game_result_keeper)

        self.layout.add_widget(self.result_keeper)
        self.layout.add_widget(self.option2)
        self.layout.add_widget(self.option3)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)

    def go_back(self, instance):
        self.manager.current = "login"

    def start_game_result_keeper(self, instance):
        self.manager.current = "result_keeper_game"
