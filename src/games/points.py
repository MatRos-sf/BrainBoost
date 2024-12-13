from typing import List


class Points:
    def __init__(self, level: int):
        self.level = level
        self.points = 0
        self.answers_status: List[bool] = []
        self.correct_answers: int = 0
        self.wrong_answer: int = 0

    def update_points(self, is_wrong_answer: bool = False, bonus: int = 1) -> None:
        if is_wrong_answer:
            self.points -= self.level * bonus
            self.wrong_answer += 1
        else:
            self.points += self.level * bonus
            self.correct_answers += 1
