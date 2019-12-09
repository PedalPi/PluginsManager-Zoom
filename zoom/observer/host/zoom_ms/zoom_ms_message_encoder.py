import warnings
from typing import Collection

import mido

from zoom.observer.host.base.zoom_equipment_message_encoder import ZoomEquipmentMessageEncoder, \
    UnsupportedCommandWarning, NotImplementedWarning


class ZoomMSMessageEncoder(ZoomEquipmentMessageEncoder):
    """
    Message encoder to Zoom MS series

    Based on:
     - https://github.com/g200kg/zoom-ms-utility/blob/master/midimessage.md
    """

    def effect_status(self, position: int, status: bool) -> Collection[mido.Message]:
        if position >= 3:
            warnings.warn("set_param actually only works with the effect in the in [0, 2]", NotImplementedWarning)
            return []

        return super().effect_status(position, status)

    def set_effect(self, effect_position: int, new_effect: int) -> Collection[mido.Message]:
        warnings.warn("set_effect is implemented, but it not update the equipment visor", NotImplementedWarning)
        return [self._zoom_small(effect_position, new_effect, 0x01)]

    def set_param(self, effect_position: int, param_position: int, new_value: int) -> Collection[mido.Message]:
        if effect_position >= 3:
            warnings.warn("set_param actually only works with the effect in the in [0, 2]", NotImplementedWarning)
            return []

        return super().set_param(effect_position, param_position, new_value)

    def set_current_pedalboard_level(self, level: int) -> Collection[mido.Message]:
        warnings.warn("Zoom MS devices doesn't supports pedalboard level", UnsupportedCommandWarning)
        return []

    def set_tempo(self, new_value: int) -> Collection[mido.Message]:
        warnings.warn("Not implemented. Maybe set_tempo is not supported", NotImplementedWarning)
        return []

    def tuner(self, on: bool, bypass=None) -> Collection[mido.Message]:
        if bypass is not None:
            warnings.warn("bypass parameter only work with None value. Not implemented for other values", NotImplementedWarning)
            return []

        status_number = 0x64 if on else 0
        return [mido.Message('control_change', control=0x4a, value=status_number)]
