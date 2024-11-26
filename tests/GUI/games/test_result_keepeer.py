from unittest.mock import MagicMock

from kivy.tests.common import GraphicUnitTest
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.textinput import TextInput

from src.GUI.games.result_keeper import ResultKeeperScreen
from src.GUI.menu import MenuScreen


class TestResultKeeperScreen(GraphicUnitTest):
    def setUp(self):
        super().setUp()
        self.result_keeper_screen = ResultKeeperScreen(name="result_keeper")

        self.menu_screen = MenuScreen(name="menu")
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(self.result_keeper_screen)
        self.screen_manager.add_widget(self.menu_screen)
        self.screen_manager.current = "menu"

    def test_countdown_starts_at_three(self):
        # Switch to result keeper screen
        self.screen_manager.current = "result_keeper"

        # Get the countdown label from the countdown layout
        countdown_label = self.result_keeper_screen.countdown_label
        self.assertEqual(countdown_label.text, "3")

        # Ensure countdown is initialized to 3
        self.assertEqual(self.result_keeper_screen.countdown, 3)

    def test_countdown(self):
        # Switch to result keeper screen which triggers on_enter
        self.screen_manager.current = "result_keeper"

        # The countdown should start at 3
        self.assertEqual(self.result_keeper_screen.countdown_label.text, "3")
        self.assertEqual(self.result_keeper_screen.countdown, 3)

        # Trigger the countdown event manually
        self.result_keeper_screen.start_countdown(0)

        # Check countdown is at 2
        self.assertEqual(self.result_keeper_screen.countdown_label.text, "2")
        self.assertEqual(self.result_keeper_screen.countdown, 2)

        # Trigger countdown again
        self.result_keeper_screen.start_countdown(0)

        # Check countdown is at 1
        self.assertEqual(self.result_keeper_screen.countdown_label.text, "1")
        self.assertEqual(self.result_keeper_screen.countdown, 1)

        # Trigger countdown again
        self.result_keeper_screen.start_countdown(0)

        # Check countdown is at 0
        self.assertEqual(self.result_keeper_screen.countdown_label.text, "0")
        self.assertEqual(self.result_keeper_screen.countdown, 0)

        # One more trigger should switch to game layout
        self.result_keeper_screen.start_countdown(0)

        # Check that layouts are properly visible/hidden
        self.assertEqual(self.result_keeper_screen.countdown_layout.opacity, 0)
        self.assertEqual(self.result_keeper_screen.game_layout.opacity, 1)

        # Check that both layouts are children of the FloatLayout
        float_layout = self.result_keeper_screen.children[0]
        self.assertIsInstance(float_layout, FloatLayout)
        self.assertIn(self.result_keeper_screen.countdown_layout, float_layout.children)
        self.assertIn(self.result_keeper_screen.game_layout, float_layout.children)

    def test_widgets_exist(self):
        self.screen_manager.current = "result_keeper"
        for _ in range(4):
            self.result_keeper_screen.start_countdown(0)

        # Test that all UI elements exist and are the correct type
        self.assertIsInstance(self.result_keeper_screen.info_label, Label)
        self.assertIsInstance(self.result_keeper_screen.timer_label, Label)
        self.assertIsInstance(self.result_keeper_screen.level_label, Label)
        self.assertIsInstance(self.result_keeper_screen.question_field, Label)
        self.assertIsInstance(self.result_keeper_screen.answer_field, TextInput)
        # Test buttons
        self.assertIsInstance(self.result_keeper_screen.try_again_button, Button)
        self.assertIsInstance(self.result_keeper_screen.back_to_menu_button, Button)

        # Test initial values
        self.assertEqual(self.result_keeper_screen.timer_label.text, "Time left: 60s")
        self.assertEqual(self.result_keeper_screen.level_label.text, "Level: 1")
        self.assertEqual(self.result_keeper_screen.answer_field.hint_text, "Answer")
        self.assertEqual(self.result_keeper_screen.try_again_button.text, "Try Again")
        self.assertEqual(
            self.result_keeper_screen.back_to_menu_button.text, "Back to Menu"
        )

    def test_timer(self):
        # Switch to result keeper screen
        self.screen_manager.current = "result_keeper"

        # Skip countdown
        for _ in range(4):
            self.result_keeper_screen.start_countdown(0)

        # Check initial timer
        self.assertEqual(self.result_keeper_screen.time_left, 60)
        self.assertEqual(self.result_keeper_screen.timer_label.text, "Time left: 60s")

        # Update timer and check value
        self.result_keeper_screen.update_timer(0)
        self.assertEqual(self.result_keeper_screen.time_left, 59)
        self.assertEqual(self.result_keeper_screen.timer_label.text, "Time left: 59s")

        # Run timer until end
        for _ in range(59):
            self.result_keeper_screen.update_timer(0)

        # Check game over state
        self.assertEqual(self.result_keeper_screen.time_left, 0)
        self.assertTrue(self.result_keeper_screen.answer_field.disabled)
        self.assertIn("Game Over", self.result_keeper_screen.info_label.text)

    def test_try_again(self):
        # Switch to result keeper screen
        self.screen_manager.current = "result_keeper"

        # Skip countdown
        for _ in range(4):
            self.result_keeper_screen.start_countdown(0)

        # Press try again
        self.result_keeper_screen.try_again(None)

        # Check that game restarted
        self.assertEqual(self.result_keeper_screen.countdown, 3)
        self.assertEqual(self.result_keeper_screen.countdown_label.text, "3")
        self.assertEqual(self.result_keeper_screen.time_left, 60)
        self.assertEqual(self.result_keeper_screen.timer_label.text, "Time left: 60s")
        self.assertFalse(self.result_keeper_screen.answer_field.disabled)

    def test_back_to_menu(self):
        # Switch to result keeper screen
        self.screen_manager.current = "result_keeper"

        # Press back to menu
        self.result_keeper_screen.back_to_menu(None)

        # Check that we're back in menu
        self.assertEqual(self.screen_manager.current, "menu")

    def test_wrong_answer(self):
        # Switch to result keeper screen
        self.screen_manager.current = "result_keeper"

        # Skip countdown
        for _ in range(4):
            self.result_keeper_screen.start_countdown(0)

        # Mock the game generator
        mock_game = MagicMock()
        mock_game.send.return_value = (
            "Next question",
            False,
        )  # Use send instead of send_answer
        mock_game.__next__.return_value = (
            "Initial question",
            None,
        )  # Mock the next() call
        self.result_keeper_screen.game = mock_game

        # Mock the result keeper
        mock_result_keeper = MagicMock()
        mock_result_keeper.level = 1  # Simulate level increase
        mock_result_keeper.points.points = 10  # Simulate points earned
        self.result_keeper_screen.result_keeper = mock_result_keeper

        # Enter a good answer and trigger enter
        self.result_keeper_screen.answer_field.text = "42"
        self.result_keeper_screen.on_answer_field_enter(None)

        # Check that answer was processed correctly
        self.assertEqual(self.result_keeper_screen.info_label.text, "Try again!")
        self.assertEqual(self.result_keeper_screen.level_label.text, "Level: 1")
        self.assertEqual(
            self.result_keeper_screen.answer_field.text, ""
        )  # Answer field should be cleared

    def test_good_answer(self):
        # Switch to result keeper screen
        self.screen_manager.current = "result_keeper"

        # Skip countdown
        for _ in range(4):
            self.result_keeper_screen.start_countdown(0)

        # Mock the game generator
        mock_game = MagicMock()
        mock_game.send.return_value = (
            "Next question",
            True,
        )  # Use send instead of send_answer
        mock_game.__next__.return_value = (
            "Initial question",
            None,
        )  # Mock the next() call
        self.result_keeper_screen.game = mock_game

        # Mock the result keeper
        mock_result_keeper = MagicMock()
        mock_result_keeper.level = 2  # Simulate level increase
        mock_result_keeper.points.points = 10  # Simulate points earned
        self.result_keeper_screen.result_keeper = mock_result_keeper

        # Enter a good answer and trigger enter
        self.result_keeper_screen.answer_field.text = "42"
        self.result_keeper_screen.on_answer_field_enter(None)

        # Check that answer was processed correctly
        self.assertEqual(
            self.result_keeper_screen.info_label.text,
            "Correct! Continue with the next operation.",
        )
        self.assertEqual(self.result_keeper_screen.level_label.text, "Level: 2")
        self.assertEqual(
            self.result_keeper_screen.answer_field.text, ""
        )  # Answer field should be cleared
