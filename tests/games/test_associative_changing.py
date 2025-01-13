import random
from unittest.mock import patch

import pytest

from src.games.mnemonic.associative_chaining import AssociativeChaining
from src.models.enum_types import Language


class TestAssociativeChaining:
    @pytest.mark.parametrize(
        "level, expected",
        [(1, 10), (2, 11), (20, 29), (90, 99), (91, 100), (92, 100), (200, 100)],
    )
    def test_size_of_payload(self, level, expected):
        """Verify that the size is changed based on the level."""
        associative_chaining = AssociativeChaining(level, Language.EN)
        assert associative_chaining.size == expected

    @pytest.mark.parametrize("level", [1, 2, random.randint(3, 90), 99, 100, 200])
    def test_create_payload_should_have_size_equal_to_size(self, level):
        associative_chaining = AssociativeChaining(level, Language.EN)
        associative_chaining.create_payload()
        assert len(associative_chaining.payload) == associative_chaining.size

    def test_check_answer_should_return_all_green_color_results(self):
        associative_chaining = AssociativeChaining(1, Language.EN)
        answer = ["a", "b", "c"]
        associative_chaining.payload = answer
        result = associative_chaining.check_answer(answer)
        for _, color in result:
            assert color == AssociativeChaining.CORRECT_ANSWER_COLOR

    def test_check_answer_should_retun_all_red_color_results(self):
        """Verify that all answers are bad"""
        associative_chaining = AssociativeChaining(1, Language.EN)
        answer = ["a", "b", "c"]
        associative_chaining.payload = ["d", "e", "f"]
        result = associative_chaining.check_answer(answer)
        for _, color in result:
            assert color == AssociativeChaining.BAD_ANSWER_COLOR

    def test_check_answer_should_return_all_yellow_color_results(self):
        """Verify that all answers are good but in the wrong order"""
        associative_chaining = AssociativeChaining(1, Language.EN)
        answer = ["a", "b", "c"]
        associative_chaining.payload = answer
        result = associative_chaining.check_answer(["b", "c", "a"])
        for _, color in result:
            assert color == AssociativeChaining.GOOD_ANSWER_COLOR

    def test_check_answer_should_return_appropriate_colors(self):
        """Verify that all all colors are correctly assigned"""
        associative_chaining = AssociativeChaining(1, Language.EN)
        answer = ["a", "b", "c", "d"]
        associative_chaining.payload = answer
        result = associative_chaining.check_answer(["z", "c", "b", "d"])
        # should be red color
        assert result[0][1] == AssociativeChaining.BAD_ANSWER_COLOR
        # should be yellow color
        assert (
            result[1][1] == AssociativeChaining.GOOD_ANSWER_COLOR
            and result[2][1] == AssociativeChaining.GOOD_ANSWER_COLOR
        )
        # should be green color
        assert result[3][1] == AssociativeChaining.CORRECT_ANSWER_COLOR

    def test_check_answer_should_return_correct_points_if_all_answers_are_good(self):
        associative_chaining = AssociativeChaining(1, Language.EN)
        answer = ["a", "b", "c"]
        associative_chaining.payload = answer
        associative_chaining.check_answer(answer)

        assert associative_chaining.points.points == 6

    def test_check_answer_should_return_correct_points_if_all_answers_are_bad(self):
        associative_chaining = AssociativeChaining(1, Language.EN)
        answer = ["a", "b", "c"]
        associative_chaining.payload = ["d", "e", "f"]
        associative_chaining.check_answer(answer)

        assert associative_chaining.points.points == -3

    def test_check_answer_should_return_correct_points_if_all_answers_are_good_but_in_the_wrong_order(
        self,
    ):
        associative_chaining = AssociativeChaining(1, Language.EN)
        answer = ["a", "b", "c"]
        associative_chaining.payload = answer
        associative_chaining.check_answer(["b", "c", "a"])

        assert associative_chaining.points.points == 3

    def test_check_answer_should_avoid_answer_when_answer_is_dash_and_donot_add_points(
        self,
    ):
        associative_chaining = AssociativeChaining(1, Language.EN)
        answer = ["a", "b", "c"]
        associative_chaining.payload = answer
        result = associative_chaining.check_answer(["-", "-", "-"])

        assert associative_chaining.points.points == 0

        for _, color in result:
            assert color == AssociativeChaining.BAD_ANSWER_COLOR

    @patch("src.games.mnemonic.associative_chaining.AssociativeChaining.create_payload")
    @patch("src.games.mnemonic.associative_chaining.AssociativeChaining.check_answer")
    def test_run(self, mock_check_answer, mock_create_payload):
        # Create instance test object
        associative_chaining = AssociativeChaining(1, Language.EN)
        associative_chaining.payload = ["a", "b", "c"]
        mock_create_payload.return_value = None

        # Ser mock check_answer
        mock_check_answer.return_value = [
            ("a", AssociativeChaining.CORRECT_ANSWER_COLOR),
            ("b", AssociativeChaining.CORRECT_ANSWER_COLOR),
            ("c", AssociativeChaining.CORRECT_ANSWER_COLOR),
        ]

        # Run generator
        game = associative_chaining.run()

        # First call should return payload
        assert next(game) == ["a", "b", "c"]

        # Send answer to game
        with pytest.raises(StopIteration) as e:
            game.send(["a", "b", "c"])

        # Capture result from StopIteration
        result = e.value.value

        # Compare results
        assert result == [
            ("a", AssociativeChaining.CORRECT_ANSWER_COLOR),
            ("b", AssociativeChaining.CORRECT_ANSWER_COLOR),
            ("c", AssociativeChaining.CORRECT_ANSWER_COLOR),
        ]
