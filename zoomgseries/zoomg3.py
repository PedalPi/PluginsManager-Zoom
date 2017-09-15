from enum import Enum

class ZoomSignal(Enum):
    LEFT_TO_RIGHT = 0
    RIGHT_TO_LEFT = 1


class ZoomG3:

    def __init__(self):
        self._tempo = 120
        self._autosave = False
        self._signal_flow = ZoomSignal.RIGHT_TO_LEFT
