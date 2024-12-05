from kivy.clock import Clock
from kivy.lang import Builder

from src.db.session import GameManager
from src.games.math import ResultKeeper

from ...models.games import GameName
from .base_game_screen import BaseGamaScreen

# Load the kv file
Builder.load_file("src/GUI/games/result_keeper.kv")


class ResultKeeperScreen(BaseGamaScreen):
    NAME_GAME = GameName.RESULT_KEEPER

    def __init__(self, session_manager: GameManager, **kwargs):
        super(ResultKeeperScreen, self).__init__(session_manager, **kwargs)

        self.result_keeper = None
        self.game = None
        self.time_left = 10  # 60 seconds for the game
        self.countdown = 3

    def on_kv_post(self, base_widget):
        """Called after kv file is loaded and all widgets are created"""
        # Initialize game state
        self.initialize_game_state()
        # Initialize UI state
        self.answer_field.disabled = False
        self.answer_field.text = ""
        self.timer_label.text = "Time left: 60s"
        self.countdown_label.text = "3"
        self.game_layout.opacity = 0
        self.countdown_layout.opacity = 1

    def initialize_game_state(self):
        """Initialize or reset the game state"""
        self.result_keeper = ResultKeeper(1)
        self.info_label.text = f"{self.result_keeper.lives_left}"
        self.game = self.result_keeper.run()
        message, _ = next(self.game)
        if hasattr(self, "question_field"):
            self.question_field.text = message
        # self.time_left = 60  # 60 seconds timer
        self.timer_event = None
        self.countdown = 3  # Initial countdown value

    def start_countdown(self, dt):
        """Update the countdown display"""
        self.countdown -= 1
        if self.countdown >= 0:
            if hasattr(self, "countdown_label"):
                self.countdown_label.text = str(self.countdown)
            return True
        else:
            # Switch layouts
            if hasattr(self, "countdown_layout"):
                self.countdown_layout.opacity = 0
            if hasattr(self, "game_layout"):
                self.game_layout.opacity = 1
            # Start the game
            self.start_timer()
            if hasattr(self, "answer_field"):
                Clock.schedule_once(
                    lambda dt: setattr(self.answer_field, "focus", True), 0
                )
            # Unschedule countdown
            if self.countdown_event:
                self.countdown_event.cancel()
            return False

    def update_timer(self, dt):
        """Update timer every second"""
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.text = f"Time left: {self.time_left}s"

        if self.time_left <= 0:
            self.game_over()
            points = self.result_keeper.points.points
            self.save_stats(points, self.result_keeper.level)
            return False
        return True

    def validate_field(self, answer: str) -> bool:
        """Validate user input in answer field"""
        try:
            int(answer)
        except ValueError:
            self.answer_field.text = ""

            self.info_label.text = "Answer must be a number!"
            Clock.schedule_once(lambda dt: setattr(self.answer_field, "focus", True), 0)
            return False
        return True

    def game_over(self):
        self.cleanup_clock_events()
        points = self.result_keeper.points.points
        level = self.result_keeper.level

        self.info_label.text = (
            f"Game Over - Time's up! You earned {points} points at level {level}!"
        )
        self.answer_field.disabled = True
        # TODO: Save to the

        # Create new UserSession with updated points
        self.show_end_game_buttons()

    def trigger_game(self, answer):
        try:
            message, result = self.game.send(int(answer))
        except StopIteration:
            self.game_over()
            return

        self.question_field.text = message

        if result:
            # If correct, get the next question
            message, _ = next(self.game)
            self.set_label_text(
                question_field=message,
                level_label=f"Level: {self.result_keeper.level}",
                info_label=f"{self.result_keeper.lives_left}",
            )
        else:
            self.info_label.text = f"{self.result_keeper.lives_left}"
        self.answer_field.text = ""
        # set focus to answer field
        Clock.schedule_once(lambda dt: setattr(self.answer_field, "focus", True), 0)

    def on_answer_field_enter(self, instance):
        """When user presses enter in answer field"""
        answer = self.answer_field.text
        if not self.validate_field(answer):
            return
        self.trigger_game(answer)

    def on_enter(self):
        """Called when the screen is entered"""
        # Start new game
        self.start_new_game()

    def on_leave(self):
        """Clean up when leaving the screen"""
        self.cleanup_clock_events()

    def start_new_game(self):
        """Start a new game with countdown"""
        self.cleanup_clock_events()
        # Reset game state
        self.initialize_game_state()
        # Reset UI state if widgets exist
        self.answer_field.disabled = False
        self.game_layout.opacity = 0
        self.countdown_layout.opacity = 1
        self.set_label_text(
            answer_field="", timer_label="Time left: 60s", countdown_label="3"
        )
        # Hide end game buttons
        self.hide_end_game_buttons()
        # Start countdown again
        self.countdown_event = Clock.schedule_interval(self.start_countdown, 1)

    def back_to_menu(self, instance):
        """Return to the main menu after clearing session"""
        self.cleanup_clock_events()
        self.manager.current = "menu"

    def show_end_game_buttons(self):
        """Show the try again and back to menu buttons"""
        if hasattr(self, "buttons_layout"):
            self.buttons_layout.opacity = 1

    def hide_end_game_buttons(self):
        """Hide the try again and back to menu buttons"""
        if hasattr(self, "buttons_layout"):
            self.buttons_layout.opacity = 0
