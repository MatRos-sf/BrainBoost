from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput


class ResultKeeperScreen(Screen):
    def __init__(self, **kwargs):
        super(ResultKeeperScreen, self).__init__(**kwargs)
        self.count = 0
        # Initialize widgets
        self.info_label = Label(
            text="Hi",
            font_size=18,
            size_hint=(1, 0.15),
            halign="center",
            valign="middle",
        )
        self.question_field = Label(
            text="Question",
            font_size=18,
            size_hint=(1, 0.15),
            halign="center",
            valign="middle",
        )
        self.answer_field = TextInput(
            hint_text="Answer",
            multiline=False,
            padding=(20, 20, 20, 20),
            size_hint=(1, 0.25),
        )
        self.setup_layout()

    def setup_layout(self):
        """Setup the screen layout with all widgets"""
        self.layout = GridLayout()
        self.layout.cols = 1
        self.layout.size_hint = (0.6, 0.7)
        self.layout.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.layout.spacing = 10

        # Add info label
        self.layout.add_widget(self.info_label)

        # Add question field
        self.layout.add_widget(self.question_field)

        # Add answer field
        self.answer_field.bind(on_text_validate=self.on_answer_field_enter)
        self.layout.add_widget(self.answer_field)
        self.add_widget(self.layout)

    def on_enter(self):
        """Called when the screen is entered"""
        from kivy.clock import Clock

        Clock.schedule_once(lambda dt: setattr(self.answer_field, "focus", True), 0.1)

    def on_answer_field_enter(self, instance):
        """When user presses enter in answer field"""
        try:
            int(self.answer_field.text)
        except ValueError:
            self.answer_field.text = ""
            self.info_label.text = "Answer must be a number!"
            return
        finally:
            Clock.schedule_once(lambda dt: setattr(self.answer_field, "focus", True), 0)

        self.answer_field.text = ""
        self.count += 1
        self.info_label.text = f"Correct answers: {self.count}"
