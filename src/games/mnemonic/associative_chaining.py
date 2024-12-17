from enum import Enum
from itertools import zip_longest
from pathlib import Path
from random import sample
from typing import Generator, List, Tuple

from src.games.points import Points

DATA_PATH = Path(__file__).parent.parent / Path("data")


class LanguagePrefix(Enum):
    PL = "pl"
    EN = "en"


class Color(Enum):
    RED = "FF0000"
    YELLOW = "FFFF00"
    GREEN = "00FF00"


class AssociativeChaining:
    BAD_ANSWER_COLOR = Color.RED.value
    CORRECT_ANSWER_COLOR = Color.GREEN.value
    GOOD_ANSWER_COLOR = Color.YELLOW.value
    START_SIZE = 10

    def __init__(self, level: int, language: LanguagePrefix = LanguagePrefix.PL):
        self.level = level
        self.level_start = self.level
        self.data_file = language.value + "_noun"
        self.path_file = DATA_PATH / Path(self.data_file)
        self.payload = []
        self.user_answers = []
        self.skip_answers = 0
        self._size = None
        self.points = Points(level)

    @property
    def size(self) -> int:
        size = AssociativeChaining.START_SIZE + self.level - 1
        return size if size <= 100 else 100

    def get_stats(self):
        return {
            "points_earned": self.points.points,
            "started_level": self.level_start,
            "finished_level": self.level,
            "wrong_answers": self.points.wrong_answer,
            "correct_answers": self.points.correct_answers,
            "skip_answers": self.skip_answers,
            "words": " ,".join(self.payload),
            "user_answers": " ,".join(self.user_answers),
            "amt_words": self.size,
        }

    def create_payload(self):
        with open(self.path_file, encoding="utf-8") as file:
            raw_payload = file.read().split("\n")
        self.payload = sample(raw_payload, self.size)

    def check_answer(self, answers: List[str]) -> List[Tuple[str, str]]:
        result = []
        answers = [a.lower() for a in answers]
        for user_answer, answer in zip_longest(answers, self.payload):
            # when to many answers
            if not answer:
                self.points.update_points(is_wrong_answer=True)
                result.append((user_answer, AssociativeChaining.BAD_ANSWER_COLOR))
                continue
            # points for good order
            if user_answer == answer:
                self.points.update_points(bonus=2)
                result.append((user_answer, AssociativeChaining.CORRECT_ANSWER_COLOR))
            # points for memorize noun
            elif user_answer in self.payload:
                self.points.update_points()
                result.append((user_answer, AssociativeChaining.GOOD_ANSWER_COLOR))
            else:
                # points for bad or missing answers
                if user_answer == "-":
                    self.skip_answers += 1
                elif user_answer is None:
                    self.points.wrong_answer += 1
                else:
                    self.points.update_points(is_wrong_answer=True)
                result.append((user_answer, AssociativeChaining.BAD_ANSWER_COLOR))
        # update level
        self.update_level()

        return result

    def update_level(self):
        if self.size == self.points.correct_answers:
            self.level += 1

    def run(self) -> Generator[List[str], List[str], List[Tuple[str, str]]]:
        self.create_payload()
        self.user_answers = yield self.payload
        result = self.check_answer(self.user_answers)
        return result
