from typing import Tuple

from zoom.model.zoom.zoom_effect import ZoomEffect
from zoom.model.zoom_pedalboard import ZoomPedalboard
from zoom.observer.host.protocol import MidiProtocol
from zoom.observer.host.zoom_iv.zoomg3v2_patch import ZoomG3v2Patch
from zoom.observer.zoom_change import ZoomChange
from zoom.zoom_effects_builder import ZoomEffectsBuilder

from zoom.zoom_model import ZoomModel


class ZoomIVMessageDecoder:

    def __init__(self, context):
        self._context = context

    def decode(self, message):
        print(len(message), message)

        if message.type == 'program_change':
            with self._context as model:
                model.to_pedalboard(+message.program)

        elif len(message) == 10:
            self.decode_small_data(message)

        elif len(message) == 15:
            print('Device info', message.hex())
            print(MidiProtocol.device_identity_reply_decode(message.data))

        # Update current pedalboard
        elif len(message) == 110:
            data = message.data[0:5] + (0,) * 5 + message.data[5:]

            # TODO: Update current pedalboard instead replace it all
            with self._context as model:
                current_pedalboard = model.current_pedalboard
                pedalboard = self.decode_specific_pedalboard(data, current_pedalboard)

                #index = model.current_pedalboard.index
                #old_pedalboard = model.pedalboards[index]
                #model.pedalboards[index] = pedalboard

            #print(pedalboard)
            #print(pedalboard.effects)

        elif len(message) == 120:
            pedalboard = self.decode_specific_pedalboard(message.data, ZoomPedalboard(""))
            with self._context as model:
                model.pedalboards.append(pedalboard)

        else:
            # Path saved in x position
            # F0 52 00 5A 32 01 00 00 xx 00 00 00 00 00 F7
            # Swap xx <--> yy
            # F0 52 00 5A 32 02 00 00 xx 00 00 yy 00 00 F7
            print(message, '\n', message.hex())
            print('Size', len(message))

    def decode_specific_pedalboard(self, data, pedalboard: ZoomPedalboard):
        builder = ZoomEffectsBuilder(None)

        manufacturing_id = data[0]
        device_id = data[1]
        model_number = data[2]

        command_number = data[3]  # 08

        name = bytes(data[0x65:0x69] + data[0x6A:0x70]).decode()

        pedalboard.name = name

        new_pedalboard = len(pedalboard.effects) == 0

        for id_effect in range(6):
            effect, effect_replaced = self._get_effect(builder, data, pedalboard, new_pedalboard, id_effect)

            effect.active = ZoomG3v2Patch.get_effect_status(data[6:], id_effect)

            for id_param, param in enumerate(effect.params):
                param.value = ZoomG3v2Patch.get_param(data, id_effect, id_param)

            if new_pedalboard:
                pedalboard.effects.append(effect)
            elif effect_replaced:
                pedalboard.effects[id_effect] = effect
            # Effect reused
            else:
                pass

        pedalboard.level = data[0x5c]

        # TODO: Display info
        # TODO: CTRL SW/PDL
        # TODO: PDL DST

        return pedalboard

    def _get_effect(self, builder, data, pedalboard, new_pedalboard, id_effect) -> Tuple[ZoomEffect, bool]:
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
        effect_generated = ZoomG3v2Patch.get_effect(builder, data, id_effect)

        if new_pedalboard:
            return effect_generated, new_pedalboard

        # Reuse same effect if it isn't changed
        old_effect = pedalboard.effects[id_effect]
        if old_effect.plugin == effect_generated.plugin:
            return old_effect, False
        else:
            return effect_generated, True

    def decode_small_data(self, message):
        # Commands (F0 52 00 5A xx)
        # 08: Specific path
        # 28: Current path / Foot switch expression
        # 31: Global info: Tempo / Signal path / Auto save / Foot switch (min, max)
        # 31: Patch info: Patch name / Patch volume / Ctrl switch assignment
        # 31: Effect param value:
        # 32: Patch saved
        type1 = message.data[0x02]
        type2 = message.data[0x03]
        type3 = message.data[0x04]
        type4 = message.data[0x05]
        value1 = message.data[0x06]
        value2 = message.data[0x07]

        if type1 != ZoomModel.ZoomG3v2.value:
            return

        # Pedalboard level
        if type2 == 0x31 and type3 == ZoomChange.PEDALBOARD_CURRENT_LEVEL.value and type4 == 0x02:
            with self._context as model:
                model.current_pedalboard.level = value1

        # Pedalboard name
        elif type2 == 0x31 and type3 == ZoomChange.PEDALBOARD_NAME.value and (0x00 <= type4 <= 0x09):
            with self._context as model:
                pos = type4
                new_letter = bytes([value1]).decode()
                name = model.current_pedalboard.name
                new_name = name[:pos] + new_letter + name[pos+1:]

                model.current_pedalboard.name = new_name

        # Param value
        elif type2 == 0x31 and (0x00 <= type3 <= 0x05):
            id_effect = type3

            if 0x00 == type4:
                with self._context as model:
                     model.current_pedalboard.effects[id_effect].active = False

            elif 0x02 <= type4 <= 0x09:
                id_param = type4 - 2
                value = (value2 << 7) + value1

                with self._context as model:
                    model.current_pedalboard.effects[id_effect].params[id_param].value = value

        print(hex(type1), hex(type2), hex(type3), hex(type4))
