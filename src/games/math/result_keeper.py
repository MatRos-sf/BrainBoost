import random
from typing import Dict, Generator, List, Optional

from src.games.points import Points


class ResultKeeper:
    def __init__(self, level: int):
        self.level = level
        self.level_start = self.level
        self.payload = []
        self.points = Points(level)
        self._is_init = False
        self.lives_left = 3
        self.steps = 0
        self.finish_round = False
        self.range_min = 0

    @property
    def range_size(self):
        return 5 + self.level * 5

    def get_stats(self) -> Dict[str, int]:
        return {
            "range_min": self.range_min,
            "range_max": self.range_size,
            "points_earned": self.points.points,
            "started_level": self.level_start,
            "finished_level": self.level,
            "steps": self.steps,
            "wrong_answers": self.points.wrong_answer,
            "correct_answers": self.points.correct_answers,
        }

    def _set_math_char(self, math_char: Optional[List[str]] = None) -> List[str]:
        """Generate a sequence of mathematical operations that work with the given payload."""
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
                payload[i] = random.randint(1, self.range_size)  # Avoid 0 for division
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

            if valid_operation and 0 <= temp_res <= self.range_size:
                result.append(char)
                i += 1
                r = temp_res
                chars = math_char[:]
            else:
                chars.remove(char)

        if len(result) < 9:  # We need 9 operations for 10 numbers
            raise ValueError("Could not find valid sequence of operations")
        self.payload = payload
        return result

    def create_payload(self, payload: Optional[List[int]] = None):
        if not payload:
            payload = []
        size_payload = len(payload)
        payload += [
            random.randint(0, self.range_size) for _ in range(10 - size_payload)
        ]
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
            case _:
                raise ValueError(f"Invalid operation: {op}")

    def _question(self, a: int, b: int, char: str):
        """Helper method to generate questions"""
        return f"{a} {char} {b} = " if self._is_init else f"{char} {b}"

    def _get_answer(
        self, expected_result: int, question: str
    ) -> Generator[tuple[str, bool], int, Optional[int]]:
        """Helper method to handle answer validation"""
        while True:
            answer = yield question, False
            if answer == expected_result:
                self.points.update_points()
                self._is_init = False
                self.steps += 1
                yield question, True  # Signal success to the UI
                return answer  # Return for next calculation
            else:
                self.points.answers_status.append(False)
                self.lives_left -= 1
                self.points.update_points(True)
                if self.lives_left == 0:
                    return None

    def round(self):
        chars = self._set_math_char()
        payload = self.payload

        # First question
        a, b = payload[0], payload[1]
        result = self.calculate(a, b, chars[0])
        answer = yield from self._get_answer(result, self._question(a, b, chars[0]))
        if answer is None:
            return None
        # Subsequent questions
        for index, no in enumerate(payload[2:], 1):
            a = answer  # Use previous answer
            b = no  # Get next number
            result = self.calculate(a, b, chars[index])
            answer = yield from self._get_answer(result, f"{chars[index]} {b} = ")
            if answer is None:
                return None
        self.create_payload([answer])
        self.finish_round = True

    def run(self) -> Generator[tuple[str, bool], int, None]:
        """Run the game, yielding (question, is_correct) tuples and accepting answers"""
        self._is_init = True
        self.create_payload()
        while True:
            answer = yield from self.round()
            if answer is None and not self.finish_round:
                return None

            if all(self.points.answers_status):
                self.points.answers_status = []
                self.points.level += 1
                self.level += 1
                self.finish_round = False
            else:
                self.points.answers_status = []
