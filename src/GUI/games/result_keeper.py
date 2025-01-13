from typing import Optional

from kivy.clock import Clock
from kivy.lang import Builder

from src.db.session import GameManager
from src.games.math import ResultKeeper
from src.models.enum_types import GameName, PointsCategory

from ...models.games import ResultKeeperModel, ResultKeeperSessionModel
from .base_game_screen import BaseGamaScreen

# Load the kv file
Builder.load_file("src/GUI/games/result_keeper.kv")


class ResultKeeperScreen(BaseGamaScreen):
    NAME_SCREEN = "result_keeper_game"
    NAME_GAME = GameName.RESULT_KEEPER
    TIME_LEFT = 60

    def __init__(
        self,
        session_manager: GameManager,
        translation,
        init_level: Optional[int] = None,
        **kwargs,
    ):
        super(ResultKeeperScreen, self).__init__(session_manager, translation, **kwargs)
        print(
            f"I'm here---------------------------------------------{self.translation}"
        )
        self.result_keeper = None
        self.time_left = ResultKeeperScreen.TIME_LEFT  # 60 seconds for the game
        self.countdown = 3

    def on_enter(self, *args):
        """Called when the screen is entered"""
        # Start new game
        self.start_new_game()

        self.answer_field.disabled = False
        self.answer_field.text = ""
        self.timer_label.text = self.get_label_with_variables(
            self.NAME_SCREEN, "timer_label", time=self.TIME_LEFT
        )
        self.countdown_label.text = self.get_label_with_variables(
            self.NAME_SCREEN, "countdown_label", time="3"
        )
        self.game_layout.opacity = 0
        self.countdown_layout.opacity = 1

    # TODO: it will be remove in the next release
    # def on_kv_post(self, base_widget):
    #     """Called after kv file is loaded and all widgets are created"""
    #     # Initialize UI state
    #     self.answer_field.disabled = False
    #     self.answer_field.text = ""
    #     self.timer_label.text = "Time left: 60s"
    #     self.countdown_label.text = "3"
    #     self.game_layout.opacity = 0
    #     self.countdown_layout.opacity = 1

    def initialize_game_state(self):
        """Initialize or reset the game state"""
        self.find_innit_level(PointsCategory.FIRST_RESULT_KEEPER.value[1])

        self.result_keeper = ResultKeeper(self.init_level)
        self.info_label.text = self.get_label_with_variables(
            self.NAME_SCREEN, "info_label", lives=self.result_keeper.lives_left
        )
        self.level_label.text = self.get_label_with_variables(
            self.NAME_SCREEN, "level_label", level=self.init_level
        )

        self.game = self.result_keeper.run()
        message, _ = next(self.game)
        self.question_field.text = message

        self.time_left = ResultKeeperScreen.TIME_LEFT
        self.timer_event = None
        self.countdown = 3  # Initial countdown value

    def start_countdown(self, dt):
        """Update the countdown display"""
        self.countdown -= 1
        if self.countdown >= 0:
            self.countdown_label.text = str(self.countdown)
            return True
        else:
            # Switch layouts
            self.countdown_layout.opacity = 0
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
            self.timer_label.text = self.get_label_with_variables(
                self.NAME_SCREEN, "timer_label", time=self.time_left
            )

        if self.time_left <= 0:
            self.game_over()
            return False
        return True

    def validate_field(self, answer: str) -> bool:
        """Validate user input in answer field"""
        try:
            int(answer)
        except ValueError:
            self.answer_field.text = ""

            self.info_label.text = self.get_message_with_variables(
                self.NAME_SCREEN, "invalid_input"
            )

            Clock.schedule_once(lambda dt: setattr(self.answer_field, "focus", True), 0)
            return False
        return True

    def game_over(self, is_end_time: bool = True):
        self.cleanup_clock_events()
        self.info_label.text = self.generate_ending_message(is_end_time)
        self.answer_field.disabled = True
        self.save_stats()
        # Create new UserSession with updated points
        self.show_end_game_buttons(ResultKeeperScreen.NAME_SCREEN)

    def trigger_game(self, answer):
        try:
            message, result = self.game.send(int(answer))
        except StopIteration:
            self.game_over(is_end_time=False)
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
            answer_field="",
            timer_label=self.get_label_with_variables(
                self.NAME_SCREEN, "timer_label", time=self.TIME_LEFT
            ),
            countdown_label="3",
        )
        # Hide end game buttons
        self.hide_end_game_buttons()
        # Start countdown again
        self.countdown_event = Clock.schedule_interval(self.start_countdown, 1)

    def save_stats(self):
        """
        Method updates the record of the table and current stats. In the following steps:
            1. Add new GameSession
            2. Update User's points
            3. If user level up then:
                a. Update the level field in GameLevel mode
                b. Update the level in the current session
            4. Update points in the current session
        """
        user_session = self.session_manager.current_session
        game_stats = self.result_keeper.get_stats()
        started_level = game_stats.get("started_level")
        finished_level = game_stats.get("finished_level")
        earned_point = game_stats.get("points_earned")

        game = user_session.stats.get(self.NAME_GAME.value)
        # Save session stats
        self.session_manager.db.add_record(
            ResultKeeperSessionModel,
            result_keeper_id=game.id,
            duration=ResultKeeperScreen.TIME_LEFT - self.time_left,
            **game_stats,
        )

        self.session_manager.db.add_points_for_game(
            user_id=user_session.id,
            point=earned_point,
            category=PointsCategory.GAME_RESULT_KEEPER,
        )
        if started_level < finished_level:
            # update level
            self.session_manager.db.update_record(
                ResultKeeperModel, game.id, {"level": finished_level}
            )
            # update level in current session
            self.session_manager.update_level_of_game(self.NAME_GAME, finished_level)
        # update points in current session
        self.session_manager.update_point(earned_point)

    def generate_ending_message(self, is_time_over):
        """Generate the ending message based on the game outcome"""
        message = ""
        if is_time_over:
            message += self.get_message_with_variables("result_keeper_game", "time_up")
        else:
            message += self.get_message_with_variables("result_keeper_game", "defeated")
        message += self.get_message_with_variables(
            "result_keeper_game",
            "stats_message",
            points=self.result_keeper.points.points,
            level=self.result_keeper.level,
        )
        return message
