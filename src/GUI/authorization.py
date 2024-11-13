from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        self.layout = GridLayout()
        self.layout.cols = 1
        self.layout.size_hint = (0.6, 0.7)
        self.layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # info label
        self.info_label = Label(
            text="",
            font_size=18,
            color='#00FFCF'
        )
        self.layout.add_widget(self.info_label)

        # user field
        self.user_field = TextInput(
            multiline=False,
            padding_y=(20, 20),
            size_hint=(1, 0.25)
        )
        self.layout.add_widget(self.user_field)

        # password field
        self.password_field = TextInput(
            multiline=False,
            padding_y=(20, 20),
            size_hint=(1, 0.25),
            password=True
        )
        self.layout.add_widget(self.password_field)

        # buttons
        self.login_button = Button(
            text="Login",
            size_hint=(1, 0.25),
            bold=True,
            background_color='#FFFFFF'
        )
        self.login_button.bind(on_press=self.authorization)
        self.layout.add_widget(self.login_button)

        self.create_button = Button(
            text="Create account",
            size_hint=(1, 0.25),
            bold=True,
            background_color='#FFFF00'
        )
        self.create_button.bind(on_press=self.create_account)
        self.layout.add_widget(self.create_button)

        self.add_widget(self.layout)

    def authorization(self, instance):
        # TODO: authorization
        raise NotImplementedError()

    def create_account(self, instance):
        #TODO: create account
        raise NotImplementedError()




