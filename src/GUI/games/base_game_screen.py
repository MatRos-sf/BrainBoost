from typing import Optional

from kivy.clock import Clock

from src.db.session import GameManager
from src.GUI.base_screen import BaseScreen
from src.models.games import GameLevel, GameSession
from src.models.user import User


class BaseGamaScreen(BaseScreen):
    def __init__(self, session_manager: GameManager, **kwargs):
        super(BaseGamaScreen, self).__init__(session_manager, **kwargs)
        self.timer_event: Optional[Clock] = None
        self.countdown_event: Optional[Clock] = None
        self.game = None
        self.time = 0

    def start_timer(self):
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def cleanup_clock_events(self):
        """Clean up all Clock events"""
        # Cancel timer if running
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None
            self.time = 0

        # Cancel countdown if running
        if self.countdown_event:
            self.countdown_event.cancel()
            self.countdown_event = None

    def try_again(self, instance):
        """Reset and restart the game"""
        self.start_new_game()

    def show_end_game_buttons(self):
        """Show the try again and back to menu buttons"""
        if hasattr(self, "buttons_layout"):
            self.buttons_layout.opacity = 1
        else:
            raise AttributeError("buttons_layout not implemented!")

    def hide_end_game_buttons(self):
        """Hide the try again and back to menu buttons"""
        if hasattr(self, "buttons_layout"):
            self.buttons_layout.opacity = 0
        else:
            raise AttributeError("buttons_layout not implemented!")

    def back_to_menu(self, instance):
        """Return to the main menu after clearing session"""
        self.cleanup_clock_events()
        self.manager.current = "menu"

    def on_leave(self):
        """Clean up when leaving the screen"""
        self.cleanup_clock_events()

    def start_new_game(self):
        pass

    def save_stats(self, earned_points: int, level: int):
        """
        This method should be called after the game.
        Method updates the record of the table and current stats. In the following steps:
            1. Add new GameSession
            2. Update User's points
            3. If user level up then:
                a. Update the level field in GameLevel mode
                b. Update the level in the current session
            4. Update points in the current session
        """
        user = self.session_manager.current_session
        payload = {"points": User.points + earned_points}
        game = user.stats.get(self.NAME_GAME.value)
        # add new record
        self.session_manager.db.add_record(
            GameSession,
            game_level_id=game.id,
            started_level=game.level,
            finished_level=level,
            points_earned=earned_points,
        )
        self.session_manager.db.update_record(User, user.id, payload)
        if game.level < level:
            # update level
            self.session_manager.db.update_record(GameLevel, game.id, {"level": level})
            self.session_manager.update_level_of_game(self.NAME_GAME, level)

        self.session_manager.update_points(earned_points)
