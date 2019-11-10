from pluginsmanager.model.pedalboard import Pedalboard

from zoom.exception.exceptions import InvalidLevelException
from zoom.observer.zoom_change import ZoomChange


class ZoomPedalboard(Pedalboard):
    def __init__(self, name):
        super().__init__(name)
        self._level = 0

    @property
    def level(self):
        """
        Pedalboard level [0-120]

        :getter: Pedalboard level
        :setter: Set the pedalboard level
        :type: int
        """
        return self._level

    @level.setter
    def level(self, new_value):
        if not(0 <= new_value <= 120):
            msg = 'Pedalboard level: New value out of range: {} [{} - {}]'.format(
                new_value,
                0,
                120
            )
            raise InvalidLevelException(msg)

        if self._level == new_value:
            return

        self._level = new_value
        self.observer.on_custom_change(ZoomChange.PEDALBOARD_CURRENT_LEVEL, self)

    def __repr__(self):
        return "<{} {} - '{}' Level {}, at 0x{:x}>".format(
            self.__class__.__name__,
            self.zoom_index,
            self.name,
            self.level,
            id(self)
        )

    @property
    def zoom_index(self):
        bank = self.index / 10
        bank = chr(65 + int(bank))
        index = self.index % 10
        return f'{bank}{index}'
