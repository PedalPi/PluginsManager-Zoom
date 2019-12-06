from typing import Tuple

from zoom.model.zoom.zoom_effect import ZoomEffect
from zoom.model.zoom_pedalboard import ZoomPedalboard
from zoom.observer.host.protocol import MidiProtocol
from zoom.observer.host.zoom_iv.zoomg3v2_patch import ZoomG3v2Patch
from zoom.observer.host.zoom_ms.zoom_ms_patch import ZoomMSPatch
from zoom.observer.zoom_change import ZoomChange
from zoom.zoom_model import ZoomModel


class ZoomMSMessageDecoder:

    def __init__(self, context):
        self._context = context

    def decode(self, message):
        print(len(message), message)

        if message.type == 'program_change':
            with self._context as model:
                model.to_pedalboard(+message.program)

        elif len(message) == 15:
            print('Device info', message.hex())
            print(MidiProtocol.device_identity_reply_decode(message.data))

        elif len(message) == 10:
            self.decode_small_data(message)

        # Update current pedalboard
        elif len(message) == 146:
            with self._context as model:
                current_pedalboard = model.current_pedalboard
                self.decode_specific_pedalboard(message.data, current_pedalboard)

        elif len(message) == 156:
            data = message.data[5:]

            pedalboard = self.decode_specific_pedalboard(data, ZoomPedalboard(""))
            with self._context as model:
                model.pedalboards.append(pedalboard)

        else:
            print("Not mapped")
            print(message, '\n', message.hex())
            print('Size', len(message))

    def decode_specific_pedalboard(self, data, pedalboard: ZoomPedalboard):
        manufacturing_id = data[0]
        device_id = data[1]
        model_number = data[2]

        command_number = data[3]

        name = bytes((data[0x83], ) + data[0x85:0x8c] + data[0x8d:0x8f]).decode()

        pedalboard.name = name

        new_pedalboard = len(pedalboard.effects) == 0

        for id_effect in range(6):
            effect, effect_replaced = self._get_effect(data, pedalboard, new_pedalboard, id_effect)

            effect.active = ZoomMSPatch.get_effect_status(data, id_effect)

            for id_param, param in enumerate(effect.params):
                param.value = ZoomMSPatch.get_param(data, id_effect, id_param)

            if new_pedalboard:
                pedalboard.effects.append(effect)
            elif effect_replaced:
                pedalboard.effects[id_effect] = effect
            # Effect reused
            else:
                pass

        # TODO: Display info

        return pedalboard

    def _get_effect(self, data, pedalboard, new_pedalboard, id_effect) -> Tuple[ZoomEffect, bool]:
        """
        If the pedalboard is a new pedalboard, it will be generates a new effect.
        This case is applied when there are loading the data of the equipment

        If is an "old" pedalboard, it will try to use the same effect object if the messages inform it.
        But if the effect has been replaced, then a new effect object will be returned

        :param builder: Effects builder
        :param data: MIDI data
        :param pedalboard: Current pedalboard (created or updated)
        :param new_pedalboard: This pedalboard is a new pedalboard?
        :param id_effect: Id of the effect that is extracting the information over the data

        :return: Tuple:
            Effect (created or updated),
            the effect has been replaced? (boolean)
        """
        effect_generated = ZoomMSPatch.get_effect(data, id_effect)

        if new_pedalboard:
            return effect_generated, new_pedalboard

        # Reuse same effect if it isn't changed
        old_effect = pedalboard.effects[id_effect]
        if old_effect.plugin == effect_generated.plugin:
            return old_effect, False
        else:
            return effect_generated, True

    def decode_small_data(self, message):
        type1 = message.data[0x02]
        type2 = message.data[0x03]
        type3 = message.data[0x04]
        type4 = message.data[0x05]
        value1 = message.data[0x06]
        value2 = message.data[0x07]

        if type1 != ZoomModel.ZoomMS50g.value:
            return

        # Param value
        if type2 == 0x31 and (0x00 <= type3 <= 0x05):
            id_effect = type3

            if 0x00 == type4:
                with self._context as model:
                     model.current_pedalboard.effects[id_effect].active = False

            elif 0x02 <= type4 <= 0x10:
                id_param = type4 - 2
                value = (value2 << 7) + value1

                with self._context as model:
                    model.current_pedalboard.effects[id_effect].params[id_param].value = value

        print(hex(type1), hex(type2), hex(type3), hex(type4))
