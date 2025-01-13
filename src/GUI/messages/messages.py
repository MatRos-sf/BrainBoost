__all__ = ["message_ends_game"]
from typing import Optional

MESSAGE_TIMES_UP = "Game Over - Time's up!\n"
MESSAGE_DEFEATED = "Game Over - You have been defeated.\n"


def stats_message(points: int, level: int) -> str:
    return f"You earned {points} points at level {level}!\n"


# TODO: Remove this file in the next major release
def message_ends_game(
    points: int,
    level: int,
    is_time_over: bool = False,
    additionally_message: Optional[str] = None,
) -> str:
    """
    Function crete message depends on the result games if time is over user get message: 'Game Over - Time's up!' otherwise
    message is: 'Game Over - You have been defeated'.
    In addition, at the very end, information about statistics and an optional message is added.
    """
    message = ""
    if is_time_over:
        message += MESSAGE_TIMES_UP
    else:
        message += MESSAGE_DEFEATED
    message += stats_message(points, level)
    return message + additionally_message if additionally_message else message
