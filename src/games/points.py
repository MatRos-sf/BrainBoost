from typing import List


class Points:
    def __init__(self, level: int):
        self.level = level
        self.points = 0
        self.answers_status: List[bool] = []

    def update_points(self, is_wrong_answer: bool = False, bonus: int = 1) -> None:
        if is_wrong_answer:
            self.points -= self.level * bonus
        else:
            self.points += self.level * bonus
