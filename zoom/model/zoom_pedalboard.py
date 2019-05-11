from pluginsmanager.model.pedalboard import Pedalboard

from zoom.exception.exceptions import InvalidLevelException


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
            msg = 'New value out of range: {} [{} - {}]'.format(
                new_value,
                0,
                120
            )
            raise InvalidLevelException(msg)

        if self._level == new_value:
            return

        self._level = new_value
        self.observer.on_custom_change(self)
