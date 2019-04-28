from enum import Enum

from pluginsmanager.banks_manager import BanksManager

from zoom.observer.zoom_host import ZoomHost


class ZoomSignal(Enum):
    LEFT_TO_RIGHT = 0
    RIGHT_TO_LEFT = 1


class ZoomG3v2(BanksManager):

    def __init__(self):
        super().__init__()

        self.host: ZoomHost = None

        self._tempo = 120
        self._autosave = False
        self._signal_flow = ZoomSignal.RIGHT_TO_LEFT

    def connect(self, host: ZoomHost):
        self.host = host
        self.register(host)
        host.connect()

    def load_data(self):
        self.host.load_data()

    def disconnect(self):
        self.host.close()
        self.host = None
