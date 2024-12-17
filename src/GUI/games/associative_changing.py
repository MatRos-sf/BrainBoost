import datetime
from itertools import zip_longest
from math import ceil
from typing import List, Optional, Tuple

from kivy.clock import Clock
from kivy.lang import Builder

from src.db.session import GameManager
from src.games.mnemonic.associative_chaining import AssociativeChaining
from src.models.games import (
    AssociativeChangingModel,
    AssociativeChangingSessionModel,
    GameName,
)
from src.models.user import PointsCategory

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
    NAME_GAME = GameName.ASSOCIATIVE_CHANGING

    def __init__(self, session_manager: GameManager, **kwargs):
        super(AssociativeChainingScreen, self).__init__(session_manager, **kwargs)
        self.associative_chaining: Optional[AssociativeChaining] = None
        self.timer_label.text = "00:00:00"
        self.time_press_start: Optional[int] = None

    def on_kv_post(self, base_widget):
        self.timer_label.text = "00:00:00"

    def on_enter(self):
        """Called when the screen is entered"""
        # Start new game
        self.start_new_game()

    def initialize_game_state(self):
        self.find_innit_level(PointsCategory.FIRST_ASSOCIATIVE_CHANGING.value[1])
        self.associative_chaining = AssociativeChaining(self.init_level)
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
        points = self.associative_chaining.points.points
        return f"\nYou earned {points} points.\nYou have memorized {self.associative_chaining.points.correct_answers} nouns and forgotten {self.associative_chaining.points.wrong_answer} nouns and missed {self.associative_chaining.skip_answers}\n"

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
            self.time_press_start = self.time
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
            self.save_stats()
            # hide and opacity start_button
            self.start_button.opacity = 0
            self.start_button.disabled = True
            self.show_end_game_buttons()
            self.__finished_message()
        else:
            raise ValueError(
                f"Invalid button text: start_game.text = {self.start_game.text}"
            )

    def save_stats(self):
        user_session = self.session_manager.current_session
        game_stats = self.associative_chaining.get_stats()
        started_level = game_stats.get("started_level")
        finished_level = game_stats.get("finished_level")
        earned_point = game_stats.get("points_earned")

        game = user_session.stats.get(self.NAME_GAME.value)
        # Save session stats
        self.session_manager.db.add_record(
            AssociativeChangingSessionModel,
            associative_changing_id=game.id,
            duration=self.time,
            memorization_time=self.time_press_start,
            **game_stats,
        )

        self.session_manager.db.add_points_for_game(
            user_id=user_session.id,
            point=earned_point,
            category=PointsCategory.GAME_ASSOCIATIVE_CHANGING,
        )
        if started_level < finished_level:
            # update level
            self.session_manager.db.update_record(
                AssociativeChangingModel, game.id, {"level": finished_level}
            )
            # update level in current session
            self.session_manager.update_level_of_game(self.NAME_GAME, finished_level)
        # update points in current session
        self.session_manager.update_point(earned_point)
