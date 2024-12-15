import datetime
from itertools import zip_longest
from math import ceil
from typing import List, Optional, Tuple

from kivy.clock import Clock
from kivy.lang import Builder

from src.db.session import GameManager
from src.games.memonics.associative_chaining import AssociativeChaining

from .base_game_screen import BaseGamaScreen

Builder.load_file("src/GUI/games/associative_chaining.kv")


def convert_answer_to_list(answer: str) -> List[str]:
    return [a.strip() for a in answer.split(",")]


def create_row(left_side: Tuple[int, str], right_side: Optional[Tuple[int, str]]):
    if right_side and left_side:
        left = f"{left_side[0]:>3}. {left_side[1]:<30}"
        right = f"{right_side[0]:>3}. {right_side[1]:<30}"
        return f"{left} {right}\n"
    else:
        return f"{left_side[0]:>3}. {left_side[1]}\n"


def pretty_print(list_to_print: List[str]):
    """
    Function to print list in a pretty way
    """
    # split list to two parts
    str_list = ""
    first_part = []
    second_part = []
    mid = ceil(len(list_to_print) / 2)
    for idx, item in enumerate(list_to_print, start=1):
        if idx <= mid:
            first_part.append((idx, item))
        else:
            second_part.append((idx, item))

    for left_side, right_side in zip_longest(first_part, second_part):
        str_list += create_row(left_side, right_side)

    return str_list


def convert_seconds_to_time(seconds: int):
    return str(datetime.timedelta(seconds=seconds))


MESSAGE = """
Please enter a list of remembered nouns separated by commas. If you don't know a noun, you can enter `-`.
For example, to recall dog, cat, fan, if you remember only dog and fan, you can enter: `dog, -, fan` to earn 4 points but if you enter: 'dog, cat' you earn 2 points.
Good luck!
"""


class AssociativeChainingScreen(BaseGamaScreen):
    def __init__(self, session_manager: GameManager, **kwargs):
        super(AssociativeChainingScreen, self).__init__(session_manager, **kwargs)
        self.associative_chaining: Optional[AssociativeChaining] = None
        self.timer_label.text = "00:00:00"

    def on_kv_post(self, base_widget):
        self.timer_label.text = "00:00:00"

    def on_enter(self):
        """Called when the screen is entered"""
        # Start new game
        self.start_new_game()

    def initialize_game_state(self):
        self.associative_chaining = AssociativeChaining(1)
        self.game = self.associative_chaining.run()

        # capture list to memorise
        question = next(self.game)
        self.question_label.text = pretty_print(question)
        # unlock label
        self.hide_end_game_buttons()
        self.start_button.opacity = 1
        self.start_button.disabled = False

        # clean label
        self.answer_field.text = ""
        self.timer_label.text = "00:00:00"

    def start_new_game(self):
        self.cleanup_clock_events()
        self.initialize_game_state()
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        """Update timer every second"""
        self.time += 1
        self.timer_label.text = f"{convert_seconds_to_time(self.time)}"

    def check_answer(self):
        answer = self.answer_field.text
        answer = convert_answer_to_list(answer)
        result = None
        # send answer to game
        try:
            self.game.send(answer)
        except StopIteration as e:
            result = e.value
        return result

    def _merge_colors(self, colors: List[Tuple[str, str]]):
        # Convert #FF0000 to RGB format with parentheses
        return [f"[color={color}]{text or ''}[/color]" for text, color in colors]

    def __finished_message(self):
        points = self.associative_chaining.points.point
        return f"\nYou earned {points} points.\nYou have memorized {self.associative_chaining.memorized} nouns and forgotten {self.associative_chaining.forgot} nouns and missed {self.associative_chaining.missed}\n"

    def show_user_answer(self, user_answer: List[Tuple[str, str]]):
        answer = self._merge_colors(user_answer)
        message = self.__finished_message()
        self.question_label.text = (
            message
            + pretty_print(answer)
            + "\n List on nouns: \n"
            + pretty_print(self.associative_chaining.payload)
        )

    def start_game(self, instance):
        # Hide question label and show answer label
        if self.start_button.text.lower() == "start":
            self.question_label.text = MESSAGE
            self.answer_field.opacity = 1
            self.start_button.text = "Stop"
        # review answer
        elif self.start_button.text.lower() == "stop":
            self.answer_field.opacity = 0
            # check answer
            answer = self.check_answer()
            self.show_user_answer(answer)
            # return to start
            self.start_button.text = "Start"
            self.timer_event.cancel()
            # time = self.time
            # hide and opacity start_button
            self.start_button.opacity = 0
            self.start_button.disabled = True
            self.show_end_game_buttons()
            self.__finished_message()
        else:
            raise ValueError(
                f"Invalid button text: start_game.text = {self.start_game.text}"
            )
