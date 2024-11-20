from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from ..models.user import User
from ..user.session import hash_password, verify_password


class LoginScreen(Screen):
    def __init__(self, session, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.session = session

        self.layout = GridLayout()
        self.layout.cols = 1
        self.layout.size_hint = (0.6, 0.7)
        self.layout.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        # info label
        self.info_label = Label(text="", font_size=18, color="#00FFCF")
        self.info_label.text = "Login"
        self.layout.add_widget(self.info_label)

        # user field
        self.user_field = TextInput(
            multiline=False, padding_y=(20, 20), size_hint=(1, 0.25)
        )
        self.layout.add_widget(self.user_field)

        # password field
        self.password_field = TextInput(
            multiline=False,
            padding=(20, 20, 20, 20),
            size_hint=(1, 0.25),
            password=True,
        )
        self.layout.add_widget(self.password_field)

        # login button
        self.login_button = Button(
            text="Login", size_hint=(1, 0.25), bold=True, background_color="#00FFCF"
        )
        self.login_button.bind(on_press=self.authorization)
        self.layout.add_widget(self.login_button)

        # create account button
        self.create_button = Button(
            text="Create account",
            size_hint=(1, 0.25),
            bold=True,
            background_color="#FFFF00",
        )
        self.create_button.bind(on_press=self.create_account_manager)
        self.layout.add_widget(self.create_button)

        self.add_widget(self.layout)

    def authorization(self, instance):
        username = self.user_field.text.strip()
        password = self.password_field.text

        user = self.session.query(User).filter_by(username=username).first()

        if user and verify_password(user.password, password):
            self.info_label.text = "Login successful!"
            self.manager.current = "menu"
        else:
            self.info_label.text = "Login failed!"

    def create_account_manager(self, instance):
        self.manager.current = "create_account"


class CreateAccountScreen(Screen):
    def __init__(self, session, **kwargs):
        super(CreateAccountScreen, self).__init__(**kwargs)
        self.session = session
        self.layout = GridLayout()
        self.layout.cols = 1
        self.layout.size_hint = (0.6, 0.7)
        self.layout.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        # info label
        self.info_label = Label(text="Create account", font_size=18, color="#00FFCF")
        self.layout.add_widget(self.info_label)

        # user field
        self.user_field = TextInput(
            multiline=False, padding_y=(20, 20), size_hint=(1, 0.25)
        )
        self.layout.add_widget(self.user_field)

        # password fields
        self.password_field_one = TextInput(
            multiline=False,
            padding=(20, 20, 20, 20),
            size_hint=(1, 0.25),
            password=True,
        )
        self.layout.add_widget(self.password_field_one)

        self.password_field_two = TextInput(
            multiline=False,
            padding=(20, 20, 20, 20),
            size_hint=(1, 0.25),
            password=True,
        )
        self.layout.add_widget(self.password_field_two)

        # create button
        self.create_button = Button(
            text="Create account",
            size_hint=(1, 0.25),
            bold=True,
            background_color="#FFFF00",
        )
        self.create_button.bind(on_press=self.create_account)
        self.layout.add_widget(self.create_button)

        # Add the layout only once
        self.add_widget(self.layout)

    def create_account(self, instance):
        try:
            # Validate input
            username = self.user_field.text.strip()
            if not username:
                self.info_label.text = "Username cannot be empty!"
                return

            password_one = self.password_field_one.text
            password_two = self.password_field_two.text

            if password_one != password_two:
                self.info_label.text = "Passwords do not match!"
                return

            if len(password_one) <= 5:
                self.info_label.text = "Password must be longer than 5 characters!"
                return

            # Check if username exists
            existing_user = (
                self.session.query(User).filter_by(username=username).first()
            )
            if existing_user:
                self.info_label.text = "Username already exists!"
                return

            # Create new user
            new_user = User(username=username, password=hash_password(password_one))
            self.session.add(new_user)
            self.session.commit()

            self.info_label.text = "Account created successfully!"
            self.manager.current = "login"

        except Exception as e:
            self.info_label.text = f"Error creating account: {str(e)}"
            self.session.rollback()
