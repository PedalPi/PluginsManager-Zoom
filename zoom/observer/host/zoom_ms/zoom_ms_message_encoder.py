import warnings

import mido

from zoom.observer.host.base.zoom_equipment_message_encoder import ZoomEquipmentMessageEncoder, \
    UnsupportedCommandWarning, NotImplementedWarning


class ZoomMSMessageEncoder(ZoomEquipmentMessageEncoder):
    """
    Message encoder to Zoom MS series

    Based on:
     - https://github.com/g200kg/zoom-ms-utility/blob/master/midimessage.md
    """

    def effect_status(self, position: int, status: bool) -> mido.Message:
        if position >= 3:
            warnings.warn("set_param actually only works with the effect in the in [0, 2]", NotImplementedWarning)

        return super().effect_status(position, status)

    def set_effect(self, effect_position, new_effect):
        # FIXME
        return self._zoom_small(effect_position, new_effect, 0x01)

    def set_param(self, effect_position: int, param_position: int, new_value: int) -> mido.Message:
        if effect_position >= 3:
            warnings.warn("set_param actually only works with the effect in the in [0, 2]", NotImplementedWarning)

        return super().set_param(effect_position, param_position, new_value)

    def set_current_pedalboard_level(self, level: int) -> mido.Message:
        warnings.warn("Zoom MS devices doesn't supports pedalboard level", UnsupportedCommandWarning)
        return self.zoom_sysex([0x31, 0x06, 0x02, level, 0])

    def set_tempo(self, new_value: int) -> mido.Message:
        # TODO
        return self._zoom_small(0x06, new_value, 0x08)

    def tuner(self, on: bool, bypass=None) -> mido.Message:
        if bypass is not None:
            warnings.warn("bypass parameter only work with None value. Not implemented for other values", NotImplementedWarning)

        status_number = 0x64 if on else 0
        return mido.Message('control_change', control=0x4a, value=status_number)
