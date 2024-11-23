import random
from typing import List, Optional


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

    def run(self):
        self.create_payload()
        chars = self._set_math_char()
        payload = self.payload
        mistake_counter = 0
        a, b = payload[0], payload[1]
        result = self.calculate(a, b, chars[0])
        answer = int(input(f"{a} {chars[0]} {b} = "))

        while True:
            if answer == result:
                break
            mistake_counter += 1
            print("Wrong answer")
            answer = int(input(f"{a} {chars[0]} {b} = "))
        for index, no in enumerate(payload[2:], 1):
            a, b = answer, no
            result = self.calculate(a, b, chars[index])
            answer = int(input(f"{chars[index]} {b} = "))
            while True:
                if answer == result:
                    break
                mistake_counter += 1
                print("Wrong answer")
                answer = int(input(f"{a} {chars[index]} {b} = "))


a = ResultKeeper(1)
a.run()
