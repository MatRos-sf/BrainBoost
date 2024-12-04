from typing import List


class Points:
    def __init__(self, level: int):
        self.level = level
        self.points = 0
        self.answers_status: List[bool] = []

    def update_points(self) -> None:
        self.points += self.level
