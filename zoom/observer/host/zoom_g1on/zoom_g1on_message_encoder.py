import warnings
from typing import Collection

import mido

from zoom.observer.host.base.zoom_equipment_message_encoder import ZoomEquipmentMessageEncoder, NotImplementedWarning


class ZoomG1onMessageEncoder(ZoomEquipmentMessageEncoder):
    """
    Message encoder to Zoom On series
    """

    def set_effect(self, effect_position: int, new_effect: int) -> Collection[mido.Message]:
        warnings.warn("set_effect is implemented, but it not update the equipment visor", NotImplementedWarning)
        return [self._zoom_small(effect_position, new_effect, 0x01)]

    def set_tempo(self, new_value: int) -> Collection[mido.Message]:
        warnings.warn("set_tempo is not implemented", NotImplementedWarning)
        return []

    def set_current_pedalboard_level(self, level: int) -> Collection[mido.Message]:
        """
        Set the current patch level
        """
        warnings.warn("set_current_pedalboard_level is not implemented", NotImplementedWarning)
        return []

    def tuner(self, on: bool, bypass=None) -> Collection[mido.Message]:
        if bypass is not None:
            warnings.warn("bypass parameter only work with None value. Not implemented for other values", NotImplementedWarning)
            return []

        status_number = 0x64 if on else 0
        return [
            mido.Message('control_change', control=0x4a, value=status_number),
            self.deprecated_you_can_talk()
        ]
