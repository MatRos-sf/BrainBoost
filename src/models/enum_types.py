from enum import Enum, StrEnum


class Language(Enum):
    PL = "PL"
    EN = "EN"


class PointsCategory(Enum):
    """
    This class return tuple where:
        first element is string. It uses to assign in Points.category models
        second element is integer. It uses to give user points for activity.
    When second element is -1 it means: points are dynamically assigned

    """

    # ACTIVITY
    CREATE_ACCOUNT = "Create Account", 10
    DAILY_LOGIN = "Daily", 5
    WEEKLY_LOGIN = "Weekly", 10
    # Games
    GAME_RESULT_KEEPER = "Game Result Keeper", -1
    FIRST_RESULT_KEEPER = "First Game Result Keeper", 10
    GAME_ASSOCIATIVE_CHANGING = "Game Associative Changing", -1
    FIRST_ASSOCIATIVE_CHANGING = "First Game Associative Changing", 10


class GameName(StrEnum):
    RESULT_KEEPER = "Result Keeper"
    ASSOCIATIVE_CHANGING = "Associative Changing"
