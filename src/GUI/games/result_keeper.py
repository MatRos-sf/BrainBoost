# from src.games.math import ResultKeeper
import random
from typing import Generator, List, Optional

from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput


class ResultKeeper:
    def __init__(self, level: int):
        self.level = level
        self.payload = []

    def _set_math_char(
        self,
        math_char: Optional[List[str]] = None,
        max_range: int = 10,
    ) -> List[str]:
        """Generate a sequence of mathematical operations that work with the given payload.

        Args:
            math_char (Optional[List[str]]): List of allowed mathematical operations. Defaults to ['+', '-', '*', '/']
            max_range (int): Maximum allowed result value. Defaults to 10
        Returns:
            List[str]: List of mathematical operations

        Raises:
            ValueError: If payload is too short or no valid sequence of operations can be found
        """
        if not self.payload:
            self.create_payload()

        payload = self.payload
        if len(payload) < 10:
            raise ValueError("Payload must contain at least 10 numbers")

        if math_char is None:
            math_char = ["+", "-", "*", "/"]

        result = []
        chars = math_char[:]
        r = payload[0]
        i = 1

        while i < 10:
            temp_res = r
            if not chars:
                chars = math_char[:]
                payload[i] = random.randint(1, max_range)  # Avoid 0 for division
                continue

            char = random.choice(chars)
            valid_operation = True

            match char:
                case "+":
                    temp_res = r + payload[i]
                case "-":
                    if r - payload[i] < 0:
                        valid_operation = False
                    else:
                        temp_res = r - payload[i]
                case "*":
                    temp_res = r * payload[i]
                case "/":
                    if payload[i] == 0 or r % payload[i] != 0:
                        valid_operation = False
                    else:
                        temp_res = r // payload[i]  # Using integer division

            if valid_operation and 0 <= temp_res <= max_range:
                result.append(char)
                i += 1
                r = temp_res
                chars = math_char[:]
            else:
                chars.remove(char)

        if len(result) < 9:  # We need 9 operations for 10 numbers
            raise ValueError("Could not find valid sequence of operations")
        self.payload = payload
        print(payload)
        return result

    def create_payload(self):
        range_game = 5 + self.level * 5
        payload = [random.randint(0, range_game) for _ in range(10)]
        self.payload = payload

    def calculate(self, a, b, op):
        match op:
            case "+":
                return a + b
            case "-":
                return a - b
            case "*":
                return a * b
            case "/":
                return a // b

    def run(self) -> Generator[tuple[str, bool], int, None]:
        self.create_payload()
        chars = self._set_math_char()
        payload = self.payload
        mistake_counter = 0
        a, b = payload[0], payload[1]
        result = self.calculate(a, b, chars[0])

        answer = yield f"{a} {chars[0]} {b} = ", False
        while True:
            if answer == result:
                break
            mistake_counter += 1
            answer = yield f"{a} {chars[0]} {b} = ", False

        for index, no in enumerate(payload[2:], 1):
            a, b = answer, no
            result = self.calculate(a, b, chars[index])
            answer = yield f"{chars[index]} {b}", True
            while True:
                if answer == result:
                    break
                mistake_counter += 1
                answer = yield f"{chars[index]} {b}", False

        return False


class ResultKeeperScreen(Screen):
    def __init__(self, **kwargs):
        super(ResultKeeperScreen, self).__init__(**kwargs)
        r = ResultKeeper(1)
        self.game = r.run()
        message, _ = next(self.game)
        self.time_left = 60  # 60 seconds timer
        self.timer_event = None
        self.countdown = 3  # Initial countdown value

        # Initialize widgets
        self.countdown_label = Label(
            text="3",
            font_size=150,  # Large font for countdown
            size_hint=(1, 1),
            halign="center",
            valign="middle",
        )

        self.info_label = Label(
            text="Get Ready!",
            font_size=18,
            size_hint=(1, 0.15),
            halign="center",
            valign="middle",
        )
        self.timer_label = Label(
            text="Time left: 60s",
            font_size=18,
            size_hint=(1, 0.15),
            halign="center",
            valign="middle",
        )
        self.question_field = Label(
            text=message,
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
        # Create two layouts: one for countdown and one for game
        self.countdown_layout = GridLayout(cols=1, spacing=10, padding=10)
        self.countdown_layout.add_widget(self.countdown_label)

        self.game_layout = GridLayout(cols=1, spacing=10, padding=10)
        self.game_layout.add_widget(self.info_label)
        self.game_layout.add_widget(self.timer_label)
        self.game_layout.add_widget(self.question_field)
        self.answer_field.bind(on_text_validate=self.on_answer_field_enter)
        self.game_layout.add_widget(self.answer_field)

        # Initially show countdown layout
        self.add_widget(self.countdown_layout)

    def start_countdown(self, dt):
        """Update the countdown display"""
        self.countdown -= 1
        if self.countdown >= 0:
            self.countdown_label.text = str(self.countdown)
            return True
        else:
            # Switch to game layout and start the game
            self.remove_widget(self.countdown_layout)
            self.add_widget(self.game_layout)
            self.start_timer()
            Clock.schedule_once(lambda dt: setattr(self.answer_field, "focus", True), 0)
            return False

    def start_timer(self):
        """Start the 60-second countdown timer"""
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        """Update the timer display and check if time's up"""
        self.time_left -= 1
        self.timer_label.text = f"Time left: {self.time_left}s"

        if self.time_left <= 0:
            self.timer_event.cancel()  # Stop the timer
            self.info_label.text = "Game Over - Time's up!"
            self.answer_field.disabled = True
            return False
        return True

    def on_enter(self):
        """Called when the screen is entered"""
        # Start the countdown
        Clock.schedule_interval(self.start_countdown, 1)

    def _check_validation_input(self, input):
        """Check if the input is a number"""
        try:
            answer = int(self.answer_field.text)
        except ValueError:
            self.answer_field.text = ""
            self.info_label.text = "Answer must be a number!"
            Clock.schedule_once(lambda dt: setattr(self.answer_field, "focus", True), 0)

        return answer

    def on_answer_field_enter(self, instance):
        """When user presses enter in answer field"""
        try:
            answer = int(self.answer_field.text)
        except ValueError:
            self.answer_field.text = ""
            self.info_label.text = "Answer must be a number!"
            Clock.schedule_once(lambda dt: setattr(self.answer_field, "focus", True), 0)
            return

        try:
            message, result = self.game.send(answer)
            self.question_field.text = message
            if result:
                self.info_label.text = "Correct! Continue with the next operation."
            else:
                self.info_label.text = "Try again!"
        except StopIteration:
            self.timer_event.cancel()  # Stop the timer when game is finished
            self.info_label.text = "Congratulations! Game finished!"
            self.answer_field.disabled = True
            return

        self.answer_field.text = ""
        Clock.schedule_once(lambda dt: setattr(self.answer_field, "focus", True), 0)

    def on_leave(self):
        """Clean up when leaving the screen"""
        if self.timer_event:
            self.timer_event.cancel()
