from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup


class InstructionPopup(Popup):
    def __init__(
        self,
        title: str,
        message: str,
        manager: ObjectProperty,
        target_screen: str,
        **kwargs
    ):
        super(InstructionPopup, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (400, 200)
        self.title = title
        self.manager = manager
        self.target_screen = target_screen

        # Create content layout
        content = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # Message label
        message_label = Label(text=message, size_hint_y=0.7)
        content.add_widget(message_label)

        # OK button
        ok_button = Button(
            text="OK",
            size_hint=(None, None),
            size=(100, 40),
            pos_hint={"center_x": 0.5},
        )
        ok_button.bind(on_press=self.go_to_screen)
        content.add_widget(ok_button)

        self.content = content

    def go_to_screen(self, *args):
        self.dismiss()
        self.manager.current = self.title_screen
