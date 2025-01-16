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
        self.size = (400, 300)  # Przykładowe rozmiary popupu
        self.title = title
        self.manager = manager
        self.target_screen = target_screen

        # Create content layout
        content = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # Message label
        message_label = Label(
            text=message,
            size_hint_y=0.7,
            halign="center",
            valign="top",
        )
        message_label.bind(size=self._update_text_size)

        # Ustawienie text_size pozwala na automatyczne zawijanie tekstu
        message_label.text_size = (self.size[0] - 40, None)  # Margines 40px

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
        self.manager.current = self.target_screen

    def _update_text_size(self, instance, value):
        """Adjust the text size to fit the label."""
        instance.text_size = (self.size[0] - 40, None)  # Aktualizuj marginesy
