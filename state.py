from enum import Enum, auto


class State(Enum):
    """
    Class which enumerate the different states used by the State Machine
    """
    IDLE = auto()
    SHOW_CATEGORIES = auto()
    SHOW_PRODUCTS = auto()
    SHOW_FAVORITES = auto()


class State_Machine:
    """
    Class used for setting up a State Machine pattern in the application

    Methods
    -------
    set_state(state)
        Set new state defined by state

    get_state
        Returns current state
    """

    def __init__(self):
        self.__state = State.IDLE

    def set_state(self, state):
        self.__state = state

    def get_state(self):
        return self.__state
        