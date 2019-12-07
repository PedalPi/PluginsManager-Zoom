import mido

from zoom.zoom_model import Manufacturer, ZoomModel


class ZoomMSMessageEncoder(object):
    """
    Message encoder to Zoom MS series

    Based on:
     - https://github.com/g200kg/zoom-ms-utility/blob/master/midimessage.md
    """

    def __init__(self, manufacturing_id: Manufacturer, device_id: int, model_number: ZoomModel):
        self.manufacturing_id = manufacturing_id
        self.device_id = device_id
        self.model_number = model_number

    def zoom_sysex(self, data):
        head = [self.manufacturing_id.value, self.device_id, self.model_number.value]
        return mido.Message('sysex', data=head + data)

    #######################
    # To organize
    #######################
    def identity_request(self):
        return mido.Message('sysex', data=[0x7e, 0x00, 0x06, 0x01])

    #######################
    # Enable/disable configuration
    #######################
    def enable_editor(self):
        return self.zoom_sysex([0x50])

    def disable_editor(self):
        return self.zoom_sysex([0x51])

    #######################
    # Obtain patch details
    #######################
    def current_patch_number(self):
        return self.zoom_sysex([0x33])

    def current_patch_details(self):
        return self.zoom_sysex([0x29])

    def specified_patch_details(self, number):
        return self.zoom_sysex([0x09, 0x00, 0x00, number])

    #######################
    # Effect and Param
    #######################
    def effect_on(self, position):
        # FIXME: Only works with the three first effects!
        return self.effect_status(position, True)

    def effect_off(self, position):
        # FIXME: Only works with the three first effects!
        return self.effect_status(position, False)

    def effect_status(self, position, status):
        # FIXME: Only works with the three first effects!
        status_number = 1 if status else 0
        return self._zoom_small(position, status_number, 0x00)

    def set_effect(self, effect_position, new_effect):
        # FIXME
        return self._zoom_small(effect_position, new_effect, 0x01)

    def set_param(self, effect_position, param_position, new_value):
        # FIXME: Only works with the three first effects!
        return self._zoom_small(effect_position, new_value, param_position + 0x02)

    def _zoom_small(self, position, value, effect_message_type):
        """
        :param position:
        :param value:
        :param effect_message_type:
                     0 - Effect status
                     1 - Set effect
                     [2..7] - Set param value
        :return:
        """
        value2 = value >> 7
        value = value & 0b01111111

        return self.zoom_sysex([0x31, position, effect_message_type, value, value2])

    #######################
    # Pedalboard
    #######################
    def to_patch(self, number):
        return mido.Message('program_change', channel=0x00, program=number)

    def set_current_pedalboard_level(self, level: int):
        # TODO
        return self.zoom_sysex([0x31, 0x06, 0x02, level, 0])

    #######################
    # Other configurations
    #######################
    def set_tempo(self, new_value):
        # TODO
        return self._zoom_small(0x06, new_value, 0x08)

    #######################
    # ???
    #######################
    def tuner_on(self):
        return self.tuner(True)

    def tuner_off(self):
        return self.tuner(False)

    def tuner(self, on=True):
        status_number = 0x64 if on else 0
        return mido.Message('control_change', control=0x4a, value=status_number)

    def tuner_mute_off(self):
        # FIXME
        return mido.Message('control_change', control=0x75, value=0x00)

    def tuner_mute_on(self):
        # FIXME
        return mido.Message('control_change', control=0x75, value=0x64)

    def deprecated_you_can_talk(self):
        # TODO
        return self.zoom_sysex([0x10])
