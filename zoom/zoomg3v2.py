from enum import Enum

from zoom.observer.host.zoom_iv.zoom_iv_host import ZoomIVHost
from zoom.observer.zoom_host import ZoomHost
from zoom.zoom_equipment import ZoomEquipment


class ZoomSignal(Enum):
    LEFT_TO_RIGHT = 0
    RIGHT_TO_LEFT = 1


class ZoomG3v2(ZoomEquipment):

    def __init__(self):
        super().__init__()
        self._total_pedalboards = 100

        self._signal_flow = ZoomSignal.RIGHT_TO_LEFT

    def connect(self):
        self.host = ZoomHost(ZoomIVHost)
        self.register(self.host)
        self.host.connect(self)
