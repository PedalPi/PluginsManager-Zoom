import warnings

import mido

from zoom.zoom_model import Manufacturer, ZoomModel


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

    def __init__(self, manufacturing_id: Manufacturer, device_id, model_number: ZoomModel):
        self.manufacturing_id = manufacturing_id
        self.device_id = device_id
        self.model_number = model_number

    def zoom_sysex(self, data) -> mido.Message:
        head = [self.manufacturing_id.value, self.device_id, self.model_number.value]
        return mido.Message('sysex', data=head + data)

    #######################
    # Equipment info
    #######################
    def identity_request(self):
        return mido.Message('sysex', data=[0x7e, 0x00, 0x06, 0x01])

    #######################
    # Enable/disable configuration
    #######################
    def enable_editor(self) -> mido.Message:
        """
        Enable the equipment controls by this API
        """
        return self.zoom_sysex([0x50])

    def disable_editor(self) -> mido.Message:
        """
        Disable the equipment controls by this API
        """
        return self.zoom_sysex([0x51])

    #######################
    # Obtain patch details
    #######################
    def current_patch_number(self) -> mido.Message:
        """
        Get the current patch number
        """
        return self.zoom_sysex([0x33])

    def current_patch_details(self) -> mido.Message:
        """
        Obtain details about the current patch
        """
        return self.zoom_sysex([0x29])

    def specified_patch_details(self, number: int) -> mido.Message:
        """
        Obtain details about a specific patch
        """
        return self.zoom_sysex([0x09, 0x00, 0x00, number])

    #######################
    # Effect and Param
    #######################
    def effect_status(self, position: int, status: bool) -> mido.Message:
        """
        Enable/disable (on/off) a specific effect of the current patch
        """
        status_number = 1 if status else 0
        return self._zoom_small(position, status_number, 0x00)

    def set_effect(self, effect_position: int, new_effect: int) -> mido.Message:
        """
        Set a effect of a specific position of the current patch
        """
        warnings.warn("set_effect is not implemented", NotImplementedWarning)
        return None

    def set_param(self, effect_position: int, param_position: int, new_value: int) -> mido.Message:
        """
        Set a param value of an effect of the current patch
        """
        return self._zoom_small(effect_position, new_value, param_position + 0x02)

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
    def to_patch(self, number: int) -> mido.Message:
        """
        Set the current patch
        """
        return mido.Message('program_change', channel=0x00, program=number)

    def set_current_pedalboard_level(self, level: int) -> mido.Message:
        """
        Set the current patch level
        """
        warnings.warn("set_current_pedalboard_level is not implemented", NotImplementedWarning)
        return None

    #######################
    # Other configurations
    #######################
    def set_tempo(self, new_value: int) -> mido.Message:
        """
        Set the general tempo
        """
        warnings.warn("set_tempo is not implemented", NotImplementedWarning)
        return None

    def tuner(self, on: bool, bypass=None) -> mido.Message:
        """
        Enable/disable the tuner

        :param bypass: :code:`None` - go to the tuner in default/configured mode
                       :code:`True` - go to the tuner in bypass mode
                       :code:`False` - go to the tuner in mute mode
                    Observe that isn't necessary all equipment has support to the :code:`True` and :code:`False` values
        """
        warnings.warn("tuner is not implemented", NotImplementedWarning)
        return None

    #######################
    # ???
    #######################
    def deprecated_you_can_talk(self) -> mido.Message:
        """
        Possibly an Ack or something like
        """
        return self.zoom_sysex([0x10])
