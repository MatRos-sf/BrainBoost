from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from src.db.session import UserSession
from src.games.math import ResultKeeper
from src.models.user import User

# Load the kv file
Builder.load_file("src/GUI/games/result_keeper.kv")


class ResultKeeperScreen(Screen):
    def __init__(self, session, **kwargs):
        super(ResultKeeperScreen, self).__init__(**kwargs)
        self.session = session

        # Store countdown event
        self.countdown_event = None
        self.timer_event = None
        self.result_keeper = None
        self.game = None
        self.time_left = 60  # 60 seconds for the game
        self.countdown = 3

    def on_kv_post(self, base_widget):
        """Called after kv file is loaded and all widgets are created"""
        # Initialize game state
        self.initialize_game_state()
        # Initialize UI state
        if hasattr(self, "answer_field"):
            self.answer_field.disabled = False
            self.answer_field.text = ""
        if hasattr(self, "info_label"):
            self.info_label.text = "Get Ready!"
        if hasattr(self, "timer_label"):
            self.timer_label.text = "Time left: 60s"
        if hasattr(self, "countdown_label"):
            self.countdown_label.text = "3"
        if hasattr(self, "game_layout"):
            self.game_layout.opacity = 0
        if hasattr(self, "countdown_layout"):
            self.countdown_layout.opacity = 1

    def initialize_game_state(self):
        """Initialize or reset the game state"""
        self.result_keeper = ResultKeeper(1)
        self.game = self.result_keeper.run()
        message, _ = next(self.game)
        if hasattr(self, "question_field"):
            self.question_field.text = message
        self.time_left = 60  # 60 seconds timer
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

    def start_timer(self):
        """Start the 60-second countdown timer"""
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        """Update timer every second"""
        if self.time_left > 0:
            self.time_left -= 1
            if hasattr(self, "timer_label"):
                self.timer_label.text = f"Time left: {self.time_left}s"

        if self.time_left <= 0:
            self.cleanup_clock_events()
            points = self.result_keeper.points.points
            level = self.result_keeper.level
            if hasattr(self, "info_label"):
                self.info_label.text = f"Game Over - Time's up! You earned {points} points at level {level}!"
            if hasattr(self, "answer_field"):
                self.answer_field.disabled = True
            # save the points
            app = App.get_running_app()
            user = app.user_session
            self.session.query(User).filter_by(id=user.id).update(
                {"points": User.points + points}
            )
            self.session.commit()
            # Create new UserSession with updated points
            app.user_session = UserSession(user.id, user.username, user.points + points)
            self.show_end_game_buttons()
            return False
        return True

    def on_answer_field_enter(self, instance):
        """When user presses enter in answer field"""
        try:
            answer = int(self.answer_field.text)
        except ValueError:
            if hasattr(self, "answer_field"):
                self.answer_field.text = ""
            if hasattr(self, "info_label"):
                self.info_label.text = "Answer must be a number!"
            if hasattr(self, "answer_field"):
                Clock.schedule_once(
                    lambda dt: setattr(self.answer_field, "focus", True), 0
                )
            return

        try:
            # First send the answer
            message, result = self.game.send(answer)

            if result:
                # If correct, get the next question
                try:
                    message, _ = next(self.game)
                    if hasattr(self, "question_field"):
                        self.question_field.text = message
                    # Update level display
                    current_level = self.result_keeper.level
                    if hasattr(self, "level_label"):
                        self.level_label.text = f"Level: {current_level}"
                    if hasattr(self, "info_label"):
                        self.info_label.text = (
                            "Correct! Continue with the next operation."
                        )
                except StopIteration:
                    self.cleanup_clock_events()
                    points = self.result_keeper.points.points
                    level = self.result_keeper.level
                    if hasattr(self, "info_label"):
                        self.info_label.text = f"Congratulations! Game finished! You earned {points} points at level {level}!"
                    if hasattr(self, "answer_field"):
                        self.answer_field.disabled = True
                    self.show_end_game_buttons()
                    return
            else:
                if hasattr(self, "info_label"):
                    self.info_label.text = "Try again!"

        except StopIteration:
            self.cleanup_clock_events()
            points = self.result_keeper.points.points
            level = self.result_keeper.level
            if hasattr(self, "info_label"):
                self.info_label.text = f"Congratulations! Game finished! You earned {points} points at level {level}!"
            if hasattr(self, "answer_field"):
                self.answer_field.disabled = True
            self.show_end_game_buttons()
            return

        if hasattr(self, "answer_field"):
            self.answer_field.text = ""
            Clock.schedule_once(lambda dt: setattr(self.answer_field, "focus", True), 0)

    def cleanup_clock_events(self):
        """Clean up all Clock events"""
        # Cancel timer if running
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None

        # Cancel countdown if running
        if self.countdown_event:
            self.countdown_event.cancel()
            self.countdown_event = None

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
        if hasattr(self, "answer_field"):
            self.answer_field.disabled = False
            self.answer_field.text = ""
        if hasattr(self, "info_label"):
            self.info_label.text = "Get Ready!"
        if hasattr(self, "timer_label"):
            self.timer_label.text = "Time left: 60s"
        if hasattr(self, "countdown_label"):
            self.countdown_label.text = "3"
        if hasattr(self, "game_layout"):
            self.game_layout.opacity = 0
        if hasattr(self, "countdown_layout"):
            self.countdown_layout.opacity = 1
        # Hide end game buttons
        self.hide_end_game_buttons()
        # Start countdown again
        self.countdown_event = Clock.schedule_interval(self.start_countdown, 1)

    def try_again(self, instance):
        """Reset and restart the game"""
        self.start_new_game()

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
