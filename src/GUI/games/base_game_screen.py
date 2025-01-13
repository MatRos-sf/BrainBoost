from typing import Optional

from kivy.clock import Clock

from src.db.session import GameManager
from src.GUI.base_screen import BaseScreen


class BaseGamaScreen(BaseScreen):
    def __init__(self, session_manager: GameManager, translation, **kwargs):
        super(BaseGamaScreen, self).__init__(
            session_manager=session_manager, translation=translation, **kwargs
        )
        self.timer_event: Optional[Clock] = None
        self.countdown_event: Optional[Clock] = None
        self.game = None
        self.time = 0
        self.init_level = None

    def find_innit_level(self, init_points: int):
        """Finds the current level of the game."""
        # must be because screen is loaded in the very beginning
        if not self.session_manager:
            level = 1
        else:
            level = self.session_manager.get_level_game(self.NAME_GAME)
            if level is None:
                raise ValueError("Could not find level of game")
        self.init_level = level

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

    def show_end_game_buttons(self, name_screen: str):
        """Show the try again and back to menu buttons"""
        if hasattr(self, "buttons_layout"):
            self.buttons_layout.opacity = 1
            self.try_again_button.text = self.get_label_with_variables(
                name_screen, "try_again_button"
            )
            self.back_to_menu_button.text = self.get_label_with_variables(
                name_screen, "back_to_menu_button"
            )

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

    def save_stats(self, *args, **kwargs):
        """
        This method should be called after the game.
        """
        raise NotImplementedError
