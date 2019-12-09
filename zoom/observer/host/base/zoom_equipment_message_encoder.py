import warnings
from typing import Collection

import mido


class EncoderWarning(Warning):
    pass


class NotImplementedWarning(EncoderWarning):
    pass


class UnsupportedCommandWarning(EncoderWarning):
    pass


class ZoomEquipmentMessageEncoder:
    """
    Define the methods that are expected to controls a device
    """

    def __init__(self, host_data: 'ZoomEquipmentHostData'):
        self.host_data = host_data

    def zoom_sysex(self, data) -> mido.Message:
        head = [self.host_data.manufacturer.value, self.host_data.device_id, self.host_data.model.value]
        return mido.Message('sysex', data=head + data)

    #######################
    # Equipment info
    #######################
    def identity_request(self) -> mido.Message:
        return mido.Message('sysex', data=[0x7e, 0x00, 0x06, 0x01])

    #######################
    # Enable/disable configuration
    #######################
    def enable_editor(self) -> Collection[mido.Message]:
        """
        Enable the equipment controls by this API
        """
        return [self.zoom_sysex([0x50])]

    def disable_editor(self) -> Collection[mido.Message]:
        """
        Disable the equipment controls by this API
        """
        return [self.zoom_sysex([0x51])]

    #######################
    # Obtain patch details
    #######################
    def current_patch_number(self) -> Collection[mido.Message]:
        """
        Get the current patch number
        """
        return [self.zoom_sysex([0x33])]

    def current_patch_details(self) -> Collection[mido.Message]:
        """
        Obtain details about the current patch
        """
        return [self.zoom_sysex([0x29])]

    def specified_patch_details(self, number: int) -> Collection[mido.Message]:
        """
        Obtain details about a specific patch
        """
        return [self.zoom_sysex([0x09, 0x00, 0x00, number])]

    #######################
    # Effect and Param
    #######################
    def effect_status(self, position: int, status: bool) -> Collection[mido.Message]:
        """
        Enable/disable (on/off) a specific effect of the current patch
        """
        status_number = 1 if status else 0
        return [self._zoom_small(position, status_number, 0x00)]

    def set_effect(self, effect_position: int, new_effect: int) -> Collection[mido.Message]:
        """
        Set a effect of a specific position of the current patch
        """
        warnings.warn("set_effect is not implemented", NotImplementedWarning)
        return []

    def set_param(self, effect_position: int, param_position: int, new_value: int) -> Collection[mido.Message]:
        """
        Set a param value of an effect of the current patch
        """
        return [self._zoom_small(effect_position, new_value, param_position + 0x02)]

    def _zoom_small(self, position: int, value: int, effect_message_type) -> mido.Message:
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
    def to_patch(self, number: int) -> Collection[mido.Message]:
        """
        Set the current patch
        """
        return [mido.Message('program_change', channel=0x00, program=number)]

    def set_current_pedalboard_level(self, level: int) -> Collection[mido.Message]:
        """
        Set the current patch level
        """
        warnings.warn("set_current_pedalboard_level is not implemented", NotImplementedWarning)
        return []

    #######################
    # Other configurations
    #######################
    def set_tempo(self, new_value: int) -> Collection[mido.Message]:
        """
        Set the general tempo
        """
        warnings.warn("set_tempo is not implemented", NotImplementedWarning)
        return []

    def tuner(self, on: bool, bypass=None) -> Collection[mido.Message]:
        """
        Enable/disable the tuner

        :param bypass: :code:`None` - go to the tuner in default/configured mode
                       :code:`True` - go to the tuner in bypass mode
                       :code:`False` - go to the tuner in mute mode
                    Observe that isn't necessary all equipment has support to the :code:`True` and :code:`False` values
        """
        warnings.warn("tuner is not implemented", NotImplementedWarning)
        return []

    #######################
    # ???
    #######################
    def deprecated_you_can_talk(self) -> mido.Message:
        """
        Possibly an Ack or something like
        """
        return self.zoom_sysex([0x10])
