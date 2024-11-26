import pytest

from src.games.math.result_keeper import Points, ResultKeeper


class TestResultKeeper:
    def test_initialize_game_state(self):
        reeesult_keeper = ResultKeeper(1)
        assert reeesult_keeper.level == 1
        assert reeesult_keeper.payload == []
        assert isinstance(reeesult_keeper.points, Points)

    def test_create_payload_should_contain_10_numbers_within_range(self):
        reeesult_keeper = ResultKeeper(1)
        reeesult_keeper.create_payload()
        assert len(reeesult_keeper.payload) == 10
        assert all(0 <= i <= 10 for i in reeesult_keeper.payload)

    @pytest.mark.parametrize(
        "a, b, op, expected_result",
        [(2, 3, "+", 5), (3, 3, "-", 0), (5, 5, "*", 25), (10, 2, "/", 5)],
    )
    def test_calculate_should_return_correct_value(self, a, b, op, expected_result):
        reeesult_keeper = ResultKeeper(1)
        assert reeesult_keeper.calculate(a, b, op) == expected_result

    def test_calculate_does_not_handle_invalid_operations(self):
        reeesult_keeper = ResultKeeper(1)
        with pytest.raises(ValueError):
            reeesult_keeper.calculate(2, 3, "%")

    def test_calculate_does_not_handle_invalid_operations_when_b_is_zero(self):
        reeesult_keeper = ResultKeeper(1)
        with pytest.raises(ZeroDivisionError):
            reeesult_keeper.calculate(2, 0, "/")

    def test_set_math_char_generates_valid_sequence(self):
        result_keeper = ResultKeeper(1)
        result_keeper.create_payload()
        math_chars = result_keeper._set_math_char()

        # Should generate 9 operations for 10 numbers
        assert len(math_chars) == 9
        # Should only contain valid operations
        assert all(op in ["+", "-", "*", "/"] for op in math_chars)

    def test_set_math_char_with_custom_operations(self):
        result_keeper = ResultKeeper(1)
        result_keeper.create_payload()
        math_chars = result_keeper._set_math_char(["+", "-"])

        # should be 9 chars
        assert len(math_chars) == 9
        # should contain only + and -
        assert all(op in ["+", "-"] for op in math_chars)
