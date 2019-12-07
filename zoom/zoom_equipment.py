from typing import Type

from pluginsmanager.banks_manager import BanksManager
from pluginsmanager.model.bank import Bank
from pluginsmanager.observer.observable_list import ObservableList

from zoom.exception.exceptions import InvalidPedalboardException
from zoom.model.zoom_pedalboard import ZoomPedalboard
from zoom.observer.host.zoom_equipment_host import ZoomEquipmentHostData
from zoom.observer.zoom_change import ZoomChange
from zoom.observer.zoom_host import ZoomHost


class ZoomEquipment(BanksManager):

    def __init__(self):
        super().__init__()

        self.host: ZoomHost = None

        self._total_pedalboards: int = None
        self._tempo = 120
        self._autosave = False

        self._current_pedalboard_id = 0

        self.append(Bank("Default Patches"))

    def _connect(self, equipment_host: Type[ZoomEquipmentHostData]):
        self.host = ZoomHost(equipment_host)
        self.register(self.host)
        self.host.connect(self)

    def load_data(self):
        self.host.load_data()

    def disconnect(self):
        self.host.close()
        self.host = None

    @property
    def total_pedalboards(self) -> int:
        return self._total_pedalboards

    @property
    def pedalboards(self) -> ObservableList:
        return self.banks[0].pedalboards

    @property
    def current_pedalboard(self) -> ZoomPedalboard:
        return self.pedalboards[self._current_pedalboard_id]

    def to_next_pedalboard(self):
        if self._current_pedalboard_id == self.total_pedalboards - 1:
            pedalboard_index = 0
        else:
            pedalboard_index = self._current_pedalboard_id + 1

        self.to_pedalboard(pedalboard_index)

    def to_previous_pedalboard(self):
        if self._current_pedalboard_id == 0:
            pedalboard_index = self.total_pedalboards - 1
        else:
            pedalboard_index = self._current_pedalboard_id - 1

        self.to_pedalboard(pedalboard_index)

    def to_pedalboard(self, pedalboard_index: int):
        if pedalboard_index < 0 or pedalboard_index >= self.total_pedalboards:
            raise InvalidPedalboardException(f'Pedalboard index need be between [{0}-{self.total_pedalboards - 1}]')

        self._current_pedalboard_id = pedalboard_index
        # Do not notify change
        self.host._pedalboard = self.pedalboards[self._current_pedalboard_id]
        self.observer_manager.on_custom_change(ZoomChange.PEDALBOARD_CURRENT, self.current_pedalboard, self._current_pedalboard_id)
