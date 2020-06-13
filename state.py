from enum import Enum, auto

class State(Enum):
    IDLE = auto()
    SHOW_CATEGORIES = auto()
    SHOW_PRODUCTS = auto()
    SHOW_FAVORITES = auto()

class State_Machine:
    def __init__(self):
        self.__state = State.IDLE
    
    def set_state(self, state):
        self.__state = state
    
    def get_state(self):
        return self.__state