import warnings

import mido

from zoom.observer.host.base.zoom_equipment_message_encoder import ZoomEquipmentMessageEncoder, NotImplementedWarning


class ZoomG1onMessageEncoder(ZoomEquipmentMessageEncoder):
    """
    Message encoder to Zoom On series
    """

    def set_effect(self, effect_position: int, new_effect: int) -> mido.Message:
        # FIXME
        return self._zoom_small(effect_position, new_effect, 0x01)

    def set_tempo(self, new_value: int) -> mido.Message:
        # FIXME
        return self._zoom_small(0x06, new_value, 0x08)

    def tuner(self, on: bool, bypass=None) -> mido.Message:
        if bypass is not None:
            warnings.warn("bypass parameter only work with None value. Not implemented for other values", NotImplementedWarning)

        status_number = 0x64 if on else 0
        return mido.Message('control_change', control=0x4a, value=status_number)
