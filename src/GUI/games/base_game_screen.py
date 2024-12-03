from typing import Optional

from kivy.clock import Clock

from src.db.session import GameManager
from src.GUI.base_screen import BaseScreen


class BaseGamaScreen(BaseScreen):
    def __init__(self, session_manager: GameManager, **kwargs):
        super(BaseGamaScreen, self).__init__(session_manager, **kwargs)
        self.timer_event: Optional[Clock] = None
        self.countdown_event = None

    def start_timer(self):
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

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

    def try_again(self, instance):
        """Reset and restart the game"""
        self.start_new_game()

    def start_new_game(self):
        pass
