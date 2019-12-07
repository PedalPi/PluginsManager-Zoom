from abc import abstractmethod

from decoder.lib.decoder_util import decode_message
from zoom.model.zoom.zoom_effect import ZoomEffect
from zoom.model.zoom_pedalboard import ZoomPedalboard
from zoom.zoom_effects_builder import ZoomEffectsBuilder
from zoom.zoom_model import ZoomModel


class ZoomEquipmentPatchDecoder:
    """
    Based on: https://github.com/g200kg/zoom-ms-utility/blob/master/midimessage.md#patch-data-format
    """

    @property
    @abstractmethod
    def effects_status_bits(self):
        return None

    @property
    @abstractmethod
    def effects_bits(self):
        return None

    @property
    @abstractmethod
    def params_bits(self):
        return None

    def __init__(self, model: ZoomModel):
        self.builder = ZoomEffectsBuilder(model)

    @abstractmethod
    def decode(self, data, pedalboard: ZoomPedalboard) -> ZoomPedalboard:
        return None

    def equipment_info(self, data):
        return {
            'manufacturing_id': data[0],
            'device_id': data[1],
            'model_number': data[2],
            'command_number': data[3]
        }

    def decode_effect(self, data, id_effect):
        effect = self.decode_effect_by_id(data, id_effect)

        effect.active = self.decode_effect_status(data, id_effect)

        for id_param, param in enumerate(effect.params):
            param.value = self.decode_param_value(data, id_effect, id_param)

        return effect

    def put_effect(self, pedalboard, effect, id_effect):
        if id_effect == len(pedalboard.effects):
            pedalboard.effects.append(effect)
        else:
            pedalboard.effects[id_effect] = effect

    def decode_effect_by_id(self, data, id_effect: int) -> ZoomEffect:
        effect_data = self.effects_bits[id_effect]

        id = decode_message(data, effect_data)

        return self.builder.build_by_id(id)

    def decode_effect_status(self, data, effect: int) -> bool:
        status_data = self.effects_status_bits[effect]
        return decode_message(data, status_data) == 1

    def decode_param_value(self, data, id_effect: int, id_param: int) -> int:
        param_data = self.params_bits[id_effect][id_param]

        return decode_message(data, param_data)
