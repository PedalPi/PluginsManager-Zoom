from enum import Enum

from pluginsmanager.banks_manager import BanksManager

from zoom.exception.exceptions import InvalidPedalboardException
from zoom.model.zoom_pedalboard import ZoomPedalboard
from zoom.observer.zoom_host import ZoomHost


class ZoomSignal(Enum):
    LEFT_TO_RIGHT = 0
    RIGHT_TO_LEFT = 1


class ZoomG3v2(BanksManager):

    def __init__(self):
        super().__init__()

        self.host: ZoomHost = None

        self._max_pedalboards = 100
        self._tempo = 120
        self._autosave = False
        self._signal_flow = ZoomSignal.RIGHT_TO_LEFT

        self._current_pedalboard_id = 0

    @property
    def current_pedalboard(self) -> ZoomPedalboard:
        return self.banks[0].pedalboards[self._current_pedalboard_id]

    def connect(self, host: ZoomHost):
        self.host = host
        self.register(host)
        host.connect()

    def load_data(self):
        self.host.load_data()

    def disconnect(self):
        self.host.close()
        self.host = None

    def to_next_pedalboard(self):
        if self._current_pedalboard_id == self._max_pedalboards - 1:
            self._current_pedalboard_id = 0
        else:
            self._current_pedalboard_id += 1

        self.to_pedalboard(self._current_pedalboard_id)

    def to_previous_pedalboard(self):
        if self._current_pedalboard_id == 0:
            self._current_pedalboard_id = self._max_pedalboards - 1
        else:
            self._current_pedalboard_id -= 1

        self.to_pedalboard(self._current_pedalboard_id)

    def to_pedalboard(self, pedalboard_index: int):
        if pedalboard_index < 0 or pedalboard_index >= self._max_pedalboards:
            raise InvalidPedalboardException(f'Pedalboard index need be between [{0}-{self._max_pedalboards - 1}]')

        # TODO - Add observer
        self.host.host.connection.send(self.host.host.message_encoder.to_patch(self._current_pedalboard_id))
