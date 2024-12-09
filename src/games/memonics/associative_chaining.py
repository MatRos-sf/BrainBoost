from enum import Enum
from itertools import zip_longest
from pathlib import Path
from random import sample
from typing import Generator, List, Tuple

from src.games.points import Points


class LanguagePrefix(Enum):
    PL = "pl"
    EN = "en"


class Color(Enum):
    RED = "#FF0000"
    YELLOW = "#FFFF00"
    GREEN = "#00FF00"


class AssociativeChaining:
    BAD_ANSWER_COLOR = Color.RED.value
    CORRECT_ANSWER_COLOR = Color.YELLOW.value
    GOOD_ANSWER_COLOR = Color.GREEN.value

    def __init__(self, level: int, language: LanguagePrefix = LanguagePrefix.PL):
        self.level = level
        self.data_file = language.value + "_noun"
        self.path_file = Path(__file__).parent / Path("data") / Path(self.data_file)
        self.payload = []
        self.size = None
        self.points = Points(level)

    def create_payload(self, size: int):
        with open(self.path_file, encoding="utf-8") as file:
            raw_payload = file.read().split("\n")
        self.payload = sample(raw_payload, size)

    def check_answer(self, answers: List[str]) -> List[Tuple[str, str]]:
        result = []
        answers = [a.lower() for a in answers]
        for user_answer, answer in zip_longest(answers, self.payload):
            # points for good order
            if user_answer == answer:
                self.points.update_points(bonus=2)
                result.append((user_answer, AssociativeChaining.CORRECT_ANSWER_COLOR))
            # points for memorizes noun
            elif user_answer in self.payload:
                self.points.update_points()
                result.append((user_answer, AssociativeChaining.GOOD_ANSWER_COLOR))
            else:
                self.points.update_points(is_wrong_answer=True)
                result.append((user_answer, AssociativeChaining.BAD_ANSWER_COLOR))
        return result

    def run(self) -> Generator[List[str], List[str], List[Tuple[str, str]]]:
        self.create_payload(10)
        answer = yield self.payload
        result = self.check_answer(answer)
        return result
